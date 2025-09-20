"""
Enhanced Financial Document Analyzer with Database and Queue Integration
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
import time
from datetime import datetime
from typing import Optional, List

# Import our modules
from database import get_db, create_tables, User, AnalysisResult, AnalysisQueue
from queue_worker import queue_manager

# Initialize database
create_tables()

app = FastAPI(
    title="Financial Document Analyzer - Enhanced",
    description="AI-powered financial document analysis with queue processing and database storage",
    version="2.0.0"
)

# User management endpoints
@app.post("/users/", response_model=dict)
async def create_user(username: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
        "total_analyses": user.total_analyses
    }

# Enhanced analysis endpoints
@app.post("/analyze/queue")
async def queue_analysis(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    user_id: int = Form(default=1),
    priority: int = Form(default=1),
    db: Session = Depends(get_db)
):
    """Queue a financial document for analysis"""
    
    # Validate user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = f"data/queue_{file_id}_{file.filename}"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Add to queue
        queue_id = queue_manager.add_to_queue(
            user_id=user_id,
            filename=file.filename,
            file_path=file_path,
            query=query.strip(),
            priority=priority
        )
        
        return {
            "status": "queued",
            "queue_id": queue_id,
            "message": "Document queued for analysis",
            "estimated_wait": "2-5 minutes"
        }
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error queuing analysis: {str(e)}")

@app.get("/analyze/status/{queue_id}")
async def get_analysis_status(queue_id: str, db: Session = Depends(get_db)):
    """Get the status of a queued analysis"""
    try:
        # Extract queue ID from queue_id string
        if queue_id.startswith("queued_redis_"):
            actual_id = int(queue_id.split("_")[-1])
        elif queue_id.startswith("processed_immediate_"):
            actual_id = int(queue_id.split("_")[-1])
        else:
            actual_id = int(queue_id)
        
        queue_item = db.query(AnalysisQueue).filter(AnalysisQueue.id == actual_id).first()
        if not queue_item:
            raise HTTPException(status_code=404, detail="Queue item not found")
        
        response = {
            "queue_id": actual_id,
            "status": queue_item.status,
            "created_at": queue_item.created_at,
            "started_at": queue_item.started_at,
            "completed_at": queue_item.completed_at
        }
        
        if queue_item.error_message:
            response["error"] = queue_item.error_message
        
        # If completed, get the result
        if queue_item.status == "completed":
            result = db.query(AnalysisResult).filter(
                AnalysisResult.user_id == queue_item.user_id,
                AnalysisResult.filename == queue_item.filename
            ).order_by(AnalysisResult.created_at.desc()).first()
            
            if result:
                response["result_id"] = result.id
                response["processing_time"] = result.processing_time
        
        return response
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid queue ID format")

@app.get("/results/{result_id}")
async def get_analysis_result(result_id: int, db: Session = Depends(get_db)):
    """Get a specific analysis result"""
    result = db.query(AnalysisResult).filter(AnalysisResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    
    return {
        "id": result.id,
        "filename": result.filename,
        "query": result.query,
        "analysis": result.analysis_result,
        "processing_time": result.processing_time,
        "status": result.status,
        "created_at": result.created_at
    }

@app.get("/users/{user_id}/results")
async def get_user_results(
    user_id: int, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """Get all analysis results for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    results = db.query(AnalysisResult).filter(
        AnalysisResult.user_id == user_id
    ).order_by(AnalysisResult.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "user_id": user_id,
        "total_results": len(results),
        "results": [
            {
                "id": r.id,
                "filename": r.filename,
                "query": r.query,
                "status": r.status,
                "processing_time": r.processing_time,
                "created_at": r.created_at
            } for r in results
        ]
    }

@app.get("/queue/status")
async def get_queue_status(user_id: Optional[int] = None):
    """Get queue status and statistics"""
    return queue_manager.get_queue_status(user_id)

# Original immediate analysis endpoint (for backward compatibility)
@app.post("/analyze")
async def analyze_document_immediate(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    user_id: int = Form(default=1),
    db: Session = Depends(get_db)
):
    """Immediate analysis (for backward compatibility)"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/immediate_{file_id}_{file.filename}"
    start_time = time.time()
    
    try:
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process immediately
        analysis = queue_manager.perform_analysis(
            queue_manager.pdf_tool._run(file_path), 
            query.strip()
        )
        
        processing_time = time.time() - start_time
        
        # Save to database
        result = AnalysisResult(
            user_id=user_id,
            filename=file.filename,
            file_size=os.path.getsize(file_path),
            query=query,
            analysis_result=analysis,
            processing_time=processing_time,
            status="completed"
        )
        db.add(result)
        
        # Update user stats
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_analyses += 1
        
        db.commit()
        
        return {
            "status": "success",
            "result_id": result.id,
            "query": query,
            "analysis": analysis,
            "processing_time": processing_time,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Enhanced Financial Document Analyzer API is running",
        "version": "2.0.0",
        "features": [
            "Queue-based processing",
            "Database storage",
            "User management",
            "Analysis history",
            "Concurrent request handling"
        ]
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Detailed health check"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    queue_status = queue_manager.get_queue_status()
    
    return {
        "status": "healthy",
        "database": db_status,
        "queue_system": "available" if queue_status["redis_connected"] else "fallback_mode",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("enhanced_main:app", host="0.0.0.0", port=8002, reload=True)
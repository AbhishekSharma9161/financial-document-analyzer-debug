"""
Queue Worker System for handling concurrent financial document analysis
Uses Redis Queue (RQ) for background task processing
"""

import os
import time
import uuid
from datetime import datetime
from typing import Optional

try:
    import redis
    from rq import Queue, Worker
    REDIS_AVAILABLE = True
except ImportError as e:
    REDIS_AVAILABLE = False
    print(f"Redis/RQ import error: {e}")
    print("Install with: pip install redis rq")

from sqlalchemy.orm import Session
from database import SessionLocal, AnalysisResult, AnalysisQueue
from tools import FinancialDocumentTool

# Redis connection
if REDIS_AVAILABLE:
    try:
        redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        # Test connection
        redis_conn.ping()
        queue = Queue('financial_analysis', connection=redis_conn)
        REDIS_CONNECTED = True
    except:
        REDIS_CONNECTED = False
        print("Redis server not available. Queue features disabled.")
else:
    REDIS_CONNECTED = False

class QueueManager:
    """Manages the analysis queue and background processing"""
    
    def __init__(self):
        self.pdf_tool = FinancialDocumentTool()
    
    def add_to_queue(self, user_id: int, filename: str, file_path: str, query: str, priority: int = 1) -> str:
        """Add analysis task to queue"""
        db = SessionLocal()
        try:
            # Create queue entry
            queue_item = AnalysisQueue(
                user_id=user_id,
                filename=filename,
                file_path=file_path,
                query=query,
                priority=priority,
                status="pending"
            )
            db.add(queue_item)
            db.commit()
            
            if REDIS_CONNECTED:
                # Add to Redis queue
                job = queue.enqueue(
                    self.process_document,
                    queue_item.id,
                    job_timeout='10m',
                    job_id=f"analysis_{queue_item.id}"
                )
                return f"queued_redis_{job.id}"
            else:
                # Fallback: process immediately
                result = self.process_document(queue_item.id)
                return f"processed_immediate_{queue_item.id}"
                
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def process_document(self, queue_id: int) -> dict:
        """Process a document analysis task"""
        db = SessionLocal()
        start_time = time.time()
        
        try:
            # Get queue item
            queue_item = db.query(AnalysisQueue).filter(AnalysisQueue.id == queue_id).first()
            if not queue_item:
                return {"error": "Queue item not found"}
            
            # Update status to processing
            queue_item.status = "processing"
            queue_item.started_at = datetime.utcnow()
            db.commit()
            
            # Perform analysis
            try:
                # Read PDF content
                pdf_content = self.pdf_tool._run(queue_item.file_path)
                
                # Simple analysis (can be enhanced with AI agents)
                analysis = self.perform_analysis(pdf_content, queue_item.query)
                
                processing_time = time.time() - start_time
                
                # Save result
                result = AnalysisResult(
                    user_id=queue_item.user_id,
                    filename=queue_item.filename,
                    file_size=os.path.getsize(queue_item.file_path) if os.path.exists(queue_item.file_path) else 0,
                    query=queue_item.query,
                    analysis_result=analysis,
                    processing_time=processing_time,
                    status="completed"
                )
                db.add(result)
                
                # Update queue status
                queue_item.status = "completed"
                queue_item.completed_at = datetime.utcnow()
                
                db.commit()
                
                return {
                    "status": "success",
                    "result_id": result.id,
                    "processing_time": processing_time,
                    "analysis": analysis
                }
                
            except Exception as e:
                # Handle processing error
                queue_item.status = "failed"
                queue_item.error_message = str(e)
                queue_item.completed_at = datetime.utcnow()
                db.commit()
                
                return {"status": "error", "message": str(e)}
                
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def perform_analysis(self, pdf_content: str, query: str) -> str:
        """Perform financial analysis on PDF content"""
        try:
            # Basic financial analysis
            analysis = f"""
# Financial Document Analysis

## Query: {query}

## Document Analysis:
- Content length: {len(pdf_content)} characters
- Analysis timestamp: {datetime.utcnow().isoformat()}

## Key Findings:
"""
            
            # Look for financial keywords
            financial_keywords = {
                'revenue': 'Revenue/Sales data found',
                'profit': 'Profitability information identified',
                'loss': 'Loss information detected',
                'cash flow': 'Cash flow statements present',
                'assets': 'Asset information available',
                'liabilities': 'Liability data found',
                'equity': 'Equity information present',
                'debt': 'Debt information identified',
                'investment': 'Investment data found',
                'dividend': 'Dividend information present'
            }
            
            findings = []
            for keyword, description in financial_keywords.items():
                if keyword.lower() in pdf_content.lower():
                    findings.append(f"- {description}")
            
            if findings:
                analysis += "\n".join(findings)
            else:
                analysis += "- No specific financial keywords detected"
            
            # Add content preview
            analysis += f"\n\n## Document Preview (first 500 characters):\n{pdf_content[:500]}..."
            
            return analysis
            
        except Exception as e:
            return f"Error in analysis: {str(e)}"
    
    def get_queue_status(self, user_id: Optional[int] = None) -> dict:
        """Get queue status and statistics"""
        db = SessionLocal()
        try:
            query = db.query(AnalysisQueue)
            if user_id:
                query = query.filter(AnalysisQueue.user_id == user_id)
            
            total = query.count()
            pending = query.filter(AnalysisQueue.status == "pending").count()
            processing = query.filter(AnalysisQueue.status == "processing").count()
            completed = query.filter(AnalysisQueue.status == "completed").count()
            failed = query.filter(AnalysisQueue.status == "failed").count()
            
            return {
                "total": total,
                "pending": pending,
                "processing": processing,
                "completed": completed,
                "failed": failed,
                "redis_connected": REDIS_CONNECTED
            }
        finally:
            db.close()

# Worker function for RQ
def start_worker():
    """Start the RQ worker"""
    if not REDIS_CONNECTED:
        print("Redis not available. Cannot start worker.")
        return
    
    worker = Worker(['financial_analysis'], connection=redis_conn)
    print("Starting financial analysis worker...")
    worker.work()

# Initialize queue manager
queue_manager = QueueManager()

if __name__ == "__main__":
    if REDIS_CONNECTED:
        print("Starting Redis Queue Worker...")
        start_worker()
    else:
        print("Redis not available. Queue system will use immediate processing fallback.")
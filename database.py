"""
Database models and configuration for Financial Document Analyzer
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = "sqlite:///./financial_analyzer.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_analyses = Column(Integer, default=0)

class AnalysisResult(Base):
    """Model for storing financial analysis results"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Foreign key to users
    filename = Column(String(255))
    file_size = Column(Integer)
    query = Column(Text)
    analysis_result = Column(Text)
    processing_time = Column(Float)  # in seconds
    status = Column(String(20), default="completed")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
class AnalysisQueue(Base):
    """Model for managing analysis queue"""
    __tablename__ = "analysis_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    filename = Column(String(255))
    file_path = Column(String(500))
    query = Column(Text)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    priority = Column(Integer, default=1)  # 1=low, 2=medium, 3=high
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
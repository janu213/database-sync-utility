from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal, init_db, JobModel
from models import DBConnection, QueryRequest, JobCreate, MappingRequest
from services.connector import DatabaseConnector
from services.executor import DataExecutor
from scheduler import start_scheduler, add_job_to_scheduler, remove_job_from_scheduler
from logger_config import setup_logger
import logging

# Setup Logger
logger = setup_logger()

app = FastAPI(title="Database Sync Utility")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()

@app.post("/api/test-connection")
def test_connection(connection: DBConnection):
    try:
        DatabaseConnector.test_connection(connection)
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/preview-query")
def preview_query(request: QueryRequest):
    try:
        results = DatabaseConnector.get_preview(request.connection, request.query)
        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # Save to DB
    db_job = JobModel(
        name=job.name,
        schedule_interval=job.schedule_interval,
        source_connection=job.source_connection.dict(),
        target_connection=job.target_connection.dict(),
        query=job.query,
        target_table=job.target_table,
        mapping=job.mapping,
        status="active"
    )
    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        
        # Add to Scheduler
        add_job_to_scheduler(db_job.id, db_job.schedule_interval)
        
        return db_job
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create job: {str(e)}")

@app.get("/api/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(JobModel).all()

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Remove from scheduler
    remove_job_from_scheduler(job_id)
    
    db.delete(job)
    db.commit()
    return {"status": "success", "message": "Job deleted"}

@app.post("/api/jobs/{job_id}/toggle")
def toggle_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status == "active":
        job.status = "paused"
        remove_job_from_scheduler(job_id)
    else:
        job.status = "active"
        add_job_to_scheduler(job_id, job.schedule_interval)
        
    db.commit()
    return {"status": "success", "new_status": job.status}

@app.put("/api/jobs/{job_id}")
def update_job(job_id: int, job_update: JobCreate, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update fields
    job.name = job_update.name
    job.schedule_interval = job_update.schedule_interval
    job.source_connection = job_update.source_connection.dict()
    job.target_connection = job_update.target_connection.dict()
    job.query = job_update.query
    job.target_table = job_update.target_table
    job.mapping = job_update.mapping
    
    db.commit()
    db.refresh(job)

    # Update Scheduler
    remove_job_from_scheduler(job.id)
    if job.status == "active":
        add_job_to_scheduler(job.id, job.schedule_interval)
    
    logger.info(f"Job updated: {job.name} (ID: {job.id})")
    return job

@app.get("/")
def read_root():
    return {"message": "Database Sync Utility Backend is running"}

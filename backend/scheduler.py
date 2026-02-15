from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal, JobModel
from services.executor import DataExecutor
from models import JobCreate, DBConnection
import json
from datetime import datetime

scheduler = BackgroundScheduler()

def job_wrapper(job_id: int):
    # Re-fetch job details from DB to get latest config (optional, but good practice)
    # Actually, we can just pass the job config, but fetching ensures we don't run deleted jobs if scheduler is out of sync
    db = SessionLocal()
    try:
        job_record = db.query(JobModel).filter(JobModel.id == job_id).first()
        if not job_record or job_record.status != "active":
            return
        
        # Convert DB model to pydantic model needed by executor
        # We need to reconstruct the objects from JSON fields
        job_create = JobCreate(
            name=job_record.name,
            schedule_interval=job_record.schedule_interval,
            source_connection=DBConnection(**job_record.source_connection),
            target_connection=DBConnection(**job_record.target_connection),
            query=job_record.query,
            target_table=job_record.target_table,
            mapping=job_record.mapping
        )
        
        DataExecutor.run_job(job_create)
        
        # Update success status
        job_record.last_run_status = "success"
        job_record.last_run_time = str(datetime.now())
        job_record.last_run_message = "Job completed successfully"
        db.commit()
        logger.info(f"Job completed successfully: {job_record.name} (ID: {job_id})")
        
    except Exception as e:
        logger.error(f"Error running job {job_id}: {e}", exc_info=True)
        # Update failure status
        if job_record:
            job_record.last_run_status = "failed"
            job_record.last_run_time = str(datetime.now())
            job_record.last_run_message = str(e)
            db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler.start()
    # Load existing jobs
    db = SessionLocal()
    try:
        jobs = db.query(JobModel).filter(JobModel.status == "active").all()
        for job in jobs:
            scheduler.add_job(
                job_wrapper, 
                'interval', 
                minutes=job.schedule_interval, 
                args=[job.id], 
                id=str(job.id),
                replace_existing=True
            )
        print(f"Loaded {len(jobs)} jobs from database.")
    finally:
        db.close()

def add_job_to_scheduler(job_id: int, interval_minutes: int):
    scheduler.add_job(
        job_wrapper,
        'interval',
        minutes=interval_minutes,
        args=[job_id],
        id=str(job_id),
        replace_existing=True
    )

def remove_job_from_scheduler(job_id: int):
    try:
        scheduler.remove_job(str(job_id))
    except:
        pass # Job might not exist

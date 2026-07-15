from sqlalchemy.orm import Session
from app import models ,  schemas
from typing import Optional

def create_job(db: Session , job: schemas.JobCreate):
    existing_job = (db.query(models.JobPosting).filter(models.JobPosting.title == job.title,
            models.JobPosting.company == job.company,
            models.JobPosting.salary == job.salary,
            models.JobPosting.location == job.location
        )
        .first())
        

    if existing_job:
        return None

    db_job = models.JobPosting(
        title = job.title,
        company = job.company,
        salary = job.salary ,
        location = job.location

    )

    db.add(db_job)

    db.commit()

    db.refresh(db_job)

    return db_job

def get_jobs(db: Session , job_id:Optional[int]=None, company:Optional[str]=None,):
    query = db.query(models.JobPosting)

    if job_id is not None:
        query = query.filter(models.JobPosting.id == job_id)

    if company is not None:
        query = query.filter(models.JobPosting.company == company)

    return query.all()

def update_job(db: Session , job_id: int , updated_job: schemas.JobCreate):
    job = (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

    if job is None:
        return None
    
    job.title = updated_job.title
    job.company = updated_job.company
    job.salary = updated_job.salary
    job.location = updated_job.location
    

    db.commit()
    db.refresh(job)

    return job

def delete_job(db: Session , job_id : int):
    job = (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

    if job is None:
        return None

    db.delete(job)

    db.commit()

    return job



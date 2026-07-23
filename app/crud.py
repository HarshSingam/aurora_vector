from sqlalchemy.orm import Session
from app import models ,  schemas
from typing import Optional

def create_job(db: Session , job: schemas.JobCreate):
    existing_job = (db.query(models.JobPosting).filter(models.JobPosting.title == job.title,
            models.JobPosting.company == job.company,
            models.JobPosting.skills == job.skills,
            models.JobPosting.salary == job.salary,
            models.JobPosting.location == job.location
        )
        .first())
        

    if existing_job:
        return None

    db_job = models.JobPosting(
        title = job.title,
        company = job.company,
        skills = job.skills,
        salary = job.salary ,
        location = job.location

    )

    db.add(db_job)

    db.commit()

    db.refresh(db_job)

    return db_job

def get_jobs(db, job_id=None, limit=None):
    query = db.query(models.JobPosting)

    if job_id is not None:
        query = query.filter(models.JobPosting.id == job_id)

    # Latest entries first
    query = query.order_by(models.JobPosting.id.desc())

    if limit is not None:
        query = query.limit(limit)

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

def create_user(db , user):
    db_user = models.User(name = user.name , email = user.email , location = user.location,
                          search_terms = user.search_terms)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db):

    return db.query(models.User).all()



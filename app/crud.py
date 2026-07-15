from sqlalchemy.orm import session
from app import models ,  schemas

def create_job(db: session , job: schemas.JobCreate):
    db_job = models.JobPosting(
        id = job.id,
        title = job.title,
        company = job.company,
        salary = job.salary ,
        location = job.location

    )

    db.add(db_job)

    db.commit()

    db.refresh(db_job)

    return db_job

def get_job(db: session):
    return db.query(models.JobPosting).all()

def get_job(db: session , job_id = int ):
    return (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

def get_job(db: session , job_company = str):
    return(db.query(models.JobPosting).filter(models.JobPosting.company == job_company).first())

def update_job(db: session , job_id: int , updated_job: schemas.JobCreate):
    job = (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

    if job is None:
        return None
    
    job.title = updated_job.title
    job.company = updated_job.company
    job.location = updated_job.location
    job.salary = updated_job.salary
    job.status = updated_job.status

    db.commit()
    db.refresh(job)

    return job

def delete_job(db: session , job_id : int):
    job = (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

    if job is None:
        return None

    db.delete(job)

    db.commit()

    return job



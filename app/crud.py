from sqlalchemy.orm import Session
from app import models ,  schemas

def create_job(db: Session , job: schemas.JobCreate):
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

def get_jobs(db: Session):
    return db.query(models.JobPosting).all()

def get_job_by_id(db: Session , job_id = int ):
    return (db.query(models.JobPosting).filter(models.JobPosting.id == job_id).first())

def get_job_by_company(db: Session , job_company = str):
    return(db.query(models.JobPosting).filter(models.JobPosting.company == job_company).first())

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



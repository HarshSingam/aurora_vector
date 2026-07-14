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


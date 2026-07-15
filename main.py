from fastapi import FastAPI ,Depends, HTTPException
from sqlalchemy.orm import Session

from app.connection import Base , engine
from app.db_connection import get_db
from app import crud, schemas



app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return{"message" : "server is running..."}

@app.post("/jobs",response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate , db: Session = Depends(get_db)):
    return crud.create_job(db , job)

@app.get("/jobs", response_model=list[schemas.JobResponse])
def get_jobs(db : Session = Depends(get_db)):
    return crud.get_jobs(db)

@app.get("/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id = int , db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db , job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@app.get("/jobs/{job_company}", response_model=schemas.JobResponse)
def get_job(job_company = str , db: Session = Depends(get_db)):
    job = crud.get_job_by_company(db , job_company)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job

@app.put("/jobs/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)):
    updated_job = crud.update_job(db, job_id, job)

    if updated_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return updated_job


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_job(db, job_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"message": "Job deleted successfully"}






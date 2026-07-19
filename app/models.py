from sqlalchemy import Column, Integer, String
from app.connection import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True , index = True)
    title = Column(String(255),nullable=False)
    company = Column(String(255),nullable=False)
    skills = Column(String(225), nullable= True)
    salary = Column(Integer, nullable=True)
    location = Column(String(255), nullable=False) #nullable won't allow null values
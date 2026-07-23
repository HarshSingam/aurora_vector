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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key= True , index= True)
    name = Column(String(100) , nullable= False)
    email = Column(String(100) , unique= True , nullable= False)
    location = Column(String(100) , nullable= False)
    search_terms = Column(String(500) , nullable= False)



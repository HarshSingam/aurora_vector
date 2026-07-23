from pydantic import BaseModel, ConfigDict
from typing import Optional

class JobCreate(BaseModel):
    title:str
    company: str
    skills: str
    salary: int
    location: str
    

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    skills: Optional[str] = None
    salary: Optional[int] =None 
    location: Optional[str] = None 
     

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    skills: str
    salary: int
    location: str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):

    name: str

    email: str

    location: str

    search_terms: str


class UserResponse(UserCreate):

    id: int

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict
from typing import Optional

class JobCreate(BaseModel):
    title:str
    company: str
    salary: int
    location: str
    

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[int] =None 
    location: Optional[str] = None 
     

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    salary: int
    location: str

    model_config = ConfigDict(from_attributes=True)
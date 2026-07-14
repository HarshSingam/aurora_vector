from pydantic import BaseModel, ConfigDict
from typing import optional 

class JobCreate(BaseModel):
    company: str
    title:str
    location: str
    status: str

class JobUpdate(BaseModel):
    company: optional[str] = None
    title: optional[str] = None 
    location: optional[str] = None 
    status: optional[str] =None 

class JobResponse(BaseModel):
    id: int
    company: str
    title: str
    location: str
    status: str

    model_config = ConfigDict(from_attributes=True)
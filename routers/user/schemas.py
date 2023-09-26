
from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class User(UserCreate):
    id: Optional[int]=None
    username:str
    is_active: Optional[bool]=None
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type:str
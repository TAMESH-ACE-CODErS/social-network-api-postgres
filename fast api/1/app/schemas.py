from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- POST SCHEMAS ---

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# --- USER SCHEMAS ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# We create a specific UserOut schema so we don't accidentally send passwords back!
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# --- USER SCHEMAS ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    # Pydantic V2 syntax for ORM mode
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    owner_id: int
    owner: UserOut
    
    # Pydantic V2 syntax for ORM mode
    model_config = ConfigDict(from_attributes=True)

# --- AUTH SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1) #le means less than equal to
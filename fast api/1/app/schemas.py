from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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
        # THE FIX 2: Silences the Pydantic V2 Warning!
        from_attributes = True

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
        # THE FIX 2: Silences the Pydantic V2 Warning!
        from_attributes = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# --- AUTHENTICATION SCHEMAS ---
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]
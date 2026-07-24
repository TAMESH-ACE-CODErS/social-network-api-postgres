from .database import Base
# 1. FIXED: You must import the specific data types from sqlalchemy!
from sqlalchemy import Column, Integer, String, Boolean

#we are creating the table datas
class Post(Base):
    __tablename__="posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title=Column(String, nullable=False, )
    content=Column(String,nullable=False,)
    published=Column(Boolean,default=True)
    
    
    





from .database import Base
# 1. FIXED: You must import the specific data types from sqlalchemy!
from sqlalchemy import Column, Integer, String, Boolean,text
from sqlalchemy.sql.sqltypes import TIMESTAMP

#we are creating the table datas
class Post(Base):
    __tablename__="posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title=Column(String, nullable=False, )
    content=Column(String,nullable=False,)
    published=Column(Boolean,server_default="TRUE" ,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
#PGsql AND THIS CODE works differently meaning it would look for "post" table only if it is not found it would create meaning if one table is there it won't alter it (drop the table again and again tand run this code and save)
    





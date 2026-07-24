# 1. FIXED: Added 'Depends' to the fastapi import list
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import sys

# 2. FIXED: Added Session import from sqlalchemy
from sqlalchemy.orm import Session

from . import models 
from .database import engine, SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 

try: 
    connect = psycopg2.connect(
        host='localhost', 
        database='fastapi',
        user='postgres', 
        password='password123',
        cursor_factory=RealDictCursor
    )
    cursor = connect.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Connection to database failed. Error was:")
    print(error)

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "i like pizza", "id": 2}
]

# 3. FIXED: Now 'Session' and 'Depends' are properly imported at the top!
@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "SQLAlchemy is working!"}

@app.get('/')
async def root():
    return {'message': 'hello world123'}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    connect.commit()
    
    return {"data": new_post}

@app.get("/posts/latest") 
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} was not found'
        ) 
    return {"post_details": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    connect.commit()
    
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
        (post.title, post.content, post.published, str(id))
    )
    updated_post = cursor.fetchone()
    connect.commit()
    
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
        
    return {'data': updated_post}
# 1. FIXED: Cleaned up all the duplicate imports at the top!
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import sys

from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

app = FastAPI()

# 2. FIXED: Put the get_db function back so your database can actually open!
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

# 3. FIXED: Removed the empty duplicate GET /sqlalchemy route that was sitting here!

@app.get('/')
async def root():
    return {'message': 'hello world123'}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts=db.query(models.Post).all()
    return {'data': posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # connect.commit()
    print(post.dict())
    new_post=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/latest") 
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first() #look for the the post
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} was not found'
        ) 
    return {"post_details": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # connect.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post,db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
    #     (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # connect.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {'data': post_query.first()}

# 4. FIXED: Kept Sanjeev's real SQLAlchemy test route here at the bottom
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # this is gonna grab every row in the posts table
    posts = db.query(models.Post).all() 
    
    # (Sanjeev just wrote "SELECT * FROM posts" here so you remember what ORM is doing under the hood!)
    print(posts)
    return {"data": posts}
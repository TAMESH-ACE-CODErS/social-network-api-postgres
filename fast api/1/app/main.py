from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import sys

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 

try: 
    # Attempt to connect to the database
    connect = psycopg2.connect(
        host='localhost', 
        database='fastapi',
        user='postgres', 
        password='password123', # Make sure this is your actual password!
        cursor_factory=RealDictCursor
    )
    cursor = connect.cursor()
    print("Database connection was successful!")
except Exception as error:
    print("Connection to database failed. Error was:")
    print(error)

# In-memory array (Left here ONLY for /posts/latest until you migrate it in the video)
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "i like pizza", "id": 2}
]

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
    post=cursor.fetchone()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} was not found'
        ) 
    return {"post_details": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # 1. EXECUTE: Fixed table name 'posts' and added '*' to RETURNING
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    
    # 2. FETCH: Grab the deleted row
    deleted_post = cursor.fetchone()
    
    # 3. COMMIT: Permanently save the deletion
    connect.commit()
    
    # 4. VALIDATE: Check if the row actually existed
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
    
    # 5. RETURN
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # 1. EXECUTE: Removed the illegal '=' and formatted correctly
    cursor.execute(
        """UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
        (post.title, post.content, post.published, str(id))
    )
    
    # 2. FETCH: Grab the newly updated row
    updated_post = cursor.fetchone()
    
    # 3. COMMIT: Permanently save the update
    connect.commit()
    
    # 4. VALIDATE: Check the fetched variable, NOT the function name
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
        
    # 5. RETURN: Send the actual updated data back to the user
    return {'data': updated_post}
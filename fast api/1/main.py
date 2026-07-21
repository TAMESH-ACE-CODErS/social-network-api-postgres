from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import status

# Type this line slowly. Stop after the dot.
my_status = status.HTTP_
app=FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published:bool = True # default valued will be true 
    rating:Optional[int]=None #a integer field if the user doesnot provide it , it will be none
        
my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favourite foods","content":"i like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
    return None #if no id is found

@app.get('/')
async def root():
    return {'message':'hello world123'}

@app.get('/posts')
def get_posts():
    return {'data':my_posts}

@app.post('/createposts')
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data": post_dict }

@app.get("/posts/latest") # collision with @app.get("/posts/{id}") pipeline here order does matter  as {id} is taken as latest
def get_latest_post():
    post =my_posts[len(my_posts)-1]
    return {"details":post}

@app.get("/posts/{id}")
def get_post(id:int): # it will check it is a integer
    print(type(id))#as this is a string we need to convert it
    post=find_post(int(id))
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found') 
    return {"post_details":f"{post}"}


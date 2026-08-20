from fastapi import FastAPI, Response, status, HTTPException, Depends ,APIRouter
from typing import List
import psycopg2,time 
from psycopg2.extras import RealDictCursor
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .. import models, schemas,utils
from ..database import engine, SessionLocal 

# Create all tables in the database (if they don't exist)
models.Base.metadata.create_all(bind=engine)

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto") #use of hashing 

router =APIRouter(
    prefix="/posts" , 
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Keep your raw psycopg2 connection here just for the print statement if you want, 
# but SQLAlchemy handles all the actual work now!
try: 
    connect = psycopg2.connect(
        host='localhost', 
        database='fastapi',
        user='postgres', 
        password='password123',
        cursor_factory=RealDictCursor
    )
    cursor = connect.cursor()
    print("Raw psycopg2 connection was successful!")
except Exception as error:
    print("Connection to database failed. Error was:")
    print(error)


@router.get('/')
async def root():
    return {'message': 'hello world123'}

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} was not found'
        ) 
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id:{id} does not exist'
        )
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


# app.include_router(post.router)
# app.include_router(user.router)
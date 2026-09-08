from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'] 
)

# FIX: Removed the duplicate root ('/') route from this file
@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Removed the duplicate unauthenticated create_posts route that was here!

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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    print(user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # THE FIX: We must return the post so Pydantic can validate and send it!
    return new_post
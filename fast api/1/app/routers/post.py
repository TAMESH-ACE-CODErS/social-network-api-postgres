from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db 

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10):
    print(limit)
    posts = db.query(models.Post).limit(limit).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # We require the user to be logged in to reach this point!
    # print(user_id.id)
    # print(user_id.email)
    new_post = models.Post(owner_id=user_id.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    post = db.query(models.Post).filter(models.Post.id == current_user.id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} was not found') 
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exist')
    
    if post.owner_id!=oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,details=f"not authorized to perform action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exist')
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
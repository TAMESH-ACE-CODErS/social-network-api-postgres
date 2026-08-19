#all operations regarding users
from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends , APIRouter
from sqlalchemy.orm import Session
from .. import database
from typing import List

router=APIRouter()

#this for user creations
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the passwords - user . password 
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/users/{id}')
def get_user(id:int, db:Session=Depends(get_db),response_model=schemas.UserOut):
    user=db.query(models.User).filter(models.User.id==id).first()  
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id}")
    
    return user 
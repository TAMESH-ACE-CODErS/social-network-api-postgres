from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # We create an expiration time by taking the exact current time, 
    # and adding 30 minutes to it!
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # We update the dictionary to include the expiration time under the "exp" key
    to_encode.update({"exp": expire})
    
    # We use the jwt library to encode the data, the secret key, and the algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# We only need ONE import line so we don't accidentally overwrite things!
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # FIX: We MUST use .username here because of the OAuth2 Form
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )
        
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid Credentials" 
        )
        
    # create a token
    # We are passing the user's ID as the "payload" data that gets hidden inside the token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # return token
    # We return it in this exact format because it is the industry standard!
    return {"access_token": access_token, "token_type": "bearer"}
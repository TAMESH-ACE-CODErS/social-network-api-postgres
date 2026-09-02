from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas, models, utils ,oauth2

# THE FIX: We added 'utils' to this import list!
from .. import database, schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm=Depends() , db: Session = Depends(database.get_db)):
    {
        "username":"asdf",
        "password":"alsdjf"
    }
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials"
        )
        
    # Now Python knows exactly what 'utils' is!
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Invalid Credentials" 
        )
        
    # create a token
    # return token
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token": access_token,"token_type":"bearer"}



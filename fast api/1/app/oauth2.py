from jose import JWTError ,jwt
from datetime import datetime , timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_schemes=OAuth2PasswordBearer(tokenUrl="")

#SECRET_KEY
#ALGORITHM
#Expiration time

SECRET_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTE=30 #After 30min it should be expiring

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnowt()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],)
        id:str=payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(id=id)
    except JWTError : 
        raise credential_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_schemes)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZE,
        details=f"Couldnot validate credentials_exception",header={"WWW-Authenticate":"Bearer"}
        )
    return verify_access_token(token,credential_exception)
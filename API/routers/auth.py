import sys
sys.path.append("..")

import models
from database import engine
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from database import get_db

models.Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "8894dce1708e9e9732c0c5167f654fc62b372fb7f8d7b609ffbbac6d7022351b"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(
    tags=["user"]
)

def get_password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False  # Unknown user
    if not verify_password(password, user.hashedpassword):
        return False  # Incorrect password
    return user  # successful

def create_access_token(username:str, user_id:int, expires_delta:Optional[timedelta]=None):
    encode = {"sub":username, "id":user_id}
    if expires_delta:
        expire = expires_delta + datetime.utcnow()
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@router.post('/registration')
async def identify_user(new_user:models.CreateUser, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == new_user.username).first()
    if user is None:
        hashed_password = get_password_hash(new_user.password)
        user_to_add = models.Users(username=new_user.username,hashedpassword = hashed_password,
        email=new_user.email, firstname=new_user.firstname, lastname=new_user.lastname)
        db.add(user_to_add)
        db.commit()
        return {"message": "You are successfully signed in."}

    raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        detail="This username is not available. Choose another one please!")


@router.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends(),
                                db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(username=user.username, user_id=user.id, expires_delta = token_expires)
    # return {"access_token": token}
    return {
            "access_token": token,
            "token_type":"bearer",
            "user_id":user.id,
            "username":user.username
            }


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
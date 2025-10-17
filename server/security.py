from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import jwt

from db import SessionDep
from userModel import UserInDB, UserPublic
from sqlModels import User


load_dotenv()
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minuites = os.getenv("ACCESS_TOKEN_EXPIRE_MINUITES")




pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def authenticate_user(email: str, password: str, session:SessionDep):
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user:
        print("DEBUG: Email/User not found.") 
        return False
    if not verify_password(password, user.password):
        print("DEBUG: Password verification failed.") # Add this
        return False
    print(f"DEBUG: User authenticated. Returning UserPublic for: {user.email}") # Add this
    return UserPublic(**user.dict())

def create_access_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc)+ timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# def get_user(email:str, session: SessionDep):
#     statement = select(User).where(User.email == email)
#     result = session.exec(statement).first()
#     if result is None:
#         return None
#     return UserInDB(**result.dict()) 

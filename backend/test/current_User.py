from fastapi import HTTPException,status, Request
from jwt import InvalidTokenError, ExpiredSignatureError
from dotenv import load_dotenv
import logging 
import os
import uuid
import jwt

from ..models.userModel import UserPublic
from ..models.sqlModels import User
from ..utils.db import SessionDep


logger = logging.getLogger(__name__) 

# openssl rand -hex 32
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minuites = os.getenv("ACCESS_TOKEN_EXPIRE_MINUITES")

async def current_user(
        request: Request, 
        session: SessionDep) -> UserPublic:

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Check if the request has a cookie named 'user_session'
    if "user_session" not in request.cookies:
        logger.warning("No 'user_session' cookie found in the request.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token not received"
        )
    # If the cookie exists, proceed to decode the JWT token
    logger.info("Cookie 'user_session' found in the request.")  

    try:
        logger.info("Attempting to get user_session cookie.")
        token = request.cookies.get("user_session")  # use correct cookie name
        print(f"DEBUG: Token found: {token}")
        if not token:
            print(f"DEBUG: Token not found: {token}")
            logger.warning("No 'user_session' cookie found.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token not recevied"
            )
        logger.info(f"Cookie 'user_session' found. Token starts with: {token[:20]}...")
        
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(f"DEBUG: Payload  found: {payload}")

        userId_str = payload.get("sub")
        userRole = payload.get("role")
        userName = payload.get("user_name")
        userEmail = payload.get("user_email")

        if not all([userId_str, userName, userRole, userEmail]):
            logger.warning(f"Missing required claims in JWT payload: sub={userId_str}, name={userName}, role={userRole}, email={userEmail}")
            raise credentials_exception

        userId = uuid.UUID(userId_str)
        user = session.get(User, userId)
        if user is None:
            logger.warning(f"User with ID {userId} not found in database.")
            raise credentials_exception
        

    except ExpiredSignatureError:
        # Catch the specific error for expired tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise credentials_exception
    logger.info(f"User found: {user.email}")

    # return current_user
    return UserPublic(**user.dict())

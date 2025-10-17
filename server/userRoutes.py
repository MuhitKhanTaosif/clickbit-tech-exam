from fastapi import APIRouter, Depends, Form, Response, Request, HTTPException,status
from sqlmodel import select
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID
from datetime import datetime, timedelta, timezone

# from ..models.userModel import User
from sqlModels import User
from userModel import UserPublic, UserFormData
from dependencies import  (access_token_expire_minuites,
                            current_user
                            )

from security import get_password_hash, create_access_token
from db import SessionDep 

router = APIRouter(
    prefix="/user",
    tags=["authentication", "authorization"]
)


@router.get('/me')
async def user(current_user: Annotated[UserPublic, Depends(current_user)], session: SessionDep):
    return current_user


@router.post('/auth/register', response_model=UserPublic)
async def createAccount(
    formData: Annotated[UserFormData, Form()],
    response: Response,
    request: Request,
    session: SessionDep):
    # Check if the email already exists in the database
    existing_user = session.exec(select(User).where(User.email == formData.email)).first()
    if existing_user:
        raise HTTPException(        
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    # Note: UserFormData should have fields: firstName, lastName, email, password
    if not formData.firstName or not formData.lastName or not formData.email or not formData.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required: firstName, lastName, email, and password."
        )   
    if len(formData.password) < 8:  # Example password policy check
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )               
    if '@' not in formData.email or '.' not in formData.email.split('@')[-1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format."
        )                                   
    # Create a new User instance    
    new_user = User(
        firstName = formData.firstName,
        lastName = formData.lastName,
        email = formData.email,
        password = get_password_hash(formData.password)
    )
    # Check if the request has a cookie named 'user_session'
    if "user_session" in request.cookies:
        response.delete_cookie(key="user_session", 
                            path="/",
                            domain=".tajuwa.com",
                            secure=True,
                            httponly=True,
                            samesite="None",)

    session.add(new_user)
    session.commit()
    # session.refresh(new_user)
    # After creating the user, we can create an access token
    # Note: The user object should be the newly created user, not the one from the current_user dependency
    print(f"DEBUG(createAccount): User object BEFORE token creation: ID={new_user.id}, Name={new_user.firstName}, Email={new_user.email}, Role={new_user.role}")
    access_token_expires = timedelta(minutes=int(access_token_expire_minuites))
    access_token = create_access_token(
        data = {"sub": str(new_user.id),
                "user_name": new_user.firstName,
                "user_email": new_user.email,
                "role": new_user.role
                }, 
        expires_delta= access_token_expires
    )
    print(f"Debug after token creation Access Token: {access_token}")
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(access_token_expire_minuites))
    expires_str = expire_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    # response.set_cookie(key="user_session",
    #                     value=access_token,
    #                     secure=True,
    #                     httponly=True,
    #                     samesite="None",
    #                     # partitioned=False,
    #                     # max_age= access_token_expire_minuites* 60,
    #                     # expires= expires_str, 
    #                     path="/",
    #                     domain=".tajuwa.com",  
    #                     )
    return new_user


@router.post('/logout')
async def logout_user(
    response: Response,
    user: Annotated[UserPublic, Depends(current_user)], # Requires an authenticated user to logout
    session: SessionDep
):
    try:
        # 1. Invalidate the user's current token by incrementing their token_version
        # This makes any existing JWTs for this user invalid for future requests.
        db_user = session.exec(select(User).where(User.id == user.id)).first()
        if not db_user:
            # This case should ideally not happen if current_user dependency works correctly,
            # but it's a good safeguard.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in database."
            )

        db_user.token_version += 1
        session.add(db_user)
        session.commit()
        session.refresh(db_user) # Refresh to ensure the token_version is updated in the session

        # 2. Clear the session cookie from the client's browser
        # Ensure the cookie parameters match those used when setting the cookie during login
        response.delete_cookie(
            key="user_session",
            secure=True,
            httponly=True,
            samesite="Strict",
        )

        return {"message": "Logout successful"}

    except HTTPException as e:
        # Re-raise any HTTPExceptions
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"Error during logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during logout."
        )


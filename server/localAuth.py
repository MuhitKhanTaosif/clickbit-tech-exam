from fastapi import APIRouter, Response, HTTPException, Form
from pydantic import BaseModel
from typing import Annotated
from datetime import timedelta, datetime, timezone
import os

from security import (
    authenticate_user,
    # access_token_expire_minuites,
    create_access_token,
)
from db import SessionDep
from userModel import UserLoginFromData

access_token_expire_minuites = os.getenv("ACCESS_TOKEN_EXPIRE_MINUITES")



router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    formData: Annotated[UserLoginFromData, Form()],
    response: Response,
    session: SessionDep,
):

    email = formData.email
    plain_password = formData.password
    user = authenticate_user(email, plain_password, session=session)
    print("user not found/error credentials") if not user else print("*user found")
    
    #print(f"Debug after user authenticated: {if not user: print(""Such email is not found")}")
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # response.delete_cookie(
    #     key="user_session",
    #     #path="/",
    #     #domain=None,
    #     secure=True,
    #     httponly=True,
    #     samesite="Strict",
    # )
    # print(
    #     f"DEBUG(localAuth): User object BEFORE token creation: ID={user.id}, Name={user.firstName}, Email={user.email}, Role={user.role}"
    # )

    access_token_expires = timedelta(minutes=int(access_token_expire_minuites))
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "user_name": user.firstName,
            "user_email": user.email,
            "role": user.role,
        },
        expires_delta=access_token_expires,
    )

    #print(f"Debug after token creation Access Token: {access_token}")

    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=int(access_token_expire_minuites)
    )
    expires_str = expire_time.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    
    print(f"DEBUG: About to set cookie with token: {access_token[:20]}...")
    print(f"DEBUG: Cookie expiry: {expires_str}")

    # response.set_cookie(
    #     key="user_session",
    #     value=access_token,
    #     secure=True,
    #     httponly=True,
    #     samesite="None",  # Changed from "Strict" for cross-site requests
    #     path="/",  # Explicitly set path
    #     domain=".tajuwa.com",  # Added leading dot for subdomain access
    #     expires=expires_str,
    #     # max_age=access_token_expire_minuites * 60,  # Alternative to expires
    # )

    response.status_code = 200
    
    return {
        "message": "Login successful", 
        "token": access_token,
        "expires_in": expires_str
    }

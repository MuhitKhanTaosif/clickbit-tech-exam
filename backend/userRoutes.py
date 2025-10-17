from fastapi import APIRouter, Depends, Form, Response, Request, HTTPException, status
from sqlmodel import select
from pydantic import ValidationError
from typing import Annotated
from uuid import UUID
from datetime import datetime, timedelta, timezone
import logging

from models.sqlModels import User
from models.userModel import (
    UserPublic, UserCreate, UserLogin, UserUpdate, UserResponse, 
    LoginResponse, LogoutResponse, UserFormData, UserLoginFromData
)
from dependencies import access_token_expire_minuites
from test.current_User import current_user
from utils.security import (
    get_password_hash, create_access_token, verify_password, 
    authenticate_user, validate_password_strength
)
from utils.db import SessionDep
from utils.logger import security_logger, request_logger
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user",
    tags=["authentication", "authorization"]
)

@router.get('/me', response_model=UserPublic)
async def get_current_user(
    current_user: Annotated[UserPublic, Depends(current_user)], 
    session: SessionDep
):
    """Get current user profile."""
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

@router.post('/auth/login', response_model=LoginResponse)
async def login(
    formData: Annotated[UserLoginFromData, Form()],
    response: Response,
    request: Request,
    session: SessionDep
):
    """Authenticate user and create session."""
    try:
        # Validate input
        if not formData.email or not formData.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )

        # Authenticate the user
        user = authenticate_user(formData.email, formData.password, session)
        if not user:
            # Log failed authentication attempt
            security_logger.log_auth_attempt(
                email=formData.email,
                success=False,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent"),
                reason="Invalid credentials"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get the full user object from database
        db_user = session.exec(select(User).where(User.email == formData.email)).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user is active
        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        

        
        # Update last login time
        db_user.last_login = datetime.now(timezone.utc)
        session.add(db_user)
        session.commit()
        
        # Set secure cookie
        response.set_cookie(
            key="user_session",
            value=access_token,
            secure=True,
            httponly=True,
            samesite="None",
            path="/",
            domain=".tajuwa.com",  
        )
        
        # Log successful authentication
        security_logger.log_auth_attempt(
            email=formData.email,
            success=True,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent")
        )
        
        return LoginResponse(user=user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for user {formData.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.post('/auth/register', response_model=UserResponse)
async def register(
    formData: Annotated[UserFormData, Form()],
    response: Response,
    request: Request,
    session: SessionDep
):
    """Register a new user account."""
    try:
        # Validate input
        if not all([formData.firstName, formData.lastName, formData.email, formData.password]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All fields are required: firstName, lastName, email, and password"
            )
        
        # Validate password strength
        password_validation = validate_password_strength(formData.password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password validation failed: {', '.join(password_validation['errors'])}"
            )

        # Check if email already exists
        existing_user = session.exec(select(User).where(User.email == formData.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        new_user = User(
            firstName=formData.firstName.strip(),
            lastName=formData.lastName.strip() if formData.lastName else None,
            email=formData.email.lower().strip(),
            password=get_password_hash(formData.password),
            is_active=True,
            is_verified=False  # Require email verification
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        # Create access token for immediate login
        access_token_expires = timedelta(minutes=int(access_token_expire_minuites))
        access_token = create_access_token(
            data={
                "sub": str(new_user.id),
                "user_name": new_user.firstName,
                "user_email": new_user.email,
                "role": new_user.role
            }, 
            expires_delta=access_token_expires
        )
        
        # Clear any existing session cookie
        if "user_session" in request.cookies:
            response.delete_cookie(
                key="user_session", 
                path="/",
                domain=".tajuwa.com",
                secure=True,
                httponly=True,
                samesite="None"
            )

        # Set secure cookie
        response.set_cookie(
            key="user_session",
            value=access_token,
            secure=True,
            httponly=True,
            samesite="None",
            path="/",
            domain=".tajuwa.com",  
        )
        
        # Create public user response
        user_public = UserPublic.model_validate(new_user)
        
        logger.info(f"New user registered: {new_user.email}")
        
        return UserResponse(
            message="User registered successfully",
            user=user_public
        )
        
    except HTTPException:
        raise
    except ValidationError as e:
        logger.error(f"Validation error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.post('/logout', response_model=LogoutResponse)
async def logout_user(
    response: Response,
    user: Annotated[UserPublic, Depends(current_user)],
    session: SessionDep
):
    """Logout user and invalidate session."""
    try:
        # Get user from database
        db_user = session.exec(select(User).where(User.id == user.id)).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Invalidate token by incrementing token_version
        db_user.token_version += 1
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        # Clear session cookie
        response.delete_cookie(
            key="user_session",
            secure=True,
            httponly=True,
            samesite="Strict",
            path="/"
        )

        logger.info(f"User logged out: {user.email}")
        return LogoutResponse()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Logout error for user {user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during logout"
        )

@router.put('/profile', response_model=UserPublic)
async def update_profile(
    user_data: UserUpdate,
    current_user: Annotated[UserPublic, Depends(current_user)],
    session: SessionDep
):
    """Update user profile."""
    try:
        # Get user from database
        db_user = session.exec(select(User).where(User.id == current_user.id)).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(db_user, field, value.strip() if isinstance(value, str) else value)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        
        logger.info(f"User profile updated: {current_user.email}")
        return UserPublic.model_validate(db_user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating profile"
        )

@router.post('/change-password')
async def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    current_user: Annotated[UserPublic, Depends(current_user)] = Depends(current_user),
    session: SessionDep = Depends()
):
    """Change user password."""
    try:
        # Get user from database
        db_user = session.exec(select(User).where(User.id == current_user.id)).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not verify_password(current_password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password strength
        password_validation = validate_password_strength(new_password)
        if not password_validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"New password validation failed: {', '.join(password_validation['errors'])}"
            )
        
        # Update password
        db_user.password = get_password_hash(new_password)
        db_user.token_version += 1  # Invalidate existing tokens
        session.add(db_user)
        session.commit()
        
        logger.info(f"Password changed for user: {current_user.email}")
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while changing password"
        )

from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from uuid import UUID
from datetime import datetime
from typing import Optional
import re

class UserBase(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50, description="User's first name")
    lastName: Optional[str] = Field(None, max_length=50, description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    
    @validator('firstName', 'lastName')
    def validate_names(cls, v):
        if v is not None and not re.match(r'^[a-zA-Z\s\'-]+$', v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")

class UserUpdate(BaseModel):
    firstName: Optional[str] = Field(None, min_length=1, max_length=50)
    lastName: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)

class UserPublic(UserBase):
    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    phone: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    id: UUID
    password: str
    role: str
    is_active: bool
    is_verified: bool
    token_version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    message: str
    user: UserPublic

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic

class LoginResponse(BaseModel):
    message: str = "Login successful"
    user: UserPublic

class LogoutResponse(BaseModel):
    message: str = "Logout successful"

# Legacy aliases for backward compatibility
UserFormData = UserCreate
UserLoginFromData = UserLogin
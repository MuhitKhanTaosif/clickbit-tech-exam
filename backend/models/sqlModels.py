from sqlmodel import SQLModel, Field, Relationship, CheckConstraint, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import event, String
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from enum import Enum
import re


class UserAuthProvider(str, Enum):
    local = "local-oauth2"
    google = "https://accounts.google.com"
    facebook = "facebook-oauth2"

class UserRole(str, Enum):
    BUYER = "buyer"
    ADMIN = "admin"

class Units(str, Enum):
    cm = "cm"
    m = "m"
    ft = "ft"
    inch = "inch"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRM = "confirm"
    PROCESSING = "processing"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
    CANCELED = "canceled"
    REFUNDED = "refunded"

class RegionEnum(str, Enum):
    DHAKA = "Dhaka"
    CHITTAGONG = "Chittagong"
    RAJSHAHI = "Rajshahi"
    KHULNA = "Khulna"
    BARISAL = "Barishal"
    SYLHET = "Sylhet"
    RANGPUR = "Rangpur"
    MYMENSINGH = "Mymensingh"

class PaymentMethod(str, Enum):
    ONLINE = "online"
    ONDELEVERY = "on_delivery"

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    firstName: str = Field(index=True, min_length=1, max_length=50)
    lastName: str | None = Field(default=None, max_length=50)
    email: str = Field(
        index=True, 
        unique=True,
        sa_column=Column("email", String, CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="valid_email"
        ))
    )
    password: str | None = Field(default=None, min_length=8)

    auth_provider: UserAuthProvider = Field(default=UserAuthProvider.local, index=True)
    provider_id: str | None = Field(default=None, index=True)

    role: UserRole = Field(default=UserRole.BUYER, index=True)

    is_active: bool = Field(default=True, index=True)
    is_verified: bool = Field(default=False, index=True)
    last_login: datetime | None = None
    token_version: int = Field(default=0)
    
    # Profile information
    phone: str | None = Field(default=None, max_length=20)
    avatar_url: str | None = Field(default=None, max_length=500)
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Soft delete
    deleted_at: datetime | None = Field(default=None, index=True)

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True

# Event listener to update updated_at timestamp
@event.listens_for(User, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.utcnow()

# Additional models for future expansion
class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    session_token: str = Field(unique=True, index=True)
    expires_at: datetime = Field(index=True)
    is_active: bool = Field(default=True, index=True)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserVerification(SQLModel, table=True):
    __tablename__ = "user_verifications"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    verification_token: str = Field(unique=True, index=True)
    verification_type: str = Field(index=True)  # email, phone, etc.
    expires_at: datetime = Field(index=True)
    is_used: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used_at: datetime | None = None



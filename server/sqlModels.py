from sqlmodel import SQLModel, Field, Relationship, CheckConstraint, Column
from sqlalchemy.dialects.postgresql import JSONB
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from enum import Enum


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    firstName: str = Field(index=True)
    lastName: str | None = None
    email: str = Field(index=True, unique=True)
    password: str | None = None

    auth_provider: UserAuthProvider = Field(default=UserAuthProvider.local, index=True)
    provider_id: str | None = Field(default=None, index=True)

    role: UserRole = Field(default=UserRole.BUYER, index=True)

    is_active: bool = Field(default=True)
    last_login: datetime | None = None
    token_version: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

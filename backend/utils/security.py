from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import jwt
import secrets
import logging
from typing import Optional, Dict, Any
from functools import wraps

from utils.db import SessionDep
from models.userModel import UserInDB, UserPublic
from models.sqlModels import User

logger = logging.getLogger(__name__)

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_verification_token() -> str:
    """Generate a secure random token for email verification."""
    return secrets.token_urlsafe(32)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Access token created for user: {data.get('sub', 'unknown')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Refresh token created for user: {data.get('sub', 'unknown')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create refresh token: {e}")
        raise

def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != token_type:
            logger.warning(f"Invalid token type. Expected: {token_type}, Got: {payload.get('type')}")
            return None
            
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            logger.warning("Token has expired")
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token signature has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return None

def authenticate_user(email: str, password: str, session: SessionDep) -> Optional[UserPublic]:
    """Authenticate a user with email and password."""
    try:
        statement = select(User).where(
            User.email == email,
            User.is_active == True,
            User.deleted_at.is_(None)
        )
        user = session.exec(statement).first()
        
        if not user:
            logger.warning(f"Authentication failed: User not found or inactive - {email}")
            return None
            
        if not user.password or not verify_password(password, user.password):
            logger.warning(f"Authentication failed: Invalid password for user - {email}")
            return None
            
        logger.info(f"User authenticated successfully: {email}")
        return UserPublic.model_validate(user)
        
    except Exception as e:
        logger.error(f"Authentication error for user {email}: {e}")
        return None

def get_user_by_id(user_id: str, session: SessionDep) -> Optional[User]:
    """Get a user by ID from the database."""
    try:
        statement = select(User).where(
            User.id == user_id,
            User.is_active == True,
            User.deleted_at.is_(None)
        )
        return session.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by ID {user_id}: {e}")
        return None

def get_user_by_email(email: str, session: SessionDep) -> Optional[User]:
    """Get a user by email from the database."""
    try:
        statement = select(User).where(
            User.email == email,
            User.deleted_at.is_(None)
        )
        return session.exec(statement).first()
    except Exception as e:
        logger.error(f"Error getting user by email {email}: {e}")
        return None

def rate_limit_key_generator(request, endpoint: str = None) -> str:
    """Generate a rate limiting key based on IP and endpoint."""
    ip = request.client.host if request.client else "unknown"
    endpoint = endpoint or request.url.path
    return f"rate_limit:{ip}:{endpoint}"

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return detailed feedback."""
    errors = []
    score = 0
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    else:
        score += 1
        
    if len(password) > 128:
        errors.append("Password must be less than 128 characters")
        
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    else:
        score += 1
        
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    else:
        score += 1
        
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")
    else:
        score += 1
        
    if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        errors.append("Password must contain at least one special character")
    else:
        score += 1
    
    # Check for common patterns
    common_patterns = ["123", "abc", "password", "qwerty", "admin"]
    if any(pattern in password.lower() for pattern in common_patterns):
        errors.append("Password contains common patterns")
        score -= 1
    
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    strength = strength_levels[min(score, 4)] if score >= 0 else "Very Weak"
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "score": max(0, score),
        "strength": strength
    }
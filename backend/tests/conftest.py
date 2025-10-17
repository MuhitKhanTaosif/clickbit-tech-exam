"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from main import app
from config import settings
from utils.db import get_session
from models.sqlModels import User, UserRole
from utils.security import get_password_hash

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def test_session(test_engine) -> Generator[Session, None, None]:
    """Create test database session."""
    with Session(test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def test_client(test_session):
    """Create test client with database session override."""
    def get_test_session():
        yield test_session
    
    app.dependency_overrides[get_session] = get_test_session
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(test_session):
    """Create a test user."""
    user = User(
        firstName="Test",
        lastName="User",
        email="test@example.com",
        password=get_password_hash("TestPassword123!"),
        role=UserRole.BUYER,
        is_active=True,
        is_verified=True
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user

@pytest.fixture
def test_admin(test_session):
    """Create a test admin user."""
    admin = User(
        firstName="Admin",
        lastName="User",
        email="admin@example.com",
        password=get_password_hash("AdminPassword123!"),
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    test_session.add(admin)
    test_session.commit()
    test_session.refresh(admin)
    return admin

@pytest.fixture
def auth_headers(test_client, test_user):
    """Get authentication headers for test user."""
    response = test_client.post(
        "/user/auth/login",
        data={
            "email": test_user.email,
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 200
    
    # Extract cookies from response
    cookies = response.cookies
    return {"Cookie": f"user_session={cookies.get('user_session')}"}

@pytest.fixture
def admin_auth_headers(test_client, test_admin):
    """Get authentication headers for test admin."""
    response = test_client.post(
        "/user/auth/login",
        data={
            "email": test_admin.email,
            "password": "AdminPassword123!"
        }
    )
    assert response.status_code == 200
    
    # Extract cookies from response
    cookies = response.cookies
    return {"Cookie": f"user_session={cookies.get('user_session')}"}


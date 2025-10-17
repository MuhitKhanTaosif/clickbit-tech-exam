"""
Integration tests for authentication endpoints.
"""
import pytest
from fastapi import status

class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_success(self, test_client):
        """Test successful user registration."""
        response = test_client.post(
            "/user/auth/register",
            data={
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "password": "SecurePassword123!"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["email"] == "john.doe@example.com"
        assert data["user"]["firstName"] == "John"
        assert data["user"]["lastName"] == "Doe"
        assert "user_session" in response.cookies
    
    def test_register_duplicate_email(self, test_client, test_user):
        """Test registration with duplicate email."""
        response = test_client.post(
            "/user/auth/register",
            data={
                "firstName": "Jane",
                "lastName": "Doe",
                "email": test_user.email,  # Duplicate email
                "password": "AnotherPassword123!"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_weak_password(self, test_client):
        """Test registration with weak password."""
        response = test_client.post(
            "/user/auth/register",
            data={
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.weak@example.com",
                "password": "weak"  # Weak password
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Password validation failed" in response.json()["detail"]
    
    def test_register_missing_fields(self, test_client):
        """Test registration with missing required fields."""
        response = test_client.post(
            "/user/auth/register",
            data={
                "firstName": "John",
                # Missing lastName, email, password
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_success(self, test_client, test_user):
        """Test successful user login."""
        response = test_client.post(
            "/user/auth/login",
            data={
                "email": test_user.email,
                "password": "TestPassword123!"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Login successful"
        assert data["user"]["email"] == test_user.email
        assert "user_session" in response.cookies
    
    def test_login_invalid_email(self, test_client):
        """Test login with invalid email."""
        response = test_client.post(
            "/user/auth/login",
            data={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, test_client, test_user):
        """Test login with invalid password."""
        response = test_client.post(
            "/user/auth/login",
            data={
                "email": test_user.email,
                "password": "WrongPassword123!"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_inactive_user(self, test_client, test_session):
        """Test login with inactive user."""
        from models.sqlModels import User, UserRole
        from utils.security import get_password_hash
        
        # Create inactive user
        inactive_user = User(
            firstName="Inactive",
            lastName="User",
            email="inactive@example.com",
            password=get_password_hash("Password123!"),
            role=UserRole.BUYER,
            is_active=False
        )
        test_session.add(inactive_user)
        test_session.commit()
        
        response = test_client.post(
            "/user/auth/login",
            data={
                "email": inactive_user.email,
                "password": "Password123!"
            }
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Account is deactivated" in response.json()["detail"]

class TestUserProfile:
    """Test user profile functionality."""
    
    def test_get_current_user(self, test_client, auth_headers, test_user):
        """Test getting current user profile."""
        response = test_client.get("/user/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user.email
        assert data["firstName"] == test_user.firstName
        assert data["lastName"] == test_user.lastName
    
    def test_get_current_user_unauthorized(self, test_client):
        """Test getting current user without authentication."""
        response = test_client.get("/user/me")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_update_profile(self, test_client, auth_headers, test_user):
        """Test updating user profile."""
        update_data = {
            "firstName": "Updated",
            "lastName": "Name",
            "phone": "+1234567890"
        }
        
        response = test_client.put(
            "/user/profile",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["firstName"] == "Updated"
        assert data["lastName"] == "Name"
        assert data["phone"] == "+1234567890"
    
    def test_change_password(self, test_client, auth_headers, test_user):
        """Test changing user password."""
        response = test_client.post(
            "/user/change-password",
            data={
                "current_password": "TestPassword123!",
                "new_password": "NewSecurePassword456!"
            },
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "Password changed successfully" in response.json()["message"]
    
    def test_change_password_wrong_current(self, test_client, auth_headers):
        """Test changing password with wrong current password."""
        response = test_client.post(
            "/user/change-password",
            data={
                "current_password": "WrongPassword123!",
                "new_password": "NewSecurePassword456!"
            },
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Current password is incorrect" in response.json()["detail"]

class TestLogout:
    """Test user logout functionality."""
    
    def test_logout_success(self, test_client, auth_headers):
        """Test successful user logout."""
        response = test_client.post("/user/logout", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert "Logout successful" in response.json()["message"]
    
    def test_logout_unauthorized(self, test_client):
        """Test logout without authentication."""
        response = test_client.post("/user/logout")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


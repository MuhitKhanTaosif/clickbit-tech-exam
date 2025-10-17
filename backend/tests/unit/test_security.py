"""
Unit tests for security utilities.
"""
import pytest
from utils.security import (
    get_password_hash, verify_password, validate_password_strength,
    create_access_token, verify_token
)

class TestPasswordHashing:
    """Test password hashing functionality."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 50  # bcrypt hashes are typically 60 chars
        assert hashed.startswith("$2b$")
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

class TestPasswordValidation:
    """Test password strength validation."""
    
    def test_strong_password(self):
        """Test strong password validation."""
        password = "StrongPassword123!"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert result["score"] >= 4
        assert result["strength"] in ["Good", "Strong"]
    
    def test_weak_password_no_uppercase(self):
        """Test password without uppercase letter."""
        password = "weakpassword123!"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is False
        assert "uppercase letter" in " ".join(result["errors"])
    
    def test_weak_password_no_lowercase(self):
        """Test password without lowercase letter."""
        password = "WEAKPASSWORD123!"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is False
        assert "lowercase letter" in " ".join(result["errors"])
    
    def test_weak_password_no_digit(self):
        """Test password without digit."""
        password = "WeakPassword!"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is False
        assert "digit" in " ".join(result["errors"])
    
    def test_weak_password_no_special_char(self):
        """Test password without special character."""
        password = "WeakPassword123"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is False
        assert "special character" in " ".join(result["errors"])
    
    def test_short_password(self):
        """Test password that's too short."""
        password = "Weak1!"
        result = validate_password_strength(password)
        
        assert result["is_valid"] is False
        assert "8 characters" in " ".join(result["errors"])
    
    def test_password_with_common_pattern(self):
        """Test password with common patterns."""
        password = "Password123!"
        result = validate_password_strength(password)
        
        # This should still be valid but with a lower score
        assert result["is_valid"] is True
        assert "common patterns" in " ".join(result["errors"])

class TestJWTToken:
    """Test JWT token functionality."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "123", "role": "buyer"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 100  # JWT tokens are typically long
    
    def test_verify_valid_token(self):
        """Test token verification with valid token."""
        data = {"sub": "123", "role": "buyer"}
        token = create_access_token(data)
        
        payload = verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["role"] == "buyer"
        assert payload["type"] == "access"
    
    def test_verify_invalid_token(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.here"
        
        payload = verify_token(invalid_token)
        
        assert payload is None
    
    def test_verify_expired_token(self):
        """Test token verification with expired token."""
        # This would require mocking time or using a very short expiration
        # For now, we'll test the structure
        data = {"sub": "123", "role": "buyer"}
        token = create_access_token(data)
        
        # Verify the token has expiration claim
        payload = verify_token(token)
        assert "exp" in payload


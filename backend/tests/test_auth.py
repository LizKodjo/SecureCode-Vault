import pytest

from app import auth


def test_password_hashing():
    """Test that passwords are properly hashed and verified"""
    password = "testpassword123"
    hashed = auth.get_password_hash(password)

    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrongpassword", hashed)


def test_password_validation():
    """Test password validation rules"""
    # Test valid password
    valid_password = "valid123"
    assert auth.validate_password(valid_password) == valid_password

    # Test with too short password
    with pytest.raises(ValueError):
        auth.validate_password("short")

    # Test empty password
    with pytest.raises(ValueError):
        auth.validate_password("")


def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "123"}
    token = auth.create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_user(db_session, test_user):
    """Test user authentication"""
    user = auth.authenticate_user(
        db_session, test_user["email"], test_user["password"])
    assert user is not None
    assert user.email == test_user["email"]

    # Test wrong password
    user = auth.authenticate_user(
        db_session, test_user["email"], "wrongpassword")
    assert user is False

    # Test non-existent user
    user = auth.authenticate_user(
        db_session, "nonexistent@example.com", "anypassword")
    assert user is False

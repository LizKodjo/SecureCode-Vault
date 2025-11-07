# isort: skip_file
# fmt: off
import sys
sys.path.insert(0, '/app')

import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient


from app.database import Base, get_db
from app.main import app
from tests.mocks import mock_encryption_service




# Test database URL - use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    # Create the tables
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client that uses the override_get_db fixture"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_encryption():
        return mock_encryption_service

    app.dependency_overrides[get_db] = override_get_db
    # Mock the encryption service for tests
    from app import crud
    original_create_snippet = crud.create_snippet

    def mock_create_snippet(db, snippet, user_id, encryption_service=None):
        return original_create_snippet(db, snippet, user_id, mock_encryption_service)

    crud.create_snippet = mock_create_snippet

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    crud.create_snippet = original_create_snippet


@pytest.fixture
def test_user(client):
    """Create a test user and return auth tokens"""
    user_data = {
        "email": "test@example.com",
        "password": "testpass123"
    }

    # Register user
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Login to get token
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    tokens = response.json()

    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "access_token": tokens["access_token"],
        "headers": {"Authorization": f"Bearer {tokens['access_token']}"}
    }

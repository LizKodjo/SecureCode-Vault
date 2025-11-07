

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "encryption" in data


def test_register_user(client):
    """Test user registration"""
    user_data = {"email": "newuser@example.com", "password": "newpass123"}

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data


def test_register_duplicate_user(client, test_user):
    """Test duplicate user registration"""
    user_data = {"email": test_user["email"], "password": "anypassword"}

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_user(client, test_user):
    """Test user login"""
    login_data = {"email": test_user["email"], "password": test_user["password"]}

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    login_data = {"email": "nonexistent@example.com", "password": "wrongpass"}

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401


def test_protected_endpoint_without_auth(client):
    """Test accessing protected endpoint without authentication"""
    response = client.get("/users/me")
    assert response.status_code == 403


def test_protected_endpoint_wth_auth(client, test_user):
    """Test accessing protected endpoint with valid authentication"""
    response = client.get("/users/me", headers=test_user["headers"])
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]

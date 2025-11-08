# SecureCode Vault API Examples

## Authentication

### Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

## Snippets

### Create a Snippet

```bash
curl -X POST "http://localhost:8000/snippets" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "My Python Function",
    "language": "python",
    "code": "def hello():\n    print(\\"Hello, World!\\")"
  }'
```

### Get User Snippets

```bash
curl -X GET "http://localhost:8000/snippets" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Sharing

### Create Share Link

```bash
curl -X POST "http://localhost:8000/snippets/1/share" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "expires_hours": 24,
    "password": "optional_password"
  }'
```

### Access Shared Snippet

```bash
curl -X GET "http://localhost:8000/shared/SHARE_TOKEN"
```

## Python Client Example

```python
import requests

API_BASE = "http://localhost:8000"

# Login
response = requests.post(f"{API_BASE}/auth/login", json={
    "email": "user@example.com",
    "password": "securepassword123"
})
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# Create snippet
response = requests.post(f"{API_BASE}/snippets", json={
    "title": "API Example",
    "language": "python",
    "code": "print('Hello from API!')"
}, headers=headers)

print(response.json())
```

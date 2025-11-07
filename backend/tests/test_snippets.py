def test_create_snippet(client, test_user):
    """Test creating a new snippet"""
    snippet_data = {
        "title": "Test Snippet",
        "language": "python",
        "code": "print('Hello, World!')",
    }

    response = client.post("/snippets", json=snippet_data, headers=test_user["headers"])
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == snippet_data["title"]
    assert data["language"] == snippet_data["language"]
    assert data["code"] == snippet_data["code"]
    assert "id" in data
    assert "user_id" in data


def test_get_snippets(client, test_user):
    """Test retrieving user's snippets"""
    # Create a snippet first
    snippet_data = {
        "title": "Test Snippet",
        "language": "python",
        "code": "print('Hello, World!')",
    }

    client.post("/snippets", json=snippet_data, headers=test_user["headers"])

    # Get snippets
    response = client.get("/snippets", headers=test_user["headers"])
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == snippet_data["title"]


def test_get_specific_snippet(client, test_user):
    """Test retrieving a specific snippet"""
    # Create a snippet
    snippet_data = {
        "title": "Specific Snippet",
        "language": "python",
        "code": "def test(): pass",
    }

    create_response = client.post(
        "/snippets", json=snippet_data, headers=test_user["headers"]
    )
    snippet_id = create_response.json()["id"]

    # Get the specific snippet
    response = client.get(f"/snippets/{snippet_id}", headers=test_user["headers"])
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == snippet_id
    assert data["title"] == snippet_data["title"]


def test_delete_snippet(client, test_user):
    """Test deleting a snippet"""
    # Create a snippet
    snippet_data = {
        "title": "To Delete",
        "language": "python",
        "code": "print('delete me')",
    }

    create_response = client.post(
        "/snippets", json=snippet_data, headers=test_user["headers"]
    )
    snippet_id = create_response.json()["id"]

    # Delete the snippet
    response = client.delete(f"/snippets/{snippet_id}", headers=test_user["headers"])
    assert response.status_code == 200
    assert response.json()["message"] == "Snippet deleted successfully"

    # Verify it's gone
    response = client.get(f"/snippets/{snippet_id}", headers=test_user["headers"])
    assert response.status_code == 404


def test_create_share_link(client, test_user):
    """Test creating a share link for a snippet"""
    # Create a snippet first
    snippet_data = {
        "title": "Share Test",
        "language": "python",
        "code": "print('shared code')",
    }

    create_response = client.post(
        "/snippets", json=snippet_data, headers=test_user["headers"]
    )
    snippet_id = create_response.json()["id"]

    # Create share link
    share_data = {"expires_hours": 24}

    response = client.post(
        f"/snippets/{snippet_id}/share", json=share_data, headers=test_user["headers"]
    )

    # Debug
    if response.status_code != 200:
        print(f"Share link creation failed: {response.status_code}")
        print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "expires_at" in data
    assert data["is_active"]


def test_access_shared_snippet(client, test_user):
    """Test accessing a shared snippet"""
    # Create a snippet and share it
    snippet_data = {
        "title": "Shared Snippet",
        "language": "python",
        "code": "print('shared content')",
    }

    create_response = client.post(
        "/snippets", json=snippet_data, headers=test_user["headers"]
    )
    snippet_id = create_response.json()["id"]

    share_response = client.post(
        f"/snippets/{snippet_id}/share",
        json={"expires_hours": 24},
        headers=test_user["headers"],
    )
    share_token = share_response.json()["token"]

    # Access the shared snippet
    response = client.get(f"/shared/{share_token}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == snippet_data["title"]
    assert data["code"] == snippet_data["code"]
    assert "shared_at" in data

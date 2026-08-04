import os
import sys

from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT_DIR)

from index import app

client = TestClient(app)


def test_register_login_and_todo_lifecycle():
    """
    Register a user, log in, create a todo, and verify retrieval.
    """
    register_payload = {
        "email": "user@example.com",
        "name": "Demo User",
        "password": "supersecret",
    }
    response = client.post("/users/register", json=register_payload)
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}

    login_payload = {"email": "user@example.com", "password": "supersecret"}
    response = client.post("/users/login", json=login_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert token_data["token_type"] == "bearer"
    assert "access_token" in token_data

    auth_headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    todo_payload = {"title": "Buy milk", "description": "Remember to buy milk"}
    response = client.post("/todos", json=todo_payload, headers=auth_headers)
    assert response.status_code == 201
    todo = response.json()
    assert todo["title"] == "Buy milk"
    assert todo["completed"] is False

    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 1
    assert todos[0]["title"] == "Buy milk"


def test_todo_endpoint_requires_authentication():
    """
    Ensure todo routes reject requests without authentication.
    """
    response = client.get("/todos")
    assert response.status_code == 401

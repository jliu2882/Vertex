import os
import sys

import asyncpg
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(ROOT_DIR)

os.environ.setdefault("JWT_SECRET_KEY", "default-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_TOKEN_EXPIRE_MINUTES", "60")

from src.index import app
from src.routes.tasks import get_db as task_get_db
from src.routes.tasks import get_current_user_id as task_get_current_user_id
from src.routes.users import get_db as user_get_db
from src.services.users import create_jwt_token, hash_password

class FakeDB:
    def __init__(self):
        self.users = []
        self.tasks = []
        self._user_id = 1
        self._task_id = 1

    def seed_user(self, email: str, username: str, password: str) -> None:
        self.users.append(
            {
                "id": self._user_id,
                "email": email,
                "username": username,
                "password_hash": hash_password(password),
            }
        )
        self._user_id += 1

    async def execute(self, query, *args):
        query_text = query.strip()
        if query_text.startswith("INSERT INTO users"):
            email, username, password_hash = args
            if any(existing["email"] == email or existing["username"] == username for existing in self.users):
                raise asyncpg.exceptions.UniqueViolationError
            self.users.append(
                {
                    "id": self._user_id,
                    "email": email,
                    "username": username,
                    "password_hash": password_hash,
                }
            )
            self._user_id += 1
            return None

        if query_text.startswith("INSERT INTO tasks"):
            user_id, title, task_description = args
            created_task = {
                "id": self._task_id,
                "user_id": user_id,
                "title": title,
                "task_description": task_description,
            }
            self.tasks.append(created_task)
            self._task_id += 1
            return created_task

        if query_text.startswith("UPDATE tasks"):
            task_id, title, task_description = args
            for task in self.tasks:
                if task["id"] == task_id:
                    if title is not None:
                        task["title"] = title
                    if task_description is not None:
                        task["task_description"] = task_description
                    break
            return None

        if query_text.startswith("DELETE FROM tasks"):
            task_id = args[0]
            self.tasks = [task for task in self.tasks if task["id"] != task_id]
            return None

        return None

    async def fetchrow(self, query, *args):
        query_text = query.strip()
        if query_text.startswith("SELECT username, password_hash FROM users"):
            email = args[0]
            for user in self.users:
                if user["email"] == email:
                    return {"username": user["username"], "password_hash": user["password_hash"]}
            return None

        if query_text.startswith("SELECT id FROM users"):
            username = args[0]
            for user in self.users:
                if user["username"] == username:
                    return {"id": user["id"]}
            return None

        if query_text.startswith("SELECT * FROM tasks WHERE id = $1"):
            task_id = args[0]
            for task in self.tasks:
                if task["id"] == task_id:
                    return task
            return None

        if query_text.startswith("INSERT INTO tasks"):
            user_id, title, task_description = args
            created_task = {
                "id": self._task_id,
                "user_id": user_id,
                "title": title,
                "task_description": task_description,
            }
            self.tasks.append(created_task)
            self._task_id += 1
            return created_task

        return None

    async def fetch(self, query, *args):
        query_text = query.strip()
        if query_text.startswith("SELECT * FROM tasks WHERE user_id = $1"):
            user_id = args[0]
            return [task for task in self.tasks if task["user_id"] == user_id]
        return []

    async def fetchval(self, query, *args):
        query_text = query.strip()
        if query_text.startswith("SELECT COUNT(*) FROM tasks WHERE user_id = $1"):
            user_id = args[0]
            if len(args) > 1:
                search_term = str(args[1]).lower()
                return sum(
                    1
                    for task in self.tasks
                    if task["user_id"] == user_id
                    and (
                        search_term in task["title"].lower()
                        or search_term in task["task_description"].lower()
                    )
                )
            return sum(1 for task in self.tasks if task["user_id"] == user_id)
        return 0


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def override_get_db(fake_db):
    async def _override():
        yield fake_db

    return _override


def override_current_user_id(user_id: int):
    async def _override():
        return user_id

    return _override


def test_register_endpoint_returns_token(client):
    fake_db = FakeDB()
    app.dependency_overrides[user_get_db] = override_get_db(fake_db)

    response = client.post(
        "/register",
        json={"email": "new@example.com", "username": "newuser", "password": "secret123"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


def test_login_endpoint_returns_token_for_existing_user(client):
    fake_db = FakeDB()
    fake_db.seed_user("user@example.com", "demo", "secret123")
    app.dependency_overrides[user_get_db] = override_get_db(fake_db)

    response = client.post(
        "/login",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


def test_task_crud_endpoints_work(client):
    fake_db = FakeDB()
    app.dependency_overrides[user_get_db] = override_get_db(fake_db)
    app.dependency_overrides[task_get_db] = override_get_db(fake_db)
    app.dependency_overrides[task_get_current_user_id] = override_current_user_id(1)

    create_response = client.post(
        "/tasks",
        json={"title": "Buy milk", "task_description": "Remember the milk"},
    )
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Buy milk"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    payload = list_response.json()
    tasks = payload["items"]
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Buy milk"

    update_response = client.put(
        f"/tasks/{created_task['id']}",
        json={"title": "Buy bread", "task_description": "Fresh bread"},
    )
    assert update_response.status_code == 200

    updated_list = client.get("/tasks").json()
    assert updated_list["items"][0]["title"] == "Buy bread"
    assert updated_list["items"][0]["task_description"] == "Fresh bread"

    delete_response = client.delete(f"/tasks/{created_task['id']}")
    assert delete_response.status_code == 204

    final_list = client.get("/tasks").json()
    assert final_list["items"] == []
    assert final_list["total"] == 0


def test_tasks_endpoint_rejects_invalid_token(client):
    fake_db = FakeDB()
    app.dependency_overrides[task_get_db] = override_get_db(fake_db)

    response = client.get(
        "/tasks",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_tasks_endpoint_rejects_unknown_user_token(client):
    fake_db = FakeDB()
    app.dependency_overrides[task_get_db] = override_get_db(fake_db)

    token = create_jwt_token("missinguser")
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

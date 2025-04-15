import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


@pytest.fixture(scope="module")
def created_task(client: TestClient) -> Dict[str, Any]:
    response = client.post("/task/", json={"title": "Do homework", "is_done": False})
    assert response.status_code == 200
    return response.json()


def test_create_task(created_task: Dict[str, Any]) -> None:
    assert created_task["title"] == "Do homework"
    assert created_task["is_done"] is False
    assert "id" in created_task


def test_get_all_tasks(client: TestClient) -> None:
    response = client.get("/task/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert any(task["title"] == "Do homework" for task in tasks)


def test_get_task_by_id(client: TestClient, created_task: Dict[str, Any]) -> None:
    task_id: int = created_task["id"]
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Do homework"


def test_update_task(client: TestClient, created_task: Dict[str, Any]) -> None:
    task_id: int = created_task["id"]
    response = client.put(
        f"/task/{task_id}",
        json={"title": "Do homework updated", "is_done": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Do homework updated"
    assert data["is_done"] is True


def test_delete_task(client: TestClient, created_task: Dict[str, Any]) -> None:
    task_id: int = created_task["id"]
    response = client.delete(f"/task/{task_id}")
    assert response.status_code == 200
    deleted = response.json()
    assert deleted["id"] == task_id

    # Confirm it's deleted
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 404

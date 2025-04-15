def test_create_task(client):
    response = client.post("/task/", json={"title": "Do homework", "is_done": False})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Do homework"
    assert data["is_done"] is False
    assert "id" in data
    # Save ID for future tests
    client.task_id = data["id"]


def test_get_all_tasks(client):
    response = client.get("/task/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert any(task["title"] == "Do homework" for task in tasks)


def test_get_task_by_id(client):
    task_id = client.task_id
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Do homework"


def test_update_task(client):
    task_id = client.task_id
    response = client.put(
        f"/task/{task_id}",
        json={"title": "Do homework updated", "is_done": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Do homework updated"
    assert data["is_done"] is True


def test_delete_task(client):
    task_id = client.task_id
    response = client.delete(f"/task/{task_id}")
    assert response.status_code == 200
    deleted = response.json()
    assert deleted["id"] == task_id

    # Confirm it's deleted
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 404

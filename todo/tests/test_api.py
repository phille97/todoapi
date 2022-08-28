from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..api import app, get_db


def override_app_db(test_db: Session):
    def get_test_db():
        yield test_db
    app.dependency_overrides[get_db] = get_test_db


client = TestClient(app)


def test_assignment_requirements(test_db: Session):
    override_app_db(test_db)

    # - Create a to do containing a text of what to do.
    resp = client.post("/items", json={"description": "be serious", "is_done": True})
    assert resp.status_code == 201
    assert resp.json() == {"id": 1, "description": "be serious", "is_done": True}

    resp = client.post("/items", json={"description": "horse around"})
    assert resp.status_code == 201
    assert resp.json() == {"id": 2, "description": "horse around", "is_done": False}

    # - Mark a to do as "done" or "not done".
    resp = client.put("/items/2", json={"is_done": True})
    assert resp.status_code == 200
    assert resp.json() == {"id": 2, "description": "horse around", "is_done": True}
    resp = client.put("/items/1", json={"is_done": False})
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "description": "be serious", "is_done": False}

    # - List all to dos.
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == [
        {"id": 1, "description": "be serious", "is_done": False},
        {"id": 2, "description": "horse around", "is_done": True}]

    # - Filter to dos on "done", "not done" and/or contains text.
    resp = client.get("/items?is_done=yes")
    assert resp.status_code == 200
    assert resp.json() == [{"id": 2, "description": "horse around", "is_done": True}]

    resp = client.get("/items?is_done=no")
    assert resp.status_code == 200
    assert resp.json() == [{"id": 1, "description": "be serious", "is_done": False}]

    resp = client.get("/items?has_description=yes")
    assert resp.status_code == 200
    assert resp.json() == [
        {"id": 1, "description": "be serious", "is_done": False},
        {"id": 2, "description": "horse around", "is_done": True}]

    resp = client.get("/items?has_description=no")
    assert resp.status_code == 200
    assert resp.json() == []

    # - Delete a to do.
    assert client.delete("/items/1").status_code == 200

    assert client.get("/items/1").status_code == 404
    assert client.get("/items/2").status_code == 200


def test_update_item(test_db: Session):
    override_app_db(test_db)

    resp = client.post("/items", json={"description": "buy house", "is_done": False})
    assert resp.status_code == 201
    assert resp.json() == {"id": 1, "description": "buy house", "is_done": False}

    resp = client.put("/items/1", json={"description": "buy horse"})
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "description": "buy horse", "is_done": False}

    resp = client.get("/items/1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "description": "buy horse", "is_done": False}


def test_delete_item(test_db: Session):
    override_app_db(test_db)

    resp = client.post("/items", json={"description": "be serious", "is_done": False})
    assert resp.status_code == 201
    assert resp.json() == {"id": 1, "description": "be serious", "is_done": False}

    assert client.get("/items/1").status_code == 200
    assert client.delete("/items/1").status_code == 200
    assert client.get("/items/1").status_code == 404


def test_read_non_existing_item(test_db: Session):
    override_app_db(test_db)
    assert client.get("/items/9001").status_code == 404


def test_update_non_existing_item(test_db: Session):
    override_app_db(test_db)
    assert client.put("/items/9001", json={"is_done": True}).status_code == 404


def test_delete_non_existing_item(test_db: Session):
    override_app_db(test_db)
    assert client.delete("/items/9001").status_code == 404

from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def token_for(username, password):
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_member_can_create_ticket_and_viewer_cannot():
    member = token_for("member", "member123")
    viewer = token_for("viewer", "viewer123")
    created = client.post("/tickets", json={"title": "Fix login"}, headers={"Authorization": f"Bearer {member}"})
    assert created.status_code == 201
    denied = client.post("/tickets", json={"title": "No access"}, headers={"Authorization": f"Bearer {viewer}"})
    assert denied.status_code == 403

def test_admin_can_delete():
    member = token_for("member", "member123")
    admin = token_for("admin", "admin123")
    created = client.post("/tickets", json={"title": "Delete me"}, headers={"Authorization": f"Bearer {member}"})
    ticket_id = created.json()["id"]
    deleted = client.delete(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {admin}"})
    assert deleted.status_code == 204

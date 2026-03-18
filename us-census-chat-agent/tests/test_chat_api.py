from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_chat():
    res = client.post("/api/chat", json={"message": "hello"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
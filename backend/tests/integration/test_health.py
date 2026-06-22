def test_health_returns_200(client):
    response = client.get("/api/health")
    assert response.status_code == 200

def test_health_returns_correct_body(client):
    response = client.get("/api/health")
    data = response.get_json()
    assert data["status"] == "ok"
    assert "message" in data

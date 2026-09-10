from fastapi import status
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """測試根目錄歡迎端點 (GET /)。"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "docs_url" in data
    assert data["docs_url"] == "/docs"


def test_health_check_endpoint(client: TestClient) -> None:
    """測試健康檢查端點 (GET /health) 與資料庫連線狀態。"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert "service" in data

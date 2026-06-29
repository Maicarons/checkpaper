"""
API 测试
"""
import pytest
from fastapi.testclient import TestClient


def test_root(client: TestClient):
    """测试根路由"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client: TestClient):
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_app_info(client: TestClient):
    """测试应用信息"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_api_health(client: TestClient):
    """测试API健康检查"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_validation_types(client: TestClient):
    """测试获取验证类型"""
    response = client.get("/api/v1/validation/types")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

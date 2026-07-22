import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# 测试1：访问 /health 返回200，ok=True
def test_health_api(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["ok"] is True

# 测试2：未登录访问 /api/metrics 被拦截（跳转302）
def test_metrics_no_login(client):
    resp = client.get("/api/metrics")
    assert resp.status_code == 302

# 测试3：登录后访问 /api/metrics 正常拿到指标数据
def test_metrics_with_login(client):
    # 模拟表单登录
    client.post("/login", data={"username": "student", "password": "day07"})
    resp = client.get("/api/metrics")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["ok"] is True
    assert "metrics" in data
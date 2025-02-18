import pytest
from main_api import app  # 确保你的 Flask 应用文件名是 main_api.py

@pytest.fixture
def client():
    """创建 Flask 测试客户端"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

##############################
#   House 相关测试
##############################

def test_add_house_success(client):
    """测试正常添加房屋"""
    payload = {
        "name": "Dream House",
        "lat": 40.7128,
        "lon": -74.0060,
        "addr": "123 Main St, NY",
        "uid": "house123",
        "floors": 2,
        "size": 120
    }
    response = client.post("/house/add", json=payload)
    assert response.status_code == 200
    assert response.json == {"message": "House added successfully"}

def test_add_house_missing_param(client):
    """测试缺少参数时的错误返回"""
    payload = {
        "name": "Dream House",
        "lat": 40.7128,
        "lon": -74.0060,
        "addr": "123 Main St, NY",
        "uid": "house123",
        "floors": 2
        # 缺少 "size"
    }
    response = client.post("/house/add", json=payload)
    assert response.status_code == 400
    assert "Missing required parameter: size" in response.json["error"]

def test_add_house_invalid_data_type(client):
    """测试参数类型错误"""
    payload = {
        "name": "Dream House",
        "lat": "invalid_lat",  # 错误的类型
        "lon": -74.0060,
        "addr": "123 Main St, NY",
        "uid": "house123",
        "floors": "two",  # 错误的类型
        "size": 120
    }
    response = client.post("/house/add", json=payload)
    assert response.status_code == 400  # 预期 API 有参数校验
    assert "error" in response.json

def test_add_house_empty_request(client):
    """测试空 JSON 请求"""
    response = client.post("/house/add", json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_add_house_no_json(client):
    """测试未提供 JSON 时的错误返回"""
    response = client.post("/house/add")
    assert response.status_code == 400
    assert response.json == {"error": "No JSON provided"}

def test_remove_house(client):
    """测试正常删除房屋"""
    payload = {"uid": "house123"}
    response = client.post("/house/remove", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "House with uid=house123 removed"

def test_remove_house_missing_uid(client):
    """测试删除房屋时缺少 UID"""
    response = client.post("/house/remove", json={})
    assert response.status_code == 400
    assert "uid is required" in response.json["error"]

def test_update_house(client):
    """测试正常更新房屋"""
    payload = {"uid": "house123", "name": "Updated House"}
    response = client.post("/house/update", json=payload)
    assert response.status_code == 200
    assert "House with uid=house123 updated" in response.json["message"]

def test_update_house_missing_uid(client):
    """测试更新房屋时缺少 UID"""
    response = client.post("/house/update", json={"name": "New Name"})
    assert response.status_code == 400
    assert "uid is required" in response.json["error"]

##############################
#   Room 相关测试
##############################

def test_add_room_success(client):
    """测试正常添加房间"""
    payload = {
        "name": "Master Bedroom",
        "belong_to_house": "house123",
        "size": 30,
        "floor": 1
    }
    response = client.post("/room/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Room added successfully"

def test_add_room_missing_fields(client):
    """测试缺少必需字段"""
    payload = {"name": "Master Bedroom"}
    response = client.post("/room/add", json=payload)
    assert response.status_code == 400
    assert "belong_to_house" in response.json["error"]

##############################
#   Device 相关测试
##############################

def test_add_device(client):
    """测试正常添加设备"""
    payload = {
        "name": "Smart Light",
        "belong_to_room": "Master Bedroom",
        "type": "Lighting"
    }
    response = client.post("/device/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Device added successfully"

def test_add_device_missing_fields(client):
    """测试缺少必需字段"""
    payload = {"name": "Smart Light"}
    response = client.post("/device/add", json=payload)
    assert response.status_code == 400
    assert "belong_to_room" in response.json["error"]

##############################
#   Users 相关测试
##############################

def test_add_user(client):
    """测试正常添加用户"""
    payload = {"user_id": "user001", "name": "Alice"}
    response = client.post("/users/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "User added successfully"

def test_add_user_missing_fields(client):
    """测试缺少必需字段"""
    payload = {"name": "Alice"}
    response = client.post("/users/add", json=payload)
    assert response.status_code == 400
    assert "user_id" in response.json["error"]

##############################
#   House-User 关系测试
##############################

def test_add_house_user_relationship(client):
    """测试正常添加房屋-用户关系"""
    payload = {"user_id": "user001", "house_uid": "house123"}
    response = client.post("/house-user/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Relationship between user and house added"

def test_add_house_user_relationship_missing_fields(client):
    """测试缺少房屋-用户关系的字段"""
    payload = {"user_id": "user001"}
    response = client.post("/house-user/add", json=payload)
    assert response.status_code == 400
    # assert "house_uid is required" in response.json["error"]

##############################
#   HTTP 方法错误测试
##############################

def test_invalid_http_method(client):
    """测试错误的 HTTP 方法"""
    response = client.get("/house/add")  # 应该是 POST，但我们用 GET
    assert response.status_code == 405  # Method Not Allowed

    response = client.delete("/house/update")  # 这个路由不支持 DELETE
    assert response.status_code == 405

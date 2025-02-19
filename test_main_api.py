import pytest
from main_api import app 

@pytest.fixture
def client():
    """Create Flask test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

##############################
#   House-related tests
##############################

def test_add_house_success(client):
    """Test successful house addition"""
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
    """Test error response when a required parameter is missing"""
    payload = {
        "name": "Dream House",
        "lat": 40.7128,
        "lon": -74.0060,
        "addr": "123 Main St, NY",
        "uid": "house123",
        "floors": 2
        # Missing "size"
    }
    response = client.post("/house/add", json=payload)
    assert response.status_code == 400
    assert "Missing required parameter: size" in response.json["error"]

def test_add_house_invalid_data_type(client):
    """Test incorrect parameter types"""
    payload = {
        "name": "Dream House",
        "lat": "invalid_lat",  # Incorrect type
        "lon": -74.0060,
        "addr": "123 Main St, NY",
        "uid": "house123",
        "floors": "two",  # Incorrect type
        "size": 120
    }
    response = client.post("/house/add", json=payload)
    assert response.status_code == 400  # Expect API to validate parameters
    assert "error" in response.json

def test_add_house_empty_request(client):
    """Test empty JSON request"""
    response = client.post("/house/add", json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_add_house_no_json(client):
    """Test error response when no JSON is provided"""
    response = client.post("/house/add")
    assert response.status_code == 400
    assert response.json == {"error": "No JSON provided"}

def test_remove_house(client):
    """Test successful house removal"""
    payload = {"uid": "house123"}
    response = client.post("/house/remove", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "House with uid=house123 removed"

def test_remove_house_missing_uid(client):
    """Test error when removing a house without a UID"""
    response = client.post("/house/remove", json={})
    assert response.status_code == 400
    assert "uid is required" in response.json["error"]

def test_update_house(client):
    """Test successful house update"""
    payload = {"uid": "house123", "name": "Updated House"}
    response = client.post("/house/update", json=payload)
    assert response.status_code == 200
    assert "House with uid=house123 updated" in response.json["message"]

def test_update_house_missing_uid(client):
    """Test error when updating a house without a UID"""
    response = client.post("/house/update", json={"name": "New Name"})
    assert response.status_code == 400
    assert "uid is required" in response.json["error"]

##############################
#   Room-related tests
##############################

def test_add_room_success(client):
    """Test successful room addition"""
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
    """Test missing required fields"""
    payload = {"name": "Master Bedroom"}
    response = client.post("/room/add", json=payload)
    assert response.status_code == 400
    assert "belong_to_house" in response.json["error"]

##############################
#   Device-related tests
##############################

def test_add_device(client):
    """Test successful device addition"""
    payload = {
        "name": "Smart Light",
        "belong_to_room": "Master Bedroom",
        "type": "Lighting"
    }
    response = client.post("/device/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Device added successfully"

def test_add_device_missing_fields(client):
    """Test missing required fields"""
    payload = {"name": "Smart Light"}
    response = client.post("/device/add", json=payload)
    assert response.status_code == 400
    assert "belong_to_room" in response.json["error"]

##############################
#   User-related tests
##############################

def test_add_user(client):
    """Test successful user addition"""
    payload = {"user_id": "user001", "name": "Alice"}
    response = client.post("/users/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "User added successfully"

def test_add_user_missing_fields(client):
    """Test missing required fields"""
    payload = {"name": "Alice"}
    response = client.post("/users/add", json=payload)
    assert response.status_code == 400
    assert "user_id" in response.json["error"]

##############################
#   House-User relationship tests
##############################

def test_add_house_user_relationship(client):
    """Test successful addition of house-user relationship"""
    payload = {"user_id": "user001", "house_uid": "house123"}
    response = client.post("/house-user/add", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Relationship between user and house added"

def test_add_house_user_relationship_missing_fields(client):
    """Test missing fields in house-user relationship"""
    payload = {"user_id": "user001"}
    response = client.post("/house-user/add", json=payload)
    assert response.status_code == 400
    # assert "house_uid is required" in response.json["error"]

##############################
#   HTTP method error tests
##############################

def test_invalid_http_method(client):
    """Test incorrect HTTP method usage"""
    response = client.get("/house/add")  # Should be POST, but using GET
    assert response.status_code == 405  # Method Not Allowed

    response = client.delete("/house/update")  # This route does not support DELETE
    assert response.status_code == 405

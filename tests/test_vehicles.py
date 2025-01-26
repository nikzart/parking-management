import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_create_vehicle(client, api_key_headers, test_vehicle_data):
    """Test vehicle registration endpoint."""
    response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["number_plate"] == test_vehicle_data["number_plate"]
    assert data["contact_name"] == test_vehicle_data["contact_name"]
    assert data["phone_number"] == test_vehicle_data["phone_number"]
    assert "id" in data
    assert "entry_timestamp" in data

def test_create_duplicate_vehicle(client, api_key_headers, test_vehicle_data):
    """Test duplicate vehicle registration is prevented."""
    # Create first vehicle
    response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Try to create duplicate
    response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT

def test_get_vehicle(client, api_key_headers, test_vehicle_data):
    """Test retrieving vehicle details."""
    # Create vehicle
    create_response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    # Get vehicle
    response = client.get(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["number_plate"] == test_vehicle_data["number_plate"]

def test_get_nonexistent_vehicle(client, api_key_headers):
    """Test retrieving non-existent vehicle."""
    response = client.get(
        "/api/v1/vehicles/NOTFOUND",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_vehicles(client, api_key_headers, test_vehicle_data):
    """Test listing vehicles with pagination."""
    # Create test vehicle
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )

    # List vehicles
    response = client.get(
        "/api/v1/vehicles",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "pagination" in data
    assert len(data["items"]) > 0
    assert data["pagination"]["total_items"] > 0

def test_remove_vehicle(client, api_key_headers, test_vehicle_data):
    """Test vehicle removal."""
    # Create vehicle
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )

    # Remove vehicle
    response = client.delete(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify removal
    response = client.get(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_vehicles(client, api_key_headers):
    """Test vehicle search functionality."""
    # Create test vehicles
    vehicles = [
        {
            "number_plate": "ABC123",
            "contact_name": "John Doe",
            "phone_number": "+1234567890"
        },
        {
            "number_plate": "XYZ789",
            "contact_name": "Jane Doe",
            "phone_number": "+9876543210"
        }
    ]
    
    for vehicle in vehicles:
        client.post(
            "/api/v1/vehicles",
            json=vehicle,
            headers=api_key_headers
        )

    # Search by number plate
    response = client.get(
        "/api/v1/vehicles/search/ABC",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["number_plate"] == "ABC123"

    # Search by contact name
    response = client.get(
        "/api/v1/vehicles/search/Jane",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["number_plate"] == "XYZ789"

def test_unauthorized_access(client, test_vehicle_data):
    """Test unauthorized access is prevented."""
    response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_rate_limiting(client, api_key_headers, test_vehicle_data):
    """Test rate limiting functionality."""
    # Make multiple requests quickly
    for _ in range(105):  # Exceeds rate limit of 100 per minute
        response = client.get(
            "/api/v1/vehicles",
            headers=api_key_headers
        )
    
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
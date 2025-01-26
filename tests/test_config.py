from fastapi import status
from datetime import datetime


def test_get_retention_period(client, api_key_headers):
    """Test getting retention period."""
    response = client.get(
        "/api/v1/config/retention",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "retention_hours" in data
    assert data["retention_hours"] == 24  # Default value


def test_update_retention_period(client, api_key_headers, test_config_data):
    """Test updating retention period."""
    response = client.put(
        "/api/v1/config/retention",
        json=test_config_data,
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["retention_hours"] == test_config_data["retention_hours"]


def test_invalid_retention_period(client, api_key_headers):
    """Test validation of retention period."""
    # Test negative value
    response = client.put(
        "/api/v1/config/retention",
        json={"retention_hours": -1},
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test zero value
    response = client.put(
        "/api/v1/config/retention",
        json={"retention_hours": 0},
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test too large value
    response = client.put(
        "/api/v1/config/retention",
        json={"retention_hours": 169},  # > 168 (1 week)
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_clear_database(client, api_key_headers, test_vehicle_data):
    """Test database clearing functionality."""
    # Create test vehicle
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )

    # Clear database with invalid confirmation
    response = client.post(
        "/api/v1/config/maintenance/clear",
        json={"confirmation": "wrong confirmation"},
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Clear database with valid confirmation
    response = client.post(
        "/api/v1/config/maintenance/clear",
        json={"confirmation": "I understand this will delete all data"},
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Database cleared successfully"
    assert isinstance(data["timestamp"], str)
    assert isinstance(data["records_removed"], int)
    assert data["records_removed"] >= 0


def test_unauthorized_config_access(client, test_config_data):
    """Test unauthorized access to configuration endpoints."""
    # Try to get retention period without API key
    response = client.get("/api/v1/config/retention")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to update retention period without API key
    response = client.put(
        "/api/v1/config/retention",
        json=test_config_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to clear database without API key
    response = client.post(
        "/api/v1/config/maintenance/clear",
        json={"confirmation": "I understand this will delete all data"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
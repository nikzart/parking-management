import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_get_audit_logs(client, api_key_headers, test_vehicle_data):
    """Test retrieving audit logs."""
    # Create a vehicle to generate audit logs
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )

    # Get audit logs
    response = client.get(
        "/api/v1/audit",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "pagination" in data
    assert len(data["items"]) > 0
    
    # Verify audit log content
    log = data["items"][0]
    assert log["action"] == "CREATE"
    assert log["entity"] == "Vehicle"
    assert "timestamp" in log

def test_get_audit_logs_with_filters(client, api_key_headers, test_vehicle_data):
    """Test audit log filtering."""
    # Create and then delete a vehicle to generate different types of logs
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    client.delete(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )

    # Filter by entity
    response = client.get(
        "/api/v1/audit/entity/Vehicle",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2  # CREATE and DELETE logs
    
    # Verify all logs are for Vehicle entity
    for log in data["items"]:
        assert log["entity"] == "Vehicle"

def test_get_recent_audit_logs(client, api_key_headers, test_vehicle_data):
    """Test retrieving recent audit logs."""
    # Generate multiple audit logs
    for i in range(3):
        test_vehicle_data["number_plate"] = f"TEST{i}"
        client.post(
            "/api/v1/vehicles",
            json=test_vehicle_data,
            headers=api_key_headers
        )

    # Get recent logs with limit
    response = client.get(
        "/api/v1/audit/recent?limit=2",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Limited to 2 most recent logs

def test_audit_log_pagination(client, api_key_headers, test_vehicle_data):
    """Test audit log pagination."""
    # Generate multiple audit logs
    for i in range(5):
        test_vehicle_data["number_plate"] = f"TEST{i}"
        client.post(
            "/api/v1/vehicles",
            json=test_vehicle_data,
            headers=api_key_headers
        )

    # Test first page
    response = client.get(
        "/api/v1/audit?page=1&per_page=2",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2
    assert data["pagination"]["current_page"] == 1
    assert data["pagination"]["total_items"] >= 5

    # Test second page
    response = client.get(
        "/api/v1/audit?page=2&per_page=2",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 2
    assert data["pagination"]["current_page"] == 2

def test_audit_log_date_filtering(client, api_key_headers, test_vehicle_data):
    """Test audit log filtering by date."""
    # Create a vehicle
    client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )

    # Get logs with date range
    now = datetime.utcnow()
    start_date = (now - timedelta(hours=1)).isoformat()
    end_date = (now + timedelta(hours=1)).isoformat()
    
    response = client.get(
        f"/api/v1/audit?start_date={start_date}&end_date={end_date}",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) > 0

def test_unauthorized_audit_access(client):
    """Test unauthorized access to audit logs."""
    response = client.get("/api/v1/audit")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get("/api/v1/audit/recent")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get("/api/v1/audit/entity/Vehicle")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
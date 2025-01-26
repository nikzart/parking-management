import pytest
from fastapi.testclient import TestClient
import json
from app.core.config import settings


def test_websocket_connection(client, api_key_headers, test_vehicle_data):
    """Test WebSocket connection and search functionality."""
    # Create test vehicles first
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

    # Test WebSocket connection with proper cleanup
    try:
        with client.websocket_connect(
            f"/ws/vehicles/search?api_key={settings.SECRET_KEY}"
        ) as websocket:
            # Test search by number plate
            websocket.send_json({
                "type": "search",
                "search_term": "ABC"
            })
            
            data = websocket.receive_json()
            assert data["type"] == "search_results"
            assert len(data["results"]) == 1
            assert data["results"][0]["number_plate"] == "ABC123"

            # Test search by contact name
            websocket.send_json({
                "type": "search",
                "search_term": "Jane"
            })
            
            data = websocket.receive_json()
            assert data["type"] == "search_results"
            assert len(data["results"]) == 1
            assert data["results"][0]["number_plate"] == "XYZ789"
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {str(e)}")


def test_websocket_invalid_api_key(client):
    """Test WebSocket connection with invalid API key."""
    with pytest.raises(Exception):
        with client.websocket_connect(
            "/ws/vehicles/search?api_key=invalid_key"
        ) as websocket:
            pass


def test_websocket_invalid_search_term(client):
    """Test WebSocket search with invalid search term."""
    try:
        with client.websocket_connect(
            f"/ws/vehicles/search?api_key={settings.SECRET_KEY}"
        ) as websocket:
            # Test with short search term
            websocket.send_json({
                "type": "search",
                "search_term": "A"
            })
            
            data = websocket.receive_json()
            assert data["type"] == "error"
            assert data["code"] == "INVALID_SEARCH"
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {str(e)}")


def test_websocket_invalid_message_type(client):
    """Test WebSocket with invalid message type."""
    try:
        with client.websocket_connect(
            f"/ws/vehicles/search?api_key={settings.SECRET_KEY}"
        ) as websocket:
            websocket.send_json({
                "type": "invalid_type",
                "search_term": "ABC"
            })
            
            data = websocket.receive_json()
            assert data["type"] == "error"
            assert data["code"] == "INVALID_MESSAGE_TYPE"
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {str(e)}")


def test_websocket_connection_limit(client, api_key_headers):
    """Test WebSocket connection limit."""
    connections = []
    max_connections = settings.MAX_WEBSOCKET_CONNECTIONS
    
    try:
        # Try to create more connections than allowed
        for _ in range(max_connections + 1):
            ws = client.websocket_connect(
                f"/ws/vehicles/search?api_key={settings.SECRET_KEY}"
            )
            connections.append(ws.__enter__())
    except Exception:
        # Expected exception for connection limit
        pass
    finally:
        # Clean up connections
        for ws in connections:
            try:
                ws.__exit__(None, None, None)
            except Exception:
                pass

    assert len(connections) <= max_connections


def test_websocket_search_no_results(client):
    """Test WebSocket search with no matching results."""
    try:
        with client.websocket_connect(
            f"/ws/vehicles/search?api_key={settings.SECRET_KEY}"
        ) as websocket:
            websocket.send_json({
                "type": "search",
                "search_term": "NONEXISTENT"
            })
            
            data = websocket.receive_json()
            assert data["type"] == "search_results"
            assert len(data["results"]) == 0
    except Exception as e:
        pytest.fail(f"WebSocket test failed: {str(e)}")
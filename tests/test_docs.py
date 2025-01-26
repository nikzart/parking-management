import pytest
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app


def format_json(data: dict) -> str:
    """Format JSON with proper indentation."""
    return json.dumps(data, indent=2)


def save_api_docs(client: TestClient, api_key_headers: dict, test_vehicle_data: dict):
    """Generate API documentation with real examples."""
    docs_dir = Path("docs/api")
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Store all endpoint documentation
    endpoints = []

    # 1. Vehicle Management
    # 1.1 Create Vehicle
    response = client.post(
        "/api/v1/vehicles",
        json=test_vehicle_data,
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Create Vehicle",
        "method": "POST",
        "path": "/api/v1/vehicles",
        "description": "Register a new vehicle entry",
        "request": {
            "headers": api_key_headers,
            "body": test_vehicle_data
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 1.2 List Vehicles
    response = client.get(
        "/api/v1/vehicles",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "List Vehicles",
        "method": "GET",
        "path": "/api/v1/vehicles",
        "description": "List all active vehicles with pagination",
        "request": {
            "headers": api_key_headers
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 1.3 Get Vehicle
    response = client.get(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Get Vehicle",
        "method": "GET",
        "path": "/api/v1/vehicles/{number_plate}",
        "description": "Get vehicle details by number plate",
        "request": {
            "headers": api_key_headers,
            "path_params": {
                "number_plate": test_vehicle_data['number_plate']
            }
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 1.4 Search Vehicles
    response = client.get(
        f"/api/v1/vehicles/search/{test_vehicle_data['number_plate'][:3]}",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Search Vehicles",
        "method": "GET",
        "path": "/api/v1/vehicles/search/{term}",
        "description": "Search vehicles by number plate or contact name",
        "request": {
            "headers": api_key_headers,
            "path_params": {
                "term": test_vehicle_data['number_plate'][:3]
            }
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 1.5 Remove Vehicle
    response = client.delete(
        f"/api/v1/vehicles/{test_vehicle_data['number_plate']}",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Remove Vehicle",
        "method": "DELETE",
        "path": "/api/v1/vehicles/{number_plate}",
        "description": "Remove a vehicle entry",
        "request": {
            "headers": api_key_headers,
            "path_params": {
                "number_plate": test_vehicle_data['number_plate']
            }
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 2. System Configuration
    # 2.1 Get Retention Period
    response = client.get(
        "/api/v1/config/retention",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Get Retention Period",
        "method": "GET",
        "path": "/api/v1/config/retention",
        "description": "Get current data retention period",
        "request": {
            "headers": api_key_headers
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 2.2 Update Retention Period
    response = client.put(
        "/api/v1/config/retention",
        json={"retention_hours": 48},
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Update Retention Period",
        "method": "PUT",
        "path": "/api/v1/config/retention",
        "description": "Update data retention period",
        "request": {
            "headers": api_key_headers,
            "body": {"retention_hours": 48}
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 2.3 Clear Database
    response = client.post(
        "/api/v1/config/maintenance/clear",
        json={"confirmation": "I understand this will delete all data"},
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Clear Database",
        "method": "POST",
        "path": "/api/v1/config/maintenance/clear",
        "description": "Clear entire database (requires confirmation)",
        "request": {
            "headers": api_key_headers,
            "body": {"confirmation": "I understand this will delete all data"}
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 3. Audit Logs
    # 3.1 Get Audit Logs
    response = client.get(
        "/api/v1/audit",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Get Audit Logs",
        "method": "GET",
        "path": "/api/v1/audit",
        "description": "Get all audit logs with pagination",
        "request": {
            "headers": api_key_headers
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 3.2 Get Entity Logs
    response = client.get(
        "/api/v1/audit/entity/Vehicle",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Get Entity Logs",
        "method": "GET",
        "path": "/api/v1/audit/entity/{entity}",
        "description": "Get audit logs for a specific entity",
        "request": {
            "headers": api_key_headers,
            "path_params": {
                "entity": "Vehicle"
            }
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 3.3 Get Recent Logs
    response = client.get(
        "/api/v1/audit/recent",
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Get Recent Logs",
        "method": "GET",
        "path": "/api/v1/audit/recent",
        "description": "Get most recent audit logs",
        "request": {
            "headers": api_key_headers
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 4. Error Cases
    # 4.1 Unauthorized Access
    response = client.get("/api/v1/vehicles")
    endpoints.append({
        "name": "Unauthorized Access",
        "method": "GET",
        "path": "/api/v1/vehicles",
        "description": "Example of unauthorized access",
        "request": {},
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # 4.2 Invalid Input
    response = client.put(
        "/api/v1/config/retention",
        json={"retention_hours": -1},
        headers=api_key_headers
    )
    endpoints.append({
        "name": "Invalid Input",
        "method": "PUT",
        "path": "/api/v1/config/retention",
        "description": "Example of invalid input validation",
        "request": {
            "headers": api_key_headers,
            "body": {"retention_hours": -1}
        },
        "response": {
            "status_code": response.status_code,
            "body": response.json()
        }
    })

    # Generate documentation
    docs = {
        "title": "Parking Management System API Documentation",
        "version": "1.0.0",
        "description": """
A robust parking management system API that handles vehicle tracking and automated data cleanup.

Features:
- Vehicle registration and tracking
- Automated data cleanup based on retention period
- Comprehensive audit logging
- Real-time vehicle search
- Rate limiting and security measures
""",
        "base_url": "/api/v1",
        "authentication": {
            "type": "API Key",
            "header": "X-API-Key",
            "description": "All endpoints require API key authentication"
        },
        "endpoints": endpoints
    }

    # Save documentation
    with open(docs_dir / "api-docs.json", "w") as f:
        json.dump(docs, f, indent=2)

    # Generate markdown version
    markdown = f"""# {docs['title']}

Version: {docs['version']}

{docs['description']}

## Authentication

{docs['authentication']['description']}

Type: {docs['authentication']['type']}  
Header: {docs['authentication']['header']}

## Endpoints

"""

    for endpoint in endpoints:
        markdown += f"""### {endpoint['name']}

{endpoint['description']}

**Method:** {endpoint['method']}  
**Path:** {endpoint['path']}

**Request:**
```json
{format_json(endpoint['request'])}
```

**Response:**
Status Code: {endpoint['response']['status_code']}
```json
{format_json(endpoint['response']['body'])}
```

"""

    with open(docs_dir / "api-docs.md", "w") as f:
        f.write(markdown)


def test_generate_api_docs(client: TestClient, api_key_headers: dict, test_vehicle_data: dict):
    """Generate API documentation."""
    save_api_docs(client, api_key_headers, test_vehicle_data)
    assert Path("docs/api/api-docs.json").exists()
    assert Path("docs/api/api-docs.md").exists()
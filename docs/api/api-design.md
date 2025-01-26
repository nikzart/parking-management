# API Design Document

## API Overview

Base URL: `/api/v1`
Content-Type: `application/json`
Authentication: API Key (X-API-Key header)

## REST Endpoints

### Vehicle Management

#### 1. Register Vehicle Entry
```
POST /vehicles
```

Request:
```json
{
  "number_plate": "ABC123",
  "contact_name": "John Doe",
  "phone_number": "+1234567890"
}
```

Response (201 Created):
```json
{
  "id": 1,
  "number_plate": "ABC123",
  "contact_name": "John Doe",
  "phone_number": "+1234567890",
  "entry_timestamp": "2025-01-26T13:00:00Z"
}
```

Error Responses:
- 400 Bad Request: Invalid input data
- 409 Conflict: Vehicle already registered
- 429 Too Many Requests: Rate limit exceeded

#### 2. List Active Vehicles
```
GET /vehicles
```

Query Parameters:
- page (optional): Page number (default: 1)
- per_page (optional): Items per page (default: 50)
- sort (optional): Sort field (entry_timestamp, number_plate)
- order (optional): Sort order (asc, desc)

Response (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "number_plate": "ABC123",
      "contact_name": "John Doe",
      "phone_number": "+1234567890",
      "entry_timestamp": "2025-01-26T13:00:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 486,
    "per_page": 50
  }
}
```

#### 3. Get Vehicle Details
```
GET /vehicles/{number_plate}
```

Response (200 OK):
```json
{
  "id": 1,
  "number_plate": "ABC123",
  "contact_name": "John Doe",
  "phone_number": "+1234567890",
  "entry_timestamp": "2025-01-26T13:00:00Z"
}
```

Error Responses:
- 404 Not Found: Vehicle not found

#### 4. Remove Vehicle
```
DELETE /vehicles/{number_plate}
```

Response (204 No Content)

Error Responses:
- 404 Not Found: Vehicle not found

### System Configuration

#### 1. Update Retention Period
```
PUT /config/retention
```

Request:
```json
{
  "retention_hours": 48
}
```

Response (200 OK):
```json
{
  "retention_hours": 48,
  "updated_at": "2025-01-26T13:00:00Z"
}
```

Error Responses:
- 400 Bad Request: Invalid retention period

#### 2. Get Retention Period
```
GET /config/retention
```

Response (200 OK):
```json
{
  "retention_hours": 48,
  "updated_at": "2025-01-26T13:00:00Z"
}
```

### Maintenance

#### 1. Clear Database
```
POST /maintenance/clear
```

Request:
```json
{
  "confirmation": "I understand this will delete all data"
}
```

Response (200 OK):
```json
{
  "message": "Database cleared successfully",
  "timestamp": "2025-01-26T13:00:00Z",
  "records_removed": 150
}
```

Error Responses:
- 400 Bad Request: Missing confirmation
- 403 Forbidden: Invalid confirmation message

## WebSocket Endpoints

### Real-time Vehicle Search
```
WebSocket /ws/vehicles/search
```

Connection Parameters:
- Authentication: API Key via query parameter
- Protocol: ws:// or wss://

Client Message Format:
```json
{
  "search_term": "ABC",
  "type": "search"
}
```

Server Message Format:
```json
{
  "type": "search_results",
  "timestamp": "2025-01-26T13:00:00Z",
  "results": [
    {
      "id": 1,
      "number_plate": "ABC123",
      "contact_name": "John Doe",
      "entry_timestamp": "2025-01-26T13:00:00Z"
    }
  ]
}
```

Error Message Format:
```json
{
  "type": "error",
  "code": "INVALID_SEARCH",
  "message": "Search term must be at least 2 characters"
}
```

## Health Check Endpoints

### System Health
```
GET /health
```

Response (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-01-26T13:00:00Z",
  "version": "1.0.0",
  "components": {
    "database": "healthy",
    "websocket": "healthy"
  }
}
```

### Detailed Health
```
GET /health/details
```

Response (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-01-26T13:00:00Z",
  "version": "1.0.0",
  "components": {
    "database": {
      "status": "healthy",
      "latency_ms": 5,
      "connections": 10
    },
    "websocket": {
      "status": "healthy",
      "active_connections": 25,
      "message_rate": 100
    }
  },
  "metrics": {
    "requests_per_minute": 150,
    "error_rate": 0.01,
    "average_response_time": 45
  }
}
```

## Rate Limiting

- Default rate limit: 100 requests per minute per client
- WebSocket connections: 5 concurrent connections per client
- Rate limit headers included in responses:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## Error Responses

Standard error response format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "number_plate",
        "message": "Invalid format"
      }
    ]
  },
  "request_id": "req_123abc",
  "timestamp": "2025-01-26T13:00:00Z"
}
```

Common Error Codes:
- VALIDATION_ERROR: Input validation failed
- NOT_FOUND: Resource not found
- ALREADY_EXISTS: Resource already exists
- RATE_LIMITED: Rate limit exceeded
- INTERNAL_ERROR: Internal server error
- UNAUTHORIZED: Missing or invalid API key
- FORBIDDEN: Insufficient permissions

## API Versioning

- Version included in URL path (/api/v1)
- Support for multiple versions simultaneously
- Deprecation notice via custom header (X-API-Deprecated)
- Minimum 6 months notice for version deprecation

## Security

- TLS required for all connections
- API key required in X-API-Key header
- Rate limiting per client
- Input validation for all endpoints
- CORS configuration required
- Request ID tracking
- Audit logging for all operations
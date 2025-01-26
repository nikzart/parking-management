# Parking Management System API Documentation

## Overview

This is the comprehensive API documentation for the Parking Management System. The system provides both REST and WebSocket endpoints for managing parking lot vehicle entries, system configuration, and audit logs.

## Table of Contents

1. [REST API Documentation](api-docs.md)
   - Vehicle Management
   - System Configuration
   - Audit Logs
   - Error Handling

2. [WebSocket API Documentation](websocket.md)
   - Real-time Vehicle Search
   - Connection Management
   - Message Formats

## Quick Start

### Authentication

All endpoints require API key authentication using the `X-API-Key` header:

```http
X-API-Key: your-api-key-here
```

### Base URL

```
/api/v1
```

### Common Response Formats

Success Response:
```json
{
  "data": {
    // Response data here
  }
}
```

Error Response:
```json
{
  "detail": "Error message here",
  "request_id": "unique-request-id"
}
```

### Rate Limiting

- REST API: 100 requests per minute per API key
- WebSocket: 10 searches per minute per connection
- Maximum 5 concurrent WebSocket connections per API key

### Monitoring

The system provides monitoring endpoints:

- Health Check: `/health`
- Metrics: `/metrics` (Prometheus format)

### Example Usage

1. Register a new vehicle:
```bash
curl -X POST http://your-server/api/v1/vehicles \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "number_plate": "ABC123",
    "contact_name": "John Doe",
    "phone_number": "+1234567890"
  }'
```

2. Search vehicles in real-time using WebSocket:
```javascript
const ws = new WebSocket('ws://your-server/ws/vehicles/search');
ws.setRequestHeader('X-API-Key', 'your-api-key');

ws.send(JSON.stringify({
  type: 'search',
  data: {
    term: 'ABC'
  }
}));
```

## API Reference

For detailed documentation of all endpoints, see:
- [REST API Documentation](api-docs.md)
- [WebSocket API Documentation](websocket.md)

## Error Codes

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 409: Conflict
- 429: Too Many Requests
- 500: Internal Server Error

WebSocket close codes:
- 1000: Normal closure
- 1008: Policy violation
- 1011: Internal error

## Best Practices

1. Always include the API key in requests
2. Implement proper error handling
3. Use pagination for list endpoints
4. Handle rate limits gracefully
5. Implement reconnection logic for WebSocket
6. Keep search terms concise
7. Regular cleanup of old data

## Support

For issues or questions:
1. Check the error response details
2. Verify request format against documentation
3. Check system health endpoint
4. Monitor rate limits
5. Contact system administrator

## Changelog

### Version 1.0.0
- Initial release
- REST API endpoints
- WebSocket support
- Rate limiting
- Monitoring endpoints
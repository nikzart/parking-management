# WebSocket API Documentation

## Real-time Vehicle Search

The parking management system provides a WebSocket endpoint for real-time vehicle search functionality.

### Endpoint

```
WebSocket: /ws/vehicles/search
```

### Authentication

Authentication is required using the same API key as the REST endpoints:
```
X-API-Key: your-api-key
```

### Message Format

Messages sent to the WebSocket must follow this format:

```json
{
  "type": "search",
  "data": {
    "term": "search term here"
  }
}
```

### Response Format

The server will respond with messages in this format:

```json
{
  "type": "search_results",
  "data": {
    "items": [
      {
        "id": 1,
        "number_plate": "ABC123",
        "contact_name": "John Doe",
        "phone_number": "+1234567890",
        "entry_timestamp": "2025-01-26T10:00:00"
      }
    ],
    "total": 1
  }
}
```

### Error Messages

If an error occurs, the server will respond with:

```json
{
  "type": "error",
  "data": {
    "detail": "Error message here"
  }
}
```

### Connection Limits

- Maximum concurrent connections: 5 per API key
- Connection will be closed after 5 minutes of inactivity
- Rate limit: 10 searches per minute per connection

### Example Usage

Using JavaScript WebSocket client:

```javascript
const ws = new WebSocket('ws://your-server/ws/vehicles/search');

// Add API key to connection
ws.setRequestHeader('X-API-Key', 'your-api-key');

// Send search request
ws.send(JSON.stringify({
  type: 'search',
  data: {
    term: 'ABC'
  }
}));

// Handle responses
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  if (response.type === 'search_results') {
    console.log('Found vehicles:', response.data.items);
  } else if (response.type === 'error') {
    console.error('Error:', response.data.detail);
  }
};

// Handle connection close
ws.onclose = () => {
  console.log('Connection closed');
};
```

### Error Codes

- 1000: Normal closure
- 1008: Policy violation (e.g., rate limit exceeded)
- 1011: Internal server error

### Best Practices

1. Implement reconnection logic with exponential backoff
2. Handle connection errors gracefully
3. Validate messages before sending
4. Close connection when not needed
5. Keep search terms concise and relevant
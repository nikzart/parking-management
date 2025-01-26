# Parking Management System

A robust parking management system backend with SQLite integration that handles vehicle tracking and automated data cleanup.

## Features

- Vehicle tracking with number plate, contact details, and timestamps
- Configurable data retention policy
- Real-time vehicle search via WebSocket
- Comprehensive audit logging
- Automated data cleanup
- Rate limiting and security measures
- Prometheus metrics integration
- Health check endpoints
- Docker containerization
- API documentation with OpenAPI/Swagger

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- SQLite 3

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd parking-system
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

### Local Development

1. Initialize the database:
```bash
alembic upgrade head
```

2. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Check container status:
```bash
docker-compose ps
```

## API Documentation

Once the server is running, access the OpenAPI documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Vehicle Management

- `POST /api/v1/vehicles` - Register new vehicle entry
- `GET /api/v1/vehicles` - List all active vehicles
- `GET /api/v1/vehicles/{number}` - Retrieve specific vehicle details
- `DELETE /api/v1/vehicles/{number}` - Manual vehicle removal
- `WebSocket /ws/vehicles/search` - Real-time vehicle search

### System Configuration

- `PUT /api/v1/config/retention` - Update data retention period
- `GET /api/v1/config/retention` - Get current retention setting
- `POST /api/v1/maintenance/clear` - Clear entire database

### Audit Logs

- `GET /api/v1/audit` - Get audit logs with filtering
- `GET /api/v1/audit/recent` - Get recent audit logs
- `GET /api/v1/audit/entity/{entity}` - Get logs for specific entity

### Health Checks

- `GET /health` - Basic health check
- `GET /health/details` - Detailed system health status

## WebSocket Usage

Connect to the WebSocket endpoint with an API key:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/vehicles/search?api_key=your-api-key');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

// Send search request
ws.send(JSON.stringify({
    type: 'search',
    search_term: 'ABC123'
}));
```

## Monitoring

The system includes Prometheus metrics and Grafana dashboards:

- Prometheus: http://localhost:9091
- Grafana: http://localhost:3000 (default credentials: admin/admin)

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Security

- API key authentication required for all endpoints
- Rate limiting per client
- Input validation and sanitization
- CORS configuration
- Audit logging for all operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
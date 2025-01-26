# Parking Management System

A robust parking management system backend with SQLite integration that handles vehicle tracking and automated data cleanup.

## Features

- Vehicle tracking with unique number plates
- Real-time vehicle search via WebSocket
- Automated data cleanup based on retention period
- Comprehensive audit logging
- Rate limiting and security measures
- Prometheus metrics integration
- Full test coverage
- OpenAPI/Swagger documentation

## Tech Stack

- FastAPI for REST and WebSocket APIs
- SQLite with SQLAlchemy ORM
- Pydantic for data validation
- Prometheus for metrics
- pytest for testing
- Docker support

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/parking-management.git
cd parking-management
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment example and configure:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Docker Support

Build and run with Docker:

```bash
docker build -t parking-management .
docker run -p 8000:8000 parking-management
```

Or using docker-compose:

```bash
docker-compose up
```

## API Documentation

- REST API: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Detailed documentation in [docs/api/](docs/api/)

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

3. Generate API documentation:
```bash
pytest tests/test_docs.py -v
```

4. Run linting:
```bash
flake8 app tests
black app tests
isort app tests
```

## Monitoring

- Health check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics (Prometheus format)

## Security

- API key authentication required for all endpoints
- Rate limiting per API key
- Input validation using Pydantic
- SQL injection protection via SQLAlchemy
- WebSocket connection limits

## Project Structure

```
.
├── app/
│   ├── api/            # API routes and websocket handlers
│   ├── core/           # Core functionality and config
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic
├── docs/
│   └── api/           # API documentation
├── tests/             # Test suite
├── alembic/           # Database migrations
└── docker/            # Docker configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
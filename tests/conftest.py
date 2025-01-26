import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
import uuid

from app.core.config import settings
from app.models.base import Base
from app.core.database import get_db
from app.main import app
from app.models.models import Vehicle, SystemConfig, AuditLog

# Set testing environment
os.environ["TESTING"] = "1"

# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test SessionLocal
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment."""
    # Set test environment variables
    os.environ["SECRET_KEY"] = "your-secret-key-here"
    os.environ["RATE_LIMIT_PER_MINUTE"] = "100"
    os.environ["MAX_WEBSOCKET_CONNECTIONS"] = "5"
    yield
    # Cleanup
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest.fixture(scope="function")
def db_engine():
    """Create test database engine."""
    Base.metadata.drop_all(bind=engine)  # Drop all tables first
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine) -> Generator:
    """Create a fresh database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Clear all tables
    session.query(Vehicle).delete()
    session.query(AuditLog).delete()
    session.query(SystemConfig).delete()
    session.commit()
    
    # Initialize system config with default values
    config = SystemConfig(retention_hours=24)
    session.add(config)
    session.commit()
    session.refresh(config)
    
    yield session
    
    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db) -> Generator:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Initialize app state for WebSocket tests
    app.state.websocket_connections = set()
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    if hasattr(app.state, "websocket_connections"):
        app.state.websocket_connections.clear()

@pytest.fixture(scope="function")
def api_key_headers() -> dict:
    """Create headers with API key for authenticated requests."""
    return {"X-API-Key": settings.SECRET_KEY}

@pytest.fixture(scope="function")
def test_vehicle_data() -> dict:
    """Sample vehicle data for tests."""
    return {
        "number_plate": f"TEST{uuid.uuid4().hex[:6].upper()}",  # Generate unique number plate
        "contact_name": "Test User",
        "phone_number": "+1234567890"
    }

@pytest.fixture(scope="function")
def test_config_data() -> dict:
    """Sample system config data for tests."""
    return {
        "retention_hours": 48
    }
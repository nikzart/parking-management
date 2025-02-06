from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
import asyncio
import prometheus_client
from prometheus_client import Counter, Histogram
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.routes import vehicles, config, audit
from app.core.database import SessionLocal
from app.api.websockets import handle_websocket_connection
from app.services.services import vehicle_service
from app.core.database import engine
from app.models.base import Base

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

async def cleanup_task():
    """Periodic task to cleanup expired vehicle records."""
    while True:
        try:
            db = SessionLocal()
            vehicle_service.cleanup_expired_vehicles(db)
        except Exception as e:
            print(f"Error in cleanup task: {e}")
        finally:
            db.close()
        # Run every hour
        await asyncio.sleep(3600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI app."""
    # Startup
    Base.metadata.create_all(bind=engine)
    
    # Start cleanup task
    cleanup_task_handle = asyncio.create_task(cleanup_task())
    
    yield
    
    # Shutdown
    cleanup_task_handle.cancel()
    try:
        await cleanup_task_handle
    except asyncio.CancelledError:
        pass

# Initialize FastAPI app
app = FastAPI(
    title="Parking Management System",
    description="API for managing parking lot vehicle entries",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect Prometheus metrics."""
    if not settings.TESTING:  # Skip metrics in tests
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status_code).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(
                time.time() - start_time
            )
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=method, endpoint=path, status=500).inc()
            raise e
    else:
        return await call_next(request)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to response headers."""
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Register routes
app.include_router(
    vehicles.router,
    prefix="/api/v1/vehicles",
    tags=["vehicles"]
)

app.include_router(
    config.router,
    prefix="/api/v1/config",
    tags=["config"]
)

app.include_router(
    audit.router,
    prefix="/api/v1/audit",
    tags=["audit"]
)

# WebSocket endpoint
app.add_api_websocket_route(
    "/ws/vehicles/search",
    handle_websocket_connection,
    name="websocket_search"
)

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Check system health."""
    try:
        # Check database connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            db_status = "healthy"
            db_latency = 0
    except Exception as e:
        db_status = "unhealthy"
        db_latency = None

    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.VERSION,
        "components": {
            "database": {
                "status": db_status,
                "latency_ms": db_latency
            }
        }
    }

# Prometheus metrics endpoint
@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """Expose Prometheus metrics."""
    return Response(
        prometheus_client.generate_latest(),
        media_type="text/plain"
    )

# Error handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request.headers.get("X-Request-ID")
        }
    )
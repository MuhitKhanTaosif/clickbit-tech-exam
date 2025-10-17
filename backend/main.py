from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import logging
from contextlib import asynccontextmanager

from config import settings
from middleware import setup_middleware
from utils.logger import setup_logging
from database import create_tables, seed_database, is_database_initialized
from userRoutes import router as user_router
from health import router as health_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting ClickBit Backend API...")
    
    try:
        # Initialize database
        if not is_database_initialized():
            logger.info("Initializing database...")
            create_tables()
            seed_database()
        else:
            logger.info("Database already initialized")
        
        logger.info("Application startup completed successfully")
        yield
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    
    # Shutdown
    logger.info("Shutting down ClickBit Backend API...")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A comprehensive backend API for ClickBit with authentication, user management, and monitoring",
    openapi_url="/openapi.json" if settings.debug else None,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

# Include routers
app.include_router(user_router)
app.include_router(health_router)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ClickBit Backend API",
        "version": settings.app_version,
        "environment": settings.environment,
        "docs_url": "/docs" if settings.debug else "Documentation not available in production",
        "health_check": "/health"
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url.path),
            "method": request.method
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": str(hash(str(exc))),  # Simple error ID for tracking
        }
    )

def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## ClickBit Backend API
        
        A comprehensive backend API providing:
        
        * **Authentication & Authorization** - Secure user registration, login, and session management
        * **User Management** - Profile management and user operations
        * **Health Monitoring** - System health checks and metrics
        * **Security** - Rate limiting, CORS, and security headers
        
        ### Authentication
        
        The API uses JWT tokens stored in secure HTTP-only cookies for authentication.
        
        ### Rate Limiting
        
        API endpoints are rate-limited to prevent abuse. Default limits:
        - 100 requests per minute per IP address
        
        ### Error Handling
        
        The API returns consistent error responses with appropriate HTTP status codes.
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "cookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": "user_session",
            "description": "JWT token stored in HTTP-only cookie"
        }
    }
    
    # Add security to all protected endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                endpoint = openapi_schema["paths"][path][method]
                # Add security to endpoints that require authentication
                if any(tag in endpoint.get("tags", []) for tag in ["authentication", "authorization"]):
                    if path not in ["/user/auth/login", "/user/auth/register"]:
                        endpoint["security"] = [{"cookieAuth": []}]
    
    # Add examples to common responses
    openapi_schema["components"]["examples"] = {
        "UserPublic": {
            "summary": "User Profile",
            "value": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "role": "buyer",
                "is_active": True,
                "is_verified": True,
                "last_login": "2024-01-15T10:30:00Z",
                "phone": "+1234567890",
                "avatar_url": None,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        },
        "ErrorResponse": {
            "summary": "Error Response",
            "value": {
                "detail": "Error message describing what went wrong",
                "error_id": "1234567890"
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True
    )
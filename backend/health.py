"""
Health check and monitoring endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional
import time
import psutil
import os
from datetime import datetime
from sqlmodel import text

from config import settings
from utils.db import SessionDep, engine
from database import check_database_health

router = APIRouter(prefix="/health", tags=["health"])

class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str
    checks: Dict[str, Any]
    uptime_seconds: float
    memory_usage: Dict[str, Any]
    disk_usage: Dict[str, Any]

class DetailedHealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str
    checks: Dict[str, Any]
    system_info: Dict[str, Any]
    application_info: Dict[str, Any]

# Application start time for uptime calculation
start_time = time.time()

def get_uptime() -> float:
    """Get application uptime in seconds."""
    return time.time() - start_time

def get_memory_usage() -> Dict[str, Any]:
    """Get memory usage information."""
    memory = psutil.virtual_memory()
    return {
        "total_gb": round(memory.total / (1024**3), 2),
        "available_gb": round(memory.available / (1024**3), 2),
        "used_gb": round(memory.used / (1024**3), 2),
        "percentage": memory.percent
    }

def get_disk_usage() -> Dict[str, Any]:
    """Get disk usage information."""
    disk = psutil.disk_usage('/')
    return {
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "percentage": round((disk.used / disk.total) * 100, 2)
    }

def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "platform": os.uname().sysname,
        "python_version": os.sys.version.split()[0]
    }

@router.get("/", response_model=HealthStatus)
async def health():
    """Simple health check endpoint."""
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        environment=settings.environment
    )

@router.get("/detailed", response_model=HealthCheck)
async def health_detailed():
    """Detailed health check with system metrics."""
    # Check database connectivity
    db_healthy, db_message = check_database_health()
    
    # Determine overall status
    overall_status = "healthy" if db_healthy else "unhealthy"
    
    checks = {
        "database": {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": db_message
        },
        "application": {
            "status": "healthy",
            "message": "Application is running"
        }
    }
    
    return HealthCheck(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        environment=settings.environment,
        checks=checks,
        uptime_seconds=round(get_uptime(), 2),
        memory_usage=get_memory_usage(),
        disk_usage=get_disk_usage()
    )

@router.get("/full", response_model=DetailedHealthCheck)
async def health_full():
    """Full health check with comprehensive system information."""
    # Check database connectivity
    db_healthy, db_message = check_database_health()
    
    # Check additional services (add as needed)
    checks = {
        "database": {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": db_message
        },
        "application": {
            "status": "healthy",
            "message": "Application is running"
        }
    }
    
    # Determine overall status
    overall_status = "healthy" if all(
        check["status"] == "healthy" for check in checks.values()
    ) else "unhealthy"
    
    return DetailedHealthCheck(
        status=overall_status,
        timestamp=datetime.utcnow(),
        version=settings.app_version,
        environment=settings.environment,
        checks=checks,
        system_info=get_system_info(),
        application_info={
            "debug_mode": settings.debug,
            "rate_limiting_enabled": settings.rate_limit_enabled,
            "cors_origins_count": len(settings.cors_origins),
            "max_file_size_mb": round(settings.max_file_size / (1024**2), 2)
        }
    )

@router.get("/database")
async def health_database(session: SessionDep):
    """Database-specific health check."""
    try:
        # Test basic query
        result = session.exec(text("SELECT 1 as test")).first()
        
        if result and result.test == 1:
            return {
                "status": "healthy",
                "message": "Database connection successful",
                "timestamp": datetime.utcnow()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database query test failed"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database health check failed: {str(e)}"
        )

@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe endpoint."""
    # Check if application is ready to serve requests
    try:
        db_healthy, _ = check_database_health()
        
        if db_healthy:
            return {"status": "ready", "timestamp": datetime.utcnow()}
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Application not ready"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Readiness check failed: {str(e)}"
        )

@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe endpoint."""
    # Simple check to see if application is alive
    return {"status": "alive", "timestamp": datetime.utcnow()}

@router.get("/metrics")
async def metrics():
    """Basic application metrics."""
    memory = get_memory_usage()
    disk = get_disk_usage()
    
    return {
        "timestamp": datetime.utcnow(),
        "uptime_seconds": round(get_uptime(), 2),
        "memory": {
            "used_percentage": memory["percentage"],
            "used_gb": memory["used_gb"]
        },
        "disk": {
            "used_percentage": disk["percentage"],
            "used_gb": disk["used_gb"]
        },
        "application": {
            "version": settings.app_version,
            "environment": settings.environment
        }
    }


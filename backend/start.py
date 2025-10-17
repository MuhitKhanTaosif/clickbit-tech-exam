#!/usr/bin/env python3
"""
ClickBit Backend API Startup Script

This script provides a convenient way to start the application with proper
configuration and database initialization.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_env_file():
    """Check if .env file exists and create from template if needed."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  .env file not found. Please copy .env.example to .env and configure it.")
            print("   cp .env.example .env")
            print("   # Then edit .env with your configuration")
            return False
        else:
            print("❌ Neither .env nor .env.example found!")
            return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import sqlmodel
        import pydantic
        print("✅ Core dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False

def setup_database():
    """Initialize database tables and seed data."""
    try:
        from database import create_tables, seed_database, is_database_initialized
        
        if not is_database_initialized():
            print("🗄️  Initializing database...")
            create_tables()
            seed_database()
            print("✅ Database initialized successfully")
        else:
            print("✅ Database already initialized")
        
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def start_server(host="0.0.0.0", port=8000, reload=True):
    """Start the FastAPI server."""
    try:
        import uvicorn
        from config import settings
        
        print(f"🚀 Starting ClickBit Backend API...")
        print(f"   Environment: {settings.environment}")
        print(f"   Debug mode: {settings.debug}")
        print(f"   Server: http://{host}:{port}")
        print(f"   Docs: http://{host}:{port}/docs")
        print(f"   Health: http://{host}:{port}/health")
        print("")
        
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload and settings.debug,
            log_level=settings.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def run_tests():
    """Run the test suite."""
    try:
        print("🧪 Running tests...")
        result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ pytest not found. Please install test dependencies:")
        print("   pip install pytest pytest-asyncio pytest-cov")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ClickBit Backend API Management")
    parser.add_argument("command", nargs="?", default="start", 
                       choices=["start", "test", "setup", "check"],
                       help="Command to run")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    args = parser.parse_args()
    
    print("🎯 ClickBit Backend API")
    print("=" * 50)
    
    if args.command == "check":
        print("🔍 Checking system requirements...")
        
        if not check_dependencies():
            sys.exit(1)
        
        if not check_env_file():
            sys.exit(1)
        
        print("✅ System check passed!")
        return
    
    elif args.command == "setup":
        print("⚙️  Setting up application...")
        
        if not check_dependencies():
            sys.exit(1)
        
        if not check_env_file():
            sys.exit(1)
        
        if not setup_database():
            sys.exit(1)
        
        print("✅ Setup completed!")
        return
    
    elif args.command == "test":
        if not run_tests():
            sys.exit(1)
        return
    
    elif args.command == "start":
        print("🚀 Starting application...")
        
        # Quick checks
        if not check_dependencies():
            sys.exit(1)
        
        if not check_env_file():
            print("\n💡 Tip: Run 'python start.py setup' to initialize the database")
            sys.exit(1)
        
        # Start server
        start_server(
            host=args.host,
            port=args.port,
            reload=not args.no_reload
        )

if __name__ == "__main__":
    main()


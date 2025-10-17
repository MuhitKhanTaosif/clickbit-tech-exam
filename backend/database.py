"""
Database initialization and management utilities.
"""
import logging
from sqlmodel import SQLModel, create_engine
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
import os
from pathlib import Path

from config import settings
from utils.db import engine
from models.sqlModels import User, UserSession, UserVerification

logger = logging.getLogger(__name__)

def create_tables():
    """Create all database tables."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """Drop all database tables."""
    try:
        SQLModel.metadata.drop_all(engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

def init_alembic():
    """Initialize Alembic for database migrations."""
    alembic_cfg = Config("alembic.ini")
    
    # Set the database URL
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    
    # Create migrations directory if it doesn't exist
    migrations_dir = Path("alembic/versions")
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    return alembic_cfg

def create_migration(message: str):
    """Create a new database migration."""
    try:
        alembic_cfg = init_alembic()
        command.revision(alembic_cfg, message=message, autogenerate=True)
        logger.info(f"Migration created: {message}")
    except Exception as e:
        logger.error(f"Error creating migration: {e}")
        raise

def upgrade_database():
    """Upgrade database to latest migration."""
    try:
        alembic_cfg = init_alembic()
        command.upgrade(alembic_cfg, "head")
        logger.info("Database upgraded to latest migration")
    except Exception as e:
        logger.error(f"Error upgrading database: {e}")
        raise

def downgrade_database(revision: str = "-1"):
    """Downgrade database by one revision."""
    try:
        alembic_cfg = init_alembic()
        command.downgrade(alembic_cfg, revision)
        logger.info(f"Database downgraded to revision: {revision}")
    except Exception as e:
        logger.error(f"Error downgrading database: {e}")
        raise

def get_current_revision():
    """Get current database revision."""
    try:
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()
    except Exception as e:
        logger.error(f"Error getting current revision: {e}")
        return None

def get_head_revision():
    """Get head revision from migrations."""
    try:
        alembic_cfg = init_alembic()
        script = ScriptDirectory.from_config(alembic_cfg)
        return script.get_current_head()
    except Exception as e:
        logger.error(f"Error getting head revision: {e}")
        return None

def is_database_initialized():
    """Check if database is initialized with tables."""
    try:
        # Try to query a simple table to check if it exists
        from sqlmodel import text
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 FROM users LIMIT 1"))
            return True
    except Exception:
        return False

def reset_database():
    """Reset database (drop and recreate all tables)."""
    try:
        logger.warning("Resetting database - all data will be lost!")
        drop_tables()
        create_tables()
        logger.info("Database reset completed")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise

def seed_database():
    """Seed database with initial data."""
    from utils.db import get_session_context
    from utils.security import get_password_hash
    from models.sqlModels import User, UserRole
    
    try:
        with get_session_context() as session:
            # Check if admin user already exists
            from sqlmodel import select
            admin_user = session.exec(select(User).where(User.email == "admin@clickbit.com")).first()
            
            if not admin_user:
                # Create admin user
                admin_user = User(
                    firstName="Admin",
                    lastName="User",
                    email="admin@clickbit.com",
                    password=get_password_hash("Admin123!"),
                    role=UserRole.ADMIN,
                    is_active=True,
                    is_verified=True
                )
                session.add(admin_user)
                session.commit()
                logger.info("Admin user created successfully")
            else:
                logger.info("Admin user already exists")
                
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

def check_database_health():
    """Check database health and connectivity."""
    try:
        with engine.connect() as connection:
            # Simple query to test connection
            from sqlmodel import text
            result = connection.execute(text("SELECT 1"))
            return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python database.py <command>")
        print("Commands: create, drop, reset, seed, upgrade, downgrade, health")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        create_tables()
    elif command == "drop":
        drop_tables()
    elif command == "reset":
        reset_database()
    elif command == "seed":
        seed_database()
    elif command == "upgrade":
        upgrade_database()
    elif command == "downgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
        downgrade_database(revision)
    elif command == "health":
        is_healthy, message = check_database_health()
        print(f"Database Health: {message}")
        sys.exit(0 if is_healthy else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


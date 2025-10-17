from fastapi import Depends, HTTPException, status
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated, Generator
from dotenv import load_dotenv
import os
import logging
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Engine configuration
engine_kwargs = {
    "echo": os.getenv("DATABASE_ECHO", "false").lower() == "true",
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 20,
}

engine = create_engine(DATABASE_URL, **engine_kwargs)

def create_db_and_tables():
    """Create database tables."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

SessionDep = Annotated[Session, Depends(get_session)]

@contextmanager
def get_session_context():
    """Get a database session context manager."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"Database session error: {e}")
        session.rollback()
        raise
    finally:
        session.close()

class DatabaseManager:
    """Database manager with common operations."""
    
    @staticmethod
    def get_by_id(session: Session, model_class, id_value):
        """Get a record by ID."""
        try:
            return session.get(model_class, id_value)
        except Exception as e:
            logger.error(f"Error getting {model_class.__name__} by ID {id_value}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    
    @staticmethod
    def get_all(session: Session, model_class, skip: int = 0, limit: int = 100):
        """Get all records with pagination."""
        try:
            statement = select(model_class).offset(skip).limit(limit)
            return session.exec(statement).all()
        except Exception as e:
            logger.error(f"Error getting all {model_class.__name__}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    
    @staticmethod
    def create(session: Session, model_instance):
        """Create a new record."""
        try:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance)
            return model_instance
        except Exception as e:
            logger.error(f"Error creating {model_instance.__class__.__name__}: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    
    @staticmethod
    def update(session: Session, model_instance):
        """Update a record."""
        try:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance)
            return model_instance
        except Exception as e:
            logger.error(f"Error updating {model_instance.__class__.__name__}: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    
    @staticmethod
    def delete(session: Session, model_instance):
        """Delete a record."""
        try:
            session.delete(model_instance)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting {model_instance.__class__.__name__}: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
    
    @staticmethod
    def soft_delete(session: Session, model_instance, deleted_at_field="deleted_at"):
        """Soft delete a record by setting deleted_at timestamp."""
        try:
            if hasattr(model_instance, deleted_at_field):
                setattr(model_instance, deleted_at_field, datetime.utcnow())
                session.add(model_instance)
                session.commit()
                session.refresh(model_instance)
                return model_instance
            else:
                raise ValueError(f"Model {model_instance.__class__.__name__} doesn't have {deleted_at_field} field")
        except Exception as e:
            logger.error(f"Error soft deleting {model_instance.__class__.__name__}: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
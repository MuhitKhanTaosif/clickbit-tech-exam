# ClickBit Backend API

A comprehensive, production-ready FastAPI backend application with advanced authentication, user management, monitoring, and security features.

## 🚀 Features

### Core Functionality

- **User Authentication & Authorization** - JWT-based authentication with secure cookies
- **User Management** - Registration, login, profile management, password changes
- **Security** - Password hashing, rate limiting, CORS, security headers
- **Health Monitoring** - Comprehensive health checks and system metrics
- **Database Management** - SQLModel with PostgreSQL, migrations with Alembic

### Advanced Features

- **Structured Logging** - JSON logging with rotation and multiple handlers
- **Configuration Management** - Environment-based configuration with validation
- **Rate Limiting** - IP-based rate limiting with Redis support
- **Comprehensive Testing** - Unit and integration tests with pytest
- **API Documentation** - Enhanced OpenAPI documentation with examples
- **Middleware Stack** - Request logging, error handling, security headers

## 📋 Requirements

- Python 3.11+
- PostgreSQL 13+
- Redis (optional, for advanced rate limiting)

## 🛠️ Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Application
APP_NAME="ClickBit Backend API"
APP_VERSION="1.0.0"
DEBUG=true
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/clickbit_db
DATABASE_ECHO=false

# Security
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
CORS_ALLOW_CREDENTIALS=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
```

### 3. Generate Secret Key

```bash
openssl rand -hex 32
```

### 4. Database Setup

```bash
# Create database tables
python database.py create

# Seed with initial data (creates admin user)
python database.py seed

# Or use Alembic for migrations
alembic upgrade head
```

### 5. Run the Application

```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Authentication

The API uses JWT tokens stored in secure HTTP-only cookies.

### Registration

```bash
curl -X POST "http://localhost:8000/user/auth/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "firstName=John&lastName=Doe&email=john@example.com&password=SecurePass123!"
```

### Login

```bash
curl -X POST "http://localhost:8000/user/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=john@example.com&password=SecurePass123!"
```

### Protected Endpoints

```bash
curl -X GET "http://localhost:8000/user/me" \
  -H "Cookie: user_session=<your-jwt-token>"
```

## 🏥 Health Monitoring

### Health Check Endpoints

- `GET /health/` - Basic health status
- `GET /health/detailed` - Detailed health with system metrics
- `GET /health/full` - Comprehensive health information
- `GET /health/database` - Database connectivity check
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/live` - Kubernetes liveness probe
- `GET /health/metrics` - Application metrics

### Example Health Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "development",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "application": {
      "status": "healthy",
      "message": "Application is running"
    }
  },
  "uptime_seconds": 3600.5,
  "memory_usage": {
    "total_gb": 8.0,
    "used_gb": 2.5,
    "percentage": 31.25
  }
}
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test categories
pytest -m unit
pytest -m integration

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py           # Test configuration and fixtures
├── unit/
│   └── test_security.py  # Unit tests for security utilities
├── integration/
│   ├── test_auth.py      # Authentication integration tests
│   └── test_health.py    # Health check integration tests
└── fixtures/             # Test data fixtures
```

## 🗄️ Database Management

### Using Database Scripts

```bash
# Create tables
python database.py create

# Drop tables
python database.py drop

# Reset database (drop and recreate)
python database.py reset

# Seed initial data
python database.py seed

# Check database health
python database.py health
```

### Using Alembic Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current revision
alembic current
```

## 📁 Project Structure

```
backend/
├── models/
│   ├── __init__.py
│   ├── sqlModels.py      # SQLModel database models
│   ├── userModel.py      # Pydantic models for API
│   └── tokenModel.py     # Token-related models
├── utils/
│   ├── __init__.py
│   ├── db.py            # Database connection and utilities
│   ├── security.py      # Security utilities (JWT, passwords)
│   └── logger.py        # Logging configuration
├── test/
│   ├── __init__.py
│   └── current_User.py  # Authentication dependency
├── tests/
│   ├── conftest.py      # Test configuration
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── config.py            # Application configuration
├── database.py          # Database management utilities
├── health.py            # Health check endpoints
├── middleware.py        # Custom middleware
├── userRoutes.py        # User authentication routes
├── main.py             # FastAPI application
├── dependencies.py      # Application dependencies
├── requirements.txt     # Python dependencies
├── alembic.ini         # Alembic configuration
└── pytest.ini         # Pytest configuration
```

## 🔒 Security Features

### Authentication & Authorization

- JWT tokens with configurable expiration
- Secure HTTP-only cookies
- Password strength validation
- Token versioning for secure logout
- Rate limiting per IP address

### Security Headers

- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security (production)
- Referrer Policy

### Input Validation

- Pydantic model validation
- Email format validation
- Password strength requirements
- SQL injection protection via SQLModel

## 📊 Logging

### Log Levels

- **ERROR**: System errors and exceptions
- **WARNING**: Security events and rate limiting
- **INFO**: Application events and user actions
- **DEBUG**: Detailed debugging information

### Log Files

- `logs/app.log` - General application logs
- `logs/error.log` - Error logs only
- `logs/security.log` - Security-related events

### Structured Logging

Logs are written in JSON format for easy parsing and analysis:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "security",
  "message": "Authentication attempt: success",
  "event_type": "auth_attempt",
  "email": "user@example.com",
  "success": true,
  "ip_address": "192.168.1.1"
}
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

```bash
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:pass@db:5432/clickbit_prod
SECRET_KEY=<production-secret-key>
LOG_LEVEL=WARNING
RATE_LIMIT_ENABLED=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the health endpoints for system status

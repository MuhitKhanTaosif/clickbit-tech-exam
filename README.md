# NDIS Service Management System (MVP)

Modern full‑stack MVP for managing NDIS services with client and admin portals.

## Table of Contents

- Overview
- Architecture
- Features
- Tech Stack
- Environments & Variables
- Backend: Setup, Run, Migrations
- Frontend: Setup, Run
- API Overview
- Admin Account & Test Data
- Development Workflow
- Deployment (Proxmox + PostgreSQL)
- Troubleshooting

---

## Overview

This MVP enables clients to sign up, log in, request NDIS services, and track status. Admins can review all requests and approve/reject/complete them. JWT Bearer auth is used (no cookies/sessions).

## Architecture

- Frontend: Next.js (React), TypeScript
- Backend: FastAPI (Python), SQLModel, Alembic
- Database: SQLLITE
- Auth: JWT Bearer via Authorization header
- API: REST under `/api/*`

Folder layout:

- `backend/`: FastAPI app, models,
- `frontend/`: Next.js app, pages, components, API client

## Features

- Client
  - Sign up, log in (JWT)
- Documentation & Observability
  - Swagger UI at `/docs`
  - Health endpoints under `/health`

## Tech Stack

- Python 3.11+
- FastAPI, SQLModel, Alembic, psycopg2-binary
- JWT via PyJWT, passlib[bcrypt]
- Next.js 14+, TypeScript

## Environments & Variables

Backend `.env` (set in `backend/` directory):

```
ENVIRONMENT=development

# JWT
SECRET_KEY=<32+ chars random string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440


Frontend `.env.local` (set in `frontend/` directory):

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Backend

### Install deps

```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run database migrations

Initialize Alembic environment is pre-wired. To generate and apply initial migration if needed:



### Start API

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docs & Health

- Swagger: `http://localhost:8000/docs`

## Frontend

### Install deps

```
cd frontend
npm install
```

### Start dev server

```
npm run dev
```

Visit `http://localhost:3000`.

## API Overview

Authentication (JWT Bearer):

- `POST /api/auth/signup` — body: `firstName`, `lastName`, `email`, `password` (x-www-form-urlencoded)
- `POST /api/auth/login` — body: `email`, `password` → returns `{ access_token, user, expires_in }`
- `GET /api/auth/me` — header: `Authorization: Bearer <token>`


```
cd frontend && echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm install && npm run dev
```

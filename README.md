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

- `backend/`: FastAPI app, models, middleware, migrations
- `frontend/`: Next.js app, pages, components, API client

## Features

- Client
  - Sign up, log in (JWT)
  - Create service requests
  - View own requests and statuses
- Admin
  - View all requests (filter by status)
  - Update request status (approve/reject/complete)
- Services
  - 10 NDIS services seeded on first run
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

# PostgreSQL (recommended to use discrete vars)
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=ndis_mvp
DATABASE_USER=ndis_user
DATABASE_PASSWORD=ndis_pass

# Or provide full DATABASE_URL instead of discrete vars
# DATABASE_URL=postgresql://ndis_user:ndis_pass@127.0.0.1:5432/ndis_mvp
```

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

```
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Start API

```
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docs & Health

- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`, `/health/detailed`

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

Services:

- `GET /api/services` — list all active services
- `GET /api/services/{id}` — service details

Client (requires client token):

- `POST /api/requests` — body: `service_id`, optional `notes` (x-www-form-urlencoded)
- `GET /api/requests/my-requests` — list own requests
- `GET /api/requests/{id}` — request details
- `PUT /api/requests/{id}` — update notes/cancel (MVP supports updating notes)

Admin (requires admin token):

- `GET /api/admin/requests?status=pending|approved|rejected|completed`
- `PUT /api/admin/requests/{id}` — body: `status` and optional `admin_notes`
- `GET /api/admin/users`
- `GET /api/admin/statistics`

All protected endpoints require header: `Authorization: Bearer <token>`

## Admin Account & Seed Data

On first startup, the backend seeds:

- Admin user: `admin@ndis.local` / password: `admin`
- 10 NDIS services

## Development Workflow

1. Configure envs for backend and frontend
2. Start PostgreSQL locally or via container
3. Run Alembic migrations
4. Start backend (uvicorn)
5. Start frontend (Next.js)
6. Use Swagger to test or the frontend UI

## Deployment (Proxmox + PostgreSQL)

1. PostgreSQL container (Proxmox)

- Expose port 5432 to backend LXC
- Create DB and user: `ndis_mvp`, `ndis_user`, grant privileges

2. Backend in LXC

- Copy `backend/`, create `.env` with production values
- Ensure `SECRET_KEY` is long and random
- Install Python deps
- Run `alembic upgrade head`
- Start with `uvicorn` or systemd service; behind a reverse proxy (e.g., Nginx)

3. Frontend in LXC or separate container

- Build: `npm run build`
- Serve: `npm run start` or via Nginx/Node process manager
- Set `NEXT_PUBLIC_API_URL` to the backend URL (including scheme/port)

4. Nginx (optional but recommended)

- Reverse proxy frontend (443) and backend (443/8443)
- Enforce HTTPS, add CORS pass-through for API

## Troubleshooting

- 401 Unauthorized: Ensure `Authorization: Bearer <token>` header is set
- DB connection errors: verify backend DB envs and network reachability
- Alembic autogenerate empty: ensure models are imported and `SQLModel.metadata` includes tables
- CORS: set appropriate origins in backend CORS if hosting across domains

---

## Quick Start (Local)

1. Start Postgres (Docker example):

```
docker run --name ndis-pg -e POSTGRES_PASSWORD=ndis_pass -e POSTGRES_USER=ndis_user -e POSTGRES_DB=ndis_mvp -p 5432:5432 -d postgres:15
```

2. Backend:

```
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

3. Frontend:

```
cd frontend && echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm install && npm run dev
```

# Notification Challenge

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/RWtAnex7Rnpj9g7VeEWgts/W9PXdruWSXAEUToNfzUV9Q/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/RWtAnex7Rnpj9g7VeEWgts/W9PXdruWSXAEUToNfzUV9Q/tree/main)
[![Coverage Status](https://coveralls.io/repos/github/lucast086/notification_challenge/badge.svg?branch=main)](https://coveralls.io/github/lucast086/notification_challenge?branch=main)

A RESTful notification API built with FastAPI that supports multiple delivery channels (Email, SMS, Push). Users can register, authenticate, and manage their own notifications. The system is designed to be extensible — adding a new channel does not require modifying existing logic.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture Decisions](#architecture-decisions)
- [Prerequisites](#prerequisites)
- [Run the App](#run-the-app)
- [Run Tests](#run-tests)
- [API Docs](#api-docs)
- [Things to Improve](#things-to-improve)

---

## Features

- User registration and login with JWT authentication
- CRUD operations for notifications (scoped to the authenticated user)
- Multi-channel notification delivery: Email, SMS, Push
- Extensible channel design — new channels require zero changes to existing code
- Input validation per channel (email format, SMS 160-char limit, push token validation)

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| ORM | SQLModel |
| Database | PostgreSQL |
| Migrations | Alembic |
| Package Manager | Poetry |
| Linter/Formatter | Ruff |
| Tests | pytest + pytest-cov |
| Coverage | Coveralls |
| CI | CircleCI |
| Containers | Docker, Docker Compose |
| Dev Environment | .devcontainer |

---

## Architecture Decisions

**Clean Architecture**
The app is split into layers: routers (controllers), services (business logic), repositories (data access), schemas (DTOs), and clients. This separation makes each layer independently testable and maintainable.

**Extensible Channel Design (Open/Closed Principle)**
Channels implement a `SendStrategy` Protocol. Adding a new channel only requires creating a new class that implements `send()` — no existing code needs to change. The channel is resolved at runtime based on the notification's channel field.

**Async throughout**
All database operations and service calls are async using `asyncpg` as the PostgreSQL driver. This ensures the API can handle concurrent requests efficiently.

**JWT Authentication**
Endpoints are protected with JWT tokens. Each user can only access their own notifications — ownership is enforced at the service layer, not just the router.

**Environment Variables**
All configuration is handled via `pydantic-settings` with a `.env` file. No secrets are hardcoded.

**Alembic for Migrations**
Database schema changes are managed with Alembic, keeping migrations versioned and reproducible.

---

## Prerequisites

- Docker and Docker Compose installed
- Linux/Mac terminal
- No services running on ports `8000` and `5432`

---

## Run the App

### Option 1 — Docker Compose (no devcontainer required)

```bash
chmod +x run_dev.sh
./run_dev.sh
```

This builds the image and starts the API + PostgreSQL. Environment variables are pre-configured in `docker-compose-dev.yml` for local development.

Once running:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

To stop:
```bash
docker compose -f docker-compose-dev.yml down
```

### Option 2 — Devcontainer (VS Code / Cursor)

Open the project in VS Code or Cursor and reopen in container when prompted. The devcontainer sets up the full environment automatically including Poetry, PostgreSQL, and all extensions.

Once inside the container, run the app with:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Run Tests

### Via Docker (from host machine)

```bash
chmod +x run_test.sh
./run_test.sh
```

Builds the image, runs the full test suite, prints `Tests passed` or `Tests failed`, and exits.

### Via Poetry (inside devcontainer)

```bash
poetry run pytest
```

Coverage report is generated in `htmlcov/`.

---

## API Docs

Swagger UI is available at `/docs` when the app is running. All endpoints are versioned under `/v1/`.

| Method | Endpoint | Description |
|---|---|---|
| POST | /v1/auth/register | Register a new user |
| POST | /v1/auth/login | Login and get JWT token |
| GET | /v1/notifications | List own notifications |
| POST | /v1/notifications | Create and send a notification |
| PUT | /v1/notifications/{id} | Update a notification |
| DELETE | /v1/notifications/{id} | Delete a notification |

---

## Things to Improve

- Add actual delivery integrations (SendGrid for email, Twilio for SMS, FCM for push) — currently channels log and simulate delivery
- Add pagination to the notifications list endpoint
- Add rate limiting per user
- Implement refresh tokens for better session management
- Add a frontend (React) to consume the API
- Set up CD pipeline for automated deployment

---

## Author

Lucas T — [GitHub](https://github.com/lucast086)

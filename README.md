# Vertex

A full-stack task management app built with React/TypeScript, FastAPI, and PostgreSQL. I built it to practice patterns you'd actually see in a production codebase — JWT authentication, async database access, containerized dev/prod environments, and a layered backend structure — rather than just another CRUD tutorial project.

## Tech Stack

**Frontend**

- React + TypeScript
- Vite (dev server / build tool)
- TanStack Query, with Devtools enabled in dev (server state, caching, refetching)
- React Router

**Backend**

- FastAPI (async Python web framework)
- Uvicorn (ASGI server that runs FastAPI, with `--reload` in dev)
- Pydantic (request/response validation — powers the `schemas/` models)
- asyncpg (direct async PostgreSQL driver — no ORM)
- PyJWT + bcrypt (auth)
- slowapi (rate limiting)

**Infrastructure**

- PostgreSQL 16
- Docker Compose (separate dev and prod configurations)
- Nginx (serves the production frontend build)

**Testing & Tooling**

- pytest + FastAPI's `TestClient` (backend tests, with DB/auth dependencies swapped out via dependency overrides)
- Vitest + React Testing Library (frontend component tests)
- ESLint + TypeScript (linting and type checking)
- Postman (manual API testing/exploration during development)

## Architecture

### Layered backend structure

The backend is organized by technical layer rather than by feature. I went with layered architecture because I anticipated the project would only have two resources that are deeply coupled, and the separation by layer makes development faster and easier to work with as a solo developer.

If I were expecting the project to grow either in resources or in developers, I would go with a domain-driven architecture that colocates everything for a given resource together to allow for easier collaboration.

### Auth flow

- Passwords are hashed with **bcrypt** before being stored — plaintext passwords never touch the database.
- On login/register, the backend issues a **JWT** (via PyJWT) containing the username and an expiry, returned in the OAuth2-standard `{ access_token, token_type }` shape so it plugs directly into FastAPI's built-in Swagger auth UI.
- Protected routes depend on `get_current_user_id`, which decodes the token and re-verifies the user still exists in the database on every request — rather than trusting the token payload blindly.
- `slowapi` rate limits are applied per-route, e.g. 60 requests/minute per client IP on registration, login, and task listing, to blunt basic brute-force and scraping attempts.

### Async database access without an ORM

Data access uses `asyncpg` directly with a connection pool and hand-written SQL, instead of an ORM like SQLAlchemy. I wanted to work directly with connection pooling and parameterized queries rather than have that abstracted away — it also means query performance and behavior are fully visible rather than depending on how an ORM decides to generate SQL. The trade-off is more boilerplate per query and manual responsibility for avoiding SQL injection (handled here via parameterized queries throughout, e.g. `$1`, `$2` placeholders — no string interpolation into SQL).

### Data model

Two tables: `users` and `tasks`, with `tasks.user_id` referencing `users.id` (cascading delete) and an index on `tasks.user_id` for fast per-user lookups. Task ownership is enforced at the service layer (`verify_task_owner`) on every update/delete, not just at query time — so a user can't act on another user's task even if they guess an ID.

## Setup

### Requirements

- Docker Desktop
- Node.js 20+
- Python 3.11+

### Environment variables

Clone .env.example to create .env and enter appropriate values for each variable.

## Getting Started

### Run with Docker

From the project root:

```bash
docker compose up --build -d
```

For the production compose file:

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### Helpful docker commands

```bash
docker compose logs -f
docker compose down -v
docker exec -it dev_db psql -U ${DB_USER} -d ${DB_NAME}$ -c "{SQL_COMMAND}"
```

### Test the project

```bash
cd backend
python -m pytest -q [test/test_endpoints.py] [-k login]
```

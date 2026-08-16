# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

TISS learning/assessment/certification platform (JPMorgan Code for Good hackathon).

## Stack

- Frontend: React + Vite (`frontend/`)
- Backend: Python + FastAPI (`backend/`)
- DB: SQLite via SQLAlchemy ORM (chosen for easy Postgres migration later)
- Auth: JWT, role field (`learner` / `admin`)
- ML: scikit-learn (on-device) + external LLM API (generative), isolated in `backend/app/ml/`

## Run

Backend:
```
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000
```
Frontend:
```
cd frontend && npm run dev
```

## Structure

```
backend/app/
  main.py        FastAPI app, CORS, router registration
  core/           config.py (env settings), database.py (SQLAlchemy engine/session)
  routers/        API endpoints, thin — delegate to services
  services/       business logic, called by routers
  models/         SQLAlchemy ORM models
  schemas/        Pydantic request/response models
  ml/             ML/LLM logic, never imported directly by routers (go through services)
frontend/src/
  api/client.js       fetch wrapper using VITE_API_BASE_URL, attaches JWT, normalizes errors
  api/auth.js          signup/login/me calls
  context/AuthContext  holds current user + token, exposes login()/logout()
  components/RequireAuth.jsx  route guard, optional `roles` prop for admin-only routes
  pages/                route-level components (LoginPage, SignupPage, ...)
```

## Auth

- Signup is learner-only (public self-signup cannot create admin accounts — flagged security boundary, seed admins directly in DB for the hackathon).
- JWT payload: `sub` (user id), `role`, `exp`. Sent as `Authorization: Bearer <token>`.
- Backend: `core/security.py` (hashing via `bcrypt` directly — passlib's bcrypt backend is broken on bcrypt>=4.1, do not reintroduce it), `core/deps.py` (`get_current_user`, `require_role(*roles)` for role-gated routes).
- Frontend: token persisted in `localStorage`, restored on load via `/auth/me`.

## Conventions

- Routes never contain business logic — call a `services/` function.
- Every route has a Pydantic schema for input validation and typed responses.
- `.env` files are gitignored; `.env.example` is committed and kept current.
- Commit after each fully working vertical slice.

## Known hackathon shortcuts

- SQLite instead of Postgres — fine for demo; needs migration for real production.
- `JWT_SECRET_KEY` default in `.env.example` must be replaced before any real deployment.

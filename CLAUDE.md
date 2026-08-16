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
  api/client.js   fetch wrapper using VITE_API_BASE_URL
```

## Conventions

- Routes never contain business logic — call a `services/` function.
- Every route has a Pydantic schema for input validation and typed responses.
- `.env` files are gitignored; `.env.example` is committed and kept current.
- Commit after each fully working vertical slice.

## Known hackathon shortcuts

- SQLite instead of Postgres — fine for demo; needs migration for real production.
- `JWT_SECRET_KEY` default in `.env.example` must be replaced before any real deployment.

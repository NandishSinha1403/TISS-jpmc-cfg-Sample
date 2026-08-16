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
- Seed the local admin with `cd backend && python -m scripts.seed_admin` (login: `nandish@tiss.edu` / `admin101`). Login requires a valid email format, so `nandish` alone can't be used as the login value.

## Courses & modules

- `Course` has many `Module`s (cascade delete). All reads (`GET /courses`, `GET /courses/{id}`) require auth but allow any role; all writes require `admin` via `require_role`.
- Modules are always addressed under their course (`/courses/{course_id}/modules/{module_id}`) — no standalone module endpoints.
- Frontend: `/courses` (learner browse), `/courses/:courseId` (module reader), `/admin/courses` (admin CRUD, role-gated by `RequireAuth roles={['admin']}`).

## Assessments

- `Quiz` belongs to a `Course` (not a module) — this is the granularity progress tracking, certification, and skill-gap matching (steps 6-8) will key off. `Question` (MCQ) belongs to a `Quiz`, has a `difficulty` field unused for now but reserved for adaptive difficulty (step 5). `QuizAttempt` records each learner submission with score/pass and raw answers.
- Auto-scoring happens server-side in `assessment_service.submit_attempt` — the client only sends `{question_id: selected_index}`.
- Security-relevant: `GET /quizzes/{id}` returns different schemas by role — `QuizLearnerDetailResponse` never includes `correct_index`; only `QuizAdminDetailResponse` does. Do not merge these schemas.
- Frontend: `/quizzes/:quizId` (learner take-quiz + result), admin quiz/question builder is inline inside `AdminCoursesPage`'s course row.

## Adaptive quiz difficulty

- Rule-based, not IRT/ML: `app/ml/adaptive_difficulty.py` steps a 3-rung ladder (easy/medium/hard) — correct steps up, wrong steps down — and picks an unused question at (or closest to) the target rung. Deliberately simple per the "maintainable, not academically perfect" requirement.
- A `Quiz` with `adaptive=True` is taken via `QuizSession`, not the all-at-once `/submit` flow: `POST /quizzes/{id}/start` returns one question, `POST /quizzes/{id}/sessions/{session_id}/answer` scores it, advances difficulty, and returns either the next question or (once `questions_per_attempt` is reached) the final `QuizResultResponse`.
- For adaptive quizzes, `GET /quizzes/{id}` returns `questions: []` to learners — the full pool isn't exposed up front, only revealed one at a time via the session flow. Admins still see the full pool (needed for question management).
- Scoring at session finalize must use only the *asked* questions (`session.asked_question_ids`), not the full quiz question pool — caught and fixed a bug here during testing where the denominator was wrong.
- Frontend: `QuizPage` branches on `quiz.adaptive` between `StaticQuiz` (existing all-at-once form) and `AdaptiveQuiz` (one question at a time, calls `/start` then `/answer` per question).

## Conventions

- Routes never contain business logic — call a `services/` function.
- Every route has a Pydantic schema for input validation and typed responses.
- `.env` files are gitignored; `.env.example` is committed and kept current.
- Commit after each fully working vertical slice.

## Known hackathon shortcuts

- SQLite instead of Postgres — fine for demo; needs migration for real production.
- `JWT_SECRET_KEY` default in `.env.example` must be replaced before any real deployment.

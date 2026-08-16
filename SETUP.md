# SETUP.md

Get this running from a fresh clone. No automated test suite exists yet — verification is manual (see bottom).

## Prerequisites

- Python 3.11+
- Node.js 18+ / npm

## 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # defaults work as-is for local dev
python -m scripts.seed_admin      # creates admin login: nandish@tiss.edu / admin101
uvicorn app.main:app --reload --port 8000
```

Backend now running at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

**Env vars** (`backend/.env`, see `.env.example`):
- `DATABASE_URL` — SQLite file path, default fine for local dev
- `JWT_SECRET_KEY` — **must** be changed before any real deployment (default is a placeholder)
- `CORS_ORIGINS` — must include the frontend's origin (default `http://localhost:5173`)
- `FRONTEND_BASE_URL` — used to build the certificate verify URL embedded in QR codes

## 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env              # default points at localhost:8000, fine for local dev
npm run dev
```

Frontend now running at `http://localhost:5173`.

**Env vars** (`frontend/.env`):
- `VITE_API_BASE_URL` — the backend URL

## 3. Log in

- Admin: `nandish@tiss.edu` / `admin101` (from the seed script above)
- Learner: sign up via the UI at `/signup` (public signup is learner-only by design)

## 4. Typical demo flow

1. Log in as admin → Manage courses → create a course, add a module, add a quiz + questions
2. Log in as a learner (new signup) → browse to the course → mark module complete → take the quiz
3. Passing every quiz in a course auto-issues a certificate → download the PDF → scan its QR code (or visit `/verify/{certificate-id}` directly) to see the public verification page

## Tests

None exist yet. To manually verify a change:
- Backend: exercise endpoints via `http://localhost:8000/docs` (Swagger UI) or `curl`
- Frontend: `npm run build` must succeed (`cd frontend && npm run build`); manually click through the affected page(s) in a browser

## Common gotchas

- If `bcrypt`/`passlib` errors appear: don't reintroduce `passlib` for password hashing — its bcrypt backend is broken on `bcrypt>=4.1`. This project hashes directly with the `bcrypt` package (see `backend/app/core/security.py`).
- Login requires a valid email format — the seeded admin's login is `nandish@tiss.edu`, not `nandish`.
- If admin/learner signup 422s on `EmailStr` validation, the backend needs `email-validator` installed (`pip install email-validator` — included in `requirements.txt`).

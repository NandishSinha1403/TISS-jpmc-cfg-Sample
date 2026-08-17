# TISS Learning & Certification Platform

A learning platform for TISS: courses with modules, quizzes (including adaptive-difficulty quizzes), auto-issued PDF certificates with QR verification, a skill-gap → job-readiness matcher, LLM-generated practice questions, and peer benchmarking.

Stack: React + Vite (frontend), FastAPI + SQLAlchemy + SQLite (backend).

## Quick start

```bash
./start.sh   # starts backend on :8000 and frontend on :5173 (installs deps + seeds admin on first run)
./stop.sh    # stops both
```

Logs: `logs/backend.log`, `logs/frontend.log`. First run creates `backend/.env` and `frontend/.env` from their `.env.example` files — edit `backend/.env` to add `OPENROUTER_API_KEY` if you want the practice-question generator to work (see below).

If you'd rather run things manually, or something in `start.sh` doesn't fit your setup, see `SETUP.md` for the step-by-step version.

## URLs

| What | URL |
|---|---|
| Frontend (learner + admin app) | http://localhost:5173 |
| Login | http://localhost:5173/login |
| Signup (learner only) | http://localhost:5173/signup |
| Learner dashboard | http://localhost:5173/ |
| Course catalog | http://localhost:5173/courses |
| Course detail | http://localhost:5173/courses/:courseId |
| Take a quiz | http://localhost:5173/quizzes/:quizId |
| **Admin panel** (manage courses/modules/quizzes) | http://localhost:5173/admin/courses |
| Certificate public verification page | http://localhost:5173/verify/:certificateId |
| Backend API | http://localhost:8000 |
| Backend interactive docs (Swagger UI) | http://localhost:8000/docs |

There's no separate admin subdomain or app — it's the same frontend, gated by role. Log in with an admin account and the `/admin/courses` route (also linked from the header nav) becomes available; a learner account can't reach it.

## Logging in

- **Admin**: `nandish@tiss.edu` / `admin101` — created automatically by `python -m scripts.seed_admin` (which `start.sh` runs for you on first launch). This is the only way to get an admin account; there's no admin signup form by design.
- **Learner**: sign up yourself at http://localhost:5173/signup — public signup always creates a learner, never an admin.

## Adding courses, modules, quizzes, and certifications

Certificates are never created by hand — they're auto-issued. Everything else is done from the admin panel:

1. Log in as admin → go to **http://localhost:5173/admin/courses**.
2. **Create a course**: title + description. Optionally tag it with a category used by the skill-gap matcher.
3. **Add modules** to the course: title + content (the module's text — this is also what the LLM practice-question generator reads from, so give it real paragraph content, not just a heading).
4. **Add a quiz** to a module: choose static or adaptive difficulty, then add questions (multiple choice, one correct answer each). You can optionally tag a quiz with a `skill_category` (digital literacy, communication, financial literacy, workplace professionalism, problem solving) — this feeds the skill-gap → job-readiness feature.
5. **Certification**: nothing to configure — when a learner passes every quiz in a course, the backend auto-issues a certificate (UUID, PDF with embedded TISS logo, QR code) the moment the last quiz is completed. It shows up on their dashboard immediately, and downloading it or scanning the QR takes anyone to the public verify page above.

All of this can also be done directly against the API via http://localhost:8000/docs if you prefer curl/Swagger to the UI — every admin action in the panel is just a thin wrapper over `POST/PUT/DELETE /courses`, `/courses/{id}/modules`, `/quizzes`, `/quizzes/{id}/questions`.

## Auto-generated practice questions (optional)

Uses OpenRouter (`openai/gpt-oss-20b:free`, a free-tier model) to generate extra practice questions from a module's content on demand. Requires `OPENROUTER_API_KEY` in `backend/.env` — without it, the feature degrades gracefully (a clear "unavailable right now" state, not a crash). Get a free key at https://openrouter.ai.

## Deploying to production (`tiss.nandish.dev`)

Vercel alone isn't enough: it runs stateless serverless functions with no persistent disk, so a long-running FastAPI process backed by a SQLite file can't live there. Split it:

- **Frontend → Vercel**, custom domain `tiss.nandish.dev`
- **Backend → Render** (free web service), a real always-running server

### 1. Push to GitHub

```bash
git add -A
git commit -m "your message"
git push origin main
```

(You've already got this repo connected to GitHub from earlier — same flow.)

### 2. Backend on Render

`render.yaml` at the repo root already describes the service (build/start commands, health check, env vars) — Render will pick it up automatically via **New → Blueprint**, pointed at this repo. Or configure a **New → Web Service** manually:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
- Env vars (set in the Render dashboard, never commit these):
  - `JWT_SECRET_KEY` — a real random secret, not the dev placeholder (`render.yaml` auto-generates one via Blueprint deploy)
  - `CORS_ORIGINS=https://tiss.nandish.dev`
  - `FRONTEND_BASE_URL=https://tiss.nandish.dev` (this is what gets embedded in certificate QR codes)
  - `OPENROUTER_API_KEY` — your real key, if you want practice questions live
  - `DATABASE_URL` — leave as `sqlite:///./tiss.db` for now (see the disk caveat below)

After the first deploy, note the Render URL it gives you (e.g. `https://tiss-backend.onrender.com`). Seed it once via Render's **Shell** tab:

```bash
python -m scripts.seed_admin
python -m scripts.seed_sample_courses
```

**Disk caveat**: Render's free plan has no persistent disk — the SQLite file survives sleep/wake but resets on every redeploy. Fine for a hackathon demo; if you need data to survive redeploys, either add Render's paid persistent disk, or migrate `DATABASE_URL` to their free Postgres add-on (expires after 90 days on the free tier). Not done here — flagging it as a decision, not solving it preemptively.

### 3. Frontend on Vercel

- Import this repo into a new Vercel project
- Root directory: `frontend`
- Framework preset: Vite (auto-detected)
- Env var: `VITE_API_BASE_URL=https://tiss-backend.onrender.com` (your real Render URL from step 2)
- `frontend/vercel.json` is already in the repo — it rewrites all paths to `index.html` so client-side routes like `/verify/:certificateId` don't 404 on a hard refresh

Then **Project Settings → Domains → Add** `tiss.nandish.dev`. Vercel will show you a CNAME target (usually `cname.vercel-dns.com`) — add that as a CNAME record for the `tiss` subdomain in your `nandish.dev` DNS provider. Propagation is usually minutes, sometimes up to ~an hour.

### 4. Keep Render from sleeping

Render's free web services spin down after ~15 minutes idle, so the first request after a lull is slow (cold start). `.github/workflows/keep-alive.yml` is already in the repo — it pings `/health` every 10 minutes via GitHub Actions, which is enough to keep it warm. Wire it up once the backend is deployed:

- Repo → **Settings → Secrets and variables → Actions → Variables** → add `BACKEND_URL` = your Render URL (e.g. `https://tiss-backend.onrender.com`)

That's it — the workflow is already scheduled and will just start working once the variable exists.

## More detail

- `SETUP.md` — manual setup, env vars, common gotchas
- `PROGRESS.md` — build status per feature, what's verified
- `DECISIONS.md` — architecture/design rationale
- `DESIGN.md` — design system (Midnight/Daylight Editorial)
- `CLAUDE.md` — full technical reference

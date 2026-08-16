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

## Progress tracking

- `ModuleCompletion` (unique per user+module) is learner-initiated via `POST /modules/{id}/complete` — completion is not inferred from viewing a page, since that can't be verified server-side without much more instrumentation than an MVP needs.
- `GET /courses/{id}/progress` returns `pct_complete` (modules completed/total), `completed_module_ids` (so the frontend can render per-module state), and per-quiz progress using the learner's **best** attempt, not the latest — a worse retake must never downgrade a prior pass. `QuizAttempt` rows already exist from the assessments feature; this reads them, doesn't duplicate them.
- Frontend: `CourseDetailPage` now fetches course + quizzes + progress together, shows a "Mark as complete" button per module (disabled once done) and best-score/pass-fail next to each quiz link.

## Certificates

- Auto-issued (not manually claimed): after every quiz submission (static and adaptive paths, in `routers/assessments.py`), `certificate_service.check_and_issue_certificate` checks whether the course now has a passing best-attempt on every one of its quizzes; if so and no certificate exists yet for that user+course, one is created. Idempotent — safe to call on every submission. A course with zero quizzes can never auto-complete.
- `Certificate` stores only `id` (the public UUID), `user_id`, `course_id`, `issued_at` — no learner name/course title duplicated, so `/verify` always reflects the live DB, not a snapshot. This is what makes the PDF non-forgeable: the PDF's data is cosmetic, only the UUID carries authority.
- PDF generation is isolated in `certificate_pdf.py` (reportlab + qrcode, pure function: values in, bytes out) — kept separate from `certificate_service.py`'s DB/business logic, same isolation principle as `app/ml/`. The QR code points at `FRONTEND_BASE_URL/verify/{uuid}` (a human-facing page), not the API.
- `GET /verify/{uuid}` is public/unauthenticated by design and returns 404 (not a 500) on any invalid or unknown UUID. `GET /certificates/{id}/pdf` is auth-required and checks ownership (or admin) before serving — verified a second learner gets 404, not another learner's PDF.
- Frontend: public `/verify/:certificateId` route (outside `RequireAuth`), and a "Download certificate" button on `CourseDetailPage` once earned — the PDF fetch attaches the JWT manually (can't use a plain `<a href>` for an authenticated binary download) and triggers a blob-URL save.
- Certificate PDF embeds the real TISS logo (`assets/Tata_Institute_of_Social_Sciences_Logo.svg`) via `svglib` (`svg2rlg` → `reportlab.graphics.renderPDF`), not a placeholder — see `_draw_logo` in `certificate_pdf.py`.

## Skill-gap → job-readiness matcher (backend only, no UI yet)

- Explainable weighted-average scoring, not a trained model — deliberate per DECISIONS.md; only worth a real model if this demonstrably falls short.
- `Quiz.skill_category` (nullable, set at quiz-create time via `QuizCreate.skill_category`) tags a quiz with one of 5 `SkillCategory` values (`digital_literacy`, `communication`, `financial_literacy`, `workplace_professionalism`, `problem_solving`). Untagged quizzes don't count toward any category.
- `app/ml/skill_gap.py` holds the pure logic (same isolation principle as `adaptive_difficulty.py`): `JOB_PROFILES` (5 sample profiles, hand-set weights summing to 1.0 per profile — see the profile table proposed and confirmed with the user), `compute_category_scores` (average of best-attempt % per category), `compute_job_readiness` (weighted sum per job + a "focus next on X" recommendation = the required category with the largest weighted gap, `weight × (100 - score)`).
- `services/skill_service.py` gathers each tagged quiz's best attempt for the learner (same "best not latest" convention as `progress_service.py`) and calls the `ml/` functions — routers never touch scoring math directly.
- Endpoints: `GET /skills/categories`, `GET /skills/jobs` (reference data), `GET /users/me/skill-gap` (a learner's own category scores + job readiness list, sorted by readiness descending). All auth-required, no role restriction, consistent with the rest of the app's read conventions.
- Verified via curl end-to-end: category averaging, weighted readiness math, and focus-next selection all hand-checked against the formulas.
- No frontend yet — per explicit sequencing, this is backend/logic first; UI (results card, practice-question panel, percentile display) comes in a later design round alongside steps 9-10.

## Design system: Midnight/Daylight Editorial (complete — all 8 screens)

- Designed via the **Superdesign** CLI (not any other tool) for the initial direction; refined through a full **Impeccable** pass (critique → adapt → typeset → layout → animate → delight → harden → audit → polish). Style direction, palette, and component patterns live in `.superdesign/design-system.md`; draft history/resume state in `.superdesign/resume.json`. See `DESIGN.md` for the current summary.
- Two token sets, one structural layout: dark ("Midnight," default, `#050505` bg / `#FF6B50` coral accent) and light ("Daylight," `#f7f6f2` bg / `#E5502F` accent), switched via `data-theme` attribute on `<html>`, persisted to `localStorage` (`tiss_theme` key) through `frontend/src/context/ThemeContext.jsx`. All colors are CSS custom properties in `frontend/src/index.css` — never hardcode a hex value in a component; both modes must keep working from the same markup.
- Typography: **EB Garamond** for display/headings (h1/h2/h3), **Inter** for body/UI/data. Numerals (scores, percentages, stats) always stay in Inter's tabular figures — never Garamond's oldstyle numerals — since they're read as data, not prose.
- Link/button text colors are **separate tokens from the decorative accent** (`--color-link`, `--color-accent-fg`) — the raw accent orange fails 4.5:1 as light-mode text-on-fill/text-on-bg; verified via actual sRGB contrast math, not eyeballing, during the audit pass. Never reuse `--color-accent` directly for text color in light mode.
- New shared components (first real component vocabulary in this app — previously every page hand-rolled raw HTML): `AppHeader` (glass nav, logo, nav links, `ThemeToggle`, user identity/logout, real mobile hamburger collapse below 768px — renders a minimal logo-only version when `user` is null, e.g. on the public verify page), `ThemeToggle`, `CustomCursor`, `ProgressBar`, `StatusBadge`, `ErrorPanel` (friendly error copy + optional retry, replaces raw `err.message` alerts app-wide).
- `CustomCursor` (`frontend/src/components/CustomCursor.jsx`): 32px circle, `mix-blend-mode: difference`, `requestAnimationFrame` + lerp follow. Gated on `matchMedia('(pointer: fine)')` checked once at mount — does not render or attach any listener on touch devices. On hovering `a`/`button` it shrinks toward near-invisible (`scale(0.1)`) so the *target element's own hover state* (a white/black invert on `.btn`, `.theme-toggle`, plain `<button>`) carries the affordance instead of the cursor itself.
- `DashboardPage` (new home route, replaces the old inline `HomePage` in `App.jsx`) aggregates `listCourses()` + per-course `getCourseProgress()` + `getCourseCertificate()` client-side — there is no dedicated "my dashboard" backend endpoint, and none is needed for this. Features a "continue learning" panel (highest-progress incomplete course) instead of a uniform card grid, plus an "almost there" nudge at ≥90% progress.
- **Certificate-earned moment** (`QuizPage.jsx`): when a quiz submission is the one that completes a course (checked by comparing certificate existence before/after submit), the result screen shows a distinct celebratory panel — not the routine pass/fail screen — with a direct download CTA. This was the critique's top finding: earning a credential looked identical to a routine quiz pass.
- **Per-question quiz review**: `QuizResultResponse` now includes per-question correctness (`build_question_review` in `assessment_service.py`) — safe to reveal only because the attempt is already finalized, same boundary principle as the "never send `correct_index` mid-attempt" rule. Frontend shows this as an expandable review on the result screen.
- All 8 pages now share the system: Dashboard, `CourseDetailPage`, `QuizPage`, `VerifyPage`, `LoginPage`, `SignupPage`, `CoursesPage`, `AdminCoursesPage`.
- See `PROGRESS.md` for current status and `DECISIONS.md` for why Superdesign/this direction was chosen.

## Conventions

- Routes never contain business logic — call a `services/` function.
- Every route has a Pydantic schema for input validation and typed responses.
- `.env` files are gitignored; `.env.example` is committed and kept current.
- Commit after each fully working vertical slice.

## Known hackathon shortcuts

- SQLite instead of Postgres — fine for demo; needs migration for real production.
- `JWT_SECRET_KEY` default in `.env.example` must be replaced before any real deployment.

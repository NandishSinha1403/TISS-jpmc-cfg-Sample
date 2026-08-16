# PROGRESS.md

Status as of this session. "Done" = fully working AND committed to git.

## Build steps (1-10)

| # | Step | Status |
|---|---|---|
| 1 | Project scaffold | ✅ Done |
| 2 | Auth (JWT, roles) | ✅ Done |
| 3 | Courses & modules CRUD | ✅ Done |
| 4 | Assessments (quiz create/take/auto-score) | ✅ Done |
| 5 | Adaptive quiz difficulty | ✅ Done |
| 6 | Progress tracking | ✅ Done |
| 7 | Credentialed certification (UUID + PDF + QR + verify) | ✅ Done |
| 8 | Skill-gap → job-readiness matcher | ⬜ Not started |
| 9 | Auto-generated practice questions (LLM) | ⬜ Not started |
| 10 | Peer-benchmarking | ⬜ Not started |

## In progress: UI/UX redesign (Midnight/Daylight Editorial)

Inserted between steps 7 and 8 at your request — not one of the original 10 numbered steps.

**Built and working (verified in-browser this session):**
- Design system defined in `.superdesign/design-system.md` (dark "Midnight" + light "Daylight" token pairs, both accessibility-checked for 4.5:1 contrast)
- Light/dark toggle in header, persisted via `localStorage`, keyboard-operable
- Custom decorative cursor (desktop/`pointer: fine` only, shrinks on button hover; buttons invert white on hover instead)
- 4 of 8 target screens fully migrated and tested: **Dashboard**, **Course detail**, **Quiz** (static + adaptive + result states), **Verify** (public certificate page)
- Certificate PDF now embeds the real TISS logo (was text-only before)

**Incomplete / not yet done:**
- ⚠️ **This session's redesign code is NOT YET COMMITTED to git.** `git status` shows modified/new files (App.jsx, index.css, main.jsx, CourseDetailPage.jsx, QuizPage.jsx, VerifyPage.jsx, new components, new pages) sitting uncommitted in the working tree.
- 4 pages still unmigrated, plain styling: Login, Signup, Courses list, Admin course management. They work, they're just visually behind the other 4.
- Dashboard looks sparse in testing because only 1 course was seeded — not a design flaw, just thin test data (flagged, not yet acted on).

**Immediate next action:** commit the redesign work (it's tested and working — no reason to leave it uncommitted), then decide: migrate the remaining 4 pages now, or move on to step 8.

## Blockers / open questions for you to decide

1. **Migrate remaining 4 pages now, or move to step 8 (skill-gap matcher)?** Both are reasonable; your call on priority.
2. **Skill categories for step 8**: the brief said "ask before inventing business logic" — I'll need you to define (or approve a proposed set of) skill categories and 3-5 sample job profiles with weighted requirements before building the matcher.
3. **LLM provider for step 9**: not yet chosen/configured — need an API key and a provider decision (OpenAI, Anthropic, etc.) before practice-question generation can be built.
4. **Dashboard seed data**: fine to leave as-is for now, or do you want a richer seed script (multiple courses/learners) for demo purposes?

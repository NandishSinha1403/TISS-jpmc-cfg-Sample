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

## Done: full Impeccable design pass (Midnight/Daylight Editorial)

Inserted between steps 7 and 8 at your request — not one of the original 10 numbered steps. All 9 Impeccable commands run in order, each verified (clean build + 0-finding detector scan) and committed separately:

1. **critique** — full-app design review, 20/32 heuristic score, 2 P1s + 3 P2/P3s found
2. **adapt** — migrated the last 4 unmigrated pages (Login/Signup/Courses/Admin) to the design system, real per-breakpoint responsive rework (not proportional shrink), real mobile nav hamburger
3. **typeset** — added EB Garamond (display) + Inter (body/data) pairing, fixed 2 more instances of the banned kicker-above-heading pattern, added a `.prose` reading-measure utility
4. **layout** — asymmetric section-heading rhythm (64px above / 16px below) directly addressing the critique's "5 same-weight sections" finding
5. **animate** — the adaptive-quiz difficulty change is now the one authored focal motion (directional badge pulse + question-card entrance), plus a consistent fast page-entrance and capped list-stagger
6. **delight** — the certificate-earned moment now gets a distinct celebratory panel instead of looking identical to a routine quiz pass (the critique's top P1), plus a product-specific "almost there" dashboard nudge at ≥90% progress
7. **harden** — shared `ErrorPanel` component (replaces raw `err.message` alerts app-wide, the other P1), per-question quiz answer review (backend + frontend, your explicit request), a real bug fix (certificate download failure was wiping the whole page instead of showing inline), copy-to-clipboard on the certificate ID
8. **audit** — found and fixed 2 real WCAG contrast failures via actual sRGB math (light-mode button text 3.80:1, link text 3.52:1 — both now above 4.5:1), fixed a heading-hierarchy skip
9. **polish** — final consistency pass, docs updated

**Not verified live**: the Claude-in-Chrome browser extension was unavailable/removed for this entire design phase. Everything was verified via clean builds, 0-finding detector scans, and direct backend curl tests (for the certificate/review logic specifically). A manual visual pass at `localhost:5173` across light/dark × mobile/tablet/desktop is still worth doing before calling this fully signed off — flagged in every relevant commit message, not silently skipped.

## Next: steps 8-10 (backend/logic first, no UI, per your sequencing)

1. **Skill-gap → job-readiness matcher** — needs skill categories and 3-5 sample job profiles with weighted requirements defined/approved before building (per "ask before inventing business logic")
2. **Auto-generated practice questions (LLM)** — needs an LLM provider decision (OpenAI, Anthropic, etc.) and API key before this can be built
3. **Peer-benchmarking** — plain SQL aggregation, no blockers identified yet

After steps 8-10 are backend-complete: a final design round for the new UI they need (results card, practice-question panel, percentile display) plus one more full-app polish pass.

## Open questions for you to decide

1. **Skill categories/job profiles for step 8** — see above, need your input before starting.
2. **LLM provider for step 9** — see above, need your decision + API key before starting.
3. **Live visual sign-off** — worth doing a manual browser pass before demo day, given the extension was unavailable for this whole phase.

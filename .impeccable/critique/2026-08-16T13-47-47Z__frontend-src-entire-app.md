---
target: entire app (frontend/src)
total_score: 20
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 2
timestamp: 2026-08-16T13-47-47Z
slug: frontend-src-entire-app
---
# Critique: Entire App (Dashboard, Course Detail, Quiz, Verify, + unmigrated screens)

Method: dual-agent (A: design review · B: detector/browser evidence). Browser extension disconnected for both — source-only run, no live screenshots or in-browser detector injection.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Loading states covered but generic text swap, no skeletons |
| 2 | Match System / Real World | 3 | Clear copy; difficulty badge shows raw enum text with no framing |
| 3 | User Control and Freedom | 2 | Adaptive quiz is a one-way ratchet — no back/review once answered |
| 4 | Consistency and Standards | 2 | Hard style discontinuity between migrated and unmigrated screens |
| 5 | Error Prevention | 2 | Static quiz allows submitting with zero questions answered |
| 6 | Recognition Rather Than Recall | 3 | Progress/pass-fail/scores all visible in-context |
| 7 | Flexibility and Efficiency | n/a | Operate-mode tool, no power-user shortcuts expected |
| 8 | Aesthetic and Minimalist Design | 3 | Clean spacing scale, but Dashboard stacks 5 same-weight sections |
| 9 | Error Recovery | 2 | Every error state is raw err.message, no retry |
| 10 | Help and Documentation | n/a | Operate-mode tool, genuinely not applicable |
| Total | | 20/32 | Acceptable (62.5%) |

## Design Specificity Verdict

Token system and copy show real authorship. Screen compositions are structurally generic. Certificate-earned moment (the product's actual payoff) gets the least composition effort of any screen.

Deterministic scan: detect.mjs --json frontend/src -> exit 2, 1 finding: overused-font on index.css:1 (Inter) — already an open question from the prior polish pass.

Visual overlays: unavailable this run (browser extension disconnected).

## Overall Impression

System-level craft is solid. Missing dramatic emphasis where it matters: passing a quiz and earning a certificate look identical; every error is treated the same regardless of severity.

## What's Working

- ProgressBar/StatusBadge correctly implement the accessibility spec in code, not just docs.
- FeaturedCourse dashboard composition is genuinely considered (relevance sort, distinct CTA copy, real hover delight).
- Token discipline is real — no hardcoded hex in component logic found.

## Priority Issues

[P1] Certificate-earned moment has no distinct visual treatment from an ordinary quiz pass. Fix: celebratory panel on certificate issuance. Command: delight.

[P1] Every error state is raw err.message with no recovery path (DashboardPage.jsx:122, CourseDetailPage.jsx:61, QuizPage.jsx:168, VerifyPage.jsx:20). Fix: shared ErrorPanel with friendly copy + retry. Command: harden.

[P2] Dashboard stacks 5 same-weight sections in one scroll. Fix: progressive disclosure, real section breaks. Command: layout/distill.

[P2] Adaptive quiz has no back/review, difficulty badge unexplained. Fix: one-line explainer. Command: clarify.

[P3] Migrated vs unmigrated screens adjacent on primary nav path (Dashboard -> Courses). Fix: prioritize CoursesPage migration. Command: adapt.

## Persona Red Flags

Jordan (first-timer): Dashboard -> Courses nav hits unmigrated page, quality cliff in first 5 minutes. Difficulty badge unexplained.

Riley (stress-tester): StaticQuiz submits with zero answers silently, no per-question review after submit.

Sam (accessibility-dependent): raw err.message alerts give screen readers no structural differentiation between error types.

## Minor Observations

- .stat-strip has no wrap/stack fallback for narrow viewports.
- VerifyPage certificate ID has no copy-to-clipboard.
- CourseDetailPage module content is flat unstyled paragraph.
- SealIcon and StatusBadge checkmark are redundant signifiers when adjacent.

## Questions to Consider

1. Why does earning a certificate look identical to failing a quiz?
2. Is no-per-question-review intentional anti-cheating or an oversight?
3. Why were Login/Signup last in migration order despite being first-touch screens?

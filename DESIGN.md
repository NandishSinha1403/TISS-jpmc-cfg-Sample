# DESIGN.md

Note: no `DESIGN.md` existed before this session — there is no "Impeccable" tool in this project's history, we used **Superdesign** for the design pass (see `DECISIONS.md`). This file is newly created to summarize the current design system for quick reference; full detail lives in `.superdesign/design-system.md`.

## Current direction: Midnight/Daylight Editorial

Bold, high-contrast, editorial/agency mood. Two token sets, one structural layout — dark is default.

- **Dark ("Midnight")**: `#050505` bg, `#111111` surface, `#ebebeb` text, `#FF6B50` coral accent
- **Light ("Daylight")**: `#f7f6f2` bg, `#ffffff` surface, `#1c1c1c` text, `#E5502F` accent (darkened coral for text-contrast on light bg)
- Font: Inter (single family, weight/size carries hierarchy — no serif/mono trio)
- Radius: generous (8-24px on cards, full-pill on nav/badges/progress) — opposite of the earlier "Editorial Tech" direction's sharp 1-2px rule
- Toggle in header, persisted to `localStorage`, keyboard-operable

## Source of truth

- `.superdesign/design-system.md` — full palette, type scale, spacing, component patterns, accessibility rules
- `.superdesign/resume.json` — Superdesign project/draft IDs, which draft is canonical per screen
- `frontend/src/index.css` — the tokens as actual CSS custom properties (implementation)

## Screens covered

| Screen | Status |
|---|---|
| Dashboard (`/`) | ✅ Implemented, tested |
| Course detail (`/courses/:id`) | ✅ Implemented, tested |
| Quiz (`/quizzes/:id`) | ✅ Implemented, tested (static + adaptive + result) |
| Certificate verify (`/verify/:id`) | ✅ Implemented, tested |
| Login / Signup | ⬜ Not migrated — plain fallback styling |
| Courses list / Admin | ⬜ Not migrated — plain fallback styling |

## Superseded direction (for history, not current)

An earlier pass produced a light, forest-green "Editorial Tech" system (hairline borders, serif headings, sharp corners) — abandoned in favor of Midnight/Daylight per your explicit pivot mid-session. Old Superdesign drafts for that direction still exist on the canvas (the CLI has no delete command) but are marked `SUPERSEDED` in `.superdesign/resume.json` and are not used anywhere in the actual app code.

## Known gaps

- Custom cursor and theme-toggle are new, first-of-their-kind interactive elements in this app — see `CLAUDE.md`'s design-system section for implementation notes.
- 4 of 8 target screens (per the last design brief) are unmigrated; see `PROGRESS.md`.

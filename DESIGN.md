# DESIGN.md

Note: there is no "Impeccable" tool history predating this doc — the initial direction was set with **Superdesign**, then refined through a full **Impeccable** pass (critique → adapt → typeset → layout → animate → delight → harden → audit → polish), all 9 steps completed and committed. Full detail lives in `.superdesign/design-system.md`; this file is the quick-reference summary.

## Current direction: Midnight/Daylight Editorial

Bold, high-contrast, editorial/agency mood. Two token sets, one structural layout — dark is default.

- **Dark ("Midnight")**: `#050505` bg, `#111111` surface, `#ebebeb` text, `#FF6B50` coral accent
- **Light ("Daylight")**: `#f7f6f2` bg, `#ffffff` surface, `#1c1c1c` text, `#E5502F` accent
- **Type**: EB Garamond for display/headings, Inter for body/UI/data — numerals always stay in Inter's tabular figures (data reads as data, not prose)
- Radius: generous (8-24px on cards, full-pill on nav/badges/progress)
- Toggle in header, persisted to `localStorage`, keyboard-operable, real mobile hamburger collapse below 768px

**Contrast note**: the raw accent orange fails WCAG AA (4.5:1) as light-mode text — both as button-fill text and as plain link color. Fixed with dedicated tokens (`--color-accent-fg` = black in light mode, `--color-link` = a darker `#C73F22`) verified via actual sRGB luminance calculation, not eyeballing. Never reuse `--color-accent` directly as a text color in light mode.

## Source of truth

- `.superdesign/design-system.md` — full palette, type scale, spacing, component patterns, accessibility rules
- `.superdesign/resume.json` — Superdesign project/draft IDs, which draft is canonical per screen
- `.impeccable/critique/` — the full critique report from the Impeccable pass (heuristic scores, priority issues, persona red flags)
- `frontend/src/index.css` — the tokens as actual CSS custom properties (implementation)

## Screens covered — all 8, fully migrated

| Screen | Status |
|---|---|
| Dashboard (`/`) | ✅ Featured "continue learning" panel + course ledger + stat strip |
| Course detail (`/courses/:id`) | ✅ |
| Quiz (`/quizzes/:id`) | ✅ static + adaptive (with focal difficulty-shift motion) + result + answer review |
| Certificate verify (`/verify/:id`) | ✅ public, copy-to-clipboard on the ID |
| Login / Signup | ✅ migrated in the adapt pass |
| Courses list / Admin | ✅ migrated in the adapt pass |

## Key moments from the Impeccable pass

- **Certificate-earned moment**: the critique's top finding was that earning a certificate looked identical to a routine quiz pass. Fixed with a distinct celebratory result panel (animated seal, large serif headline, direct download CTA) that only appears when the submission is the one that actually completes the course.
- **Adaptive difficulty focal motion**: the difficulty badge and question card now visually communicate the ladder stepping up/down after each answer — the one animation thesis specific to this product's actual mechanic.
- **Per-question quiz review**: expandable review of right/wrong answers after any quiz submission, added per explicit request.

## Superseded direction (for history, not current)

An earlier pass produced a light, forest-green "Editorial Tech" system (hairline borders, serif headings, sharp corners) — abandoned in favor of Midnight/Daylight per an explicit mid-session pivot. Old Superdesign drafts for that direction still exist on the canvas (the CLI has no delete command) but are marked `SUPERSEDED` in `.superdesign/resume.json` and are not used anywhere in the actual app code.

## Known gaps / not verified live

- The Claude-in-Chrome browser extension was unavailable/removed for most of this design phase — all work was verified via clean builds, a 0-finding detector scan, and (for the certificate/review logic) direct backend curl tests. Live in-browser visual confirmation across the 4 modified pages is still worth a manual pass at `localhost:5173` before treating this as fully signed off.

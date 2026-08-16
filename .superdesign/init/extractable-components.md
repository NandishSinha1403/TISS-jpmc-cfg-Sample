# Extractable Components

**Nothing exists yet to extract** — see `components.md` and `layouts.md`: this codebase has zero shared UI primitives and zero layout/nav components today. Every page currently hand-rolls raw HTML.

This file instead lists the components the Editorial Tech redesign should **introduce** as the new shared vocabulary, since they'll recur across all four target screens and should be designed once, consistently, rather than per-page.

#### Layout Components (new — none exist today)
- **AppHeader** — logo (TISS mark) + primary nav + user identity/logout. Needed on every authenticated screen (dashboard, course view, quiz screen); absent on the public verify page.
  - Extractable props: `activeRoute` (string, for nav highlight), `userName`, `userRole`, `onLogout`
  - Hardcoded: TISS logo asset, nav link labels

#### Basic Components (new — none exist today)
- **Button** — primary (forest-green fill), secondary (outline/1px border), disabled state. Used for "Mark as complete," "Submit quiz," "Download certificate," "Next," "Log out," etc.
  - Extractable props: `variant` (primary/secondary), `disabled`, `label`
- **ProgressBar** — course completion %, described as a "scan-line" flourish per the brief but must remain legible/functional without animation (no hover-only, no animation-dependent meaning).
  - Extractable props: `percent` (number 0–100), `label`
- **Card** — course card (dashboard), module card (course view), question card (quiz), certificate card. One visual pattern (1px border, no shadow, ≤2px corner radius) reused across all four screens.
  - Extractable props: `title`, `meta` (Space Mono label text), `children`
- **StatusBadge / MetaLabel** — Space Mono, uppercase, wide-tracking label for things like "PASSED," "NOT PASSED," "MEDIUM DIFFICULTY," "CERTIFICATE ID," quiz score numbers. This is the component that makes real data (scores, %, IDs, difficulty) visually consistent across screens — high priority to define once in `design-system.md`.
  - Extractable props: `text`, `tone` (neutral/success/warning — success = passed, warning = not passed, kept as text+icon distinction, never color-only, for accessibility)
- **QuizOption** — radio-style answer choice, used identically in both `StaticQuiz` and `AdaptiveQuiz` question rendering today (currently duplicated inline in `QuizPage.jsx`).
  - Extractable props: `label`, `selected`, `onSelect`

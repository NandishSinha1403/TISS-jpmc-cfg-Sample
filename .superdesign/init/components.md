# Shared UI Primitives

Framework: React 19 + Vite (plain JSX, no TypeScript). No component library (no shadcn/MUI/Chakra/Radix/Ant). No Tailwind — plain CSS with `:root` CSS variables in `src/index.css`.

**There are no shared/reusable UI primitives in this codebase.** Every page (`src/pages/*.jsx`) writes its own raw HTML elements (`<form>`, `<input>`, `<button>`, `<ul>`, `<article>`) directly, styled only by the global `#center` layout rule and default browser styling — there is no `Button.jsx`, `Card.jsx`, `Input.jsx`, etc. to extract or reproduce.

The one repeated structural pattern across pages is wrapping page content in `<section id="center">...</section>` (see `layouts.md` / `theme.md` for the CSS this maps to).

This is a greenfield styling opportunity: the Editorial Tech design system introduces the first real component vocabulary (buttons, cards, progress bars, labels) for this app.

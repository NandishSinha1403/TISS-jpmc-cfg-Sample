# Theme / Design Tokens

## Part 1 — Compact summary

**Current state: no real design system.** `src/index.css` still contains the unmodified Vite+React starter theme (purple accent `#aa3bff`, system-ui fonts, light/dark via `prefers-color-scheme`). No page actually relies on this theme meaningfully beyond `#center` (flex-centering wrapper), `#root` (max-width shell with side borders), and `h1`/`h2`/`code` base styles. `App.css` is 100% leftover Vite template CSS (`.hero`, `#next-steps`, `.ticks`, `#docs`, `#spacer`) — **dead code, unused by any current page**, safe to discard in the redesign.

**TISS brand color found in the actual logo asset** (`assets/Tata_Institute_of_Social_Sciences_Logo.svg`): fills used are `#008000` (pure green), `#000000` (black), `#666666` (grey), `#ffffff` (white). This confirms the requested muted-forest-green ("Editorial Tech") direction is genuinely on-brand for TISS — the design system should treat `#008000` as the brand-authority anchor and deliberately mute/desaturate it toward the requested `#3d7068`-family accent, not invent an unrelated palette.

No Tailwind config exists — plain CSS with `:root` custom properties.

## Part 2 — Raw source dumps

### `src/index.css` (full file, current/legacy — to be replaced)

```css
:root {
  --text: #6b6375;
  --text-h: #08060d;
  --bg: #fff;
  --border: #e5e4e7;
  --code-bg: #f4f3ec;
  --accent: #aa3bff;
  --accent-bg: rgba(170, 59, 255, 0.1);
  --accent-border: rgba(170, 59, 255, 0.5);
  --social-bg: rgba(244, 243, 236, 0.5);
  --shadow:
    rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

  --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
  --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, Consolas, monospace;

  font: 18px/145% var(--sans);
  letter-spacing: 0.18px;
  color-scheme: light dark;
  color: var(--text);
  background: var(--bg);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  @media (max-width: 1024px) {
    font-size: 16px;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --text: #9ca3af;
    --text-h: #f3f4f6;
    --bg: #16171d;
    --border: #2e303a;
    --code-bg: #1f2028;
    --accent: #c084fc;
    --accent-bg: rgba(192, 132, 252, 0.15);
    --accent-border: rgba(192, 132, 252, 0.5);
    --social-bg: rgba(47, 48, 58, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
  }

  #social .button-icon {
    filter: invert(1) brightness(2);
  }
}

body {
  margin: 0;
}

#root {
  width: 1126px;
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
  border-inline: 1px solid var(--border);
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

h1,
h2 {
  font-family: var(--heading);
  font-weight: 500;
  color: var(--text-h);
}

h1 {
  font-size: 56px;
  letter-spacing: -1.68px;
  margin: 32px 0;
  @media (max-width: 1024px) {
    font-size: 36px;
    margin: 20px 0;
  }
}
h2 {
  font-size: 24px;
  line-height: 118%;
  letter-spacing: -0.24px;
  margin: 0 0 8px;
  @media (max-width: 1024px) {
    font-size: 20px;
  }
}
p {
  margin: 0;
}

code,
.counter {
  font-family: var(--mono);
  display: inline-flex;
  border-radius: 4px;
  color: var(--text-h);
}

code {
  font-size: 15px;
  line-height: 135%;
  padding: 4px 8px;
  background: var(--code-bg);
}
```

### `src/App.css` (full file — dead Vite-template CSS, unused by any current page)

```css
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero { /* ...unused decorative logo-spin styles... */ }
#next-steps { /* ...unused Vite template footer links... */ }
#docs { /* ... */ }
#spacer { /* ... */ }
.ticks { /* ... */ }
```

### TISS logo brand colors (extracted, `assets/Tata_Institute_of_Social_Sciences_Logo.svg`)

```
fill: #008000  (primary brand green)
fill: #000000  (black)
fill: #666666  (grey)
fill: #ffffff  (white)
```

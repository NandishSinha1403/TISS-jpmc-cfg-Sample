# TISS Learning Platform — Design System: "Midnight Editorial"

## Product context

A skills-training / employment-readiness platform built for TISS (Tata Institute of Social Sciences) to replace closed classrooms. Learners are **working adults**, not students on campus — the tone must read as credible, ambitious, and modern, not gamified or childish. Learners browse courses, read module content, take quizzes (some adaptive-difficulty), track progress, and earn verifiable certificates (PDF + QR-code public verification). Key JTBD: "show me exactly where I stand" (progress %, quiz scores, pass/fail, certificate validity) — real data must always be legible, never decorative.

## Visual direction: Midnight Editorial

Bold, high-contrast, magazine/agency-editorial mood — oversized display type, generous whitespace, a glass-effect floating nav, a single confident accent color (coral/orange) used sparingly against a near-black canvas. This replaces the prior "Editorial Tech" (light, forest-green, hairline-serif) direction; that system is superseded, not blended in.

## Brand anchor

The real TISS logo (`assets/Tata_Institute_of_Social_Sciences_Logo.svg`) uses `#008000` (green) as its brand color. Midnight Editorial does NOT use green as the primary accent — the coral `#FF6B50` is the direction the user explicitly specified for this pass. The TISS logo itself is still reproduced faithfully wherever it appears (nav, certificates) in its real colors; it simply isn't the UI's *accent* color in this style. Do not recolor the logo to coral.

## Light/dark mode — REQUIRED, same structure both ways

This design system ships **two token sets sharing one structural layout** — swap colors/contrast only, never re-layout between modes. A header-mounted toggle switches between them; state persists via `localStorage` (this is a real deployed web app, not a Claude.ai artifact, so `localStorage` is permitted and expected here).

### Dark mode tokens (default / "Midnight")

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#050505` | Page background |
| `--color-surface` | `#111111` | Cards, panels |
| `--color-surface-raised` | `#1a1a1a` | Nav pills, chips, hover surfaces |
| `--color-fg` | `#ebebeb` | Primary text, headings |
| `--color-fg-muted` | `#a3a3a3` | Secondary text users must still read (descriptions, labels, meta) — **NOT** the reference spec's `#666666`/`#444444`/`#888888`, which fail 4.5:1 against `#050505`/`#111111`. `#a3a3a3` on `#050505` is ~9.5:1; verify against `#111111` too (~8.7:1) — both pass comfortably. |
| `--color-fg-decorative` | `#444444` | TRUE decoration only (dividers, watermark numerals, disabled icon tint) — never text a user must read |
| `--color-accent` | `#FF6B50` | Primary accent — CTAs, links, active states, progress fill, focus rings |
| `--color-accent-fg` | `#050505` | Text/icon color placed ON TOP of `--color-accent` fills (e.g. coral button label) — verified high contrast against coral |
| `--color-border` | `rgba(255,255,255,0.12)` | Card/nav borders |
| `--color-success` | `#4ADE80` | Passed / verified — paired with check glyph, ~7:1 on `#050505` |
| `--color-warning` | `#FF6B50` | Not passed / invalid — reuses accent coral paired with an x glyph + text (status is never color-only regardless) |
| `--glass-bg` | `rgba(17,17,17,0.8)` | Floating/glass nav background, paired with `backdrop-filter: blur(12px)` |

### Light mode tokens ("Daylight Editorial")

Same structural roles, inverted — this is literally the palette validated in the prior Editorial Tech pass, reused here as the light-mode pairing per the brief:

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#f7f6f2` | Page background |
| `--color-surface` | `#ffffff` | Cards, panels |
| `--color-surface-raised` | `#f0efe9` | Nav pills, chips, hover surfaces |
| `--color-fg` | `#1c1c1c` | Primary text, headings |
| `--color-fg-muted` | `#4a4a46` | Secondary text users must still read — ~9:1 on `#f7f6f2`, ~9.8:1 on `#ffffff` |
| `--color-fg-decorative` | `#b4b4b4` | TRUE decoration only |
| `--color-accent` | `#E5502F` | Coral, darkened ~10% from `#FF6B50` for light-background contrast (raw `#FF6B50` on white is only ~2.7:1 for text use; the darkened value clears 4.5:1 for text/icons while the raised `#FF6B50` is still fine as a large-area fill with dark text on top) |
| `--color-accent-fg` | `#ffffff` | Text/icon color on top of accent fills |
| `--color-border` | `rgba(28,28,28,0.12)` | Card/nav borders |
| `--color-success` | `#1E7A4C` | Passed / verified, ~5.2:1 on `#f7f6f2` |
| `--color-warning` | `#B23A20` | Not passed / invalid, darkened coral, ~5.9:1 on `#f7f6f2` |
| `--glass-bg` | `rgba(255,255,255,0.75)` | Floating/glass nav background, same blur treatment |

**Rule for every draft/component going forward:** never hardcode a hex value in markup — always reference the token so both modes render correctly from one structure. When a variation prompt says "dark mode" or "light mode," it means "render this exact structure with that token set," not a different layout.

## Typography

- **Font**: `'Satoshi', 'Inter', system-ui, sans-serif` (Satoshi as primary display/body face per the reference; Inter as the loaded fallback). One typeface family, not a serif/sans/mono trio like the previous system — weight and size carry the hierarchy instead.
- **Display/hero** (landing greeting, certificate learner name): weight 700–800, extremely large (`clamp(48px, 10vw, 140px)`), tight tracking (`-0.04em` to `-0.05em`), line-height `0.9–1.05`.
- **Headings** (h1–h3): weight 600–700, tight tracking (`-0.02em`).
- **Body**: weight 400–500, normal tracking, generous line-height (`1.5–1.6`) for readability against the dark background.
- **Eyebrows / meta labels** (section labels, status tags, dates): weight 700, uppercase, wide tracking (`0.2em–0.4em`), small size (10–12px) — this system's equivalent of the old Space Mono data-label role. Data values (scores, %, IDs) use the same treatment: bold, uppercase where it's a label, tabular/normal case where it's a raw number.

## Spacing & layout

- `4px` base unit, same scale as before: 4/8/12/16/24/32/48/64/96/128px — Midnight Editorial leans on the larger end of this scale generously ("generous whitespace" per brief).
- Content max-width `1280px` for landing-style sections, `760px` for reading-width content (module text, quiz questions) so long-form text doesn't stretch full-width on a dark background.
- Radius: generous here (`8px`–`24px`+ on large cards, full-round on nav pills/avatars/icon buttons) — opposite of the previous system's ≤2px rule. This system is soft/rounded, not hairline/sharp.
- No 1px-everywhere rule from the prior system — borders are subtle (`rgba(255,255,255,0.12)` dark / `rgba(28,28,28,0.12)` light) and shadows are allowed sparingly for the glass-nav effect (`backdrop-filter: blur`), but avoid drop-shadow-heavy card elevation — depth comes from the blur/glass surfaces and contrast, not stacked shadows on every card.

## Component patterns

### Navigation
- **Top nav**: fixed, full-width, transparent-over-hero initially acceptable, but must remain usable (sufficient contrast) once content scrolls beneath it — prefer the glass treatment (`--glass-bg` + blur) at all times for reliability rather than a "transparent until scroll" trick, since that trick risks failing the "no text a user must read below 4.5:1" rule against varying background content.
- **Mode toggle**: lives in the header, a simple two-state icon control (sun/moon), minimum 44px touch target, clear focus ring, NOT hover-only — it's a real button with a visible static affordance, and its current state (which mode is active) must be conveyed by the icon+label, not implied only by the page having already changed color.
- Nav items: full static visible state (not hover-reveal) — label text at rest, coral or bold-white indicates the active route.

### Buttons
- **Primary**: solid `--color-accent` fill, `--color-accent-fg` text, bold uppercase label at small tracking OR sentence-case bold depending on context (short verbs like "SUBMIT" uppercase-tracked; longer labels like "Download certificate" sentence-case bold) — pick one per button, stay consistent within a button.
- **Secondary**: outline (`1px solid --color-border`) on `--color-surface` or transparent, `--color-fg` text; on hover (desktop-only enhancement) may lighten/invert, but the resting state must already be a fully legible, clearly-clickable button — hover is a polish, never the only affordance.
- **Disabled**: reduced opacity (`0.4`) + `cursor: not-allowed`, never relies on hover or color shift to communicate disabled-ness.
- Minimum 44px touch target on all interactive elements.

### Cards / panels
- `background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 16px–24px; padding: var(--space-8) or more;` Optional subtle glass/blur variant for floating elements (nav, modals) only — content cards stay solid-surface for reading legibility.

### Progress bar
- Track: `height: 6px–8px; background: var(--color-surface-raised); border-radius: 999px (full pill);` Fill: `background: var(--color-accent);` The numeric percent is always printed as text beside/above the bar (bold, tabular), never conveyed by width alone. Optional scan-line/shimmer animation on the fill is a decorative flourish only, respects `prefers-reduced-motion`, and is never load-bearing for reading the percent.

### Status badges
- Pill-shaped (`border-radius: 999px`), glyph (✓/✕) + bold uppercase text + a tinted background (accent/success/warning at low opacity, e.g. `rgba(74,222,128,0.15)` for success in dark mode) with full-opacity text/glyph on top — never color-alone, always legible against both the badge background and the page background.

### Custom cursor (decorative, desktop-only — implementation spec, not a static-mockup element)

This is a JS/CSS behavior to build in the follow-up React implementation step, not something a static HTML design draft can meaningfully show — document the spec here so the implementation matches this design pass's intent:

- A single `<div>`, 32px diameter circle, `position: fixed; pointer-events: none; z-index: 9999; background-color: white; mix-blend-mode: difference;`
- Position updates via `requestAnimationFrame` with linear interpolation (lerp) toward the real cursor position — a lagging-follow feel, never 1:1 with the OS cursor.
- On hovering any `<a>` or `<button>`: CSS `transition: transform 0.2s; transform: scale(2.5);`
- Gate activation on `window.matchMedia('(pointer: fine)').matches` — on any touch/coarse-pointer device, the component must not mount at all (no listeners attached, no DOM node rendered), not merely be hidden via CSS.
- `pointer-events: none` on the cursor div guarantees it never blocks real clicks/taps — confirm this holds in implementation testing, don't just assert it.
- Purely decorative: removing it must not remove or degrade any functionality.

## Motion

- Generous, confident transitions (200–500ms ease) on hover states, card reveals, and the scroll-reveal hero text — but per the accessibility brief, **scroll-reveal and any scan-line/shimmer effects are decorative flourishes only**: content must already exist in the DOM and be readable with `prefers-reduced-motion: reduce` disabling the animation, never gating access to information.
- No hover-only *functional* interactions anywhere — hover MAY add polish (color shift, scale, underline) but every interactive element already has a fully legible, fully clickable/tappable resting state, since many learners will be on touch devices.

## Accessibility requirements (non-negotiable, per brief — apply independently to BOTH modes)

1. No text a user must read uses a token below 4.5:1 contrast against its actual background in that mode. This explicitly REJECTS the reference implementation's `#666666`, `#444444`, `#888888` grays wherever they'd sit on `#050505`/`#111111` for real body/label text — those exact values are demoted to `--color-fg-decorative` (pure decoration, e.g. a divider or a muted background numeral) and replaced by `--color-fg-muted` (`#a3a3a3` dark / `#4a4a46` light) for any text a user actually reads.
2. No functional interaction depends on `:hover` alone — every button/link/toggle has a static, fully visible, fully operable resting state; touch devices get full parity.
3. Status (pass/fail/valid/invalid/verified) is always glyph+text, never color-only, in both modes.
4. The custom cursor and any scroll/scan-line motion are decorative-only, gated behind `prefers-reduced-motion`/`(pointer: fine)` as specified above, and never required to use or understand the page.
5. The mode toggle itself must be keyboard-operable and announce its current/target state (e.g. `aria-pressed` or equivalent), not rely on icon color alone to convey which mode is active.

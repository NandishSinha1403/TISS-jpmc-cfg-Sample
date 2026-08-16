const TONE_CLASS = {
  success: "badge-success",
  warning: "badge-warning",
  neutral: "badge-neutral",
};

const GLYPH = {
  success: "✓",
  warning: "✕",
  neutral: null,
};

export default function StatusBadge({ tone = "neutral", children }) {
  return (
    <span className={`badge ${TONE_CLASS[tone]}`}>
      {GLYPH[tone] && <span aria-hidden="true">{GLYPH[tone]}</span>}
      {children}
    </span>
  );
}

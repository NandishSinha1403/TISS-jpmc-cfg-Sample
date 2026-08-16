export default function ProgressBar({ percent, label }) {
  const clamped = Math.max(0, Math.min(100, percent));
  return (
    <div className="progress-row">
      <div className="progress-track" style={{ flex: 1 }} role="progressbar" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
        <div className="progress-fill" style={{ width: `${clamped}%` }} />
      </div>
      <span className="progress-percent">{clamped.toFixed(0)}%</span>
    </div>
  );
}

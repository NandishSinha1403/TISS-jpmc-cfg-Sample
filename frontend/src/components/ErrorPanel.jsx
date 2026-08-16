const FRIENDLY_MESSAGES = [
  { match: /failed to fetch|network/i, message: "Can't reach the server. Check your connection and try again." },
  { match: /incorrect email or password/i, message: "That email or password isn't right. Double-check and try again." },
  { match: /already exists/i, message: "An account with that email already exists." },
  { match: /not found/i, message: "That couldn't be found — it may have been removed." },
];

function friendlyMessage(raw) {
  const hit = FRIENDLY_MESSAGES.find((entry) => entry.match.test(raw || ""));
  return hit ? hit.message : raw || "Something went wrong.";
}

export default function ErrorPanel({ message, onRetry }) {
  return (
    <div className="card error-panel" role="alert">
      <p className="error-panel-text">{friendlyMessage(message)}</p>
      {onRetry && (
        <button type="button" className="btn btn-secondary" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

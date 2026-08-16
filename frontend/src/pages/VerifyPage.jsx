import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { verifyCertificate } from "../api/certificates";
import StatusBadge from "../components/StatusBadge";
import ErrorPanel from "../components/ErrorPanel";

export default function VerifyPage() {
  const { certificateId } = useParams();
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  function load() {
    setError("");
    setLoading(true);
    verifyCertificate(certificateId)
      .then(setResult)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(load, [certificateId]);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(result.certificate_id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard access denied — silently no-op, copy is a convenience, not required
    }
  }

  if (loading) return <div className="content content--narrow"><p>Verifying...</p></div>;
  if (error) return <div className="content content--narrow"><ErrorPanel message={error} onRetry={load} /></div>;

  if (!result.valid) {
    return (
      <div className="content content--narrow verify-panel">
        <StatusBadge tone="warning">Certificate not found</StatusBadge>
        <p>This certificate ID does not match any issued certificate.</p>
      </div>
    );
  }

  return (
    <div className="content content--narrow verify-panel">
      <StatusBadge tone="success">Certificate verified</StatusBadge>
      <h1>{result.learner_name}</h1>
      <div className="card verify-record">
        <div className="verify-record-row">
          <span className="eyebrow">Course</span>
          <span>{result.course_title}</span>
        </div>
        <div className="verify-record-row">
          <span className="eyebrow">Issued</span>
          <span>{new Date(result.issued_at).toLocaleDateString()}</span>
        </div>
        <div className="verify-record-row">
          <span className="eyebrow">Certificate ID</span>
          <span className="verify-id-row">
            <span className="mono-id">{result.certificate_id}</span>
            <button type="button" className="btn btn-secondary copy-btn" onClick={handleCopy}>
              {copied ? "Copied" : "Copy"}
            </button>
          </span>
        </div>
      </div>
    </div>
  );
}

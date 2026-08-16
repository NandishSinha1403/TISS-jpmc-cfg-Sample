import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { verifyCertificate } from "../api/certificates";

export default function VerifyPage() {
  const { certificateId } = useParams();
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    verifyCertificate(certificateId)
      .then(setResult)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [certificateId]);

  if (loading) return <p>Verifying...</p>;
  if (error) return <p role="alert">{error}</p>;

  if (!result.valid) {
    return (
      <section id="center">
        <h1>Certificate not found</h1>
        <p>This certificate ID does not match any issued certificate.</p>
      </section>
    );
  }

  return (
    <section id="center">
      <h1>Certificate verified</h1>
      <p><strong>Learner:</strong> {result.learner_name}</p>
      <p><strong>Course:</strong> {result.course_title}</p>
      <p><strong>Issued:</strong> {new Date(result.issued_at).toLocaleDateString()}</p>
      <p><strong>Certificate ID:</strong> {result.certificate_id}</p>
    </section>
  );
}

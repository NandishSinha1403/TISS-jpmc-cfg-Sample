import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login({ email, password });
      navigate("/");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="content content--narrow auth-shell">
      <div className="card auth-card">
        <h1>Log in</h1>
        <form onSubmit={handleSubmit} className="field-list">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? "Logging in..." : "Log in"}
          </button>
        </form>
        {error && <p role="alert" className="form-error">{error}</p>}
        <p className="auth-switch">
          No account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

// ============================================================================
// File: frontend/src/pages/RegisterPage.jsx
// Role: Account creation form (username/email/password). Routed at
//       "/register".
// ============================================================================

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx";
import PasswordField from "../components/PasswordField.jsx";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password1: "", password2: "" });
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    if (form.password1 !== form.password2) {
      setError("Passwords don't match.");
      return;
    }

    setIsSubmitting(true);
    try {
      await register(form);
      navigate("/");
    } catch {
      setError("We couldn't create that account. Please check your details and try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="chat-scroll">
      <div className="chat-column" style={{ maxWidth: 380, paddingTop: 40 }}>
        <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 500 }}>Create your account</h1>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange} required style={inputStyle} />
          <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={inputStyle} />
          <PasswordField name="password1" placeholder="Password" value={form.password1} onChange={handleChange} />
          <PasswordField name="password2" placeholder="Confirm password" value={form.password2} onChange={handleChange} />

          {error && <div className="meta-mono" style={{ color: "var(--crisis)" }}>{error}</div>}

          <button type="submit" className="composer-send-btn" style={buttonStyle} disabled={isSubmitting}>
            {isSubmitting ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="meta-mono" style={{ marginTop: 16 }}>
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  );
}

const inputStyle = {
  padding: "10px 14px",
  borderRadius: "var(--radius-sm)",
  border: "1px solid var(--mist)",
  fontSize: "0.95rem",
  background: "var(--surface)",
};

const buttonStyle = {
  padding: "10px 14px",
  borderRadius: "var(--radius-sm)",
  border: "none",
  fontWeight: 600,
};
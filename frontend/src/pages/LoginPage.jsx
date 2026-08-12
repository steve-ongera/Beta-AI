// ============================================================================
// File: frontend/src/pages/LoginPage.jsx
// Role: Username/password login form + Google OAuth entry point.
//       Routed at "/login".
// ============================================================================

import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx";
import GoogleLoginButton from "../components/GoogleLoginButton.jsx";
import PasswordField from "../components/PasswordField.jsx";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(form);
      navigate("/");
    } catch {
      setError("That username or password didn't work. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="chat-scroll">
      <div className="chat-column" style={{ maxWidth: 380, paddingTop: 40 }}>
        <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 500 }}>Welcome back</h1>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <input
            name="username"
            placeholder="Username or email"
            value={form.username}
            onChange={handleChange}
            required
            style={inputStyle}
          />
          <PasswordField
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
          />

          {error && <div className="meta-mono" style={{ color: "var(--crisis)" }}>{error}</div>}

          <button type="submit" className="composer-send-btn" style={buttonStyle} disabled={isSubmitting}>
            {isSubmitting ? "Logging in…" : "Log in"}
          </button>
        </form>

        <div style={{ marginTop: 10 }}>
          <GoogleLoginButton />
        </div>

        <p className="meta-mono" style={{ marginTop: 16 }}>
          New here? <Link to="/register">Create an account</Link>
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
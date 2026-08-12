// ============================================================================
// File: frontend/src/components/PasswordField.jsx
// Role: Password <input> with a show/hide eye-icon toggle. Used by
//       LoginPage.jsx and RegisterPage.jsx so the behavior only lives once.
// ============================================================================

import React, { useState } from "react";

export default function PasswordField({ name, placeholder, value, onChange, required = true }) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div style={{ position: "relative" }}>
      <input
        name={name}
        type={isVisible ? "text" : "password"}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        style={{
          padding: "10px 42px 10px 14px",
          borderRadius: "var(--radius-sm)",
          border: "1px solid var(--mist)",
          fontSize: "0.95rem",
          background: "var(--surface)",
          width: "100%",
        }}
      />
      <button
        type="button"
        onClick={() => setIsVisible((v) => !v)}
        aria-label={isVisible ? "Hide password" : "Show password"}
        aria-pressed={isVisible}
        style={{
          position: "absolute",
          right: 4,
          top: "50%",
          transform: "translateY(-50%)",
          background: "none",
          border: "none",
          width: 34,
          height: 34,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          borderRadius: "50%",
          color: "var(--slate-muted)",
        }}
      >
        <i className={`bi ${isVisible ? "bi-eye-slash" : "bi-eye"}`} aria-hidden="true" />
      </button>
    </div>
  );
}
// ============================================================================
// File: frontend/src/pages/SettingsPage.jsx
// Role: Account info + preferences (theme toggle). Auth-only — wrapped in
//       <ProtectedRoute> in App.jsx. Calls authApi.updatePreferences (new
//       PATCH /api/auth/user/ endpoint on the users app).
// ============================================================================

import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth.jsx";
import { authApi } from "../services/api.js";

export default function SettingsPage() {
  const { user } = useAuth();
  const [theme, setTheme] = useState(user?.preferences?.theme || "light");
  const [isSaving, setIsSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleThemeChange = async (nextTheme) => {
    setTheme(nextTheme);
    setIsSaving(true);
    setSaved(false);
    try {
      await authApi.updatePreferences({ theme: nextTheme });
      setSaved(true);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="chat-scroll">
      <div className="chat-column" style={{ maxWidth: 480, paddingTop: 40 }}>
        <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 500 }}>Settings</h1>

        <section style={{ marginTop: 20 }}>
          <div className="history-label" style={{ color: "var(--slate-muted)" }}>Account</div>
          <p>{user?.username}</p>
          <p className="meta-mono">{user?.email}</p>
        </section>

        <section style={{ marginTop: 20 }}>
          <div className="history-label" style={{ color: "var(--slate-muted)" }}>Appearance</div>
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            {["light", "dark"].map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => handleThemeChange(option)}
                style={{
                  padding: "8px 16px",
                  borderRadius: "var(--radius-sm)",
                  border: theme === option ? "1px solid var(--moss)" : "1px solid var(--mist)",
                  background: theme === option ? "var(--moss)" : "var(--surface)",
                  color: theme === option ? "#fff" : "var(--slate)",
                  textTransform: "capitalize",
                }}
              >
                {option}
              </button>
            ))}
          </div>
          {isSaving && <div className="meta-mono" style={{ marginTop: 8 }}>Saving…</div>}
          {saved && !isSaving && <div className="meta-mono" style={{ marginTop: 8 }}>Saved.</div>}
        </section>
      </div>
    </div>
  );
}
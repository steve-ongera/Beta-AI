// ============================================================================
// File: frontend/src/components/ModuleSwitcher.jsx
// Role: Sidenav-header dropdown listing active AI-app modules (today: just
//       Mental Health). Scaffolding so adding a 2nd module later needs no
//       UI rework — it just appears here once registered via seed data.
// ============================================================================

import React, { useState } from "react";
import { useModules } from "../hooks/useModules.js";

export default function ModuleSwitcher() {
  const { modules, isLoading } = useModules();
  const [isOpen, setIsOpen] = useState(false);

  if (isLoading || modules.length <= 1) {
    // Nothing to switch between yet — stay out of the way.
    return <span className="brand-mark">Beta AI</span>;
  }

  return (
    <div style={{ position: "relative" }}>
      <button
        type="button"
        className="brand-mark"
        style={{ background: "none", border: "none", color: "inherit", display: "flex", alignItems: "center", gap: 6 }}
        onClick={() => setIsOpen((open) => !open)}
      >
        Beta AI
        <i className="bi bi-chevron-down" style={{ fontSize: "0.7rem" }} aria-hidden="true" />
      </button>

      {isOpen && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            marginTop: 6,
            background: "var(--surface)",
            color: "var(--ink)",
            borderRadius: "var(--radius-sm)",
            boxShadow: "var(--shadow-lifted)",
            minWidth: 200,
            zIndex: 10,
            overflow: "hidden",
          }}
        >
          {modules.map((mod) => (
            <div key={mod.slug} className="history-item" style={{ color: "var(--ink)" }}>
              <i className={`bi ${mod.icon || "bi-app"}`} style={{ marginRight: 8 }} aria-hidden="true" />
              {mod.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
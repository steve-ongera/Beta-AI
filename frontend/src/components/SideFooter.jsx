// ============================================================================
// File: frontend/src/components/SideFooter.jsx
// Role: Bottom-of-sidenav account area — login link for guests, avatar +
//       logout for authenticated users. Rendered inside App.jsx.
// ============================================================================

import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export default function SideFooter({ user, isAuthenticated }) {
  const { logout } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="sidefooter">
        <Link to="/login" className="new-chat-btn" style={{ marginBottom: 0 }}>
          <i className="bi bi-box-arrow-in-right" aria-hidden="true" />
          Log in
        </Link>
      </div>
    );
  }

  const initial = (user?.username || user?.email || "?").charAt(0).toUpperCase();

  return (
    <div className="sidefooter">
      <span className="avatar-circle">{initial}</span>
      <div style={{ flex: 1, overflow: "hidden" }}>
        <div style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {user?.username || user?.email}
        </div>
      </div>
      <Link to="/settings" aria-label="Settings" className="composer-icon-btn" style={{ color: "inherit" }}>
        <i className="bi bi-gear" aria-hidden="true" />
      </Link>
      <button
        type="button"
        onClick={logout}
        aria-label="Log out"
        className="composer-icon-btn"
        style={{ color: "inherit" }}
      >
        <i className="bi bi-box-arrow-right" aria-hidden="true" />
      </button>
    </div>
  );
}
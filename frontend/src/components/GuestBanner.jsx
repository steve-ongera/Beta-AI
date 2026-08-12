// ============================================================================
// File: frontend/src/components/GuestBanner.jsx
// Role: Top-of-main-panel notice shown to logged-out users, prompting login
//       for full-accuracy responses. Rendered inside App.jsx.
// ============================================================================

import React from "react";
import { Link } from "react-router-dom";

export default function GuestBanner() {
  return (
    <div className="guest-banner">
      <span>
        <i className="bi bi-info-circle" aria-hidden="true" style={{ marginRight: 6 }} />
        You're browsing as a guest — responses are general guidance only.
      </span>
      <Link to="/login" className="btn-link">
        Log in for personalized responses
      </Link>
    </div>
  );
}
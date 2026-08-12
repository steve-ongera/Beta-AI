// ============================================================================
// File: frontend/src/pages/NotFoundPage.jsx
// Role: Catch-all route (*) for unmatched URLs.
// ============================================================================

import React from "react";
import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="session-empty-state" style={{ margin: "auto" }}>
      <h1>Page not found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <Link to="/">Back to your conversation</Link>
    </div>
  );
}
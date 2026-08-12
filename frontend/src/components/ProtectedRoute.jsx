// ============================================================================
// File: frontend/src/components/ProtectedRoute.jsx
// Role: Redirects to /login if not authenticated; used to guard routes like
//       /settings. Waits for useAuth's initial load before deciding.
// ============================================================================

import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.jsx";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div className="meta-mono" style={{ padding: 20 }}>Loading…</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
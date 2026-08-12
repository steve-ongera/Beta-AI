// ============================================================================
// File: frontend/src/App.jsx
// Role: Top-level app shell — sidenav + off-canvas toggle, guest banner,
//       and the route table (chat / login / register).
// ============================================================================

import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";

import SideNav from "./components/SideNav.jsx";
import SideFooter from "./components/SideFooter.jsx";
import GuestBanner from "./components/GuestBanner.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import RegisterPage from "./pages/RegisterPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";
import { useAuth } from "./hooks/useAuth.js";

export default function App() {
  const { user, isAuthenticated } = useAuth();
  const [isNavOpen, setIsNavOpen] = useState(false);

  const closeNav = () => setIsNavOpen(false);
  const toggleNav = () => setIsNavOpen((open) => !open);

  return (
    <div className={`app-shell ${isNavOpen ? "nav-open" : ""}`}>
      <button
        type="button"
        className="nav-toggle"
        aria-label={isNavOpen ? "Close menu" : "Open menu"}
        aria-expanded={isNavOpen}
        onClick={toggleNav}
      >
        <i className={`bi ${isNavOpen ? "bi-x-lg" : "bi-list"}`} aria-hidden="true" />
      </button>

      {isNavOpen && <div className="nav-scrim" onClick={closeNav} />}

      <aside className={`sidenav ${isNavOpen ? "is-open" : ""}`}>
        <SideNav isAuthenticated={isAuthenticated} onNavigate={closeNav} />
        <SideFooter user={user} isAuthenticated={isAuthenticated} />
      </aside>

      <main className="main-panel">
        {!isAuthenticated && <GuestBanner />}
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/c/:sessionId" element={<ChatPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
    </div>
  );
}
// ============================================================================
// File: frontend/src/components/SideNav.jsx
// Role: Collapsible side navigation — brand mark, "New conversation", and
//       the chat history list (auth users only). Rendered inside App.jsx.
// ============================================================================

import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useChatHistory } from "../hooks/useChat.js";

export default function SideNav({ isAuthenticated, onNavigate }) {
  const navigate = useNavigate();
  const { sessions, isLoading } = useChatHistory();

  const handleNewChat = () => {
    navigate("/");
    onNavigate?.();
  };

  return (
    <div>
      <div className="sidenav-header">
        <span className="brand-mark">MindBridge</span>
      </div>

      <button type="button" className="new-chat-btn" onClick={handleNewChat}>
        <i className="bi bi-plus-lg" aria-hidden="true" />
        New conversation
      </button>

      {isAuthenticated ? (
        <>
          <div className="history-label">Recent</div>
          {isLoading && <div className="meta-mono" style={{ padding: "8px 10px" }}>Loading…</div>}
          {!isLoading && sessions.length === 0 && (
            <div className="meta-mono" style={{ padding: "8px 10px" }}>No conversations yet</div>
          )}
          {sessions.map((session) => (
            <Link
              key={session.id}
              to={`/c/${session.id}`}
              className="history-item"
              onClick={onNavigate}
              title={session.title}
            >
              {session.title || "New conversation"}
            </Link>
          ))}
        </>
      ) : (
        <div className="meta-mono" style={{ padding: "8px 10px", lineHeight: 1.5 }}>
          Log in to save your conversation history across visits.
        </div>
      )}
    </div>
  );
}
// ============================================================================
// File: frontend/src/pages/ChatPage.jsx
// Role: Main chat screen — message list (with crisis-flag styling) and the
//       composer (text + image attach). Routed at "/" and "/c/:sessionId".
// ============================================================================

import React, { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { useChat } from "../hooks/useChat.js";

const CRISIS_STATIC_RESOURCES = [
  { name: "988 Suicide & Crisis Lifeline (US)", contact: "Call or text 988" },
];

export default function ChatPage() {
  const { sessionId } = useParams();
  const { messages, isSending, crisisAlert, error, sendMessage } = useChat(sessionId);
  const [draft, setDraft] = useState("");
  const [pendingImage, setPendingImage] = useState(null);
  const scrollRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isSending]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!draft.trim() && !pendingImage) return;
    sendMessage({ content: draft.trim(), image: pendingImage });
    setDraft("");
    setPendingImage(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit(event);
    }
  };

  return (
    <>
      <div className="chat-scroll" ref={scrollRef}>
        <div className="chat-column">
          {messages.length === 0 && (
            <div className="session-empty-state">
              <h1>What's on your mind today?</h1>
              <p>This space is here to listen. Nothing you share here is a substitute for care from a licensed professional.</p>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id} className={`message-row role-${message.role}`}>
              <div className={`message-bubble ${message.risk_flag === "high_risk" ? "risk-high" : ""}`}>
                <p style={{ margin: 0, whiteSpace: "pre-wrap" }}>{message.content}</p>
                {message.risk_flag === "high_risk" && (
                  <div className="crisis-resources">
                    {CRISIS_STATIC_RESOURCES.map((r) => (
                      <div key={r.name}>
                        <strong>{r.name}</strong> — {r.contact}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isSending && (
            <div className="message-row role-assistant">
              <div className="message-bubble" style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className="breathing-dot" />
                <span className="meta-mono">thinking</span>
              </div>
            </div>
          )}

          {error && (
            <div className="message-bubble risk-high" style={{ alignSelf: "center" }}>
              {error}
            </div>
          )}
        </div>
      </div>

      <form className="composer" onSubmit={handleSubmit}>
        <div className="composer-inner">
          <button
            type="button"
            className="composer-icon-btn"
            aria-label="Attach an image"
            onClick={() => fileInputRef.current?.click()}
          >
            <i className="bi bi-image" aria-hidden="true" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            hidden
            onChange={(e) => setPendingImage(e.target.files?.[0] || null)}
          />

          <textarea
            rows={1}
            placeholder="Share what's on your mind…"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={handleKeyDown}
          />

          <button
            type="submit"
            className="composer-icon-btn composer-send-btn"
            aria-label="Send message"
            disabled={isSending || (!draft.trim() && !pendingImage)}
          >
            <i className="bi bi-arrow-up" aria-hidden="true" />
          </button>
        </div>
        {pendingImage && (
          <div className="meta-mono" style={{ maxWidth: 720, margin: "6px auto 0" }}>
            Attached: {pendingImage.name}
          </div>
        )}
      </form>
    </>
  );
}
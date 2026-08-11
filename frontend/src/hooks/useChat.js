// ============================================================================
// File: frontend/src/hooks/useChat.js
// Role: useChatHistory (sidenav session list) + useChat (active session's
//       messages, sending, crisis-alert state). Talks to mentalHealthApi.
// ============================================================================

import { useCallback, useEffect, useState } from "react";
import { mentalHealthApi } from "../services/api.js";
import { useAuth } from "./useAuth.js";

export function useChatHistory() {
  const { isAuthenticated } = useAuth();
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const refresh = useCallback(async () => {
    if (!isAuthenticated) {
      setSessions([]);
      return;
    }
    setIsLoading(true);
    try {
      const data = await mentalHealthApi.listSessions();
      setSessions(data.results || data);
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { sessions, isLoading, refresh };
}

export function useChat(sessionId) {
  const [messages, setMessages] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(sessionId || null);
  const [isSending, setIsSending] = useState(false);
  const [crisisAlert, setCrisisAlert] = useState(null);
  const [error, setError] = useState(null);

  const loadSession = useCallback(async (id) => {
    if (!id) return;
    const data = await mentalHealthApi.getSession(id);
    setMessages(data.messages || []);
    setCurrentSessionId(id);
  }, []);

  useEffect(() => {
    if (sessionId) loadSession(sessionId);
  }, [sessionId, loadSession]);

  const sendMessage = useCallback(
    async ({ content, image }) => {
      setError(null);
      setCrisisAlert(null);

      const optimisticUser = {
        id: `optimistic-${Date.now()}`,
        role: "user",
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, optimisticUser]);
      setIsSending(true);

      try {
        const data = await mentalHealthApi.sendMessage({
          sessionId: currentSessionId,
          content,
          image,
        });

        setCurrentSessionId(data.session_id);
        setMessages((prev) => [
          ...prev.filter((m) => m.id !== optimisticUser.id),
          { ...data.user_message, role: "user" },
          { ...data.assistant_message, role: "assistant" },
        ]);

        if (data.crisis_escalation) {
          setCrisisAlert({
            resources: data.crisis_resources || [],
          });
        }
      } catch (err) {
        setError(err?.response?.data?.detail || "Something went wrong sending that message.");
      } finally {
        setIsSending(false);
      }
    },
    [currentSessionId]
  );

  const startNewSession = useCallback(() => {
    setMessages([]);
    setCurrentSessionId(null);
    setCrisisAlert(null);
  }, []);

  return {
    messages,
    sessionId: currentSessionId,
    isSending,
    crisisAlert,
    error,
    sendMessage,
    startNewSession,
  };
}
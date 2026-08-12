// ============================================================================
// File: frontend/src/components/GoogleLoginButton.jsx
// Role: Loads Google Identity Services and renders the real "Sign in with
//       Google" button, exchanging the returned ID token via useAuth's
//       loginWithGoogle() -> POST /api/auth/google/. Replaces the earlier
//       placeholder alert() button in LoginPage.jsx.
//
// Setup: set VITE_GOOGLE_CLIENT_ID in frontend/.env (matches
//        GOOGLE_OAUTH_CLIENT_ID in the backend's .env).
// ============================================================================

import React, { useEffect, useRef } from "react";
import { useAuth } from "../hooks/useAuth.js";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const GIS_SCRIPT_SRC = "https://accounts.google.com/gsi/client";

function loadGisScript() {
  return new Promise((resolve, reject) => {
    if (window.google?.accounts?.id) return resolve();
    const existing = document.querySelector(`script[src="${GIS_SCRIPT_SRC}"]`);
    if (existing) {
      existing.addEventListener("load", () => resolve());
      return;
    }
    const script = document.createElement("script");
    script.src = GIS_SCRIPT_SRC;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

export default function GoogleLoginButton() {
  const { loginWithGoogle } = useAuth();
  const buttonRef = useRef(null);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID) return;

    let cancelled = false;

    loadGisScript().then(() => {
      if (cancelled || !window.google?.accounts?.id) return;

      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: async (response) => {
          try {
            await loginWithGoogle(response.credential);
            window.location.href = "/";
          } catch {
            // useAuth surfaces errors via its own state; nothing extra needed here.
          }
        },
      });

      if (buttonRef.current) {
        window.google.accounts.id.renderButton(buttonRef.current, {
          theme: "outline",
          size: "large",
          width: 320,
          text: "continue_with",
        });
      }
    });

    return () => {
      cancelled = true;
    };
  }, [loginWithGoogle]);

  if (!GOOGLE_CLIENT_ID) {
    return (
      <div className="meta-mono" style={{ padding: "10px 0" }}>
        Google sign-in isn't configured yet (missing VITE_GOOGLE_CLIENT_ID).
      </div>
    );
  }

  return <div ref={buttonRef} />;
}
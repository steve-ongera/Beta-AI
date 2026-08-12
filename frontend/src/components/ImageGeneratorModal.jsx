// ============================================================================
// File: frontend/src/components/ImageGeneratorModal.jsx
// Role: Auth-only "generate an image" panel — prompt in, generated image
//       out. Calls mediaApi.generateImage (POST /api/media/generate/),
//       which existed on the backend but had no frontend caller until now.
// ============================================================================

import React, { useState } from "react";
import { mediaApi } from "../services/api.js";

export default function ImageGeneratorModal({ onClose }) {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async (event) => {
    event.preventDefault();
    if (!prompt.trim()) return;
    setIsGenerating(true);
    setError(null);
    try {
      const data = await mediaApi.generateImage(prompt.trim());
      setResult(data);
      if (data.status === "failed") {
        setError("Image generation failed — please try a different prompt.");
      }
    } catch {
      setError("Something went wrong generating that image.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="modal-scrim" onClick={onClose}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ fontFamily: "var(--font-display)", fontSize: "1.2rem", fontWeight: 500, margin: 0 }}>
            Generate an image
          </h2>
          <button type="button" className="composer-icon-btn" onClick={onClose} aria-label="Close">
            <i className="bi bi-x-lg" aria-hidden="true" />
          </button>
        </div>

        <form onSubmit={handleGenerate} style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
          <textarea
            rows={3}
            placeholder="Describe the image you'd like…"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            style={{
              padding: 10,
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--mist)",
              fontFamily: "var(--font-body)",
              resize: "vertical",
            }}
          />
          <button type="submit" className="composer-send-btn" style={{ padding: "10px 14px", borderRadius: "var(--radius-sm)", border: "none", fontWeight: 600 }} disabled={isGenerating}>
            {isGenerating ? "Generating…" : "Generate"}
          </button>
        </form>

        {error && <div className="meta-mono" style={{ color: "var(--crisis)", marginTop: 10 }}>{error}</div>}

        {result?.status === "complete" && result.image && (
          <img
            src={result.image}
            alt={prompt}
            style={{ width: "100%", borderRadius: "var(--radius-md)", marginTop: 14 }}
          />
        )}

        {result?.status === "pending" && (
          <div className="meta-mono" style={{ marginTop: 10 }}>
            <span className="breathing-dot" style={{ marginRight: 8 }} />
            Still working on it — this can take a moment.
          </div>
        )}
      </div>
    </div>
  );
}
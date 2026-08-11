// ============================================================================
// File: frontend/vite.config.js
// Role: Vite dev server + build config for the React app.
// ============================================================================

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
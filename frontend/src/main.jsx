// ============================================================================
// File: frontend/src/main.jsx
// Role: React entry point — mounts <App/> (wrapped in Router + AuthProvider)
//       onto #root from index.html.
// ============================================================================

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import { AuthProvider } from "./hooks/useAuth.jsx";
import "./styles/main.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
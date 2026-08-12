// ============================================================================
// File: frontend/src/hooks/useModules.js
// Role: Fetches the active AI-app module registry from the chat app's
//       GET /api/modules/ endpoint. Powers ModuleSwitcher.jsx today and any
//       future multi-module app switcher.
// ============================================================================

import { useEffect, useState } from "react";
import { modulesApi } from "../services/api.js";

export function useModules() {
  const [modules, setModules] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    modulesApi
      .list()
      .then((data) => {
        if (!cancelled) setModules(data.results || data);
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return { modules, isLoading };
}
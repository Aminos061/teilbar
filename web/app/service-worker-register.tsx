"use client";

import { useEffect } from "react";

// Nur im Produktionsbuild: Im Entwicklungsmodus soll kein Service Worker dazwischenfunken.
export default function ServiceWorkerRegister() {
  useEffect(() => {
    if (process.env.NODE_ENV !== "production" || !("serviceWorker" in navigator)) return;
    navigator.serviceWorker
      .register("/sw.js", { scope: "/", updateViaCache: "none" })
      .catch((error) => console.error("Service Worker konnte nicht registriert werden", error));
  }, []);

  return null;
}

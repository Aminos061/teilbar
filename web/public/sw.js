// Service Worker von Teilbar (docs/adr/0007-tech-stack-der-app.md).
// Bewusst ohne fetch-Handler: Es wird nichts zwischengespeichert und nichts umgeleitet.
// Damit kann nie eine Seite eines anderen oder abgemeldeten Nutzers aus dem Cache kommen.
// Offline-Betrieb ist kein Ziel. Wer ihn später ergänzt, darf Antworten mit Anmeldung nicht cachen.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

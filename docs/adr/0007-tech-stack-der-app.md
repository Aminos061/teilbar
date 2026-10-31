# 0007 Tech-Stack der App

Status: angenommen · 2026-10-31

## Kontext

ADR 0003 legt fest, dass `docker compose up` die App startet, und lässt den Stack offen. Der Prototyp (`index.html`, GitHub Pages) hat kein Backend: Hausbuch und Freigabe per QR-Code gibt es nur im Browser. Die App braucht jetzt Konten, gemeinsame Daten und Dateien (Bilder). Vier Personen bauen sie in einem Semester, ohne Budget und ohne eigenen Server. Sie soll sich auf dem Handy wie eine App anfühlen, ohne dass wir Stores bedienen.

## Entscheidung

- **Frontend:** Next.js mit TypeScript und App Router, ESLint. Ordner `web/`. Versionen fest gepinnt (exakte Versionen in `package.json`, Lockfile im Repo).
- **Backend:** Supabase für Datenbank (Postgres), Auth und Storage. Schema nur über Migrationen in `web/supabase/migrations/`.
- **Supabase lokal** zum Entwickeln über die Supabase CLI (`supabase start`, gepinnte Version). Die CLI braucht eine Docker-kompatible Laufzeit, deshalb bekommt der Devcontainer Docker-in-Docker.
- **Supabase in der Cloud** für Vorschau und Deployment: ein Projekt im kostenlosen Tarif. Stand 2026-10-31 sind das 2 aktive Projekte, 500 MB Datenbank, 1 GB Storage, 50 000 aktive Nutzer im Monat; das Projekt wird nach einer Woche ohne Aktivität pausiert.
- **PWA:** Manifest über `app/manifest.ts`, Icons, Service Worker; installierbar ist die App nur über HTTPS. Offline-Fähigkeit ist kein Ziel dieser Entscheidung.
- **Geheimnisse:** Keys liegen nur in `web/.env.local` oder in GitHub-Secrets. Im Repo steht nur `web/.env.example`.
- **Vertrag aus ADR 0003 bleibt:** `docker compose up` startet die App.
- **Der Prototyp bleibt unverändert** auf GitHub Pages, bis die App ihn ersetzt.

## Folgen

- Alle Daten und Dateien liegen bei Supabase. Wir müssen die Datenbank-Zugriffsregeln (Row Level Security) von Anfang an in den Migrationen pflegen, weil Browser-Code direkt auf die Datenbank zugreift.
- Der kostenlose Tarif pausiert das Cloud-Projekt bei Inaktivität. Vor einer Vorführung muss es jemand wecken.
- Lokal läuft neben der App ein Supabase-Stack aus mehreren Containern. Der Erststart des Devcontainers und von `supabase start` dauert länger und braucht Arbeitsspeicher.
- Server Actions und Supabase-Auth brauchen einen laufenden Next.js-Server. Ein statischer Export wie beim Prototyp geht nicht. Wo die App für die Abgabe gehostet wird, ist hier nicht entschieden und braucht ein eigenes ADR.
- Versionswechsel von Next.js, Supabase CLI und Node gehen nur per PR.

## Quellen

- Next.js, PWA-Anleitung (Manifest, HTTPS, Service Worker): https://nextjs.org/docs/app/guides/progressive-web-apps
- Supabase, lokale Entwicklung (Container-Laufzeit nötig): https://supabase.com/docs/guides/local-development
- Supabase, Preise und Grenzen des Free-Tarifs (abgerufen 2026-10-31): https://supabase.com/pricing

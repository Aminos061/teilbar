# 0007 Tech-Stack der App

Status: angenommen · 2026-10-31

## Kontext

ADR 0003 legt fest, dass `docker compose up` die App startet, und lässt den Stack offen. Der Prototyp (`index.html`, GitHub Pages) hat kein Backend: Hausbuch und Freigabe per QR-Code gibt es nur im Browser. Die App braucht jetzt Konten, gemeinsame Daten und Dateien (Bilder). Vier Personen bauen sie in einem Semester, ohne Budget und ohne eigenen Server. Sie soll sich auf dem Handy wie eine App anfühlen, ohne dass wir Stores bedienen.

## Entscheidung

- **Frontend:** Next.js mit TypeScript und App Router, ESLint. Ordner `web/`. Versionen fest gepinnt (exakte Versionen in `package.json`, Lockfile im Repo).
- **Backend:** Supabase für Datenbank (Postgres), Auth und Storage. Schema nur über Migrationen in `web/supabase/migrations/`.
- **Supabase lokal** zum Entwickeln über die Supabase CLI. Die CLI braucht eine Docker-kompatible Laufzeit, deshalb bekommt der Devcontainer Docker-in-Docker (Feature `docker-in-docker:2`, in `devcontainer-lock.json` gepinnt). Die CLI selbst ist als Dev-Abhängigkeit in `web/package.json` exakt gepinnt und wird beim Erstellen des Containers mit `npm ci` installiert. Gestartet wird sie über `npm run db:start`. `analytics` und `edge_runtime` sind in `web/supabase/config.toml` aus, um Arbeitsspeicher zu sparen.
- **Supabase in der Cloud** für Vorschau und Deployment: ein Projekt im kostenlosen Tarif. Stand 2026-10-31 sind das 2 aktive Projekte, 500 MB Datenbank, 1 GB Storage, 50 000 aktive Nutzer im Monat; das Projekt wird nach einer Woche ohne Aktivität pausiert.
- **PWA:** Manifest über `app/manifest.ts`, Icons, Service Worker; installierbar ist die App nur über HTTPS. Offline-Fähigkeit ist kein Ziel dieser Entscheidung.
- **Geheimnisse:** Keys liegen nur in `web/.env.local` oder in GitHub-Secrets. Im Repo steht nur `web/.env.example`.
- **Cloud-Regeln:** Alle teilen sich dieses eine Cloud-Projekt, Vorschau-Datenbanken je PR gibt es nicht. Migrationen laufen deshalb nur nach dem Merge auf `main` gegen die Cloud; in PRs wird gegen die lokale Supabase getestet. Region ist die EU. Für Tests in der Cloud gibt es keine echten personenbezogenen Daten.
- **Vertrag aus ADR 0003 bleibt:** `docker compose up` startet die App (`web`). Die Supabase CLI startet ihre eigenen Container und steht nicht in der Compose-Datei. Für die lokale Datenbank gehört deshalb `supabase start` davor. Der `web`-Dienst läuft mit `network_mode: host` und erreicht sie so unter `http://127.0.0.1:54321`, derselben Adresse wie der Browser. Das gilt im Devcontainer (Linux); auf einem Host unter Windows oder macOS wäre ein anderer Weg nötig. `README.md` beschreibt beide Schritte.
- **Der Prototyp bleibt unverändert** auf GitHub Pages, bis die App ihn ersetzt.

## Folgen

- Alle Daten und Dateien liegen bei Supabase. Wir müssen die Datenbank-Zugriffsregeln (Row Level Security) von Anfang an in den Migrationen pflegen, weil Browser-Code direkt auf die Datenbank zugreift.
- Der kostenlose Tarif pausiert das Cloud-Projekt bei Inaktivität. Vor einer Vorführung muss es jemand wecken.
- Das gemeinsame Cloud-Projekt ist eine Engstelle: Wer Migrationen einspielt, ändert die Datenbank für alle. Das Einspielen nach dem Merge ist deshalb Teil des Ablaufs im PR-Review.
- Die Hausbuch-Daten betreffen Mitbewohner. Die EU-Region senkt das Risiko, ersetzt aber keine Prüfung des Datenschutzes, bevor echte Nutzer die App verwenden.
- Lokal läuft neben der App ein Supabase-Stack aus mehreren Containern. Der Erststart des Devcontainers und von `supabase start` dauert länger und braucht Arbeitsspeicher (Richtwert: 8 GB für Docker). Docker-in-Docker läuft privilegiert und legt die Images in einem eigenen Volume ab.
- Zwei Orte pinnen Versionen: `.devcontainer/` für die Umgebung, `web/package.json` samt Lockfile für alles, was die App braucht, einschließlich der Supabase CLI.
- Server Actions und Supabase-Auth brauchen einen laufenden Next.js-Server. Ein statischer Export wie beim Prototyp geht nicht. Wo die App für die Abgabe gehostet wird, ist hier nicht entschieden und braucht ein eigenes ADR.
- Versionswechsel von Next.js, Supabase CLI und Node gehen nur per PR.

## Quellen

- Next.js, PWA-Anleitung (Manifest, HTTPS, Service Worker): https://nextjs.org/docs/app/guides/progressive-web-apps
- Supabase, lokale Entwicklung (Container-Laufzeit nötig): https://supabase.com/docs/guides/local-development
- Supabase, Preise und Grenzen des Free-Tarifs (abgerufen 2026-10-31): https://supabase.com/pricing

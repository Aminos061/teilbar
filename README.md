# Teilbar · Prototyp

**Nachbarn statt Fremde.** Teilbar ist eine Nachbarschafts-App nach dem Allmende-Prinzip: Nachbarn passen kostenlos auf Tiere und Wohnungen auf, wenn jemand nicht da ist (Tiersitting und Housesitting). Statt Bezahlung gibt es ein Kennenlern-Treffen, Vertrauensstufen und Empfehlungen.

Dieses Repository enthält einen klickbaren Prototyp als statische Webseite. Er zeigt den Ablauf eines Sittings aus Sicht der Personas Sarah, Lena, Karl und Jonas, mit Demo-Daten aus einem fiktiven Haus in der Lindenstraße. Dazu kommt das **Hausbuch**: Suchende halten Aufgaben, Hinweise mit Fotos, Notfallkontakte und Hausregeln einmal fest und nutzen sie in jeder Anfrage. Per QR-Code teilen sie es mit Personen, die sie schon kennen; diese kommen als **Gast** ohne Konto in die App (im Prototyp: Sarahs Bruder David).

## Prototyp starten

Der Prototyp braucht **keine Installation, keinen Build und keine Internetverbindung**. Alle Dateien (HTML, Schriften, Bilder) liegen im Repository. Läuft in jedem aktuellen Browser (Chrome, Firefox, Safari).

### 1. Dateien holen

Entweder mit Git:

```bash
git clone https://github.com/Aminos061/teilbar.git
cd teilbar
```

Oder ohne Git: Auf GitHub auf **Code → Download ZIP** klicken und die ZIP-Datei entpacken.

### 2a. Einfachster Weg: Datei im Browser öffnen

Die Datei `index.html` im Ordner `teilbar` im Browser öffnen, zum Beispiel per Doppelklick oder im Terminal:

| System | Befehl im Ordner `teilbar` |
| --- | --- |
| macOS | `open index.html` |
| Linux | `xdg-open index.html` |

### 2b. Alternative: lokaler Webserver

Falls der Browser lokale Dateien blockiert, im Ordner `teilbar` einen kleinen Webserver starten. Python 3 ist auf den meisten Linux-Systemen vorinstalliert, auf macOS ist es mit den Xcode Command Line Tools dabei (`xcode-select --install`).

```bash
python3 -m http.server 8000
```

Dann im Browser **http://localhost:8000** öffnen. Beenden mit `Strg+C` (macOS: `ctrl+C`).

### Online-Version

Der Prototyp ist zusätzlich über GitHub Pages erreichbar: https://aminos061.github.io/teilbar/

## Bedienung

Links neben dem Handy steht die Demo-Steuerung, rechts das Handy mit der App.

- **Abläufe:** Links stehen fünf Abläufe mit ihren Schritten. Ein Klick auf einen Schritt springt direkt dorthin und wechselt zur passenden Person.
  - **Hausbuch anlegen** (3 Schritte): Sarah übernimmt Vorschläge für Katze und Wohnung, schreibt einen Hinweis mit Foto (wo das Futter steht) und ergänzt eine eigene Aufgabe.
  - **Sitting im Haus** (9 Schritte): Sarah stellt eine Anfrage für Katze Minka und Pflanzen und wählt die Aufgaben aus ihrem Hausbuch, Lena aus dem 4. OG tippt „Kann ich übernehmen“, beide schreiben im Chat, treffen sich, füllen die Sitting-Vereinbarung aus (aus dem Hausbuch vorausgefüllt), übergeben den Schlüssel, Lena erledigt die Aufgaben (mit „Wie?“ zu jeder Aufgabe), Sarah sieht im Urlaub den Status, am Ende empfehlen sich beide.
  - **Gassi in der Straße** (3 Schritte): Im Haus hat niemand Zeit, Jonas erweitert seine Anfrage auf die Straße, Karl übernimmt und bekommt die Hinweise aus Jonas' Hausbuch.
  - **Hausbuch teilen** (4 Schritte): Sarah erstellt einen QR-Code mit PIN für ihren Bruder David, David öffnet ihn als Gast ohne Konto und hakt ab, Sarah sieht, wer da war, und widerruft die Freigabe.
  - **Anmelden (Karl)** (4 Schritte): Registrierung mit Name, Adresse und Brief-Code. Der Demo-Code ist `1234`.
- **Tastatur:** `→` und `←` (oder ein Presenter-Klicker) gehen zum nächsten oder vorherigen Schritt. `B` schaltet den Beamer-Modus mit großer Schrift ein und aus.
- **Vorspulen:** springt im laufenden Sitting einige Tage weiter.
- **Neustart:** setzt alle Demo-Daten zurück.
- **Ansicht:** Mit den runden Bildern unten links wechselt man die Person (Sarah, Lena, Karl, Jonas, David als Gast).
- **Gast-Ansicht direkt:** `index.html?gast` öffnet die App so, wie David sie nach dem Scannen des QR-Codes sieht. Der QR-Code im Prototyp (`img/freigabe-qr.svg`) führt auf https://aminos061.github.io/teilbar/?gast.
- Auf dem Handy (Bildschirmbreite unter 500 px) erscheint die Steuerung als Leiste über und unter der App.

### Einzelne Bildschirme direkt öffnen

Für Screenshots lässt sich jeder wichtige Bildschirm direkt aufrufen, zum Beispiel `index.html?shot=vereinbarung`. Mit dem Zusatz `&bare` wird nur der Handy-Bildschirm ohne Steuerung gezeigt (`index.html?shot=vereinbarung&bare`).

Verfügbare Namen: `start`, `anfrage`, `detail`, `angebot`, `chat`, `vereinbarung`, `sitting`, `status`, `notfall`, `abschluss`, `erweitern`, `karl`, `nachbarn`, `profil`, `ob0`, `ob2`, `ob3`, `hbneu`, `hbhint`, `hausbuch`, `wie`, `freigabe`, `gast`, `gastliste`.

## Was simuliert ist

Der Prototyp hat kein Backend. Alle Daten sind fest eingebaut und werden beim Neuladen zurückgesetzt.

- Die Adress-Verifizierung per Brief ist simuliert (Code `1234`).
- Foto-Updates vom Tier sind ein festes Beispielbild, Fotos im Hausbuch ebenso oder ein Platzhalter.
- Hinweise und neue Aufgaben im Hausbuch kommen aus vorbereiteten Beispielen; Art, Zuordnung und Rhythmus lassen sich wählen.
- Die Freigabe (QR-Code, PIN `2580`, Widerrufen) läuft nur im Browser; der Gast-Link zeigt immer dieselbe Demo-Freigabe.
- Chat-Nachrichten, die man selbst eintippt, erscheinen nur lokal im Browser.
- Nicht enthalten sind laut Briefing: Bezahlung, Punkte, Foodsharing, Geräte-Verleih und KI im Produkt.

## Aufbau des Repositorys

| Pfad | Inhalt |
| --- | --- |
| `index.html` | gesamter Prototyp (HTML, CSS und JavaScript in einer Datei) |
| `img/` | Porträts der Personas, Foto von Katze Minka und QR-Code der Demo-Freigabe |
| `fonts/` | Schrift Inter (lokal eingebunden, damit der Prototyp offline läuft) |
| `.nojekyll` | sorgt dafür, dass GitHub Pages die Dateien unverändert ausliefert |

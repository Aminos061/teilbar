# Glossar

Agenten und Menschen verwenden diese Begriffe genau so. Unter _Avoid_ stehen Wörter, die wir dafür nicht benutzen.

## App

Folgt, sobald die Codebase angelegt ist. Bis dahin gelten die Begriffe aus dem Prototyp (`index.html`).

## KI-Labor

Das Team protokolliert, wie es KI-Agenten bei der Entwicklung von Teilbar einsetzt, und prüft Hypothesen darüber in Experimenten. Jede Aufgabe im Labor ist ein Issue der App.

### Arbeit

**Aufgabe**:
Eine abgegrenzte Arbeitseinheit, z. B. eine Anforderung klären oder einen Bildschirm bauen. Jede Aufgabe ist genau ein GitHub-Issue.
_Avoid_: Task, Ticket, Story

**Sitzung**:
Ein zusammenhängendes Gespräch einer Person mit einem Agenten in einem Harness. Eine Aufgabe kann mehrere Sitzungen haben.
_Avoid_: Interaktion, Session, Thread, Chat

**Sitzungsprotokoll**:
Der Datensatz, der am Ende einer Sitzung über diese Sitzung entsteht (`ai-lab/daten/sitzungen/`).
_Avoid_: Log, Interaktionsprotokoll, Transkript

**Konfiguration**:
Harness, Modell, Effort-Stufe und aktive Skills, MCP-Server und Werkzeuge einer Sitzung oder eines Laufs.
_Avoid_: Setup, Setting, Umgebung

**Haupt-Konfiguration**:
Die Konfiguration, mit der eine Person im Alltag hauptsächlich arbeitet.
_Avoid_: Standard-Tool

### Erkenntnis

**Sichtung**:
Die Durchsicht einer fremden Quelle (Repo, Framework, Tool, Kurs, Studie) durch eine Person und ihren Agenten. Das Ergebnis sind Kandidaten, kein installiertes Paket.
_Avoid_: Review, Evaluation, Import

**Kandidat**:
Eine Idee aus einer Sitzung oder Sichtung, die eine Hypothese werden könnte. Noch nicht zum Testen ausgewählt.
_Avoid_: Idee, Vorschlag, Backlog-Hypothese

**Hypothese**:
Eine prüfbare Aussage der Form „Wenn …, dann …, weil …“ über den Einsatz von KI-Agenten.
_Avoid_: Annahme, These, Vermutung

**Experiment**:
Eine geplante Prüfung einer Hypothese: dieselbe Aufgabe in mindestens zwei Konfigurationen.
_Avoid_: Test, Versuch, A/B-Test

**Lauf**:
Eine einzelne Bearbeitung der Experiment-Aufgabe in einer Konfiguration.
_Avoid_: Run, Durchgang, Versuch

**Befund**:
Das Ergebnis eines Experiments: Es stützt die Hypothese, stützt sie nicht oder lässt sie offen.
_Avoid_: Ergebnis, Erkenntnis, Learning

**Schattenpreis**:
Was die Tokens einer Sitzung oder eines Laufs zum API-Listenpreis gekostet hätten, auch wenn ein Abo sie pauschal abdeckt.
_Avoid_: Kosten (allein), Preis

### Rollen

**Lab-Lead**:
Die Person, die das KI-Labor betreut, das Lab-Review moderiert und über seine Regeln entscheidet (Amin).
_Avoid_: Admin, Owner

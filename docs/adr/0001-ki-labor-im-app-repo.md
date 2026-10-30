# 0001 KI-Labor im App-Repo, öffentlich und kostenlos

Status: angenommen · 2026-10-30

## Kontext

Im Modul KDE wird die dokumentierte Erfahrung mit KI-Agenten bewertet. Das Team (4 Personen) braucht einen Ort für Sitzungen, Hypothesen und Experimente, den die Prüfer finden und der auf Issues, Commits und PRs der App verweisen kann. Das Repo `Aminos061/teilbar` ist öffentlich, weil GitHub Pages den Prototyp nur so kostenlos ausliefert.

## Entscheidung

- Das KI-Labor liegt in `ai-lab/` im App-Repo, nicht in einem eigenen Repo.
- Alles ist öffentlich. Agenten schwärzen Keys, Tokens und private Daten mit `[GESCHWÄRZT]`. gitleaks prüft vor jedem Commit und in der CI. Roh-Transkripte kommen nie ins Repo.
- Alles muss kostenlos sein. Uni-Qwen läuft nur im Hochschulnetz oder mit VPN, darauf weist das Setup hin.
- Wir fangen neu an: Sitzungen vor dem 30.10.2026 werden nicht nachträglich erfasst.

## Folgen

Ein Klon reicht für App und Labor. Wer protokolliert, muss an die Öffentlichkeit denken. Die CA1-Doku deckt die Designphase ab, das Labor beginnt mit der Umsetzung.

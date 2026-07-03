# Flag Game

[🇬🇧 English](README.md) · [🇩🇪 Deutsch](README.de.md)

Ein interaktives Flaggen-Quiz, entwickelt mit Python und Flet.

Errate das Land anhand seiner Flagge, nutze Hinweise bei Bedarf und versuche, einen möglichst hohen Punktestand zu erreichen.

> Die Benutzeroberfläche ist auf Englisch. Ländernamen werden aktuell auf Deutsch eingegeben.

---

## Projektübersicht

Flag Game ist ein Python-Lernprojekt mit einer grafischen Benutzeroberfläche. Das Spiel kombiniert lokale Länder- und Flaggendaten mit Spiel-Logik, Eingabevalidierung, zufälligen Hinweisen und einer lokalen Highscore-Liste.

Spielerinnen und Spieler können Länder anhand ihrer Flaggen erraten, Fragen nach Hinweisen beantworten und ihren Fortschritt innerhalb einer Spielrunde verfolgen.

---

## Features

- Lokaler Länderdatensatz mit eingebundenen Flaggenbildern
- Zufällige Länderauswahl ohne Wiederholungen innerhalb eines Spiels
- Fünf Versuche pro Land
- Zufällige Hinweise nach falschen Antworten:
  - Hauptstadt
  - Kontinent
  - Bevölkerung
  - Nachbarländer
- Teilweise ausgeblendete Anzeige des Ländernamens
- Groß-/Kleinschreibung und Akzente werden bei Antworten berücksichtigt
- Lokale Highscore-Speicherung
- Top-10-Highscore-Ansicht
- Neues Spiel kann jederzeit gestartet werden
- Ausführbar als Desktop-Anwendung oder Web-App mit Flet

---

## Verwendete Technologien

- Python 3.10+
- Flet
- JSON
- Unidecode
- Lokale Dateispeicherung

---

## Spielablauf

1. Starte die Anwendung.
2. Gib deinen Namen ein.
3. Sieh dir die Flagge an und gib den Ländernamen auf Deutsch ein.
4. Drücke **Guess** oder die Eingabetaste.
5. Bei einer falschen Antwort wird ein zufälliger Hinweis angezeigt.
6. Du hast maximal fünf Versuche, bevor die richtige Lösung angezeigt wird.
7. Drücke die Eingabetaste oder **Next Country**, um weiterzumachen.

Ein Land wird nach jeder Runde aus dem aktuellen Pool entfernt und erscheint erst wieder, wenn ein neues Spiel gestartet wird.

---

## Projekt lokal starten

### Voraussetzungen

- Python 3.10 oder neuer
- `uv` wird für die Verwaltung der Projektumgebung empfohlen

### Repository klonen

```bash
git clone https://github.com/alexpetrovici/FlagGame.git
cd FlagGame
```

### Abhängigkeiten installieren

```bash
uv sync
```

### Als Desktop-App starten

```bash
uv run flet run
```

### Im Browser starten

```bash
uv run flet run --web
```

---

## Projektstruktur

```text
FlagGame/
├── src/
│   ├── assets/
│   │   ├── countries.json
│   │   ├── icon.png
│   │   └── flag images
│   ├── country.py
│   ├── logic_handler.py
│   └── main.py
├── country_api.py
├── flag_loader.py
├── pyproject.toml
├── README.md
├── README.de.md
└── .gitignore
```

---

## Geübte Konzepte

| Konzept | Verwendung im Projekt |
|---|---|
| GUI-Entwicklung | Interaktive Benutzeroberfläche mit Flet |
| Zustandsverwaltung | Speichert aktuelles Land, Versuche, Hinweise und Punktestand |
| Zufallsauswahl | Wählt Länder und Hinweise zufällig aus |
| JSON | Lädt Länderinformationen aus einer lokalen JSON-Datei |
| Objektorientierung | Verwendet eine `Country`-Klasse für Länderdaten |
| Dateiverarbeitung | Speichert und lädt lokale Highscores |
| Datenaufbereitung | Wandelt Länder- und Grenzcodes in lesbare Namen um |
| Eingaben normalisieren | Behandelt Groß-/Kleinschreibung, Akzente, Bindestriche und Apostrophe |
| Modulare Struktur | Trennt Benutzeroberfläche, Spiellogik, Daten und Hilfsskripte |

---

## Daten und Assets

Das Spiel verwendet eine lokale JSON-Datei mit Länderinformationen sowie lokal gespeicherte Flaggenbilder.

Die enthaltenen Hilfsskripte wurden verwendet, um Länderinformationen und Flaggenbilder vorzubereiten:

- `country_api.py` ruft Länderinformationen ab.
- `flag_loader.py` lädt Flaggenbilder in den Assets-Ordner herunter.

Das eigentliche Spiel läuft mit lokal gespeicherten Daten und Assets.

---

## Highscores

Highscores werden lokal auf dem jeweiligen Gerät gespeichert:

```text
~/.flaggame/highscore.json
```

Die Top-10-Ansicht zeigt die höchsten gespeicherten Punktestände an.

---

## Ideen für die Zukunft

- Nur einen finalen Score pro abgeschlossenem Spiel speichern
- Sprachumschaltung für englische und deutsche Ländernamen
- Schwierigkeitsstufen oder zeitbasierte Runden
- Soundeffekte und visuelles Feedback
- Automatisierte Tests für Spiellogik und Highscore-Verwaltung
- Paketierung der Anwendung für Windows und Linux

---

## Autor

Alexandru Petrovici

Erstellt als Python- und Flet-Lernprojekt.

# Flag Game

[🇬🇧 English](README.md) · [🇩🇪 Deutsch](README.de.md)

An interactive country flag guessing game built with Python and Flet.

Guess the country from its flag, use hints when needed, and try to build the highest score.

> The interface is in English, while country names currently need to be entered in German.

---

## Features

- 250 country and territory records with locally stored flag assets
- Random country selection without repeats during a game
- Five attempts per country
- Random hints after incorrect guesses:
  - Capital
  - Continent
  - Population
  - Bordering countries
- Masked country name display
- Case- and accent-insensitive answer matching
- Local high-score tracking
- Top 10 high-score screen
- Start a new game at any time
- Runs as a desktop app or web app through Flet

---

## Tech Stack

- Python 3.10+
- Flet
- JSON
- Unidecode
- Local file persistence

---

## How to Play

1. Start the application.
2. Enter your name.
3. Look at the flag and enter the country name in German.
4. Press **Guess** or press Enter.
5. Incorrect guesses reveal a random hint.
6. You have up to five attempts before the correct answer is shown.
7. Press Enter or **Next Country** to continue.

A country is removed from the current pool after each round, so it will not appear again until a new game begins.

---

## Run Locally

### Requirements

- Python 3.10 or later
- `uv` recommended for managing the project environment

### Clone the Repository

```bash
git clone https://github.com/alexpetrovici/flag-game.git
cd flag-game
```

### Install Dependencies

```bash
uv sync
```

### Run as a Desktop App

```bash
uv run flet run
```

### Run in the Browser

```bash
uv run flet run --web
```

---

## Project Structure

```text
flag-game/
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
└── .gitignore
```

---

## Key Concepts Practised

| Concept | Use in the Project |
|---|---|
| GUI development | Interactive interface built with Flet |
| State management | Tracks the current country, attempts, hints, and score |
| Randomization | Selects countries and hints randomly |
| JSON | Loads country information from a local JSON file |
| Object-oriented programming | Uses a `Country` class to represent country data |
| File handling | Saves and loads local high-score records |
| Data transformation | Converts country border codes into readable names |
| Input normalization | Handles capitalization, accents, hyphens, and apostrophes |
| Modular structure | Separates UI, country logic, data loading, and helper scripts |

---

## Data and Assets

The game uses a bundled JSON file containing country information and local flag images.

The included helper scripts were used to collect country data and flag assets:

- `country_api.py` retrieves country information.
- `flag_loader.py` downloads flag images into the assets folder.

The game itself runs from locally stored data and assets.

---

## High Scores

High scores are stored locally on the user’s device:

```text
~/.flaggame/highscore.json
```

The Top 10 screen displays the highest saved scores.

---

## Future Ideas

- Save one final score per completed game instead of individual score updates
- Add a language selector for English and German country names
- Add difficulty levels or timed rounds
- Add sound effects and visual feedback
- Add automated tests for country logic and score handling
- Package the application for Windows and Linux

---

## Author

Alexandru Petrovici

Built as a Python and Flet learning project.

import json
import random
from pathlib import Path
import os

import flet as ft
from flet import View, Text, Page, Button, Image
from unidecode import unidecode

from country import Country
from logic_handler import load_countries_file, load_countries


# ---------- Constants ----------

BASE_DIR = Path(__file__).parent
file_path = BASE_DIR / "assets" / "countries.json"

APP_DATA_DIR = Path.home() / ".flaggame"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)


HIGHSCORE_FILE = APP_DATA_DIR / "highscore.json"
MAX_TRIES = 5


# ---------- Country helpers ----------

def init_game():
    countries_json = load_countries_file(file_path)
    return load_countries(countries_json)


def get_random_country(countries_list):
    random_index = random.randrange(len(countries_list))
    return countries_list.pop(random_index)


def normalize_text(text):
    return unidecode(text).strip().lower().replace("'", "").replace("-", " ")


def mask_country_name(name):
    return "".join(char if char in [" ", "-"] else "•" for char in name)


def format_population(population):
    return f"{population:,}".replace(",", ".")


def get_capital(country):
    if country.capital:
        return country.capital[0]
    return "No capital"


def get_continent(country):
    if country.continents:
        return country.continents[0]
    return "Unknown continent"


def create_country_name_map(countries_list):
    country_map = {}

    for country in countries_list:
        country_map[country.cca3] = country.name_ger

    return country_map


def get_borders(country, country_name_map):
    if not country.borders:
        return "No bordering countries"

    border_names = []

    for border_code in country.borders:
        border_name = country_name_map.get(border_code, border_code)
        border_names.append(border_name)

    return ", ".join(border_names)


# ---------- Highscore helpers ----------

def save_highscore(player_name, score):
    entry = {
        "name": player_name,
        "score": score,
    }

    with open(HIGHSCORE_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_scores():
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as file:
            return [json.loads(line) for line in file]

    except FileNotFoundError:
        return []


def load_highscore():
    scores = load_scores()

    if not scores:
        return "Highscore: -"

    best_score = max(scores, key=lambda entry: entry["score"])
    return f"Highscore: {best_score['name']} - {best_score['score']}"


def load_top_scores(limit=10):
    scores = load_scores()

    if not scores:
        return "No scores yet."

    scores = sorted(scores, key=lambda entry: entry["score"], reverse=True)
    top_scores = scores[:limit]

    lines = []

    for index, entry in enumerate(top_scores, start=1):
        medal = ""

        if index == 1:
            medal = "🥇"
        elif index == 2:
            medal = "🥈"
        elif index == 3:
            medal = "🥉"

        lines.append(f"{medal} {index}. {entry['name']} - {entry['score']}")

    return "\n".join(lines)


# ---------- Main app ----------

def main(page: Page):
    page.title = "Flag Game"
    page.bgcolor = "#0F172A"
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    loaded_countries: list[Country] = init_game()
    country_name_map = create_country_name_map(loaded_countries)

    # Stores the current game state.
    game = {
        "current_country": get_random_country(loaded_countries),
        "correct_answers": 0,
        "tries": 0,
        "answer_shown": False,
        "used_hints": [],
    }

    # ---------- UI controls ----------

    title_text = Text(
        "Flag Game",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#F8FAFC",
    )

    player_name_input = ft.TextField(
        label="Player Name",
        value="Alex",
        width=300,
    )

    highscore_text = Text(
        value=load_highscore(),
        size=15,
        color="#FACC15",
    )

    countries_left_text = Text(
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#E2E8F0",
    )

    result_text = Text(
        value="",
        size=20,
        color="#F8FAFC",
    )

    country_input = ft.TextField(
        label="Your guess",
        width=300,
    )

    flag_image = Image(
        src=f"{game['current_country'].cca3}.png",
        width=500,
        height=300,
    )

    flag_container = ft.Container(
        content=flag_image,
        padding=20,
        border_radius=20,
        bgcolor="#0F172A",
        border=ft.Border(
            left=ft.BorderSide(2, "#334155"),
            top=ft.BorderSide(2, "#334155"),
            right=ft.BorderSide(2, "#334155"),
            bottom=ft.BorderSide(2, "#334155"),
        ),
    )

    masked_country_text = Text(
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#F8FAFC",
    )

    hint_capital_text = Text(size=20, color="#CBD5E1")
    hint_continent_text = Text(size=20, color="#CBD5E1")
    hint_population_text = Text(size=20, color="#CBD5E1")
    hint_borders_text = Text(size=20, color="#CBD5E1")

    correct_counter_text = Text(size=15, color="#94A3B8")
    tries_counter_text = Text(size=15, color="#94A3B8")

    # ---------- UI update helpers ----------

    def update_counters():
        correct_counter_text.value = f"Correct answers: {game['correct_answers']}"
        tries_counter_text.value = f"Tries: {game['tries']} / {MAX_TRIES}"
        countries_left_text.value = f"Countries left: {len(loaded_countries) + 1}"

    def update_view():
        country = game["current_country"]

        flag_image.src = f"{country.cca3}.png"
        masked_country_text.value = f"Country: {mask_country_name(country.name_ger)}"

        hint_capital_text.value = "Capital: ?"
        hint_continent_text.value = "Continent: ?"
        hint_population_text.value = "Population: ?"
        hint_borders_text.value = "Borders: ?"

        result_text.value = ""
        result_text.color = "#F8FAFC"

        update_counters()

    def show_random_hint(country):
        available_hints = []

        if "capital" not in game["used_hints"]:
            available_hints.append("capital")

        if "continent" not in game["used_hints"]:
            available_hints.append("continent")

        if "population" not in game["used_hints"]:
            available_hints.append("population")

        if "borders" not in game["used_hints"]:
            available_hints.append("borders")

        if not available_hints:
            return

        hint = random.choice(available_hints)
        game["used_hints"].append(hint)

        if hint == "capital":
            hint_capital_text.value = f"Capital: {get_capital(country)}"

        elif hint == "continent":
            hint_continent_text.value = f"Continent: {get_continent(country)}"

        elif hint == "population":
            hint_population_text.value = f"Population: {format_population(country.population)}"

        elif hint == "borders":
            hint_borders_text.value = f"Borders: {get_borders(country, country_name_map)}"

    # ---------- Event handlers ----------

    def next_country(e):
        if not loaded_countries:
            result_text.value = "Game Over!"
            result_text.color = "#F8FAFC"
            page.update()
            return

        game["current_country"] = get_random_country(loaded_countries)
        game["tries"] = 0
        game["answer_shown"] = False
        game["used_hints"] = []

        country_input.value = ""
        update_view()
        page.update()

    def new_game(e):
        nonlocal loaded_countries
        nonlocal country_name_map

        loaded_countries = init_game()
        country_name_map = create_country_name_map(loaded_countries)

        game["current_country"] = get_random_country(loaded_countries)
        game["correct_answers"] = 0
        game["tries"] = 0
        game["answer_shown"] = False
        game["used_hints"] = []

        country_input.value = ""
        update_view()
        page.update()

    async def exit_game(e):
        await page.window.close()

    def country_guess(e):
        if game["answer_shown"]:
            next_country(None)
            return

        country = game["current_country"]

        guess = normalize_text(country_input.value)
        correct_answer = normalize_text(country.name_ger)

        if guess == correct_answer:
            game["correct_answers"] += 1

            save_highscore(player_name_input.value, game["correct_answers"])
            highscore_text.value = load_highscore()

            result_text.value = "Correct! Press Enter for next country."
            result_text.color = "#22C55E"
            masked_country_text.value = f"Country: {country.name_ger}"
            game["answer_shown"] = True

        else:
            game["tries"] += 1

            if game["tries"] >= MAX_TRIES:
                result_text.value = (
                    f"No tries left! Correct answer: {country.name_ger}. "
                    "Press Enter for next country."
                )
                result_text.color = "#EF4444"
                masked_country_text.value = f"Country: {country.name_ger}"
                game["answer_shown"] = True
            else:
                result_text.value = f"Wrong! Try again. Tries: {game['tries']} / {MAX_TRIES}"
                result_text.color = "#EF4444"
                show_random_hint(country)

        update_counters()
        page.update()

    def go_back(e):
        page.views.pop()
        page.update()

    def show_highscores(e):
        highscore_title = Text(
            "🏆 Top 10 Highscores",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_GREY_900,
        )

        scores_text = Text(
            load_top_scores(),
            size=20,
            selectable=True,
            color=ft.Colors.BLUE_GREY_900,
        )

        highscore_column = ft.Column(
            controls=[
                highscore_title,
                scores_text,
                Button("Back", on_click=go_back),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        highscore_card = ft.Container(
            content=highscore_column,
            padding=40,
            border_radius=25,
            width=500,
            bgcolor=ft.Colors.BLUE_GREY_100,
        )

        page.views.append(
            View(
                route="/highscores",
                controls=[highscore_card],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

        page.update()

    country_input.on_submit = country_guess

    update_view()

    # ---------- Layout ----------

    buttons_row = ft.Row(
        controls=[
            Button("Guess", on_click=country_guess),
            Button("Next Country", on_click=next_country),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    new_game_row = ft.Row(
        controls=[
            Button("New Game", on_click=new_game),
            Button("Highscores", on_click=show_highscores),
            Button("Exit", on_click=exit_game),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    counters_row = ft.Row(
        controls=[
            correct_counter_text,
            tries_counter_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
    )

    hints_column = ft.Column(
        controls=[
            hint_capital_text,
            hint_continent_text,
            hint_population_text,
            hint_borders_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    main_column = ft.Column(
        controls=[
            title_text,
            player_name_input,
            highscore_text,
            countries_left_text,
            flag_container,
            masked_country_text,
            hints_column,
            counters_row,
            country_input,
            buttons_row,
            new_game_row,
            result_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    main_card = ft.Container(
        content=main_column,
        padding=40,
        border_radius=25,
        width=700,
        bgcolor="#1E293B",
    )

    page.views.append(
        View(
            route="/",
            controls=[main_card],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
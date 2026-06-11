import random
from unidecode import unidecode
import json

import flet as ft
from flet import View, Text, Page, Button, Image

from logic_handler import load_countries_file, load_countries
from country import Country


# TODO


def init_game():
    countries_json = load_countries_file("countries.json")
    return load_countries(countries_json)


def get_random_country(countries_list):
    random_index = random.randrange(len(countries_list))
    return countries_list.pop(random_index)


def normalize_text(text):
    return unidecode(text).strip().lower().replace("'", "").replace("-", " ")


def mask_country_name(name):
    return "".join(char if char in [" ", "-"] else "•" for char in name)


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


def format_population(population):
    return f"{population:,}".replace(",", ".")


def save_highscore(player_name, score):
    entry = {
        "name": player_name,
        "score": score,
    }

    with open("highscore.json", "a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_highscore():
    try:
        with open("highscore.json", "r", encoding="utf-8") as file:
            scores = [json.loads(line) for line in file]

        if not scores:
            return "Highscore: -"

        best_score = max(scores, key=lambda entry: entry["score"])
        return f"Highscore: {best_score['name']} - {best_score['score']}"

    except FileNotFoundError:
        return "Highscore: -"
    


def main(page: Page):
    page.title = "Country Guess"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    loaded_countries: list[Country] = init_game()
    country_name_map = create_country_name_map(loaded_countries)

    game = {
        "current_country": get_random_country(loaded_countries),
        "correct_answers": 0,
        "tries": 0,
        "answer_shown": False,
        "used_hints": [],
        "score_saved": False,
    }

    result_text = Text(value="", size=20)
    country_input = ft.TextField(label="Your guess", width=300)

    flag_image = Image(
        src=f"{game['current_country'].cca3}.png",
        width=400,
        height=250,
    )

    masked_country_text = Text(size=20, text_align=ft.TextAlign.CENTER)

    hint_capital_text = Text(size=20)
    hint_continent_text = Text(size=20)
    hint_population_text = Text(size=20)
    hint_borders_text = Text(size=20)

    correct_counter_text = Text(size=15)
    tries_counter_text = Text(size=15)
    countries_left_text = Text(size=18,weight=ft.FontWeight.BOLD,)
    player_name_input = ft.TextField(label="Player Name",value="Alex")
    highscore_text = Text(value=load_highscore(), size=15)


    def update_counters():
        correct_counter_text.value = f"Correct answers: {game['correct_answers']}"
        tries_counter_text.value = f"Tries: {game['tries']} / 5"
        countries_left_text.value = (f"Countries left: {len(loaded_countries) + 1}")


    def update_view():
        country = game["current_country"]

        flag_image.src = f"{country.cca3}.png"
        masked_country_text.value = f"Country: {mask_country_name(country.name_ger)}"

        hint_capital_text.value = "Capital: ?"
        hint_continent_text.value = "Continent: ?"
        hint_population_text.value = "Population: ?"
        hint_borders_text.value = "Borders: ?"

        result_text.value = ""
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
            hint_population_text.value = (
                f"Population: {format_population(country.population)}"
            )

        elif hint == "borders":
            hint_borders_text.value = (
                f"Borders: {get_borders(country, country_name_map)}"
            )


    def next_country(e):
        if not loaded_countries:
            highscore_text.value = load_highscore()
            result_text.value = "Game Over!"
            page.update()
            return

        game["current_country"] = get_random_country(loaded_countries)
        game["tries"] = 0
        game["answer_shown"] = False
        game["used_hints"] = []

        country_input.value = ""
        update_view()
        page.update()


    async def exit_game(e):
        await page.window.close()


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
        game["score_saved"] = False

        country_input.value = ""
        update_view()
        page.update()


    def country_guess(e):
        if game["answer_shown"]:
            next_country(None)
            return

        country = game["current_country"]

        guess = normalize_text(country_input.value)
        correct_answer = normalize_text(country.name_ger)

        if guess == correct_answer:
            game["correct_answers"] += 1

            save_highscore(
                player_name_input.value,
                game["correct_answers"]
            )

            highscore_text.value = load_highscore()

            result_text.value = "Correct! Press Enter for next country."
            masked_country_text.value = f"Country: {country.name_ger}"
            game["answer_shown"] = True

        else:
            game["tries"] += 1

            if game["tries"] >= 5:
                result_text.value = (
                    f"No tries left! Correct answer: {country.name_ger}. "
                    "Press Enter for next country."
                )
                masked_country_text.value = f"Country: {country.name_ger}"
                game["answer_shown"] = True
            else:
                result_text.value = f"Wrong! Try again. Tries: {game['tries']} / 5"
                show_random_hint(country)

        update_counters()
        page.update()

    country_input.on_submit = country_guess

    update_view()


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
            player_name_input,
            highscore_text,
            countries_left_text,
            flag_image,
            masked_country_text,
            hints_column,
            counters_row,
            country_input,
            buttons_row,
            new_game_row,
            result_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    page.views.append(
        View(
            route="/",
            controls=[main_column],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
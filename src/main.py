import random
import flet as ft
from flet import View, Text, Row, View, Page, AppBar, Button, Text, IconButton, Image

from logic_handler import load_countries_file, load_countries
from country import Country


def init_game():
    countries_json = load_countries_file("countries.json")
    countries = load_countries(countries_json)
    return countries


def get_random_country(countries_list):
    random_index = random.randrange(len(countries_list))
    return countries_list.pop(random_index)


def mask_country_name(name):
    return "".join(char if char in [" ", "-"] else "*"for char in name)


def get_capital(country):
    if country.capital:
        return country.capital[0]
    return "No capital"


def get_continent(country):
    if country.continents:
        return country.continents[0]
    return "Unknown continent"


def main(page: Page):
    loaded_countries: list[Country] = init_game()
    
    game = {
        "current_country": get_random_country(loaded_countries),
        "correct_answers": 0,
        "tries": 0,
        "answer_shown": False,
    }


    def update_counters():
        correct_counter_text.value = f"Correct answers: {game['correct_answers']}"
        tries_counter_text.value = f"Tries: {game['tries']} / 5"


    def country_guess(e):
        if game["answer_shown"]:
            next_country(None)
            return

        country = game["current_country"]
        guess = country_input.value.strip().lower()

        if guess == country.name_ger.lower():
            game["correct_answers"] += 1
            result_text.value = "Correct! Press Enter for next country."
            masked_country_text.value = f"Country: {country.name_ger}"
            game["answer_shown"] = True

        else:
            game["tries"] += 1

            if game["tries"] >= 5:
                result_text.value = f"No tries left! Correct answer: {country.name_ger}. Press Enter for next country."
                masked_country_text.value = f"Country: {country.name_ger}"
                game["answer_shown"] = True
            else:
                result_text.value = f"Wrong! Try again. Tries: {game['tries']} / 5"

                if game["tries"] == 1:
                    hint_capital_text.value = f"Capital: {get_capital(country)}"

                elif game["tries"] == 2:
                    hint_continent_text.value = f"Continent: {get_continent(country)}"

                elif game["tries"] == 3:
                    population = f"{country.population:,}".replace(",", ".")
                    hint_population_text.value = f"Population: {population}"

        update_counters()
        page.update()


    result_text = Text(value="", size=30)
    country_input = ft.TextField(label="Your guess", on_submit=country_guess)


    flag_image = Image(
        src=f"{game['current_country'].cca3}.png",
        width=600,
        height=400,
        repeat=ft.ImageRepeat.NO_REPEAT,
    )


    masked_country_text = Text(size=20)
    correct_counter_text = Text(size=15)
    tries_counter_text = Text(size=15)
    hint_capital_text = Text("Capital: ?", size=20)
    hint_continent_text = Text("Continent: ?", size=20)
    hint_population_text = Text("Population: ?", size=20)


    def update_view():
        country = game["current_country"]

        flag_image.src = f"{country.cca3}.png"
        masked_country_text.value = f"Country: {mask_country_name(country.name_ger)}"
        hint_capital_text.value = "Capital: ?"
        hint_continent_text.value = "Continent: ?"
        hint_population_text.value = "Population: ?"
        result_text.value = ""
        tries_counter_text.value = f"Tries: {game['tries']} / 5"
        correct_counter_text.value = f"Correct answers: {game['correct_answers']}"


    def next_country(e):

        if not loaded_countries:
            result_text.value = "Game Over! No countries left."
            page.update()
            return

        game["current_country"] = get_random_country(loaded_countries)
        game["tries"] = 0
        game["answer_shown"] = False

        country_input.value = ""
        update_view()
        update_counters()
        page.update()

    update_view()


    page.views.append(
        View(
            route="/",
            controls=[
                flag_image,
                masked_country_text,
                hint_capital_text,
                hint_continent_text,
                hint_population_text,
                correct_counter_text,
                tries_counter_text,
                country_input,
                Button("Check Guess", on_click=country_guess),
                Button("Next Country", on_click=next_country),
                result_text,
            ],
        )
    )

    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
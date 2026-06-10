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


def main(page: Page):
    loaded_countries: list[Country] = init_game()
    
    game = {
        "current_country": get_random_country(loaded_countries)
    }

    def country_guess(e):
        country = game["current_country"]

        guess = country_input.value.strip().lower()

        if guess == country.name_ger.lower():
            result_text.value = "Correct!"
        else:
            result_text.value = (
                f"Wrong! Correct answer: {country.name_ger}"
            )
        
        masked_country_text.value = f"Country: {country.name_ger}"

        page.update()

    result_text = Text(value="", size=30)
    country_input = ft.TextField(label="Your guess", on_submit=country_guess)

    flag_image = Image(
        src=f"{game['current_country'].cca3}.png",
        width=600,
        height=400,
        repeat=ft.ImageRepeat.NO_REPEAT,
    )

    #text_field_country_name = Text(size=30)
    text_field_capital_name = Text(size=30)
    text_field_continent_name = Text(size=30)
    text_field_population = Text(size=30)
    masked_country_text = Text(size=30)

    def update_view():
        country = game["current_country"]

        flag_image.src = f"{country.cca3}.png"
        masked_country_text.value = f"Country: {mask_country_name(country.name_ger)}"
        #text_field_country_name.value = f"Country: "
        text_field_capital_name.value = f"Capital: {country.capital[0]}"
        text_field_continent_name.value = f"Continent: {country.continents[0]}"
        text_field_population.value = (f"Population: {country.population:,}".replace(",", "."))
        result_text.value = ""


    def next_country(e):
        game["current_country"] = get_random_country(loaded_countries)

        country_input.value = ""
        update_view()
        page.update()

    update_view()

    page.views.append(
        View(
            route="/",
            controls=[
                flag_image,
                masked_country_text,
                #text_field_country_name,
                text_field_capital_name,
                text_field_continent_name,
                text_field_population,
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
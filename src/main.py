import random
import flet as ft

from country import Country
from logic_handler import load_countries_file, load_countries


def init_game():
    countries_json = load_countries_file("countries.json")
    return load_countries(countries_json)


def get_random_country(countries_list):
    random_index = random.randrange(len(countries_list))
    return countries_list.pop(random_index)


def format_population(population):
    return f"{population:,}".replace(",", ".")


def main(page: ft.Page):
    page.title = "Flag Game"

    loaded_countries: list[Country] = init_game()
    page.data = get_random_country(loaded_countries)
    current_country = page.data

    result_text = ft.Text(value="", size=30)

    flag_image = ft.Image(src=f"{current_country.cca3}.png", width=600, height=400,)

    capital_text = ft.Text(size=30)
    continent_text = ft.Text(size=30)
    population_text = ft.Text(size=30)

    def update_country_view():
        current_country = page.data

        flag_image.src = f"{current_country.cca3}.png"
        capital_text.value = f"Capital: {current_country.capital[0]}"
        continent_text.value = f"Continent: {current_country.continents[0]}"
        population_text.value = f"Population: {format_population(current_country.population)}"
        result_text.value = ""

    def country_guess(e):
        current_country = page.data
        result_text.value = current_country.name_ger
        page.update()

    def next_country(e):
        page.data = get_random_country(loaded_countries)
        update_country_view()
        page.update()

    update_country_view()

    page.views.append(
        ft.View(
            route="/",
            controls=[
                flag_image,
                capital_text,
                continent_text,
                population_text,
                ft.Button("Country Guess", on_click=country_guess),
                ft.Button("Next Country", on_click=next_country),
                result_text,
            ],
        )
    )

    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
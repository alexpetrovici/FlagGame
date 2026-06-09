import flet as ft
from flet import View, Text, Row, View, Page, AppBar, Button, Text, IconButton, Image
from logic_handler import load_countries_file, load_countries
from country import Country
import random

#TODO 

def init_game():
    countries_json = load_countries_file("countries.json")
    countries = load_countries(countries_json)
    return countries

def get_random_country(countries_list):
    random_index = random.randrange(len(countries_list))
    return countries_list.pop(random_index)

def main(page: Page):
    counter = ft.Text("0", size=50, data=0)
    loaded_countries: list[Country] = init_game()
    current_country = get_random_country(loaded_countries)
    
    result_text = Text(value="", size=30)

    flag_image = Image(
        src=f"{current_country.cca3}.png",
        width=600,
        height=400,
        repeat=ft.ImageRepeat.NO_REPEAT,
    )

    def country_guess(e):
        result_text.value = current_country.name_ger
        page.update()

    page.views.append(View(route="/", controls=[
        flag_image,
        Text(value=f"Capital: {current_country.capital[0]}", size=30),
        Text(value=f"Continent: {current_country.continents[0]}", size=30),
        #Text(value=f"Borders: {current_country.borders}", size=30),
        Text(value=f"Population: {current_country.population:,}".replace(",", "."), size=30),
        Button("Country Guess", on_click=country_guess),
        result_text,],))
    page.update()


if __name__ == "__main__":
    ft.app(target=main,assets_dir="assets")
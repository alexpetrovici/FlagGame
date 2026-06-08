import json
import requests

url = "https://restcountries.com/v3.1/all?fields=name,flags,borders,capital,continents,translations,languages,population"

response = requests.get(url)

if response.status_code == 200:
    countries = response.json()
    with open("countries.json", "w") as f:
        json.dump(countries, f, indent=4)
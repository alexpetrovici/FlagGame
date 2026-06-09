import requests
import json
import os

'''
Loads all the country flags from the API https://restcountries.com and saves them in src/assets as .png
'''

country_file = open("countries.json", encoding="utf-8")
countries = json.load(country_file)

for country in countries:
    flag_url = country["flags"]["png"]
    file_name = country["translations"]["deu"]["official"]
    try:
        capital_name = country["capital"][0]
    except IndexError:
        capital_name = "Country has no Capital"
    
    response = requests.get(flag_url)
    if response.status_code == 200:
        with open(os.path.join("src", "assets", (file_name + ".png")), "wb") as file:
            file.write(response.content)
    print(f"Country: {file_name}")
    print(f"Capital: {capital_name}")
    print(f"Flag: {flag_url}\n")
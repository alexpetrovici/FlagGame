import json
from country import Country

def load_countries_file(country_file):
    with open(country_file, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def load_countries(data):
    countries= []
    for country in data:
        cca3 = country['cca3']
        name_ger = country['translations']["deu"]["official"]
        capital = country['capital']
        borders = country['borders']
        population = country['population']
        continents = country['continents']
        #Country(cca3, name_ger, capital, borders, population, continents)
        countries.append(Country(cca3, name_ger, capital, borders, population, continents))
    return countries
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def covid_numbers():
    url = "https://www.worldometers.info/coronavirus/"
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    contador = soup.find_all('div', class_="maincounter-number")

    numeros = []
    for i in contador:
        numeros.append(i.text.strip().replace(",","."))

    return numeros

print(covid_numbers())


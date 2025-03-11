"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Pavlína Nováková
email: spiki15@seznam.cz
discord: Pavlína Nováková (pavlinanovakova)
"""

# potřebné knihovny
import requests
from bs4 import BeautifulSoup
import csv
import sys


# Získání obsahu HTML
def nacti_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# Seznam obcí s jejich čísly a názvy
def ziskej_data_obci(district_url):
    soup = nacti_html(district_url)
    radky = soup.select("table tr")[2:]
    obce = []

    for row in radky:
        cells = row.find_all("td")
        if len(cells) > 1 and cells[0].find("a"):
            kod_obce = cells[0].text.strip()
            nazev_obce = cells[1].text.strip()
            url_obce = "https://www.volby.cz/pls/ps2017nss/" + cells[0].find("a")["href"]
            obce.append((kod_obce, nazev_obce, url_obce))
    return obce


# Seznam politických stran
def ziskej_nazvy_stran(url_obce):
    soup = nacti_html(url_obce)
    nazvy_stran_1 = [tag.text.strip() for tag in soup.select("td[headers='t1sa1 t1sb2']")]
    nazvy_stran_2 = [tag.text.strip() for tag in soup.select("td[headers='t2sa1 t2sb2']")]
    return nazvy_stran_1 + nazvy_stran_2


# Výsledky voleb pro danou obec
def ziskej_vysledky_voleb(kod_obce, nazev_obce, url_obce):
    soup = nacti_html(url_obce)
    volici = soup.find("td", headers="sa2").text.strip()
    obalky = soup.find("td", headers="sa3").text.strip()
    platne_hlasy = soup.find("td", headers="sa6").text.strip()
    hlasy = [tag.text.strip() for tag in soup.select("td[headers*='t1sb3'], td[headers*='t2sb3']")]
    return [kod_obce, nazev_obce, volici, obalky, platne_hlasy] + hlasy


# Hlavní funkce 
def main():
    if len(sys.argv) != 3:
        print("Použij: python elections_scraper.py <URL okresu> <výstupní CSV soubor>")
        sys.exit(1)
    
    url_okresu = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    obce = ziskej_data_obci(url_okresu)

    if not obce:
        print("Chyba: Nebylo možné načíst seznam obcí.")
        sys.exit(1)

    nazvy_stran = ziskej_nazvy_stran(obce[0][2])

    with open(vystupni_soubor, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        header = ["kód", "obec", "voliči", "obálky", "platné hlasy"] + nazvy_stran
        writer.writerow(header)

        for kod_obce, nazev_obce, url_obce in obce:
            writer.writerow(ziskej_vysledky_voleb(kod_obce, nazev_obce, url_obce))
    
    print(f"Výsledky uloženy do {vystupni_soubor}")

if __name__ == "__main__":
    main()
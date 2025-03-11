# Elections Scraper
Projekt, který extrahuje data o výsledcích voleb z webových stránek. Skript prochází zadanou URL okresu, získává data o obcích a jejich volebních výsledcích, a následně je ukládá do CSV souboru.

## Požadavky
*   Nainstalované následující knihovny:
    *   `requests`
    *   `beautifulsoup4`
    *   `csv`
    *   `sys`

## Instalace
* Vytvořte si virtuální prostředí: python -m venv venv
* Aktivujte virtuální prostředí (Windows): venv\Scripts\activate
* Nainstalujte požadované knihovny: pip install -r requirements.txt

## Použití
Soubor se spustí po zadání 2 argumentů: python elections_scraper.py `<odkaz-uzemniho-celku>`  `<vysledny-soubor>`
* Příklad spuštění: `python elections_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "prostejov_vysledky.csv"`

## Výstupní soubor
* kód obce
* název obce
* počet voličů
* počet vydaných obálek
* počet platných hlasů
* název stran a jejich získaný počet hlasů

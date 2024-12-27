# Projektový seminář
Python projekt pro předmět Projektový seminář

## Použité knihovny
- cleverminer
- pandas
- openpyx1
- psycopg2
- python-dotenv

## Prerekvizity
- nainstalovaný python
- nainstalovaný postgresql

## Instalace
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- vytvořit .env soubor s proměnnými DB_HOST, DB_NAME, DB_USER, DB_PASSWORD pro komunikaci s lokální databází
- spustit python script (např. v IDE nebo ručně přes příkaz "python fileName.py")

## Poznámky
- Z důvodu velikosti tento repozitář obsahuje pouze již upravené excely
- Pokud chcete spustit skript pro úpravu prvotních dat (není třeba pro spuštění úloh nebo datové pumpy) je třeba stáhnout původní excel (src/dataPump/filter2023Data)
- Traffic violations - https://data.montgomerycountymd.gov/Public-Safety/Traffic-Violations/4mse-ku6q/about_data
- Weather data - https://catalog.data.gov/dataset/dickerson-weather-station-data
- Jména stažených souborů musí být přizpůsobeny python skriptu (v souborech filterTrafficViolations2023.py, filterWeather2023.py)

# Projektový seminář
Python projekt pro předmět Projektový seminář

## Použité knihovny
- cleverminer
- pandas
- openpyx1
- psycopg2
- python-dotenv

## Prerekvizity
- python
- postgresql

## Instalace
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- vytvořit .env soubor s proměnnými DB_HOST, DB_NAME, DB_USER, DB_PASSWORD pro komunikaci s lokální databází
- spustit python script (např. v IDE nebo ručně přes příkaz "python fileName.py")

## Poznámky
- pro spuštění skriptu pro úpravu prvotních dat je třeba stáhnout původní excel (src/dataPump/filter2023Data)
- Traffic violations - https://data.montgomerycountymd.gov/Public-Safety/Traffic-Violations/4mse-ku6q/about_data
- Weather data - https://catalog.data.gov/dataset/dickerson-weather-station-data
- The names of the downloaded files have to be adjusted to the python scripts (filterTrafficViolations2023, filterWeather2023)
- z důvodu velikosti tento repozitář obsahuje pouze již upravené excely
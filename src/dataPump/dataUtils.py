import pandas as pd

def filter_and_order_columns(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = [
        "SeqID", "Date Of Stop", "Time Of Stop", "SubAgency", "Description", "Accident", "Belts",
        "Personal Injury", "Property Damage", "Fatal", "Commercial License", "HAZMAT",
        "Commercial Vehicle", "Alcohol", "Search Conducted", "Search Outcome", "VehicleType",
        "Year", "Make", "Model", "Color", "Violation Type", "Charge", "Contributed To Accident",
        "Race", "Gender", "Driver City", "Driver State", "DL State", "Arrest Type"
    ]

    # Map the original column names to the SQL column names
    column_mapping = {
        "SeqID": "seq_id",
        "Date Of Stop": "date_of_stop",
        "Time Of Stop": "time_of_stop",
        "SubAgency": "subagency",
        "Description": "description",
        "Accident": "accident",
        "Belts": "belts",
        "Personal Injury": "personal_injury",
        "Property Damage": "property_damage",
        "Fatal": "fatal",
        "Commercial License": "commercial_license",
        "HAZMAT": "hazmat",
        "Commercial Vehicle": "commercial_vehicle",
        "Alcohol": "alcohol",
        "Search Conducted": "search_conducted",
        "Search Outcome": "search_outcome",
        "VehicleType": "vehicle_type",
        "Year": "year",
        "Make": "make",
        "Model": "model",
        "Color": "color",
        "Violation Type": "violation_type",
        "Charge": "charge",
        "Contributed To Accident": "contributed_to_accident",
        "Race": "race",
        "Gender": "gender",
        "Driver City": "driver_city",
        "Driver State": "driver_state",
        "DL State": "dl_state",
        "Arrest Type": "arrest_type"
    }

    # Filter and rename columns
    filtered_df = df[required_columns].rename(columns=column_mapping)
    
    return filtered_df

def categorize_temperature(temp):
    if temp < 47 or temp > 82:
        return 'unusual'
    else:
        return 'normal'
    
def categorize_wind(wind):
    if wind > 6.3:
        return 'windy'
    else:
        return 'not-windy'

def add_weather_attributes(traffic_df, weather_df):
    # Convert 'Date Time' to datetime without specifying a format (handles ISO format directly)
    weather_df['Date Time'] = pd.to_datetime(weather_df['Date Time'], errors='coerce')
    weather_df = weather_df.dropna(subset=['Date Time']).drop_duplicates(subset=['Date Time'])
    weather_df = weather_df.sort_values(by='Date Time')

    # Add rounded datetime column for merging
    traffic_df['Datetime'] = pd.to_datetime(traffic_df['date_of_stop'] + ' ' + traffic_df['time_of_stop'])
    traffic_df['DatetimeRounded'] = traffic_df['Datetime'].dt.round('h')

    # Merge traffic and weather data
    merged_df = pd.merge(traffic_df, weather_df, left_on='DatetimeRounded', right_on='Date Time', how='left')

    # Add weather attributes
    merged_df['rain'] = merged_df['RAIN ']
    merged_df['temperature'] = merged_df['TMP10-DK ']
    merged_df['wind'] = merged_df['SPD10-DK ']

    merged_df['wasRaining'] = merged_df['rain'] > 0
    merged_df['temperature_type'] = merged_df['temperature'].apply(categorize_temperature)
    merged_df['wind_type'] = merged_df['wind'].apply(categorize_wind)

    # Remove unnecessary columns
    columns_to_remove = ['Datetime', 'DatetimeRounded', 'Date Time', 'SPD10-DK ', 'TMP10-DK ', 'DEW PT.  ', 'RAIN ']
    merged_df = merged_df.drop(columns=columns_to_remove)

    return merged_df

def categorize_time(time_str):
        hour = int(time_str.split(':')[0])

        if hour < 5:
            return "night"
        elif hour < 11:
            return "morning"
        elif hour < 17:
            return "afternoon"
        else:
            return "evening"

def add_time_category(traffic_df):
    traffic_df['time_of_stop_category'] = traffic_df['time_of_stop'].apply(categorize_time)
    return traffic_df


def prepare_city_incomes(file_path):
    # Define a mapping of state names to abbreviations (https://www.bu.edu/brand/guidelines/editorial-style/us-state-abbreviations/)
    state_abbreviations = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "District of Columbia": "DC",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
    }

    cities_income_df = pd.read_csv(file_path, encoding='cp1250', sep=',', skiprows=1)

    # Filter only the required columns and make a copy
    filtered_df = cities_income_df[["Geographic Area Name", "Estimate!!Households!!Median income (dollars)"]].copy()

    filtered_df.rename(columns={"Estimate!!Households!!Median income (dollars)": "MedIncome"}, inplace=True)

    # Split "Geographic Area Name" into "City" and "State"
    filtered_df[['City', 'State']] = filtered_df["Geographic Area Name"].str.extract(r'^(.*?),\s*(.*)$', expand=True)

    # Map state names to their abbreviations
    filtered_df['Abbr'] = filtered_df['State'].map(state_abbreviations)
    
    filtered_df = filtered_df.drop(columns=["Geographic Area Name"])

    return filtered_df


def categorize_city_income(median):
    if median < 1:
        return 'unknown income'
    elif median < 91971:
        return 'low income'
    elif median < 104062:
        return 'medium income'
    else:
        return 'high income'

def add_cityMedian(traffic_df: pd.DataFrame, cities_path) -> pd.DataFrame:
    cities_df = prepare_city_incomes(cities_path)

    # Function to clean and convert median income values
    def clean_median_income(value):
        if pd.isna(value):
            return -1  # Return -1 for missing values
        value = str(value).replace(",", "").replace("+", "").strip()
        try:
            return int(value)
        except ValueError:
            return -1  # Return -1 for invalid values

    # Clean the MedIncome column in cities_df
    cities_df['MedIncome'] = cities_df['MedIncome'].apply(clean_median_income)

    # Create a hash map of state -> city to median income mapping ... naive n2 algorithm is too slow
    state_city_income_map = {}
    for state in cities_df['Abbr'].unique():
        state_cities = cities_df[cities_df['Abbr'] == state]
        state_city_income_map[state] = {
            city.lower(): med_income
            for city, med_income in zip(state_cities['City'], state_cities['MedIncome'])
        }

    # Function to find city median income with substring matching
    def find_city_median(row, state_city_income_map):
        state = row['driver_state']
        driver_city = str(row['driver_city']).lower() if pd.notna(row['driver_city']) else ""
        
        if state not in state_city_income_map:
            return -1
        
        # Get all cities for the state
        state_cities = state_city_income_map[state]
        
        # Check for a city match (substring)
        for city, med_income in state_cities.items():
            if driver_city in city:
                return med_income
        
        # No match found
        return -1

    traffic_df['cityMedian'] = traffic_df.apply(find_city_median, axis=1, state_city_income_map=state_city_income_map)
    traffic_df['cityIncomeCategory'] = traffic_df["cityMedian"].apply(categorize_city_income)
    return traffic_df
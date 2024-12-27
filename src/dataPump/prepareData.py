import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dataPump.dataUtils import add_cityMedian, add_time_category, add_weather_attributes, filter_and_order_columns



# Define file paths
dir_path = os.path.dirname(os.path.realpath(__file__))
traffic_path = os.path.join(dir_path, '../../Filtered_Traffic_Violations_2023.csv')
cities_path = os.path.join(dir_path, '../../Cities_Incomes.csv')
weather_path = os.path.join(dir_path, '../../Filtered_Weather_Data_2023.csv')
root_path = os.path.abspath(os.path.join(dir_path, '../../../'))

# Load data
traffic_df = pd.read_csv(traffic_path, encoding='cp1250', sep=',')
weather_df = pd.read_csv(weather_path, encoding='cp1250', sep=',')

traffic_df = traffic_df.drop_duplicates(subset='SeqID', keep='first')
traffic_df = filter_and_order_columns(traffic_df)
traffic_df = add_cityMedian(traffic_df, cities_path)

traffic_df = add_weather_attributes(traffic_df, weather_df)
traffic_df = add_time_category(traffic_df)

def get_traffic_violations():
    return traffic_df

def prepare_data_for_db():
    columns_to_insert = [
        "seq_id", "date_of_stop", "time_of_stop", "subagency", "description", "accident", "belts",
        "personal_injury", "property_damage", "fatal", "commercial_license", "hazmat",
        "commercial_vehicle", "alcohol", "search_conducted", "search_outcome", "vehicle_type",
        "year", "make", "model", "color", "violation_type", "charge", "contributed_to_accident",
        "race", "gender", "driver_city", "driver_state", "dl_state", "arrest_type", "cityMedian",
        "rain", "temperature", "wind"
    ]
    
    df = traffic_df.copy()
    df = df[columns_to_insert]
    
    # Convert DataFrame to a list of tuples, so that it can be inserted to SQL
    return [tuple(row) for row in df.itertuples(index=False)]


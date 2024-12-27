# This file is for demonstration of how the original csv from the source was prepared
# The repository contains already prepared data (because the source is too large - 3,15M rows)
# If you want to try it, you can download the data from the source - https://data.montgomerycountymd.gov/Environment/Dickerson-Weather-Station-Data/qp7x-aiq4/about_data

import os
import pandas as pd

# Define paths
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, '../../../'))
# Adjust file path so that it matches the downloaded traffic violations
data_path = os.path.join(dir_path, '../../../Dickerson_Weather_Station_Data.csv')

# Read the CSV file
df = pd.read_csv(data_path, encoding='cp1250', sep=',', low_memory=False)

# Convert 'Date Time' column to datetime format
df['Date Time'] = pd.to_datetime(df['Date Time'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

# Filter rows where the year is 2023
df_2023 = df[df['Date Time'].dt.year == 2023]

# Create a complete hourly time range from 01-04-2023 to 31-10-2023
hourly_time_range = pd.date_range(start="2023-04-01 00:00:00", end="2023-10-31 23:00:00", freq="H")

# Create a DataFrame with the complete time range
hourly_df = pd.DataFrame({'Date Time': hourly_time_range})

# Merge the weather data with the complete hourly time range
merged_df = pd.merge(hourly_df, df_2023, on='Date Time', how='left')

# Forward-fill missing weather data
merged_df[['SPD10-DK ', 'TMP10-DK ', 'DEW PT.  ', 'RAIN ']] = merged_df[['SPD10-DK ', 'TMP10-DK ', 'DEW PT.  ', 'RAIN ']].fillna(method='ffill')

# Sort the DataFrame by 'Date Time'
merged_df = merged_df.sort_values(by='Date Time')

# Save the complete hourly weather data to a CSV file
output_path = os.path.join(root_path, 'Filtered_Weather_Data_2023.csv')
merged_df.to_csv(output_path, index=False, sep=',')


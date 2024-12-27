# This file is for demonstration of how the original csv from the source was prepared
# The repository contains already prepared data (because the size before preparation is too large - 2M rows)
# If you want to try it, you can download the data from this source - https://data.montgomerycountymd.gov/Public-Safety/Traffic-Violations/4mse-ku6q/about_data

import os
import pandas as pd

# File paths
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(dir_path, '../../../'))
# Adjust file path so that it matches the downloaded traffic violations
traffic_path = os.path.join(dir_path, '../../../Traffic_Violations_20241218.csv')

# Read the CSV file
df = pd.read_csv(traffic_path, encoding='cp1250', sep=',')
df = df.drop_duplicates(subset='SeqID', keep='first')

df['Date Of Stop'] = pd.to_datetime(df['Date Of Stop'], format='%m/%d/%Y', errors='coerce')

# Define the date range for filtering (march 2023 data are too inconsistent, after 2023-10-30 there are no consistent data)
start_date = '2023-04-01'
end_date = '2023-10-30'

df_filtered = df[
    (df['Date Of Stop'] >= start_date) &
    (df['Date Of Stop'] <= end_date)
    #(df['Date Of Stop'].dt.month != 3)  # Exclude March because there are inconsistent weather data
]

# Save the filtered data to a new CSV file
output_path = os.path.join(root_path, 'Filtered_Traffic_Violations_2023.csv')
df_filtered.to_csv(output_path, index=False, sep=',')
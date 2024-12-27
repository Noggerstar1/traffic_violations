import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

from prepareData import prepare_data_for_db

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

sample_data = prepare_data_for_db()

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS traffic_violations (
        id SERIAL PRIMARY KEY,
        seq_id TEXT NOT NULL,
        date_of_stop TIMESTAMP NOT NULL,
        time_of_stop TEXT NOT NULL,
        subagency TEXT,
        description TEXT,
        accident TEXT,
        belts TEXT,
        personal_injury TEXT,
        property_damage TEXT,
        fatal TEXT,
        commercial_license TEXT,
        hazmat TEXT,
        commercial_vehicle TEXT,
        alcohol TEXT,
        search_conducted TEXT,
        search_outcome TEXT,
        vehicle_type TEXT,
        year TEXT,
        make TEXT,
        model TEXT,
        color TEXT,
        violation_type TEXT,
        charge TEXT,
        contributed_to_accident TEXT,
        race TEXT,
        gender TEXT,
        driver_city TEXT,
        driver_state TEXT,
        dl_state TEXT,
        arrest_type TEXT,
        cityMedian INT,
        rain FLOAT,
        temperature FLOAT,
        wind FLOAT
    );
    """
    cursor.execute(create_table_query)

    # Delete all data from the table
    cursor.execute("TRUNCATE TABLE traffic_violations;")

    insert_query = """
        INSERT INTO traffic_violations (
            seq_id,date_of_stop,time_of_stop,subagency,description,accident,belts,personal_injury,property_damage,
            fatal,commercial_license,hazmat,commercial_vehicle,alcohol,search_conducted,search_outcome,vehicle_type,year,
            make,model,color,violation_type,charge,contributed_to_accident,race,gender,driver_city,driver_state,dl_state,
            arrest_type,cityMedian,rain,temperature,wind)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Execute the insertion
    cursor.executemany(insert_query, sample_data)


    # Commit the transaction
    conn.commit()
    print("Table created (if it didn't exist), data deleted, and new data inserted successfully.")

except psycopg2.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()

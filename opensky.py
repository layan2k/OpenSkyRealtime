import pandas as pd
import requests
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

OPENSKY_API = os.getenv('OPENSKY_API')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

url = f'{OPENSKY_API}/states/all'

def fetch_data():
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
        exit(1)

    response.raise_for_status()

    data = response.json()['states']

    columns = ['icao24',
               'callsign',
               'origin_country',
               'time_position',
               'last_contact',
               'latitude',
               'longitude',
               'baro_altitude',
               'on_ground',
               'velocity',
               'true_track',
               'vertical_rate',
               'sensors',
               'geo_altitude',
               'squawk',
               'spi',
               'position_source'
               ]

    df = pd.DataFrame(data, columns=columns)


    df = df[[
        "icao24",
        "callsign",
        "origin_country",
        "time_position",
        "last_contact",
        "latitude",
        "longitude",
        "baro_altitude",
        "geo_altitude",
        "velocity"
    ]]

    df['time_position'] = pd.to_datetime(df['time_position'], unit='s')
    df['last_contact'] = pd.to_datetime(df['last_contact'], unit='s')

    df.dropna(subset=[
        'icao24',
        'last_contact',
        'latitude',
        'longitude'
    ])

    try:
        engine = create_engine(f'postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
        df.to_sql('flight_position',
                  engine,
                  if_exists='append',
                  index=False)
        print(f'{len(df)} rows inserted into PostgreSQL database')
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")
        exit(1)








from dagster import job, op, resource
import pandas as pd
from sqlalchemy import create_engine
import json
from pymongo import MongoClient
#import asyncpg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import pg8000

# PostgreSQL configuration as a resource
@resource(config_schema={
    'user': str,
    'password': str,
    'host': str,
    'port': str,
    'database': str
})
def postgres_resource(init_context):
    config = init_context.resource_config
    engine = create_engine(
        f"postgresql+psycopg://{config['postgres']}:{config['Password123']}@{config['localhost']}:{config['5432']}/{config['oil_data']}"
    )
    return engine

# Operation to load the data
@op
def load_data():
    file_path = 'D:/query_oil crude prices.json'  # Replace with your dataset
    try:
        # Load JSON data
        with open(file_path, 'r') as file:
          data = json.load(file)
    except Exception as e:
        raise Exception(f"Error loading dataset: {e}")

# Operation to clean the data
@op
def clean_data(data: pd.DataFrame):
    # Drop duplicates and handle missing values
    data = data.drop_duplicates()
    data = data.fillna(data.median(numeric_only=True))
    return data

# Operation to store data in PostgreSQL
@op(required_resource_keys={"postgres"})
def store_data(context, data: pd.DataFrame):
    engine = context.resources.postgres
    table_name = 'cleaned_data'  # Replace with your table name
    try:
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        context.log.info(f"Data stored successfully in table '{table_name}'.")
    except Exception as e:
        raise Exception(f"Error storing data: {e}")

# Define the pipeline job
@job(resource_defs={"postgres": postgres_resource})
def data_pipeline():
    data = load_data()
    cleaned_data = clean_data(data)
    store_data(cleaned_data)


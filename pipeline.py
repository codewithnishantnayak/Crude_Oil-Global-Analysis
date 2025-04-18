import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine
import plotly.graph_objects as go
import requests

def run_etl_pipeline():
    """Run the ETL pipeline."""
    # Fetch data
    api_url = "https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo"
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    if "data" not in data:
        raise ValueError("Unexpected API response format")

    raw_data = pd.DataFrame(data["data"])
    raw_data['value'] = pd.to_numeric(raw_data['value'], errors='coerce')
    raw_data['date'] = pd.to_datetime(raw_data['date'])
    cleaned_data = raw_data.dropna().sort_values(by='date')

    # Store preprocessed data in MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_collection = mongo_client["oil_data"]["preprocessed_data"]
    mongo_collection.delete_many({})
    mongo_collection.insert_many(cleaned_data.to_dict('records'))

    # Transform and save to PostgreSQL
    mongo_data = pd.DataFrame(list(mongo_collection.find({}, {'_id': 0})))
    mongo_data['value_normalized'] = (
        mongo_data['value'] - mongo_data['value'].min()
    ) / (mongo_data['value'].max() - mongo_data['value'].min())

    pg_conn_str = "postgresql://postgres:Password123@localhost:5432/oil_data"
    pg_engine = create_engine(pg_conn_str)
    mongo_data.to_sql("structured_data", pg_engine, if_exists="replace", index=False)

def fetch_visualization_data():
    """Fetch data from PostgreSQL for visualization."""
    pg_conn_str = "postgresql://postgres:Password123@localhost:5432/oil_data"
    pg_engine = create_engine(pg_conn_str)

    query = "SELECT * FROM structured_data"
    structured_data = pd.read_sql(query, pg_engine)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=structured_data['date'],
            y=structured_data['value'],
            mode='lines',
            name='Original Value',
            line=dict(color='blue', width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=structured_data['date'],
            y=structured_data['value_normalized'],
            mode='lines',
            name='Normalized Value',
            line=dict(color='green', width=2, dash='dot'),
        )
    )
    fig.update_layout(
        title="Brent Crude Oil Prices Over Time",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
    )

    return fig.to_html(full_html=False)

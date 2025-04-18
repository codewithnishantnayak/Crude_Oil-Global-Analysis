from flask import Flask
from .assets import register_assets
from .dagster_forecast_pipeline import load_dataset, forecast_next_10_days, forecasting_job, schedule


def create_app():
    """Application factory."""
    app = Flask(__name__)
    
    # Register assets
    register_assets(app)
    
    with app.app_context():
        # Import routes
        from . import routes
        return app

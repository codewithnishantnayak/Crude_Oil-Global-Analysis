from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
import logging
from logger import setup_logger
from app.routes import blueprint  # Import the blueprint for routes

# Initialize Flask app
def create_app():
    app = Flask(__name__)
         
    # Configuration for Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password123@localhost:5432/oil_data'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/oil_data'
    
    # Initialize SQLAlchemy
    db = SQLAlchemy(app)
    
    # Initialize PyMongo
    mongo = PyMongo(app)
    
    # Register Blueprints
    app.register_blueprint(blueprint)
    
    # Setup logger
    setup_logger(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

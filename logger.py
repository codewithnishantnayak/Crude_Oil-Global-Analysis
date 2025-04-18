import logging
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    # Create a file handler for logging
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=3)
    file_handler.setLevel(logging.INFO)
    
    # Create a console handler for logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Define the logging format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the Flask app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)
    
    # Log the startup message
    app.logger.info("Application startup complete.")

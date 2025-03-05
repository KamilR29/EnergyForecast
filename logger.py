import logging

def configure_logging():
    """
    Configure logging to log to both console and a file.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', mode='a')
    ])

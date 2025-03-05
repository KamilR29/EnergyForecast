"""
This module provides functions to load a model, make predictions, and generate future data
predictions using historical electricity prices.
"""

import glob
import logging
import os
from datetime import datetime

import pandas as pd
from autogluon.tabular import TabularPredictor

# Constants
FILE_PATH = 'data/electricity.csv'


def get_latest_model_path(directory):
    """
    Get the most recently modified folder in the specified directory.

    Args:
        directory (str): The directory to search for model folders.

    Returns:
        str: The path to the most recently modified folder.
    """
    folders = [f for f in glob.glob(os.path.join(directory, 'ag-*')) if os.path.isdir(f)]
    logging.info(f"Found {len(folders)} model folders")
    logging.info(folders)
    latest_folder = max(folders, key=os.path.getmtime)
    logging.info(f"Latest folder: {latest_folder}")
    return latest_folder


def load_model(model_path):
    """
    Load the saved model using AutoGluon.

    Args:
        model_path (str): The path to the saved model.

    Returns:
        TabularPredictor: The loaded prediction model.
    """
    logging.info(f"Loading model from {model_path}")
    return TabularPredictor.load(model_path)


def make_prediction(input_data, date_to, predictor):
    """
    Generate future rows with predicted values up to a specified date.

    Args:
        input_data (pd.DataFrame): The input data containing historical prices.
        date_to (datetime): The date up to which predictions should be made.
        predictor (TabularPredictor): The loaded prediction model.

    Returns:
        list: A list of dictionaries containing the combined original and predicted data.
    """
    if 'Date' in input_data.columns:
        input_data['Date'] = pd.to_datetime(input_data['Date'])

    last_date = input_data['Date'].max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), end=date_to, freq='MS')

    future_data = pd.DataFrame({'Date': future_dates})
    future_data = future_data.merge(
        input_data[['Country', 'ISO3 Code']].drop_duplicates(),
        how='cross'
    )

    combined_data = pd.concat([input_data, future_data], ignore_index=True)
    combined_data['Price (EUR/MWhe)'] = predictor.predict(
        combined_data.drop(columns=['Price (EUR/MWhe)'], errors='ignore'))

    return combined_data.to_dict(orient='records')


def generate_future_data(date_to):
    """
    Generate future data predictions up to a specified date.

    Args:
        date_to (datetime): The date up to which predictions should be made.

    Returns:
        list: A list of dictionaries containing the combined original and predicted data.
    """
    try:
        model_path = get_latest_model_path('AutogluonModels')
        predictor = load_model(model_path)
    except Exception as e:
        logging.error(f"Error loading model: {e}")

    try:
        data = pd.read_csv(FILE_PATH)
    except FileNotFoundError as e:
        logging.error(f"Error reading data file: {e}")

    return make_prediction(data, date_to, predictor)


def get_prices_for_country_predicted(country_name, data):
    """
    Get predicted prices for a specific country from the data.

    Args:
        country_name (str): The name of the country.
        data (list): The list of dictionaries containing the combined original and predicted data.

    Returns:
        list: A list of predicted prices for the specified country.
    """
    filtered_data = [round(entry['Price (EUR/MWhe)'], 2)
                     for entry in data if entry['Country'] == country_name]
    return filtered_data


def run(year, month, day, country):
    """
    Run the prediction process for a specific date and country.

    Args:
        year (int): The year of the target date.
        month (int): The month of the target date.
        day (int): The day of the target date.
        country (str): The name of the country.

    Returns:
        list: A list of predicted prices for the specified country.
    """
    predictions = generate_future_data(datetime(year, month, day))
    selected_country = country
    prices_predicted = get_prices_for_country_predicted(selected_country, predictions)

    return prices_predicted

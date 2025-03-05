"""
This module trains a model to predict electricity prices using AutoGluon.
"""
import logging

import pandas as pd
from autogluon.tabular import TabularPredictor

# Constants
FILE_PATH = 'data/electricity.csv'
TARGET = 'Price (EUR/MWhe)'

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except pd.errors.EmptyDataError:
        logging.error("Error: The file is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        logging.error("Error: The file could not be parsed.")
        return pd.DataFrame()
    except FileNotFoundError:
        logging.error("Error: The file was not found.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return pd.DataFrame()


def clean_data(df):
    """
    Clean the data by removing NaNs, duplicates, and normalizing numerical columns.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: Cleaned DataFrame.
    """
    df = df.dropna()
    df = df.drop_duplicates()

    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        lower_bound = df[col].quantile(0.01)
        upper_bound = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].mean()) / df[numerical_cols].std()
    return df


def split_data(df):
    """
    Split the data into training and testing sets.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    tuple: Training and testing DataFrames.
    """
    train = df.sample(frac=0.8, random_state=42)
    test = df.drop(train.index)
    return train, test


def main():
    """
    Main function to load data, clean it, split it, and train the model.
    """
    df = load_data(FILE_PATH)
    if df.empty:
        logging.error("Failed to load data.")
        return

    df = clean_data(df)
    train_data, test_data = split_data(df)

    predictor = TabularPredictor(label=TARGET, eval_metric='rmse').fit(train_data)
    predictor.evaluate(test_data)

    logging.info("Model training complete")


if __name__ == "__main__":
    main()

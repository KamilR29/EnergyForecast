"""
This module provides the main application logic for the Energy Forecast app.
It uses Streamlit for the web interface, and integrates with a prediction model
to forecast future electricity prices for various countries.
"""

from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from logger import configure_logging
from predictor import run

LOGO_PATH = "images/logo.png"

st.title("Energy Forecast")
load_dotenv()
llm = ChatOpenAI(model="gpt-4o")

countries = [
    "Austria", "Belgium", "Czechia", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece", "Hungary", "Italy",
    "Latvia", "Lithuania", "Luxembourg", "Netherlands", "Norway", "Poland", "Portugal", "Romania",
    "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland"
]
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def is_leap_year(year):
    """
    Check if a given year is a leap year.

    Args:
        year (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_month_number(month):
    """
    Convert a month name to its corresponding number.

    Args:
        month (str): The name of the month.

    Returns:
        int: The number of the month.
    """
    month_to_number = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return month_to_number[month]


def run_llm(predicted_prices, country):
    """
    Generate a response using a language model based on predicted prices.

    Args:
        predicted_prices (list): A list of predicted prices.
        country (str): The name of the country.

    Returns:
        None
    """
    lowest_price = min(predicted_prices)
    highest_price = max(predicted_prices)

    prompt = (
        f"Create an answer: In the specified time range, the predicted prices in {country} will range from "
        f"{lowest_price} to {highest_price}. I recommend installing photovoltaic panels or exploring other alternative "
        f"energy sources. List of other sources without description. Search online to find other sources. Return short information"
    )
    llm_response = llm.invoke(prompt)
    with st.sidebar.chat_message("assistant"):
        st.markdown(llm_response.content)


def generate_monthly_dates(start, end):
    """
    Generate a list of monthly dates between two dates.

    Args:
        start (datetime): The start date.
        end (datetime): The end date.

    Returns:
        list: A list of datetime objects representing the first day of each month in the range.
    """
    dates = []
    current_date = start
    while current_date <= end:
        dates.append(current_date)
        next_month = current_date.month + 1
        next_year = current_date.year + (next_month // 13)
        current_date = datetime(next_year, next_month % 12 or 12, 1)
    return dates

configure_logging()

selected_year = st.number_input("Enter a year:", min_value=2025, max_value=9999, value=2025, step=1)

selected_month = st.selectbox("Choose a month:", months)

selected_month_number = get_month_number(selected_month)

selected_country = st.selectbox("Choose a country:", countries)
st.sidebar.image(LOGO_PATH, width=150)
print(selected_year, selected_month_number, 1, selected_country)

start_date = datetime(2015, 1, 1)
end_date = datetime(selected_year, selected_month_number, 1)
date_range = generate_monthly_dates(start_date, end_date)

result = run(selected_year, selected_month_number, 1, selected_country)
print(result)

x_values = date_range

df = pd.DataFrame({
    "column1": x_values,
    "column2": result
})
df["column1"] = pd.to_datetime(df["column1"])

st.line_chart(df.set_index("column1")["column2"])
run_llm(result, selected_country)

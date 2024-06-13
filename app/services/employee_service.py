from datetime import date
from typing import Optional

import pandas as pd


def sales_by_employee(df: pd.DataFrame, start_date: date, end_date: date, key_employee: str) -> pd.DataFrame:
    """
    Filter sales data by employee within a given date range.

    Args:
        df (pd.DataFrame): The DataFrame containing sales data with columns 'KeyDate' and 'KeyEmployee'.
        start_date (date): The start date for the date range filter.
        end_date (date): The end date for the date range filter.
        key_employee (str): The key identifying the employee to filter by.

    Returns:
        pd.DataFrame: A DataFrame filtered to include only rows where the 'KeyDate' is within the specified date range
        and the 'KeyEmployee' matches the given key_employee.
    """
    # Filter the DataFrame based on the provided criteria
    return df[(df["KeyDate"] >= start_date) & (df["KeyDate"] <= end_date) & (df["KeyEmployee"] == key_employee)]

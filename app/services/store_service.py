from datetime import date
from typing import Union

import pandas as pd


def sales_by_store(df: pd.DataFrame, start_date: Union[date, str], end_date: Union[date, str], key_store: Union[int, str]) -> pd.DataFrame:
    """
    Filter sales data by store within a given date range.

    Args:
        df (pd.DataFrame): The DataFrame containing sales data with columns 'KeyDate' and 'KeyStore'.
        start_date (Union[date, str]): The start date for the date range filter.
        end_date (Union[date, str]): The end date for the date range filter.
        key_store (Union[int, str]): The key identifying the store to filter by.

    Returns:
        pd.DataFrame: A DataFrame filtered to include only rows where the 'KeyDate' is within the specified date range
        and the 'KeyStore' matches the given key_store.
    """

    # Filter the DataFrame based on the provided criteria
    return df[(df["KeyDate"] >= start_date) & (df["KeyDate"] <= end_date) & (df["KeyStore"] == key_store)]

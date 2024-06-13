from datetime import date
from typing import Union

import pandas as pd


def sales_by_product(df: pd.DataFrame, start_date: Union[date, str], end_date: Union[date, str], key_product: Union[int, str]) -> pd.DataFrame:
    """
    Filter sales data by product within a given date range.

    Args:
        df (pd.DataFrame): The DataFrame containing sales data with columns 'KeyDate' and 'KeyProduct'.
        start_date (Union[date, str]): The start date for the date range filter.
        end_date (Union[date, str]): The end date for the date range filter.
        key_product (Union[int, str]): The key identifying the product to filter by.

    Returns:
        pd.DataFrame: A DataFrame filtered to include only rows where the 'KeyDate' is within the specified date range
        and the 'KeyProduct' matches the given key_product.
    """

    # Filter the DataFrame based on the provided criteria
    return df[(df["KeyDate"] >= start_date) & (df["KeyDate"] <= end_date) & (df["KeyProduct"] == key_product)]

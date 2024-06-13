import os
from typing import Union

import pandas as pd
import os


def load_csv_file() -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame and convert the 'KeyDate' column to datetime.date type.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data with 'KeyDate' as datetime.date.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    file_name = os.environ.get("CSV_FILE_NAME", "celes.csv")
    csv_file_path = os.path.join(root_dir, "..", "..", file_name)

    df = pd.read_csv(csv_file_path)
    # Ensure KeyDate in the DataFrame is of type date
    print("the dataframe  ", df)
    print("the columns", df.columns)
    df["KeyDate"] = pd.to_datetime(df["KeyDate"]).dt.date
    return df


def get_mean_of_column(df: pd.DataFrame, key_store: Union[int, str], column: str) -> float:
    """
    Calculate the mean of the 'Amount' column for rows where the specified column matches the given key_store.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        key_store (Union[int, str]): The value to filter the specified column by.
        column (str): The column to filter by.

    Returns:
        float: The mean of the 'Amount' column for the filtered rows.
    """
    filtered_df = df[df[column] == key_store]
    return filtered_df["Amount"].mean()


def get_total_of_column(df: pd.DataFrame, key_store: Union[int, str], column: str) -> float:
    """
    Calculate the total (sum) of the 'Amount' column for rows where the specified column matches the given key_store.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        key_store (Union[int, str]): The value to filter the specified column by.
        column (str): The column to filter by.

    Returns:
        float: The total (sum) of the 'Amount' column for the filtered rows.
    """
    filtered_df = df[df[column] == key_store]
    return filtered_df["Amount"].sum()
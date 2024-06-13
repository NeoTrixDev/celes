import logging
from datetime import date
from datetime import datetime
from typing import Dict
from typing import List

import pandas as pd
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.employee_service import sales_by_employee
from app.services.product_service import sales_by_product
from app.services.store_service import sales_by_store
from app.utils.utils import get_mean_of_column
from app.utils.utils import get_total_of_column
from app.utils.utils import load_csv_file
from os import  environ

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the CSV file
df = load_csv_file()
app = FastAPI()

if not environ.get("IGNORE_AUTH_MIDDLEWARE", False):
    from app.middleware.auth import firebase_auth_middleware
    app.middleware("http")(firebase_auth_middleware)

auth_scheme = HTTPBearer()
@app.get("/sales-by-employee")
def retrieve_employee_by_sales(
    key_employee: str,
    start_date_str: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date_str: str = Query(..., description="End date in YYYY-MM-DD format"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> List[Dict]:
    """
    Retrieve sales data by employee within a given date range.

    Args:
        key_employee (str): The key identifying the employee.
        start_date_str (str): Start date in YYYY-MM-DD format.
        end_date_str (str): End date in YYYY-MM-DD format.

    Returns:
        List[Dict]: A list of dictionaries representing the sales data.

    Raises:
        HTTPException: If the date format is invalid or no data is found for the given criteria.
    """
    logger.info("Endpoint /sales-by-employee called with key_employee: %s, start_date: %s, end_date: %s", key_employee, start_date_str, end_date_str)
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error("Invalid date format: %s, %s", start_date_str, end_date_str)
        raise HTTPException(status_code=400, detail="Invalid date format. Please provide date in YYYY-MM-DD format.")

    result = sales_by_employee(df, start_date, end_date, key_employee)
    if result.empty:
        logger.error("No data found for key_employee: %s, date range: %s - %s", key_employee, start_date, end_date)
        raise HTTPException(status_code=404, detail="No data found for the given date range and key employee.")

    return result.to_dict(orient="records")


@app.get("/sales-by-product")
def retrieve_sales_by_product(
    key_product: str,
    start_date_str: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date_str: str = Query(..., description="End date in YYYY-MM-DD format"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> List[Dict]:
    """
    Retrieve sales data by product within a given date range.

    Args:
        key_product (str): The key identifying the product.
        start_date_str (str): Start date in YYYY-MM-DD format.
        end_date_str (str): End date in YYYY-MM-DD format.

    Returns:
        List[Dict]: A list of dictionaries representing the sales data.

    Raises:
        HTTPException: If the date format is invalid or no data is found for the given criteria.
    """
    logger.info("Endpoint /sales-by-product called with key_product: %s, start_date: %s, end_date: %s", key_product, start_date_str, end_date_str)
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error("Invalid date format: %s, %s", start_date_str, end_date_str)
        raise HTTPException(status_code=400, detail="Invalid date format. Please provide date in YYYY-MM-DD format.")

    result = sales_by_product(df, start_date, end_date, key_product)
    if result.empty:
        logger.error("No data found for key_product: %s, date range: %s - %s", key_product, start_date, end_date)
        raise HTTPException(status_code=404, detail="No data found for the given date range and key product.")

    return result.to_dict(orient="records")


@app.get("/sales-by-store")
def retrieve_sales_by_store(
    key_store: str,
    start_date_str: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date_str: str = Query(..., description="End date in YYYY-MM-DD format"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> List[Dict]:
    """
    Retrieve sales data by store within a given date range.

    Args:
        key_store (str): The key identifying the store.
        start_date_str (str): Start date in YYYY-MM-DD format.
        end_date_str (str): End date in YYYY-MM-DD format.

    Returns:
        List[Dict]: A list of dictionaries representing the sales data.

    Raises:
        HTTPException: If the date format is invalid or no data is found for the given criteria.
    """
    logger.info("Endpoint /sales-by-store called with key_store: %s, start_date: %s, end_date: %s", key_store, start_date_str, end_date_str)
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        logger.error("Invalid date format: %s, %s", start_date_str, end_date_str)
        raise HTTPException(status_code=400, detail="Invalid date format. Please provide date in YYYY-MM-DD format.")

    result = sales_by_store(df, start_date, end_date, key_store)
    if result.empty:
        logger.error("No data found for key_store: %s, date range: %s - %s", key_store, start_date, end_date)
        raise HTTPException(status_code=404, detail="No data found for the given date range and key store.")

    return result.to_dict(orient="records")


@app.get("/statistics-by-store")
def retrieve_statistics_by_store(key_store: str,  token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Dict:
    """
    Retrieve statistics for a specific store.

    Args:
        key_store (str): The key identifying the store.

    Returns:
        Dict: A dictionary containing the mean and total sales for the store.

    Raises:
        HTTPException: If no data is found for the given key store.
    """
    logger.info("Endpoint /statistics-by-store called with key_store: %s", key_store)
    mean_store = get_mean_of_column(df, key_store, "KeyStore")
    total_store = get_total_of_column(df, key_store, "KeyStore")

    if pd.isna(mean_store) or total_store == 0:
        logger.error("No data found for key_store: %s", key_store)
        raise HTTPException(status_code=404, detail="No data found for the given key store.")

    return {"keyStore": key_store, "meanStore": mean_store, "totalStore": total_store}


@app.get("/statistics-by-product")
def retrieve_statistics_by_product(key_product: str,     token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> Dict:
    """
    Retrieve statistics for a specific product.

    Args:
        key_product (str): The key identifying the product.

    Returns:
        Dict: A dictionary containing the mean and total sales for the product.

    Raises:
        HTTPException: If no data is found for the given key product.
    """
    logger.info("Endpoint /statistics-by-product called with key_product: %s", key_product)
    mean_product = get_mean_of_column(df, key_product, "KeyProduct")
    total_product = get_total_of_column(df, key_product, "KeyProduct")

    if pd.isna(mean_product) or total_product == 0:
        logger.error("No data found for key_product: %s", key_product)
        raise HTTPException(status_code=404, detail="No data found for the given key product.")

    return {"keyProduct": key_product, "meanProduct": mean_product, "totalProduct": total_product}


@app.get("/statistics-by-employee")
def retrieve_statistics_by_employee(key_employee: str,     token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> Dict:
    """
    Retrieve statistics for a specific employee.

    Args:
        key_employee (str): The key identifying the employee.

    Returns:
        Dict: A dictionary containing the mean and total sales for the employee.

    Raises:
        HTTPException: If no data is found for the given key employee.
    """
    logger.info("Endpoint /statistics-by-employee called with key_employee: %s", key_employee)
    mean_employee = get_mean_of_column(df, key_employee, "KeyEmployee")
    total_employee = get_total_of_column(df, key_employee, "KeyEmployee")

    if pd.isna(mean_employee) or total_employee == 0:
        logger.error("No data found for key_employee: %s", key_employee)
        raise HTTPException(status_code=404, detail="No data found for the given key employee.")

    return {"keyEmployee": key_employee, "meanEmployee": mean_employee, "totalEmployee": total_employee}
# CELES

## Overview

This API provides endpoints to retrieve sales data and statistics based on different criteria such as employees, products, and stores within specified date ranges. It uses FastAPI framework and integrates Firebase authentication middleware for secure access.

### Get started
To simulate the datamart, a csv file is being generated using pandas, to generate the file, you can run the following file located in the root's project.

```bash
python read_parquet_file.py 1s0irIrngQVeRDXY8F5gizkttG9Rqshg0
```

## Endpoints

![image](https://github.com/NeoTrixDev/test/assets/172324850/35fefb13-38e3-4cb5-8ed9-68bca39bdab9)


### Retrieve Sales Data

#### `GET /sales-by-employee`

Retrieve sales data by employee within a specified date range.

- **Parameters:**
  - `key_employee`: Key identifying the employee.
  - `start_date_str`: Start date in YYYY-MM-DD format.
  - `end_date_str`: End date in YYYY-MM-DD format.

#### `GET /sales-by-product`

Retrieve sales data by product within a specified date range.

- **Parameters:**
  - `key_product`: Key identifying the product.
  - `start_date_str`: Start date in YYYY-MM-DD format.
  - `end_date_str`: End date in YYYY-MM-DD format.

#### `GET /sales-by-store`

Retrieve sales data by store within a specified date range.

- **Parameters:**
  - `key_store`: Key identifying the store.
  - `start_date_str`: Start date in YYYY-MM-DD format.
  - `end_date_str`: End date in YYYY-MM-DD format.

### Retrieve Statistics

#### `GET /statistics-by-store`

Retrieve statistics for a specific store.

- **Parameters:**
  - `key_store`: Key identifying the store.

#### `GET /statistics-by-product`

Retrieve statistics for a specific product.

- **Parameters:**
  - `key_product`: Key identifying the product.

#### `GET /statistics-by-employee`

Retrieve statistics for a specific employee.

- **Parameters:**
  - `key_employee`: Key identifying the employee.


## Token Generation

To generate a token, open the index.html file within the web folder. Use email and password(those will be provided by email) to generate, now you have a token that you can use with your request. 

## Docker

To run the application using Docker, follow these steps:

1. **Build Docker Image:**
   ```bash
   docker build -t celes-app .
   docker run -d -p 8080:80 celes-app

The service will be available in http://localhost:8080/docs, remember to generate the token first and use the Authorize button in the swagger webapp.


## Local run 
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## Testing

Depending of your PYTHONENV configuration, please run the following command to setup the PYTHONPATH

```bash
export PYTHONPATH=$(pwd)
```
Once the PYTHONPATH is set, run pytest ton run the test. 
```bash
pytest
```

A similar output should be displayed.
![image](https://github.com/NeoTrixDev/test/assets/172324850/671a8763-ccdd-4abb-9cc0-3679d05cead9)

## To be Improved
- Poetry Integration: Consider using Poetry for better library management and dependency resolution.
- Docker Compose: Implement Docker Compose with a volume to enable the container to watch for file changes automatically.
- Enhanced UI: Develop a more sophisticated user interface to present data in a visually appealing and informative format.

# fastapi-api-project-


# Overview 

This Local REST API is designed to facilitate data migration and management with the following capabilities:

Data Upload: Receive and process historical data from CSV files.
Database Integration: Upload these files into a new database.
Batch Transactions: Allow batch insertion of 1 to 1000 rows in a single request.
Query-Based Data Insights:
Quarterly Hiring Report (2021): Retrieve the number of employees hired per job and department, grouped by quarters. The results are alphabetically ordered by department and job.
Above-Average Hiring Departments (2021): List department IDs, names, and employee counts for departments that hired more employees than the overall mean in 2021, ordered by employee count.


# development framework 

Framework: FastAPI – A modern, high-performance web framework for API development.
Server: Uvicorn – ASGI server to run FastAPI applications.
Database: SQLite – A lightweight, file-based database for development and testing.
ORM: SQLAlchemy – Object Relational Mapper for database operations.
Programming Language: Python.


# Repositorie content 

| **File/Folder**                      | **Description**                                                   |
|-------------------------------------|-------------------------------------------------------------------|
| `app/historical_data/`                  | Folder where CSV files are uploaded.                              |
| `app/main.py`                           | The entry point of the FastAPI application. 
  `app/models.py`                      | Defines the database models.                     |
| `app/queries.py`                        | Queries used for the endpoints.                                   |
| `app/session.py`                     | Contains database setup and SQLite interactions.                  |
| `app/test.db`                        | SQLite database file used in the project.                         |                                      |


# Api Enpoints
POST /upload_csv: Uploads a CSV file to the specified database table. The target table name must be provided in the request.
GET /get_hired_employees_2021: Retrieves the number of employees hired in 2021 per job and department, grouped by quarter, and sorted alphabetically by department and job.
GET /get_hired_employees_over_avg_2021: Returns the list of department IDs, names, and the number of employees hired for departments that hired more employees than the 2021 average, ordered by the number of employees hired.


# How to use 
FastAPI provides an interactive API documentation available at /docs when the server is running. Use this interface to test and interact with the API endpoints effortlessly.

To get started:

Run the application using Uvicorn.
Navigate to the interactive documentation in your browser.
Use the provided endpoints to upload data, run queries, and retrieve insights.

http://localhost:8000/docs#/


![alt text](img/image.png)


# Section 1 Use of upload_csv

![alt text](img/image-1.png)

Results 

![alt text](img/image-2.png)

![alt text](img/image-3.png)

![alt text](img/image-4.png)

# Section 2  Use of get_hired_employees_2021

![alt text](img/image-5.png)

Results 

![alt text](img/image-6.png)

# Section 2  Use of get_hired_employees_over_avg_2021
Results

![alt text](img/image-7.png)


# Documentation 

https://docs.python.org/3/library/venv.html
https://fastapi.tiangolo.com/


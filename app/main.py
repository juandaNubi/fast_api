from fastapi import FastAPI, UploadFile, File, HTTPException,Response
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from models import Base, Department, Job, Employee  # Import models
from seccion import engine,SessionLocal
from queries import HIRED_EMPLOYEES_2021,HIRED_EMPLOYEES_OVER_AVG_2021
import pandas as pd
import numpy as np
import os

# Directory where CSV files will be saved
UPLOAD_DIR = "historical_data"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

SCHEMAS = {
    "departments": {0: 'int64', 1: 'object'},
    "jobs": {0: 'int64', 1: 'object'},
    "hired_employees": {0: 'int64', 1: 'object', 2: 'object', 3: 'int64', 4: 'int64'}
}

def create_tables(): 
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)

def read_csv(file_path: str):
    """Read a CSV file into a DataFrame, ensuring all columns are read as strings."""
    return pd.read_csv(file_path, header=None, dtype=str)

def cast_dataframe_to_schema(data, schema):
    """Cast DataFrame columns to the types specified in the schema."""
    for col_index, col_type in schema.items():
        if col_type == 'int64':
            data[col_index] = pd.to_numeric(data[col_index], errors='raise')
        elif col_type == 'object':
            data[col_index] = data[col_index].astype(str)
    return data

def extract_column_types(model):
    """Extract expected column types from an SQLAlchemy model."""
    column_types = []
    for column in model.__table__.columns:
        if isinstance(column.type, Integer):
            column_types.append('int64')  # Pandas integer type
        elif isinstance(column.type, String):
            column_types.append('object')  # Pandas object type for strings
        elif isinstance(column.type, DateTime):
            column_types.append('object')  # Pandas datetime type (treat as object for simplicity)
        else:
            column_types.append(str(column.type))  # Handle other types as strings
    return column_types

def validate_csv_structure(data, expected_types):
    """Validate column count of CSV columns against SQLAlchemy."""
    if len(data.columns) != len(expected_types):
        raise HTTPException(status_code=400, detail="Column count mismatch between CSV and database table.")
    
    # Validate each column's data type in order
    for i, expected_type in enumerate(expected_types):
        actual_type = data.iloc[:, i].dtype  # Get the data type of the i-th column
        if str(actual_type) != expected_type:
            raise HTTPException(status_code=400, detail=f"Column {i+1} has incorrect type. Expected {expected_type}, got {actual_type}.")
        
def remove_empty_rows(data):
    """Remove rows with missing values and return the IDs of rows that were removed."""
    # Identify rows with missing values
    df_nulls = data[data.isnull().any(axis=1)]
    
    # Extract IDs of rows with missing values (assuming the first column is 'id')
    if not df_nulls.empty:
        id_nulls = df_nulls[0].to_list()  # Assuming first column (index 0) is the 'id'
        print(f"Rows with missing values were found and removed. IDs: {id_nulls}")
    else:
        id_nulls = []

    # Remove rows with missing values
    data.dropna(inplace=True)

    # Return cleaned data and the IDs of the removed rows
    return data, id_nulls

def split_dataframe(df, batch_size=1000):
    """Split a DataFrame into batches."""
    return np.array_split(df, np.ceil(len(df) / batch_size))

def insert_data_in_batches(session, table_class, data_batches, column_mapping):
    """Insert data in batches into the database."""
    for batch in data_batches:
        try:
            records = batch.to_dict(orient='records')
            for record in records:
                mapped_record = {column_mapping[i]: value for i, value in record.items()}
                obj = table_class(**mapped_record)
                session.add(obj)
            session.commit()  # Commit the transaction
        except Exception as e:
            session.rollback()  # Rollback in case of error
            raise HTTPException(status_code=500, detail=str(e))
        
def execute_query(query: str, engine) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a DataFrame.
    Args:
        query (str): SQL query to execute.
    """
    df = pd.read_sql(query, engine)
    return Response(df.to_json(orient="records"), media_type="application/json")   

def start_application():
    """Initialize the FastAPI application."""
    app = FastAPI()
    create_tables()

    @app.post("/upload/")
    async def upload_csv(table: str, file: UploadFile = File(...)):
        """Upload a CSV file to the specified table."""
        if table not in ["departments", "jobs", "hired_employees"]:
            raise HTTPException(status_code=400, detail="Invalid table name.")

        # Save the uploaded file locally
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        # Read the CSV file
        df = read_csv(file_location)

        # Remove rows with missing values before validation
        df_cleaned, removed_ids = remove_empty_rows(df)

        # Select the correct SQLAlchemy model based on the table name
        table_classes = {
            "departments": Department,
            "jobs": Job,
            "hired_employees": Employee
        }

        schemas = SCHEMAS[table]
        # Get the expected column types from the selected model
        expected_types = extract_column_types(table_classes[table])

        # Cast df_cleaned according to the schema
        df_cleaned = cast_dataframe_to_schema(df_cleaned, schemas)

        # Validate the data types in the CSV file (after removing empty rows)
        validate_csv_structure(df_cleaned, expected_types)

        # Column mapping based on the table
        column_mapping = {
            "departments": {0: 'id', 1: 'department'},
            "jobs": {0: 'id', 1: 'job'},
            "hired_employees": {0: 'id', 1: 'name', 2: 'datetime', 3: 'department_id', 4: 'job_id'}
        }

        # Split the data into batches
        data_batches = split_dataframe(df_cleaned)

        # Insert the cleaned data into the database
        session = SessionLocal()
        try:
            insert_data_in_batches(session, table_classes[table], data_batches, column_mapping[table])
        except HTTPException as e:
            session.rollback()
            raise e
        finally:
            session.close()

        # Return success message and list of removed rows (if any)
        return {"status": "success", "removed_rows_ids": removed_ids}
    
    @app.get("/get_hired_employees_2021")
    async def get_hired_employees_2021():
        query = HIRED_EMPLOYEES_2021  
        return execute_query(query, engine)
    
    @app.get("/get_hired_employees_over_AVG_2021")
    async def get_hired_employees_over_avg_2021():
        query = HIRED_EMPLOYEES_OVER_AVG_2021 
        return execute_query(query, engine)

    return app

app = start_application()

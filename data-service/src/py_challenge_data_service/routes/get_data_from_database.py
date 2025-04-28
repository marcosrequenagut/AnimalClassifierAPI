from fastapi import APIRouter
from dotenv import load_dotenv
import os
from py_challenge_data_service.utils import get_db_connection

# Creates a new instance of a router in FastAPI, which is
# used to define and organize a set of routes/endpoints in a modular way
router = APIRouter()

@router.get("/get_data_from_database", summary = "Get all stored animal data and predictions")
def get_data_from_databae():
    """
    This endpoint fetches all the stored animal data and their predictions from the database.
    """
    # Coneccting to the SQL Database
    connection = get_db_connection()

    # Create a "cursor" object, which is used to execute SQL queries
    cursor = connection.cursor()

    # Define the query
    query = """
    SELECT * FROM NEW_DATA
    """

    # Execute the query
    cursor.execute(query)

    # Get the data 
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    # Close the Database and stop the connection
    cursor.close()
    connection.close()

    return data
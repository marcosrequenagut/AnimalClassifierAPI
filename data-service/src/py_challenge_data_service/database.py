from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import oracledb

# Load the DB credentials
load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
sid = os.getenv("sid")


connection = oracledb.connect(user=USERNAME, password=PASSWORD, host=HOST, sid=sid)

cursor = connection.cursor()

connection.commit()
print("Succesfully Conexion")

cursor.close()

connection.close()

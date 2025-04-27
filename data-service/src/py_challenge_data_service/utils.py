import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
sid = os.getenv("sid")

def get_db_connection():
    return oracledb.connect(user=USERNAME, password=PASSWORD, host=HOST, sid=sid)
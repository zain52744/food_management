import mysql.connector

def create_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="F4d220190@"
    )

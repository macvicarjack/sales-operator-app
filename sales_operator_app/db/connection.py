from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2

def get_connection():
    """
    Get a connection to the PostgreSQL database using DATABASE_URL from environment variables.
    Returns:
        psycopg2.extensions.connection: PostgreSQL connection object
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    conn = psycopg2.connect(database_url)
    return conn

def close_connection(connection):
    """
    Close the database connection.
    Args:
        connection: Database connection to close
    """
    if connection:
        connection.close()

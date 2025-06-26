import os
import psycopg2

def get_connection():
    """
    Establish a connection to the PostgreSQL database using environment variables.
    Returns:
        psycopg2.extensions.connection: PostgreSQL connection object
    """
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        database=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        port=os.environ.get("POSTGRES_PORT", 5432)
    )
    return conn 
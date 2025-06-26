from dotenv import load_dotenv
import os
import psycopg2

# Load .env from project root (parent of db directory)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

def get_connection():
    """
    Establish a connection to the PostgreSQL database using DATABASE_URL from environment variables.
    Returns:
        psycopg2.extensions.connection: PostgreSQL connection object
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    conn = psycopg2.connect(database_url)
    return conn 
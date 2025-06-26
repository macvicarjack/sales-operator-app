from dotenv import load_dotenv
import os
import psycopg2

# Load .env from project root (parent of db directory)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

def get_connection():
    """
    Get a connection to the PostgreSQL database using DATABASE_URL from environment variables.
    Returns:
        psycopg2.extensions.connection: PostgreSQL connection object
    """
    database_url = os.getenv("DATABASE_URL")
    
    # Debug logging (without credentials)
    if database_url:
        # Extract host from URL for debugging (without credentials)
        try:
            if database_url.startswith('postgresql://'):
                host_part = database_url.split('@')[1].split('/')[0]
                print(f"🔧 Connecting to database host: {host_part}")
            else:
                print(f"🔧 Database URL format: {database_url[:20]}...")
        except:
            print("🔧 Database URL loaded (format check failed)")
    else:
        print("❌ DATABASE_URL environment variable is not set!")
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

import os
from dotenv import load_dotenv
import psycopg2

# Load .env from project root (parent of db directory)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Retrieve DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Fail loudly if DATABASE_URL is missing
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL not found. Make sure .env is loaded or Render env variable is set.")

def get_connection():
    """
    Establish a connection to the PostgreSQL database using DATABASE_URL from environment variables.
    Returns:
        psycopg2.extensions.connection: PostgreSQL connection object
    """
    try:
        # Use psycopg2.connect with DATABASE_URL
        conn = psycopg2.connect(DATABASE_URL)
        
        # Safe debug print - only log the host part
        host_part = DATABASE_URL.split('@')[-1].split('/')[0]
        print(f"✅ Connected to database: {host_part}")
        
        return conn
    except psycopg2.Error as e:
        print(f"❌ Database connection failed: {e}")
        raise RuntimeError(f"Failed to connect to database: {e}") 
import sqlite3
import os
from pathlib import Path

def get_connection():
    """
    Get a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    # Get the directory where this file is located
    db_dir = Path(__file__).parent
    
    # Create the database file path
    db_path = db_dir / "sales_operator.db"
    
    # Create connection with check_same_thread=False for Streamlit compatibility
    connection = sqlite3.connect(
        str(db_path),
        check_same_thread=False
    )
    
    # Enable foreign keys
    connection.execute("PRAGMA foreign_keys = ON")
    
    return connection

def close_connection(connection):
    """
    Close the database connection.
    
    Args:
        connection (sqlite3.Connection): Database connection to close
    """
    if connection:
        connection.close()

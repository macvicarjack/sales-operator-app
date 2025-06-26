"""
Pytest configuration and fixtures for Sales Operator tests.
Provides in-memory SQLite database setup for isolated testing.
"""

import pytest
import sqlite3
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from the app
sys.path.append(str(Path(__file__).parent.parent))

from db.connection import get_db_connection

@pytest.fixture
def test_db():
    """
    Create an in-memory SQLite database for testing.
    
    Returns:
        sqlite3.Connection: In-memory database connection
    """
    # Create in-memory database
    conn = sqlite3.connect(":memory:")
    
    # Load schema from schema.sql
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Execute schema to create tables
    conn.executescript(schema_sql)
    conn.commit()
    
    yield conn
    
    # Clean up
    conn.close()

@pytest.fixture
def test_db_connection(test_db):
    """
    Provide a test database connection that can be used by services.
    
    Returns:
        sqlite3.Connection: Configured test database connection
    """
    return test_db

@pytest.fixture
def sample_task_data():
    """
    Sample task data for testing.
    
    Returns:
        dict: Sample task data
    """
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "customer_name": "Test Customer",
        "customer_tier": "A",
        "potential_revenue": 1000.0,
        "type": "normal",
        "status": "open",
        "urgency": "high",
        "next_followup_date": "2024-01-15 10:00:00"
    }

@pytest.fixture
def sample_lead_data():
    """
    Sample lead data for testing.
    
    Returns:
        dict: Sample lead data
    """
    return {
        "name": "John Doe",
        "company": "Test Company",
        "email": "john@testcompany.com",
        "status": "new"
    } 
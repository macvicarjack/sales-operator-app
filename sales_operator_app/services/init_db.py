#!/usr/bin/env python3
"""
Database initialization script for Sales Operator.
Run this script to create the database and tables.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from db
sys.path.append(str(Path(__file__).parent.parent))

from db.connection import get_connection, close_connection

def init_db():
    schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
    with open(schema_path, "r") as f:
        schema = f.read()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(schema)
        conn.commit()
        print("✅ Database schema applied successfully!")
    except Exception as e:
        print(f"❌ Error applying schema: {e}")
        conn.rollback()
    finally:
        cur.close()
        close_connection(conn)

if __name__ == "__main__":
    print("🚀 Initializing Sales Operator Database...")
    print("=" * 50)
    
    init_db()
    
    print("\n🎉 Database setup complete!")
    print("You can now run your Streamlit app with: streamlit run app.py") 
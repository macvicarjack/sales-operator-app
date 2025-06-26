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

def init_database():
    """
    Initialize the database by reading and executing the schema file.
    """
    try:
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Read the schema file
        schema_file = Path(__file__).parent.parent / "db" / "schema.sql"
        
        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        print(f"📖 Reading schema from: {schema_file}")
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema SQL
        print("🔧 Creating database tables...")
        cursor.executescript(schema_sql)
        
        # Commit the changes
        conn.commit()
        
        # Verify the tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('leads', 'tasks')")
        tables = cursor.fetchall()
        
        created_tables = [table[0] for table in tables]
        
        if 'leads' in created_tables:
            print("✅ Database initialized successfully!")
            print("📊 Created table: leads")
            
            # Show leads table structure
            cursor.execute("PRAGMA table_info(leads)")
            columns = cursor.fetchall()
            print("\n📋 Leads table structure:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        if 'tasks' in created_tables:
            print("\n📊 Created table: tasks")
            
            # Show tasks table structure
            cursor.execute("PRAGMA table_info(tasks)")
            columns = cursor.fetchall()
            print("\n📋 Tasks table structure:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        if not created_tables:
            print("❌ Failed to create tables")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    finally:
        # Close the connection
        close_connection(conn)

if __name__ == "__main__":
    print("🚀 Initializing Sales Operator Database...")
    print("=" * 50)
    
    success = init_database()
    
    if success:
        print("\n🎉 Database setup complete!")
        print("You can now run your Streamlit app with: streamlit run app.py")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1) 
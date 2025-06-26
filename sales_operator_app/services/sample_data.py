#!/usr/bin/env python3
"""
Sample data script for Sales Operator.
Adds sample leads to the database for testing.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import from db
sys.path.append(str(Path(__file__).parent.parent))

from db.connection import get_connection

def add_sample_leads():
    """
    Add sample leads to the database for testing.
    """
    try:
        # Get database connection
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sample lead data
        sample_leads = [
            ("John Smith", "TechCorp Inc", "john.smith@techcorp.com", "new"),
            ("Sarah Johnson", "Innovate Solutions", "sarah.j@innovate.com", "contacted"),
            ("Mike Davis", "Global Enterprises", "mike.davis@global.com", "qualified"),
            ("Lisa Chen", "StartupXYZ", "lisa.chen@startupxyz.com", "converted"),
            ("David Wilson", "MegaCorp", "david.wilson@megacorp.com", "new"),
            ("Emily Brown", "Creative Agency", "emily.brown@creative.com", "contacted"),
            ("Alex Rodriguez", "Digital Dynamics", "alex.r@digital.com", "qualified"),
            ("Maria Garcia", "Future Tech", "maria.garcia@futuretech.com", "new"),
        ]
        
        # Insert sample leads (PostgreSQL: use %s)
        cursor.executemany(
            """
            INSERT INTO leads (name, company, email, status)
            VALUES (%s, %s, %s, %s)
            """,
            sample_leads
        )
        
        # Commit the changes
        conn.commit()
        
        print(f"✅ Added {len(sample_leads)} sample leads to the database!")
        
        # Show the added leads
        cursor.execute("SELECT name, company, email, status FROM leads ORDER BY created_at DESC LIMIT 5")
        recent_leads = cursor.fetchall()
        
        print("\n📋 Recent leads:")
        for lead in recent_leads:
            print(f"  - {lead[0]} from {lead[1]} — {lead[2]} — {lead[3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample leads: {e}")
        return False
    
    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 Adding Sample Leads to Database...")
    print("=" * 50)
    
    success = add_sample_leads()
    
    if success:
        print("\n🎉 Sample data added successfully!")
        print("You can now view the leads in your Streamlit app.")
    else:
        print("\n💥 Failed to add sample data!")
        sys.exit(1) 
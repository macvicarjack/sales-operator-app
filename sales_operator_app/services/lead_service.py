"""
Lead service for managing lead data in the Sales Operator app.
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from db.connection import get_connection

def get_all_leads() -> List[Dict[str, Any]]:
    """
    Fetch all leads from the database, ordered by creation date (newest first).
    
    Returns:
        List[Dict[str, Any]]: List of lead dictionaries with keys:
            - id: Lead ID
            - name: Lead name
            - company: Company name
            - email: Email address
            - status: Lead status
            - created_at: Creation timestamp
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Execute query to get all leads, ordered by creation date
        cursor.execute("""
            SELECT id, name, company, email, status, created_at 
            FROM leads 
            ORDER BY created_at DESC
        """)
        
        # Fetch all results
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        leads = []
        for row in rows:
            lead = {
                'id': row[0],
                'name': row[1],
                'company': row[2],
                'email': row[3],
                'status': row[4],
                'created_at': row[5]
            }
            leads.append(lead)
        
        return leads
        
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return []
    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()

def add_lead(name: str, company: str, email: str, status: str) -> bool:
    """
    Add a new lead to the database.
    
    Args:
        name (str): Lead name (required)
        company (str): Company name
        email (str): Email address
        status (str): Lead status
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate required fields
        if not name.strip():
            print("❌ Error: Name is required")
            return False
        
        # Log the parameters being passed into the SQL query
        print("🔧 Adding lead with parameters:")
        print(f"   name: {name}")
        print(f"   company: {company}")
        print(f"   email: {email}")
        print(f"   status: {status}")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Prepare values for insert
        values = (name.strip(), company.strip(), email.strip(), status)
        
        # Insert the new lead using parameterized SQL
        sql = """
            INSERT INTO leads (name, company, email, status)
            VALUES (%s, %s, %s, %s)
        """
        
        print(f"🔧 SQL Query: {sql.strip()}")
        print(f"🔧 Values: {values}")
        
        cursor.execute(sql, values)
        
        # Commit the changes
        conn.commit()
        
        print(f"✅ Successfully added lead: {name}")
        return True
        
    except Exception as e:
        print("❌ DB ERROR: Failed to add lead")
        print(f"❌ Error details: {e}")
        print(f"❌ Parameters that failed: name='{name}', company='{company}', email='{email}', status='{status}'")
        return False
    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()

def get_lead_by_id(lead_id: int) -> Dict[str, Any]:
    """
    Fetch a single lead by ID.
    
    Args:
        lead_id (int): The ID of the lead to fetch
        
    Returns:
        Dict[str, Any]: Lead dictionary or None if not found
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, name, company, email, status, created_at 
            FROM leads 
            WHERE id = %s
            """,
            (lead_id,)
        )
        
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'company': row[2],
                'email': row[3],
                'status': row[4],
                'created_at': row[5]
            }
        return None
        
    except Exception as e:
        print(f"Error fetching lead by id: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close() 
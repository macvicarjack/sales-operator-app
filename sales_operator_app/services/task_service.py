"""
Task service for managing tasks in the Sales Operator app.
"""

from db.postgres_connection import get_connection
from typing import List, Dict, Any
import datetime
from utils.config import (
    TIER_WEIGHTS,
    TASK_SCORE_WEIGHTS,
    DEFAULT_FOLLOWUP_DAYS,
    MAX_TASK_SCORE,
    MIN_TASK_SCORE
)

def add_task(data: dict) -> bool:
    """
    Insert a new task into the tasks table.
    Args:
        data (dict): Dictionary with keys matching the tasks schema.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Log the parameters being passed into the SQL query
        print("🔧 Adding task with parameters:")
        for key, value in data.items():
            print(f"   {key}: {value}")
        
        conn = get_connection()
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        values = list(data.values())
        sql = f"INSERT INTO tasks ({columns}) VALUES ({placeholders})"
        
        print(f"🔧 SQL Query: {sql}")
        print(f"🔧 Values: {values}")
        
        cursor.execute(sql, values)
        conn.commit()
        
        print(f"✅ Successfully added task with ID: {cursor.fetchone()[0] if cursor.description else 'unknown'}")
        return True
        
    except Exception as e:
        print("❌ DB ERROR: Failed to add task")
        print(f"❌ Error details: {e}")
        print(f"❌ Data that failed: {data}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def get_open_tasks() -> List[Dict[str, Any]]:
    """
    Return all tasks where status != 'done', ordered by next_followup_date (if present) or created_at.
    Returns:
        List[Dict[str, Any]]: List of open task dicts.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = '''
            SELECT * FROM tasks
            WHERE status != %s
            ORDER BY 
                CASE WHEN next_followup_date IS NOT NULL THEN next_followup_date ELSE created_at END ASC
        '''
        cursor.execute(sql, ('done',))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error fetching open tasks: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def get_quick_tasks() -> List[Dict[str, Any]]:
    """
    Return all quick tasks not marked as done, ordered by due_date.
    Returns:
        List[Dict[str, Any]]: List of quick task dicts.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = '''
            SELECT * FROM tasks
            WHERE type = %s AND status != %s
            ORDER BY due_date ASC
        '''
        cursor.execute(sql, ('quick', 'done'))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error fetching quick tasks: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

def mark_task_done(task_id: int) -> bool:
    """
    Set status = 'done' and completed_at = CURRENT_TIMESTAMP for a given task ID.
    Args:
        task_id (int): The ID of the task to mark as done.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = '''
            UPDATE tasks
            SET status = %s, completed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        '''
        cursor.execute(sql, ('done', task_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error marking task done: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def calculate_task_score(task: dict) -> float:
    """
    Calculate a score (0-100) for a task based on urgency and value.
    Args:
        task (dict): Task dictionary with keys matching the schema.
    Returns:
        float: Score between 0 and 100.
    """
    # Helper to parse dates
    def parse_date(val, date_only=False):
        if not val:
            return None
        try:
            if date_only:
                return datetime.datetime.strptime(val, "%Y-%m-%d").date()
            return datetime.datetime.fromisoformat(val)
        except Exception:
            return None

    now = datetime.datetime.now()
    today = now.date()

    # 1. Days since last action (weighted by TASK_SCORE_WEIGHTS["days_open"])
    last_action = parse_date(task.get("last_action_date"))
    if last_action:
        days_since_last = (now - last_action).days
    else:
        # If no last action, use created_at
        created_at = parse_date(task.get("created_at"))
        days_since_last = (now - created_at).days if created_at else 0
    # Cap at 10 days for normalization
    days_since_last = max(0, days_since_last)
    days_since_last_norm = min(days_since_last, 10) / 10  # 0 to 1
    last_action_score = days_since_last_norm * (MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["days_open"])

    # 2. Days until next follow-up (weighted by TASK_SCORE_WEIGHTS["next_followup"])
    next_followup = parse_date(task.get("next_followup_date"))
    if next_followup:
        days_until_followup = (next_followup - now).days
    else:
        days_until_followup = DEFAULT_FOLLOWUP_DAYS
    if days_until_followup < 0:
        # Overdue follow-up
        followup_score = MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["next_followup"]
    else:
        # 0 days = max score, 7+ days = 0
        followup_score = max(0, (MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["next_followup"]) - 
                           min(days_until_followup, 7) * ((MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["next_followup"]) / 7))

    # 3. Customer tier (weighted by TASK_SCORE_WEIGHTS["tier"])
    tier = (task.get("customer_tier") or "").upper()
    tier_weight = TIER_WEIGHTS.get(tier, 0)
    tier_score = (tier_weight / max(TIER_WEIGHTS.values())) * (MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["tier"])

    # 4. Potential revenue (weighted by TASK_SCORE_WEIGHTS["revenue"])
    try:
        revenue = float(task.get("potential_revenue") or 0)
    except Exception:
        revenue = 0
    
    # Normalize revenue to 0-1 scale (assuming max reasonable revenue is 50,000)
    max_reasonable_revenue = 50000
    revenue_normalized = min(revenue / max_reasonable_revenue, 1.0)
    revenue_score = revenue_normalized * (MAX_TASK_SCORE * TASK_SCORE_WEIGHTS["revenue"])

    # If status is waiting and next_followup_date is in the future, score = 0
    status = (task.get("status") or "").lower()
    if status == "waiting" and next_followup and next_followup > now:
        return MIN_TASK_SCORE

    total = last_action_score + followup_score + tier_score + revenue_score
    return float(max(MIN_TASK_SCORE, min(MAX_TASK_SCORE, total))) 
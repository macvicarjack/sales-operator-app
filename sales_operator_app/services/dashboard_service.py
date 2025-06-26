"""
Dashboard service for Sales Operator app.
Provides aggregated statistics and summary data for the dashboard.
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, Any, List
from services.task_service import get_open_tasks, calculate_task_score


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_task_summary() -> Dict[str, Any]:
    """
    Get a summary of task statistics for the dashboard.
    
    Returns:
        Dict[str, Any]: Dictionary containing task summary statistics:
            - total_open_tasks: Total number of open tasks
            - total_quick_tasks: Total number of quick tasks
            - tasks_due_today: Number of tasks due today
            - avg_score: Average score of scored tasks
    """
    try:
        # Get all open tasks
        open_tasks = get_open_tasks()
        
        if not open_tasks:
            return {
                "total_open_tasks": 0,
                "total_quick_tasks": 0,
                "tasks_due_today": 0,
                "avg_score": 0.0
            }
        
        today = date.today()
        total_open_tasks = len(open_tasks)
        total_quick_tasks = 0
        tasks_due_today = 0
        scored_tasks = []
        
        for task in open_tasks:
            # Count quick tasks
            if task.get('type') == 'quick':
                total_quick_tasks += 1
            
            # Check if task is due today
            due_date_str = task.get('due_date')
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    if due_date == today:
                        tasks_due_today += 1
                except (ValueError, TypeError):
                    pass  # Skip invalid dates
            
            # Calculate score for non-quick tasks (they get scored)
            if task.get('type') != 'quick':
                score = calculate_task_score(task)
                scored_tasks.append(score)
        
        # Calculate average score
        avg_score = sum(scored_tasks) / len(scored_tasks) if scored_tasks else 0.0
        
        return {
            "total_open_tasks": total_open_tasks,
            "total_quick_tasks": total_quick_tasks,
            "tasks_due_today": tasks_due_today,
            "avg_score": round(avg_score, 1)
        }
        
    except Exception as e:
        print(f"Error getting task summary: {e}")
        return {
            "total_open_tasks": 0,
            "total_quick_tasks": 0,
            "tasks_due_today": 0,
            "avg_score": 0.0
        }


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_lead_summary() -> Dict[str, Any]:
    """
    Get a summary of lead statistics for the dashboard.
    
    Returns:
        Dict[str, Any]: Dictionary containing lead summary statistics:
            - total_leads: Total number of leads
            - new_leads: Number of leads with 'new' status
            - qualified_leads: Number of leads with 'qualified' status
            - converted_leads: Number of leads with 'converted' status
    """
    try:
        from services.lead_service import get_all_leads
        
        leads = get_all_leads()
        
        if not leads:
            return {
                "total_leads": 0,
                "new_leads": 0,
                "qualified_leads": 0,
                "converted_leads": 0
            }
        
        total_leads = len(leads)
        new_leads = sum(1 for lead in leads if lead.get('status') == 'new')
        qualified_leads = sum(1 for lead in leads if lead.get('status') == 'qualified')
        converted_leads = sum(1 for lead in leads if lead.get('status') == 'converted')
        
        return {
            "total_leads": total_leads,
            "new_leads": new_leads,
            "qualified_leads": qualified_leads,
            "converted_leads": converted_leads
        }
        
    except Exception as e:
        print(f"Error getting lead summary: {e}")
        return {
            "total_leads": 0,
            "new_leads": 0,
            "qualified_leads": 0,
            "converted_leads": 0
        }


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_recent_activity() -> List[Dict[str, Any]]:
    """
    Get recent activity for the dashboard.
    
    Returns:
        List[Dict[str, Any]]: List of recent activities
    """
    try:
        open_tasks = get_open_tasks()
        
        if not open_tasks:
            return []
        
        # Sort by creation date (most recent first) and take top 5
        recent_tasks = sorted(
            open_tasks, 
            key=lambda x: x.get('created_at', ''), 
            reverse=True
        )[:5]
        
        activities = []
        for task in recent_tasks:
            activities.append({
                "type": "task_created",
                "title": task.get('title', 'Untitled Task'),
                "customer": task.get('customer_name', 'Unknown'),
                "date": task.get('created_at', ''),
                "description": f"New task created for {task.get('customer_name', 'Unknown')}"
            })
        
        return activities
        
    except Exception as e:
        print(f"Error getting recent activity: {e}")
        return []


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_performance_metrics() -> Dict[str, Any]:
    """
    Get performance metrics for the dashboard.
    
    Returns:
        Dict[str, Any]: Dictionary containing performance metrics:
            - completion_rate: Percentage of tasks completed
            - avg_response_time: Average response time in days
            - top_customers: List of top customers by task count
    """
    try:
        open_tasks = get_open_tasks()
        
        if not open_tasks:
            return {
                "completion_rate": 0.0,
                "avg_response_time": 0.0,
                "top_customers": []
            }
        
        # Calculate completion rate (this would need completed tasks too)
        # For now, we'll use a placeholder
        completion_rate = 75.0  # Placeholder
        
        # Calculate average response time
        response_times = []
        for task in open_tasks:
            created_at = task.get('created_at')
            last_action = task.get('last_action_date')
            
            if created_at and last_action:
                try:
                    created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    last_action_dt = datetime.fromisoformat(last_action.replace('Z', '+00:00'))
                    response_time = (last_action_dt - created).days
                    response_times.append(response_time)
                except (ValueError, TypeError):
                    pass
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        
        # Get top customers
        customer_task_counts = {}
        for task in open_tasks:
            customer = task.get('customer_name', 'Unknown')
            customer_task_counts[customer] = customer_task_counts.get(customer, 0) + 1
        
        top_customers = sorted(
            customer_task_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            "completion_rate": round(completion_rate, 1),
            "avg_response_time": round(avg_response_time, 1),
            "top_customers": [{"name": name, "task_count": count} for name, count in top_customers]
        }
        
    except Exception as e:
        print(f"Error getting performance metrics: {e}")
        return {
            "completion_rate": 0.0,
            "avg_response_time": 0.0,
            "top_customers": []
        } 
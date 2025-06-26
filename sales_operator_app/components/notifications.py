"""
Notifications component for Sales Operator app.
Provides reusable toast-style message functions for user feedback.
"""

import streamlit as st
from typing import Optional
from utils.session import get_state, set_state


def notify_success(message: str, duration: Optional[int] = None) -> None:
    """
    Display a success notification message.
    
    Args:
        message (str): The success message to display.
        duration (Optional[int]): Duration in seconds to show the message (None for persistent).
    """
    st.success(f"✅ {message}")
    
    # Store notification in session state for potential tracking
    notifications = get_state("notifications", [])
    notifications.append({
        "type": "success",
        "message": message,
        "timestamp": st.session_state.get("_timestamp", 0)
    })
    set_state("notifications", notifications[-10:])  # Keep last 10 notifications


def notify_info(message: str, duration: Optional[int] = None) -> None:
    """
    Display an info notification message.
    
    Args:
        message (str): The info message to display.
        duration (Optional[int]): Duration in seconds to show the message (None for persistent).
    """
    st.info(f"ℹ️ {message}")
    
    # Store notification in session state for potential tracking
    notifications = get_state("notifications", [])
    notifications.append({
        "type": "info",
        "message": message,
        "timestamp": st.session_state.get("_timestamp", 0)
    })
    set_state("notifications", notifications[-10:])  # Keep last 10 notifications


def notify_error(message: str, duration: Optional[int] = None) -> None:
    """
    Display an error notification message.
    
    Args:
        message (str): The error message to display.
        duration (Optional[int]): Duration in seconds to show the message (None for persistent).
    """
    st.error(f"❌ {message}")
    
    # Store notification in session state for potential tracking
    notifications = get_state("notifications", [])
    notifications.append({
        "type": "error",
        "message": message,
        "timestamp": st.session_state.get("_timestamp", 0)
    })
    set_state("notifications", notifications[-10:])  # Keep last 10 notifications


def notify_warning(message: str, duration: Optional[int] = None) -> None:
    """
    Display a warning notification message.
    
    Args:
        message (str): The warning message to display.
        duration (Optional[int]): Duration in seconds to show the message (None for persistent).
    """
    st.warning(f"⚠️ {message}")
    
    # Store notification in session state for potential tracking
    notifications = get_state("notifications", [])
    notifications.append({
        "type": "warning",
        "message": message,
        "timestamp": st.session_state.get("_timestamp", 0)
    })
    set_state("notifications", notifications[-10:])  # Keep last 10 notifications


def notify_task_completed(task_title: str) -> None:
    """
    Display a task completion notification.
    
    Args:
        task_title (str): The title of the completed task.
    """
    notify_success(f"Task '{task_title}' completed successfully!")


def notify_lead_added(lead_name: str) -> None:
    """
    Display a lead addition notification.
    
    Args:
        lead_name (str): The name of the added lead.
    """
    notify_success(f"Lead '{lead_name}' added successfully!")


def notify_form_error(field_name: str) -> None:
    """
    Display a form validation error notification.
    
    Args:
        field_name (str): The name of the field with an error.
    """
    notify_error(f"Please fill in the '{field_name}' field.")


def notify_database_error(operation: str) -> None:
    """
    Display a database operation error notification.
    
    Args:
        operation (str): The operation that failed (e.g., 'save', 'load', 'update').
    """
    notify_error(f"Failed to {operation} data. Please try again.")


def notify_network_error() -> None:
    """
    Display a network connectivity error notification.
    """
    notify_error("Network connection issue. Please check your internet connection.")


def notify_permission_denied() -> None:
    """
    Display a permission denied notification.
    """
    notify_error("You don't have permission to perform this action.")


def notify_data_loaded(count: int, data_type: str) -> None:
    """
    Display a data loaded notification.
    
    Args:
        count (int): Number of items loaded.
        data_type (str): Type of data loaded (e.g., 'tasks', 'leads').
    """
    notify_info(f"Loaded {count} {data_type} successfully.")


def notify_no_data(data_type: str) -> None:
    """
    Display a no data available notification.
    
    Args:
        data_type (str): Type of data that's not available (e.g., 'tasks', 'leads').
    """
    notify_info(f"No {data_type} found. Add some to get started!")


def clear_notifications() -> None:
    """
    Clear all stored notifications from session state.
    """
    set_state("notifications", [])


def get_notification_history() -> list:
    """
    Get the notification history from session state.
    
    Returns:
        list: List of recent notifications.
    """
    return get_state("notifications", [])


def show_notification_summary() -> None:
    """
    Display a summary of recent notifications (for debugging/admin purposes).
    """
    notifications = get_notification_history()
    
    if notifications:
        st.subheader("📋 Recent Notifications")
        for i, notification in enumerate(notifications[-5:], 1):  # Show last 5
            st.write(f"{i}. [{notification['type'].upper()}] {notification['message']}")
    else:
        st.info("No recent notifications.")


def notify_with_action(message: str, action_text: str, action_func, notification_type: str = "info") -> None:
    """
    Display a notification with an action button.
    
    Args:
        message (str): The notification message.
        action_text (str): Text for the action button.
        action_func: Function to call when action button is clicked.
        notification_type (str): Type of notification ('success', 'info', 'error', 'warning').
    """
    # Display the notification
    if notification_type == "success":
        st.success(f"✅ {message}")
    elif notification_type == "error":
        st.error(f"❌ {message}")
    elif notification_type == "warning":
        st.warning(f"⚠️ {message}")
    else:
        st.info(f"ℹ️ {message}")
    
    # Add action button
    if st.button(action_text, key=f"action_{hash(message)}"):
        action_func() 
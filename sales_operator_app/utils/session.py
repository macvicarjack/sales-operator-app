"""
Session state utility module for Sales Operator app.
Provides centralized session state management across pages.
"""

import streamlit as st
from typing import Any, Optional


def get_state(key: str, default: Any = None) -> Any:
    """
    Get a value from session state, or set it to default if missing.
    
    Args:
        key (str): The session state key to retrieve.
        default (Any): Default value to set if key is missing.
        
    Returns:
        Any: The current value from session state or the default value.
    """
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def set_state(key: str, value: Any) -> None:
    """
    Set a value in session state.
    
    Args:
        key (str): The session state key to set.
        value (Any): The value to store in session state.
    """
    st.session_state[key] = value


def reset_state(key: str) -> None:
    """
    Clear a key from session state.
    
    Args:
        key (str): The session state key to remove.
    """
    if key in st.session_state:
        del st.session_state[key]


def has_state(key: str) -> bool:
    """
    Check if a key exists in session state.
    
    Args:
        key (str): The session state key to check.
        
    Returns:
        bool: True if the key exists in session state, False otherwise.
    """
    return key in st.session_state


def get_state_safe(key: str, default: Any = None) -> Any:
    """
    Safely get a value from session state without setting a default.
    
    Args:
        key (str): The session state key to retrieve.
        default (Any): Default value to return if key is missing.
        
    Returns:
        Any: The current value from session state or the default value.
    """
    return st.session_state.get(key, default)


def clear_all_state() -> None:
    """
    Clear all session state.
    """
    st.session_state.clear()


def get_state_keys() -> list:
    """
    Get all session state keys.
    
    Returns:
        list: List of all session state keys.
    """
    return list(st.session_state.keys())


def set_multiple_state(**kwargs: Any) -> None:
    """
    Set multiple values in session state at once.
    
    Args:
        **kwargs: Key-value pairs to set in session state.
    """
    for key, value in kwargs.items():
        st.session_state[key] = value


def get_multiple_state(*keys: str, defaults: Optional[dict] = None) -> dict:
    """
    Get multiple values from session state.
    
    Args:
        *keys: Session state keys to retrieve.
        defaults (Optional[dict]): Dictionary of default values for keys.
        
    Returns:
        dict: Dictionary of key-value pairs from session state.
    """
    defaults = defaults or {}
    result = {}
    
    for key in keys:
        if key not in st.session_state:
            default_value = defaults.get(key, None)
            st.session_state[key] = default_value
        result[key] = st.session_state[key]
    
    return result


def reset_multiple_state(*keys: str) -> None:
    """
    Clear multiple keys from session state.
    
    Args:
        *keys: Session state keys to remove.
    """
    for key in keys:
        reset_state(key)


def toggle_state(key: str, default: bool = False) -> bool:
    """
    Toggle a boolean value in session state.
    
    Args:
        key (str): The session state key to toggle.
        default (bool): Default value if key is missing.
        
    Returns:
        bool: The toggled value.
    """
    current_value = get_state(key, default)
    new_value = not current_value
    set_state(key, new_value)
    return new_value


def increment_state(key: str, default: int = 0, step: int = 1) -> int:
    """
    Increment a numeric value in session state.
    
    Args:
        key (str): The session state key to increment.
        default (int): Default value if key is missing.
        step (int): Amount to increment by.
        
    Returns:
        int: The incremented value.
    """
    current_value = get_state(key, default)
    new_value = current_value + step
    set_state(key, new_value)
    return new_value


def append_to_list_state(key: str, value: Any, max_length: Optional[int] = None) -> list:
    """
    Append a value to a list in session state.
    
    Args:
        key (str): The session state key containing the list.
        value (Any): Value to append to the list.
        max_length (Optional[int]): Maximum length of the list.
        
    Returns:
        list: The updated list.
    """
    current_list = get_state(key, [])
    if not isinstance(current_list, list):
        current_list = []
    
    current_list.append(value)
    
    if max_length is not None and len(current_list) > max_length:
        current_list = current_list[-max_length:]
    
    set_state(key, current_list)
    return current_list


def remove_from_list_state(key: str, value: Any) -> list:
    """
    Remove a value from a list in session state.
    
    Args:
        key (str): The session state key containing the list.
        value (Any): Value to remove from the list.
        
    Returns:
        list: The updated list.
    """
    current_list = get_state(key, [])
    if isinstance(current_list, list) and value in current_list:
        current_list.remove(value)
        set_state(key, current_list)
    
    return current_list 
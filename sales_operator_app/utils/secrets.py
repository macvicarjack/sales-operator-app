"""
Secrets utility module for Sales Operator app.
Provides safe access to environment variables and secrets.
"""

import os
from typing import Optional


def get_secret(key: str) -> str:
    """
    Get a secret value from environment variables.
    
    Args:
        key (str): The environment variable key to retrieve.
        
    Returns:
        str: The value of the environment variable.
        
    Raises:
        ValueError: If the environment variable is missing.
    """
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


def get_secret_optional(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a secret value from environment variables with optional fallback.
    
    Args:
        key (str): The environment variable key to retrieve.
        default (Optional[str]): Default value if key is not found.
        
    Returns:
        Optional[str]: The value of the environment variable or default.
    """
    return os.environ.get(key, default)


def get_secret_with_fallback(key: str, fallback_key: str) -> str:
    """
    Get a secret value with a fallback key if the primary key is missing.
    
    Args:
        key (str): The primary environment variable key to retrieve.
        fallback_key (str): The fallback environment variable key.
        
    Returns:
        str: The value of the environment variable.
        
    Raises:
        ValueError: If both environment variables are missing.
    """
    value = os.environ.get(key)
    if value is not None:
        return value
    
    fallback_value = os.environ.get(fallback_key)
    if fallback_value is not None:
        return fallback_value
    
    raise ValueError(f"Missing required environment variables: {key} and {fallback_key}")


def is_secret_set(key: str) -> bool:
    """
    Check if an environment variable is set.
    
    Args:
        key (str): The environment variable key to check.
        
    Returns:
        bool: True if the environment variable is set, False otherwise.
    """
    return key in os.environ and os.environ[key] is not None


def get_database_url() -> str:
    """
    Get the database URL from environment variables.
    
    Returns:
        str: The database URL.
        
    Raises:
        ValueError: If DATABASE_URL environment variable is missing.
    """
    return get_secret("DATABASE_URL")


def get_api_key(service: str) -> str:
    """
    Get an API key for a specific service.
    
    Args:
        service (str): The service name (e.g., 'openai', 'sendgrid').
        
    Returns:
        str: The API key for the service.
        
    Raises:
        ValueError: If the API key environment variable is missing.
    """
    key_name = f"{service.upper()}_API_KEY"
    return get_secret(key_name) 
"""
validators.py

Provides common validation functions for user input.
"""

def validate_positive_int(value) -> bool:
    """
    Validates that the value is a non-negative integer.

    Args:
        value: Input value (usually a string or integer).
    Returns:
        bool: True if value is a non-negative integer, otherwise False.
    """
    try:
        i = int(value)
        return i >= 0
    except ValueError:
        return False

def validate_non_empty(value: str) -> bool:
    """
    Validates that the string is non-empty and not just whitespace.

    Args:
        value (str): The string to validate.
    Returns:
        bool: True if the string contains non-whitespace characters, otherwise False.
    """
    return bool(value and value.strip())

def validate_email(value: str) -> bool:
    """
    Checks whether the input value is formatted like an email address.

    Args:
        value (str): Email string to validate.
    Returns:
        bool: True if the string resembles an email address, False otherwise.
    """
    if not validate_non_empty(value):
        return False
    if "@" in value and "." in value.split("@")[-1]:
        return True
    return False

def validate_date(value: str) -> bool:
    """
    Validates whether the input string is a valid ISO date (YYYY-MM-DD).

    Args:
        value (str): Date string in ISO format.
    Returns:
        bool: True if the string is a valid ISO date, otherwise False.
    """
    from datetime import datetime
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False

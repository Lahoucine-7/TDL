# utils/validators.py

def validate_positive_int(value):
    try:
        i = int(value)
        return i >= 0
    except ValueError:
        return False

def validate_non_empty(value):
    return bool(value and value.strip())

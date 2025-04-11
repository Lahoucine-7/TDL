"""
grid_config.py

Defines a common grid configuration dictionary that standardizes column weights,
minimum sizes, and spacing for task table components. This configuration is used in
various components (e.g., task rows and table headers) to ensure consistent layout.
"""

COMMON_GRID_CONFIG = {
    0: {"weight": 0, "minsize": 30},    # Checkbox column (fixed small size)
    1: {"weight": 0, "minsize": 1},     # Separator column
    2: {"weight": 10, "minsize": 150},  # Title column (expandable)
    3: {"weight": 0, "minsize": 1},     # Separator column
    4: {"weight": 1, "minsize": 100},   # Project column (expandable)
    5: {"weight": 0, "minsize": 1},     # Separator column
    6: {"weight": 1, "minsize": 100},   # Status column (expandable)
    7: {"weight": 0, "minsize": 1},     # Separator column
    8: {"weight": 1, "minsize": 50},    # Priority column (expandable)
    9: {"weight": 0, "minsize": 1},     # Separator column
    10: {"weight": 1, "minsize": 50},   # Due date column (expandable)
    11: {"weight": 0, "minsize": 1},    # Separator column
    12: {"weight": 1, "minsize": 120},  # Last update column (expandable)
    13: {"weight": 0},                 # Button for details (fixed)
    14: {"weight": 0}                  # Button for deletion (fixed)
}

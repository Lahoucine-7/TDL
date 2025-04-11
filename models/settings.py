"""
settings.py

Defines the Setting model using a dataclass. This model represents a user-specific
setting in the application, storing key-value pairs along with creation and update timestamps.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Setting:
    id: Optional[int] = None              # Unique identifier for the setting.
    user_id: int = 0                      # Associated user's identifier.
    key: str = ""                         # The key/name of the setting.
    value: str = ""                       # The value for the setting.
    created_at: Optional[str] = None      # ISO-formatted creation timestamp.
    updated_at: Optional[str] = None      # ISO-formatted last update timestamp.

    def __str__(self) -> str:
        """
        Provides a string representation of the setting.

        Returns:
            str: A formatted string displaying the setting id, user id, key, and value.
        """
        return f"Setting({self.id}, User {self.user_id}, {self.key}: {self.value})"

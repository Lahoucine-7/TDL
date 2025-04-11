"""
user.py

Defines the User model using a dataclass. This model represents a user in the application
and includes fields for user identification, username, email address, password (hash),
display theme, and timestamps such as creation, update, and last login.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None           # Unique user identifier.
    username: str = ""                 # Username.
    email: str = ""                    # User's email address.
    password: str = ""                 # User's password (hashed version recommended).
    theme: str = "dark"                # Preferred display theme; defaults to "dark".
    created_at: Optional[str] = None   # ISO timestamp for when the user was created.
    updated_at: Optional[str] = None   # ISO timestamp for the last update.
    last_login: Optional[str] = None   # ISO timestamp for the last login.

    def __str__(self) -> str:
        """
        Returns a string representation of the user.

        Returns:
            str: A formatted string displaying the user id and username.
        """
        return f"User({self.id}, {self.username})"

# models/user.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password: str = ""
    theme: str = "dark"

    def __str__(self):
        return f"User({self.id}, {self.username})"

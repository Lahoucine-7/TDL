"""
project.py

Defines the Project model using a dataclass. This model represents a project
in the application and includes fields such as id, name, description, creation
and update timestamps, as well as optional fields for color, icon, and ordering.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: Optional[int] = None              # Unique project identifier.
    name: str = ""                        # Name of the project.
    description: str = ""                 # Detailed description of the project.
    created_at: Optional[str] = None      # ISO-formatted creation timestamp.
    updated_at: Optional[str] = None      # ISO-formatted last update timestamp.
    color: Optional[str] = None           # Optional color code for project display.
    icon: Optional[str] = None            # Optional path to an icon representing the project.
    position: Optional[int] = None        # Optional display position or ordering.

    def __str__(self) -> str:
        """
        String representation of a project.
        
        Returns:
            str: A formatted string with project id and name.
        """
        return f"Project({self.id}, {self.name})"

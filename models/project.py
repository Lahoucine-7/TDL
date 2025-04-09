# models/project.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: Optional[int] = None
    name: str = ""
    description: str = ""

    def __str__(self):
        return f"Project({self.id}, {self.name})"

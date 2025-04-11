"""
subtask.py

Defines the Subtask model using a dataclass. A Subtask represents a smaller unit of work,
which is associated with a main task. It includes fields for id, parent task identifier,
title, description, and completion status.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Subtask:
    id: Optional[int] = None          # Unique identifier of the subtask.
    task_id: int = 0                  # Identifier of the parent task.
    title: str = ""                   # Title of the subtask.
    description: Optional[str] = None # Optional detailed description.
    done: bool = False                # Boolean flag to indicate completion.

    def __str__(self) -> str:
        """
        String representation of a subtask.
        
        Returns:
            str: A formatted string with subtask id, title, and status.
        """
        return f"Subtask({self.id}, {self.title}, done={self.done})"

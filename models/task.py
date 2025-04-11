"""
task.py

Defines the Task model using a dataclass. This model represents a task in the application,
including fields such as id, title, description, timestamps (creation, update, due date),
time, duration, priority, status, completion flag, associated project, and a list of subtasks.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from models.subtask import Subtask

@dataclass
class Task:
    id: Optional[int] = None               # Unique identifier of the task.
    title: str = ""                        # Title of the task.
    description: str = ""                  # Detailed description.
    created_at: Optional[str] = None       # ISO timestamp of creation.
    updated_at: Optional[str] = None       # ISO timestamp of the last update.
    due_date: Optional[str] = None         # Due date in ISO format.
    time: Optional[str] = None             # Specific time (if applicable).
    duration: Optional[int] = None         # Estimated duration in minutes.
    priority: Optional[str] = None         # Priority level (e.g., "low", "medium", "high").
    status: Optional[str] = None           # Current status (e.g., "not started", "in progress", "completed").
    done: bool = False                     # Boolean flag indicating whether the task is completed.
    project_id: Optional[int] = None       # Associated project's identifier.
    subtasks: List[Subtask] = field(default_factory=list)  # List of associated subtasks.

    def __str__(self) -> str:
        """
        String representation of the task.

        Returns:
            str: A formatted string with task id and title. If the task is done, its title is marked accordingly.
        """
        if self.done:
            return f"~~Task({self.id}, {self.title})~~"
        return f"Task({self.id}, {self.title})"

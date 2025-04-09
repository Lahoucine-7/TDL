# models/task.py

from dataclasses import dataclass, field
from typing import List, Optional
from models.subtask import Subtask

@dataclass
class Task:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[int] = None
    done: bool = False
    project_id: Optional[int] = None
    subtasks: List[Subtask] = field(default_factory=list)

    def __str__(self):
        if self.done:
            return f"~~Task({self.id}, {self.title})~~"
        return f"Task({self.id}, {self.title})"

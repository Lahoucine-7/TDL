# models/task.py

from dataclasses import dataclass, field
from typing import List, Optional
from models.subtask import Subtask

@dataclass
class Task:
    key: Optional[int] = None
    title: str = ""
    description: str = ""
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[int] = None
    done: bool = False
    subtasks: List[Subtask] = field(default_factory=list)

    def __str__(self):
        if self.done:
            return f"~~Task({self.key}, {self.title})~~"
        return f"Task({self.key}, {self.title})"

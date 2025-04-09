# models/subtask.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Subtask:
    id: Optional[int] = None
    task_id: int = 0
    title: str = ""
    description: Optional[str] = None
    done: bool = False

    def __str__(self):
        return f"Subtask({self.id}, {self.title}, done={self.done})"

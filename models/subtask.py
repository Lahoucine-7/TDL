# models/subtask.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Subtask:
    key: Optional[int] = None
    task_key: int = 0
    title: str = ""
    description: Optional[str] = None
    done: bool = False

    def __str__(self):
        return f"Subtask({self.key}, {self.title}, done={self.done})"

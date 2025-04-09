# models/settings.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Setting:
    id: Optional[int] = None
    user_id: int = 0
    key: str = ""
    value: str = ""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Task:
    id: int
    title: str
    status: Literal['active', 'completed'] = 'active'

from dataclasses import dataclass
from typing import Any


@dataclass
class DataObject:
    name: str
    category: str
    visualized: bool
    data: Any

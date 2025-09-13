from dataclasses import dataclass
from src.datatypes.animation import Animation
from typing import List

@dataclass
class Dialog:
    Text: str
    Character_Dir: str
    Italic: bool = False
    Bold: bool = False
    Animations: List[Animation] = None

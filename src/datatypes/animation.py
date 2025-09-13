from dataclasses import dataclass
from typing import Callable, Tuple
import pygame
from src.animation.protocol import Animatable

@dataclass
class Animation:
    AnimateObj: Animatable
    Position: Tuple[int, int] = (0, 0)
    Scale: float = 1
    
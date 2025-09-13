from dataclasses import dataclass
from cv2.typing import Scalar

@dataclass
class Confetti:
    PosX: int
    PosY: str
    Color: Scalar
    Speed: int

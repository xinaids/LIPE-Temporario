from dataclasses import dataclass

@dataclass
class Player:
    Id: int
    Name: str | None
    Team: str = ""
    Movements: list[int] | None = None
    Active: bool = True

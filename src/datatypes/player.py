from dataclasses import dataclass

@dataclass
class Player:
    Id: int
    Name: str | None
    Age: int | None
    Team: str
    Movements: list[int] | None
    Active: bool
    
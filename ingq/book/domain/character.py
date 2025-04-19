from dataclasses import dataclass


@dataclass
class Character:
    name: str
    age: int
    gender: str
    characteristic: list[str]

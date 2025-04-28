from dataclasses import dataclass


@dataclass
class Character:
    grammatical_person: str
    historical_background: str
    name: str
    age: int
    gender: str
    characteristic: list[str]

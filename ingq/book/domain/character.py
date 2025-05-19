from dataclasses import dataclass


@dataclass
class Character:
    grammatical_person: str
    historical_background: str
    name: str
    age: str
    gender: str
    characteristic: str

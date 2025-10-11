from dataclasses import dataclass
from typing import Optional

@dataclass
class RegisteredStudent:
    id: Optional[str]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    gender: str
    birth_date: str
    age: int
    contact: str
    guardian_name: str
    guardian_contact: str

@dataclass
class EnrolledStudent:
    id: str
    grade_level: str
    strand: str

"""
Staff Entity - Core business object
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Staff:
    """Staff entity representing a bookstore staff member"""
    id: Optional[int] = None
    name: str = ""
    role: str = ""

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role
        }

"""
Customer Entity - Core business object
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer entity representing a bookstore customer"""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password: str = ""

    def validate(self) -> bool:
        """Validate customer data"""
        if not self.name or len(self.name) < 2:
            raise ValueError("Name must be at least 2 characters")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        if not self.password or len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        return True

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

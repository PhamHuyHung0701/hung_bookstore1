"""
Rating Entity - Core business object
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Rating:
    """Rating entity representing a customer rating for a book"""
    customer_id: int
    book_id: int
    score: int

    def to_dict(self) -> dict:
        """Convert entity to dictionary"""
        return {
            'customer_id': self.customer_id,
            'book_id': self.book_id,
            'score': self.score
        }

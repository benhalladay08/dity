from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class BaseMapper(ABC, Generic[T]):
    """Abstract base class for all mappers in the DIT project."""

    @abstractmethod
    def to_dict(self, obj: T) -> dict:
        """Convert an object to a dictionary representation."""
        pass

    @abstractmethod
    def from_dict(self, data: dict) -> T:
        """Create an object from a dictionary representation."""
        pass

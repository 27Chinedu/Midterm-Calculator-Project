"""
Operation classes and factory for the calculator application.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
from app.exceptions import OperationError, DivisionByZeroError

class Operation(ABC):
    """Abstract base class for calculator operations."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the operation on two operands."""
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        """Get the symbol representing this operation."""
        pass

class AddOperation(Operation):
    """Addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a + b
    
    def get_symbol(self) -> str:
        return "+"




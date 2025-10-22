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

class SubtractOperation(Operation):
    """Subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a - b
    
    def get_symbol(self) -> str:
        return "-"

class MultiplyOperation(Operation):
    """Multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        return a * b
    
    def get_symbol(self) -> str:
        return "*"

class DivideOperation(Operation):
    """Division operation."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return a / b
    
    def get_symbol(self) -> str:
        return "/"

class PowerOperation(Operation):
    """Power operation."""
    
    def execute(self, a: float, b: float) -> float:
        try:
            return a ** b
        except (OverflowError, ValueError) as e:
            raise OperationError(f"Power operation failed: {e}")
    
    def get_symbol(self) -> str:
        return "^"

class RootOperation(Operation):
    """Root operation (a^(1/b))."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate root with zero index")
        try:
            if a < 0 and b % 2 == 0:
                raise OperationError("Cannot calculate even root of negative number")
            return a ** (1/b)
        except (OverflowError, ValueError) as e:
            raise OperationError(f"Root operation failed: {e}")
    
    def get_symbol(self) -> str:
        return "√"

class ModulusOperation(Operation):
    """Modulus operation."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate modulus with zero divisor")
        return a % b
    
    def get_symbol(self) -> str:
        return "%"

class IntegerDivideOperation(Operation):
    """Integer division operation."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return float(int(a // b))
    
    def get_symbol(self) -> str:
        return "//"

class PercentageOperation(Operation):
    """Percentage calculation (a/b * 100)."""
    
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot calculate percentage with zero base")
        return (a / b) * 100
    
    def get_symbol(self) -> str:
        return "%%"




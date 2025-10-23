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
            if b < 0:
                raise OperationError("Cannot calculate root with negative degree")
            
            # Handle negative bases with odd roots properly
            if a < 0 and b % 2 == 1:
                # For odd roots of negative numbers, we can compute directly
                result = -((-a) ** (1/b))
            else:
                result = a ** (1/b)
            
            # Check for complex results
            if isinstance(result, complex):
                raise OperationError("Result is complex number")
                
            return result
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

class AbsoluteDifferenceOperation(Operation):
    """Absolute difference operation."""
    
    def execute(self, a: float, b: float) -> float:
        return abs(a - b)
    
    def get_symbol(self) -> str:
        return "|a-b|"

class OperationFactory:
    """Factory class for creating operation instances."""
    
    _operations: Dict[str, Type[Operation]] = {
        'add': AddOperation,
        'subtract': SubtractOperation,
        'multiply': MultiplyOperation,
        'divide': DivideOperation,
        'power': PowerOperation,
        'root': RootOperation,
        'modulus': ModulusOperation,
        'int_divide': IntegerDivideOperation,
        'percent': PercentageOperation,
        'abs_diff': AbsoluteDifferenceOperation
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        """Create an operation instance by name."""
        operation_class = cls._operations.get(operation_name.lower())
        if not operation_class:
            raise OperationError(f"Unknown operation: {operation_name}")
        return operation_class()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Get list of available operation names."""
        return list(cls._operations.keys())



"""
Calculation class to represent a single calculation.
"""

from datetime import datetime
from typing import Optional

class Calculation:
    """Represents a single calculation with operation and operands."""
    
    def __init__(self, operation: str, operand1: float, operand2: float, 
                 result: float, timestamp: Optional[datetime] = None):
        """
        Initialize a Calculation.
        
        Args:
            operation: The operation performed
            operand1: First operand
            operand2: Second operand
            result: Result of the calculation
            timestamp: When the calculation was performed
        """
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self) -> str:
        """String representation of the calculation."""
        return f"{self.operand1} {self.operation} {self.operand2} = {self.result}"
    
    def __repr__(self) -> str:
        """Detailed representation of the calculation."""
        return (f"Calculation(operation='{self.operation}', "
                f"operand1={self.operand1}, operand2={self.operand2}, "
                f"result={self.result}, timestamp={self.timestamp})")
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary."""
        return {
            'operation': self.operation,
            'operand1': self.operand1,
            'operand2': self.operand2,
            'result': self.result,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Calculation':
        """Create Calculation from dictionary."""
        return cls(
            operation=data['operation'],
            operand1=float(data['operand1']),
            operand2=float(data['operand2']),
            result=float(data['result']),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
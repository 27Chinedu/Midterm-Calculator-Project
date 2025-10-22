"""
Input validation utilities for the calculator application.
"""

from typing import Tuple, Optional
from app.calculator_config import config
from app.exceptions import ValidationError

class InputValidator:
    """Validates user inputs for the calculator."""
    
    @staticmethod
    def validate_number(value: str, param_name: str = "value") -> float:
        """
        Validate and convert string to float.
        
        Args:
            value: String to validate
            param_name: Name of parameter for error messages
            
        Returns:
            Validated float value
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            num = float(value)
        except ValueError:
            raise ValidationError(f"{param_name} must be a number, got: {value}")
        
        if abs(num) > config.max_input_value:
            raise ValidationError(
                f"{param_name} exceeds maximum allowed value "
                f"({config.max_input_value})"
            )
        
        return num
    
    @staticmethod
    def validate_operation(operation: str) -> str:
        """
        Validate operation name.
        
        Args:
            operation: Operation name to validate
            
        Returns:
            Validated operation name
            
        Raises:
            ValidationError: If operation is invalid
        """
        from .operations import OperationFactory
        
        valid_operations = OperationFactory.get_available_operations()
        if operation.lower() not in valid_operations:
            raise ValidationError(
                f"Invalid operation: {operation}. "
                f"Valid operations: {', '.join(valid_operations)}"
            )
        
        return operation.lower()
    
    @staticmethod
    def parse_calculation_input(user_input: str) -> Tuple[str, Optional[float], Optional[float]]:
        """
        Parse user input for calculation command.
        
        Args:
            user_input: User input string
            
        Returns:
            Tuple of (operation, operand1, operand2)
            
        Raises:
            ValidationError: If parsing fails
        """
        parts = user_input.strip().split()
        
        if len(parts) < 1:
            raise ValidationError("No command provided")
        
        operation = parts[0].lower()
        
        # Check if it's a calculation operation
        from app.operations import OperationFactory
        valid_operations = OperationFactory.get_available_operations()
        
        if operation not in valid_operations:
            return operation, None, None
        
        if len(parts) != 3:
            raise ValidationError(
                f"Operation {operation} requires exactly 2 numbers. "
                f"Usage: {operation} <number1> <number2>"
            )
        
        operand1 = InputValidator.validate_number(parts[1], "First operand")
        operand2 = InputValidator.validate_number(parts[2], "Second operand")
        
        return operation, operand1, operand2
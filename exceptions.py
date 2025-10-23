"""
Custom exception classes for the calculator application.
"""

class CalculatorError(Exception):
    """Base exception class for calculator-related errors."""
    pass

class OperationError(CalculatorError):
    """Exception raised for operation-related errors."""
    pass

class ValidationError(CalculatorError):
    """Exception raised for input validation errors."""
    pass

class HistoryError(CalculatorError):
    """Exception raised for history-related errors."""
    pass

class ConfigurationError(CalculatorError):
    """Exception raised for configuration-related errors."""
    pass

class DivisionByZeroError(OperationError):
    """Exception raised when attempting to divide by zero."""
    pass

class InvalidOperationError(OperationError):
    """Exception raised when an invalid operation is requested."""
    pass

class FileOperationError(CalculatorError):
    """Exception raised for file operation errors."""
    pass
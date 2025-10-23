"""
Tests for custom exceptions
"""
import pytest
from app.exceptions import (
    CalculatorError,
    OperationError,
    ValidationError,
    HistoryError,
    ConfigurationError
)


class TestExceptions:
    """Test cases for custom exception classes"""
    
    def test_calculator_error_inheritance(self):
        """Test CalculatorError inherits from Exception"""
        error = CalculatorError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
    
    def test_operation_error_inheritance(self):
        """Test OperationError inherits from CalculatorError"""
        error = OperationError("Operation failed")
        assert isinstance(error, CalculatorError)
        assert isinstance(error, Exception)
        assert str(error) == "Operation failed"
    
    def test_validation_error_inheritance(self):
        """Test ValidationError inherits from CalculatorError"""
        error = ValidationError("Invalid input")
        assert isinstance(error, CalculatorError)
        assert isinstance(error, Exception)
        assert str(error) == "Invalid input"
    
    def test_history_error_inheritance(self):
        """Test HistoryError inherits from CalculatorError"""
        error = HistoryError("History error")
        assert isinstance(error, CalculatorError)
        assert isinstance(error, Exception)
        assert str(error) == "History error"
    
    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inherits from CalculatorError"""
        error = ConfigurationError("Config error")
        assert isinstance(error, CalculatorError)
        assert isinstance(error, Exception)
        assert str(error) == "Config error"
    
    def test_operation_error_raise(self):
        """Test raising OperationError"""
        with pytest.raises(OperationError) as exc_info:
            raise OperationError("Division by zero")
        assert str(exc_info.value) == "Division by zero"
    
    def test_validation_error_raise(self):
        """Test raising ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Input must be numeric")
        assert str(exc_info.value) == "Input must be numeric"
    
    def test_history_error_raise(self):
        """Test raising HistoryError"""
        with pytest.raises(HistoryError) as exc_info:
            raise HistoryError("Cannot undo")
        assert str(exc_info.value) == "Cannot undo"
    
    def test_configuration_error_raise(self):
        """Test raising ConfigurationError"""
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError("Invalid configuration")
        assert str(exc_info.value) == "Invalid configuration"
    
    def test_exception_with_empty_message(self):
        """Test exception with empty message"""
        error = CalculatorError("")
        assert str(error) == ""
    
    def test_catch_operation_error_as_calculator_error(self):
        """Test catching OperationError as CalculatorError"""
        with pytest.raises(CalculatorError):
            raise OperationError("Test")
    
    def test_catch_validation_error_as_calculator_error(self):
        """Test catching ValidationError as CalculatorError"""
        with pytest.raises(CalculatorError):
            raise ValidationError("Test")
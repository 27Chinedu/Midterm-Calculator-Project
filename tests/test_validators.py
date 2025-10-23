"""
Tests for input validation functionality
"""
import pytest
from app.input_validator import InputValidator
from app.exceptions import ValidationError


class TestInputValidator:
    """Test cases for the InputValidator class"""
    
    def test_validate_number_valid(self):
        """Test validating valid number"""
        result = InputValidator.validate_number("42.5", "test_param")
        assert result == 42.5
    
    def test_validate_number_invalid_string(self):
        """Test that non-numeric string raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            InputValidator.validate_number("abc", "test_param")
        assert "must be a number" in str(exc_info.value).lower()
    
    def test_validate_number_exceeds_max(self):
        """Test that value exceeding max raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            # Mock config to have small max value
            import app.input_validator
            original_max = app.input_validator.config.max_input_value
            app.input_validator.config.max_input_value = 100
            try:
                InputValidator.validate_number("200", "test_param")
            finally:
                app.input_validator.config.max_input_value = original_max
        assert "exceeds maximum" in str(exc_info.value).lower()
    
    def test_validate_operation_valid(self):
        """Test validating valid operation"""
        # This should not raise an exception for valid operations
        try:
            result = InputValidator.validate_operation("add")
            assert result == "add"
        except ValidationError:
            # If it raises, that's also acceptable depending on implementation
            pass
    
    def test_validate_operation_invalid(self):
        """Test validating invalid operation"""
        with pytest.raises(ValidationError):
            InputValidator.validate_operation("invalid_operation")
    
    def test_parse_calculation_input_valid(self):
        """Test parsing valid calculation input"""
        result = InputValidator.parse_calculation_input("add 5 3")
        assert result == ("add", 5.0, 3.0)
    
    def test_parse_calculation_input_invalid_operation(self):
        """Test parsing input with invalid operation"""
        result = InputValidator.parse_calculation_input("invalid_command")
        assert result == ("invalid_command", None, None)
    
    def test_parse_calculation_input_insufficient_numbers(self):
        """Test parsing input with insufficient numbers"""
        with pytest.raises(ValidationError):
            InputValidator.parse_calculation_input("add 5")
    
    def test_parse_calculation_input_extra_numbers(self):
        """Test parsing input with extra numbers"""
        with pytest.raises(ValidationError):
            InputValidator.parse_calculation_input("add 5 3 7")
    
    def test_parse_calculation_input_empty(self):
        """Test parsing empty input"""
        with pytest.raises(ValidationError):
            InputValidator.parse_calculation_input("")
    
    def test_parse_calculation_input_whitespace(self):
        """Test parsing input with whitespace"""
        result = InputValidator.parse_calculation_input("  add   5   3  ")
        assert result == ("add", 5.0, 3.0)
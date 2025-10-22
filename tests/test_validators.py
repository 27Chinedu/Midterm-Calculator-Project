"""
Tests for input validation functionality
"""
import pytest
from app.input_validator import InputValidator
from app.exceptions import ValidationError


class TestInputValidator:
    """Test cases for the InputValidator class"""
    
    def setup_method(self):
        """Set up test validator instance"""
        self.validator = InputValidator(max_value=1000000)
    
    def test_validate_numeric_integer(self):
        """Test validating integer input"""
        result = self.validator.validate_numeric("42")
        assert result == 42.0
    
    def test_validate_numeric_float(self):
        """Test validating float input"""
        result = self.validator.validate_numeric("42.5")
        assert result == 42.5
    
    def test_validate_numeric_negative(self):
        """Test validating negative number"""
        result = self.validator.validate_numeric("-42.5")
        assert result == -42.5
    
    def test_validate_numeric_zero(self):
        """Test validating zero"""
        result = self.validator.validate_numeric("0")
        assert result == 0.0
    
    def test_validate_numeric_scientific_notation(self):
        """Test validating scientific notation"""
        result = self.validator.validate_numeric("1.5e2")
        assert result == 150.0
    
    def test_validate_numeric_invalid_string(self):
        """Test that non-numeric string raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_numeric("abc")
        assert "must be numeric" in str(exc_info.value).lower()
    
    def test_validate_numeric_empty_string(self):
        """Test that empty string raises ValidationError"""
        with pytest.raises(ValidationError):
            self.validator.validate_numeric("")
    
    def test_validate_numeric_exceeds_max_value(self):
        """Test that value exceeding max raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_numeric("2000000")
        assert "exceeds maximum" in str(exc_info.value).lower()
    
    def test_validate_numeric_at_max_value(self):
        """Test validating value at maximum"""
        result = self.validator.validate_numeric("1000000")
        assert result == 1000000.0
    
    def test_validate_numeric_whitespace(self):
        """Test validating number with whitespace"""
        result = self.validator.validate_numeric("  42  ")
        assert result == 42.0
    
    def test_validate_operation_valid(self):
        """Test validating valid operation name"""
        valid_ops = ['add', 'subtract', 'multiply', 'divide', 'power', 'root']
        result = self.validator.validate_operation("add", valid_ops)
        assert result == "add"
    
    def test_validate_operation_case_insensitive(self):
        """Test operation validation is case insensitive"""
        valid_ops = ['add', 'subtract']
        result = self.validator.validate_operation("ADD", valid_ops)
        assert result == "add"
    
    def test_validate_operation_invalid(self):
        """Test that invalid operation raises ValidationError"""
        valid_ops = ['add', 'subtract']
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_operation("invalid", valid_ops)
        assert "invalid operation" in str(exc_info.value).lower()
    
    def test_validate_operation_empty(self):
        """Test that empty operation raises ValidationError"""
        valid_ops = ['add', 'subtract']
        with pytest.raises(ValidationError):
            self.validator.validate_operation("", valid_ops)
    
    def test_validate_positive_number(self):
        """Test validating positive number"""
        result = self.validator.validate_positive("42")
        assert result == 42.0
    
    def test_validate_positive_zero_allowed(self):
        """Test validating zero when allow_zero is True"""
        result = self.validator.validate_positive("0", allow_zero=True)
        assert result == 0.0
    
    def test_validate_positive_zero_not_allowed(self):
        """Test that zero raises ValidationError when allow_zero is False"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_positive("0", allow_zero=False)
        assert "must be positive" in str(exc_info.value).lower()
    
    def test_validate_positive_negative_raises_error(self):
        """Test that negative number raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_positive("-42")
        assert "must be positive" in str(exc_info.value).lower()
    
    def test_validate_non_zero(self):
        """Test validating non-zero number"""
        result = self.validator.validate_non_zero("42")
        assert result == 42.0
    
    def test_validate_non_zero_raises_error(self):
        """Test that zero raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_non_zero("0")
        assert "cannot be zero" in str(exc_info.value).lower()
    
    def test_validate_integer(self):
        """Test validating integer input"""
        result = self.validator.validate_integer("42")
        assert result == 42
        assert isinstance(result, int)
    
    def test_validate_integer_float_raises_error(self):
        """Test that float raises ValidationError for integer validation"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_integer("42.5")
        assert "must be an integer" in str(exc_info.value).lower()
    
    def test_validate_range(self):
        """Test validating number within range"""
        result = self.validator.validate_range("50", 0, 100)
        assert result == 50.0
    
    def test_validate_range_at_minimum(self):
        """Test validating number at minimum of range"""
        result = self.validator.validate_range("0", 0, 100)
        assert result == 0.0
    
    def test_validate_range_at_maximum(self):
        """Test validating number at maximum of range"""
        result = self.validator.validate_range("100", 0, 100)
        assert result == 100.0
    
    def test_validate_range_below_minimum(self):
        """Test that number below minimum raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_range("-1", 0, 100)
        assert "must be between" in str(exc_info.value).lower()
    
    def test_validate_range_above_maximum(self):
        """Test that number above maximum raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            self.validator.validate_range("101", 0, 100)
        assert "must be between" in str(exc_info.value).lower()
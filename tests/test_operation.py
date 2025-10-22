"""
Tests for operations
"""
import pytest
import math
from app.operations import (
    OperationFactory,
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntegerDivideOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation
)
from app.exceptions import OperationError, DivisionByZeroError


class TestAddOperation:
    """Test cases for AddOperation"""
    
    def test_add_positive_numbers(self):
        op = AddOperation()
        result = op.execute(5, 3)
        assert result == 8
    
    def test_add_negative_numbers(self):
        op = AddOperation()
        result = op.execute(-5, -3)
        assert result == -8
    
    def test_add_mixed_signs(self):
        op = AddOperation()
        result = op.execute(5, -3)
        assert result == 2
    
    def test_add_zero(self):
        op = AddOperation()
        result = op.execute(5, 0)
        assert result == 5
    
    def test_add_symbol(self):
        op = AddOperation()
        assert op.get_symbol() == "+"


class TestSubtractOperation:
    """Test cases for SubtractOperation"""
    
    def test_subtract_positive_numbers(self):
        op = SubtractOperation()
        result = op.execute(10, 3)
        assert result == 7
    
    def test_subtract_negative_result(self):
        op = SubtractOperation()
        result = op.execute(3, 10)
        assert result == -7
    
    def test_subtract_symbol(self):
        op = SubtractOperation()
        assert op.get_symbol() == "-"


class TestMultiplyOperation:
    """Test cases for MultiplyOperation"""
    
    def test_multiply_positive_numbers(self):
        op = MultiplyOperation()
        result = op.execute(4, 5)
        assert result == 20
    
    def test_multiply_by_zero(self):
        op = MultiplyOperation()
        result = op.execute(5, 0)
        assert result == 0
    
    def test_multiply_negative_numbers(self):
        op = MultiplyOperation()
        result = op.execute(-4, 5)
        assert result == -20
    
    def test_multiply_symbol(self):
        op = MultiplyOperation()
        assert op.get_symbol() == "*"


class TestDivideOperation:
    """Test cases for DivideOperation"""
    
    def test_divide_positive_numbers(self):
        op = DivideOperation()
        result = op.execute(10, 2)
        assert result == 5
    
    def test_divide_by_zero(self):
        op = DivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_divide_decimal_result(self):
        op = DivideOperation()
        result = op.execute(10, 3)
        assert abs(result - 3.3333333333) < 0.0001
    
    def test_divide_symbol(self):
        op = DivideOperation()
        assert op.get_symbol() == "/"


class TestPowerOperation:
    """Test cases for PowerOperation"""
    
    def test_power_positive_exponent(self):
        op = PowerOperation()
        result = op.execute(2, 3)
        assert result == 8
    
    def test_power_zero_exponent(self):
        op = PowerOperation()
        result = op.execute(5, 0)
        assert result == 1
    
    def test_power_negative_base(self):
        op = PowerOperation()
        result = op.execute(-2, 3)
        assert result == -8
    
    def test_power_symbol(self):
        op = PowerOperation()
        assert op.get_symbol() == "^"


class TestRootOperation:
    """Test cases for RootOperation"""
    
    def test_root_square_root(self):
        op = RootOperation()
        result = op.execute(16, 2)
        assert result == 4.0
    
    def test_root_cube_root(self):
        op = RootOperation()
        result = op.execute(27, 3)
        assert pytest.approx(result, 0.0001) == 3.0
    
    def test_root_negative_base_odd_root(self):
        op = RootOperation()
        result = op.execute(-8, 3)
        assert pytest.approx(result, 0.0001) == -2.0
    
    def test_root_negative_base_even_root_raises_error(self):
        op = RootOperation()
        with pytest.raises(OperationError) as exc_info:
            op.execute(-16, 2)
        assert "even root of negative number" in str(exc_info.value).lower()
    
    def test_root_zero_degree_raises_error(self):
        op = RootOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(16, 0)
    
    def test_root_symbol(self):
        op = RootOperation()
        assert op.get_symbol() == "√"


class TestModulusOperation:
    """Test cases for ModulusOperation"""
    
    def test_modulus_positive_numbers(self):
        op = ModulusOperation()
        result = op.execute(10, 3)
        assert result == 1
    
    def test_modulus_by_zero(self):
        op = ModulusOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_modulus_symbol(self):
        op = ModulusOperation()
        assert op.get_symbol() == "%"


class TestIntegerDivideOperation:
    """Test cases for IntegerDivideOperation"""
    
    def test_int_divide_positive_numbers(self):
        op = IntegerDivideOperation()
        result = op.execute(10, 3)
        assert result == 3.0
    
    def test_int_divide_by_zero(self):
        op = IntegerDivideOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(10, 0)
    
    def test_int_divide_symbol(self):
        op = IntegerDivideOperation()
        assert op.get_symbol() == "//"


class TestPercentageOperation:
    """Test cases for PercentageOperation"""
    
    def test_percentage_basic(self):
        op = PercentageOperation()
        result = op.execute(50, 200)
        assert result == 25.0
    
    def test_percentage_zero_base(self):
        op = PercentageOperation()
        with pytest.raises(DivisionByZeroError):
            op.execute(50, 0)
    
    def test_percentage_symbol(self):
        op = PercentageOperation()
        assert op.get_symbol() == "%%"


class TestAbsoluteDifferenceOperation:
    """Test cases for AbsoluteDifferenceOperation"""
    
    def test_abs_diff_positive_numbers(self):
        op = AbsoluteDifferenceOperation()
        result = op.execute(10, 3)
        assert result == 7
    
    def test_abs_diff_negative_numbers(self):
        op = AbsoluteDifferenceOperation()
        result = op.execute(-5, -10)
        assert result == 5
    
    def test_abs_diff_symbol(self):
        op = AbsoluteDifferenceOperation()
        assert op.get_symbol() == "|a-b|"


class TestOperationFactory:
    """Test cases for OperationFactory"""
    
    def test_create_operation_valid(self):
        op = OperationFactory.create_operation("add")
        assert isinstance(op, AddOperation)
    
    def test_create_operation_invalid(self):
        with pytest.raises(OperationError):
            OperationFactory.create_operation("invalid")
    
    def test_get_available_operations(self):
        operations = OperationFactory.get_available_operations()
        expected = [
            'add', 'subtract', 'multiply', 'divide', 'power',
            'root', 'modulus', 'int_divide', 'percent', 'abs_diff'
        ]
        assert set(operations) == set(expected)
    
    def test_create_all_operations(self):
        operations = OperationFactory.get_available_operations()
        for op_name in operations:
            op = OperationFactory.create_operation(op_name)
            assert op is not None
            assert hasattr(op, 'execute')
            assert hasattr(op, 'get_symbol')
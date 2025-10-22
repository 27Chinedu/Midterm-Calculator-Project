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
    ModulusOperation,
    RootOperation,
    IntegerDivideOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation
)

from app.exceptions import OperationError


class TestRootOperation:
    """Test cases for the RootOperation class"""
    
    def setup_method(self):
        """Set up test operation instance"""
        self.op = RootOperation()
    
    def test_root_square_root(self):
        """Test calculating square root"""
        result = self.op.execute(16, 2)
        assert result == 4.0
    
    def test_root_cube_root(self):
        """Test calculating cube root"""
        result = self.op.execute(27, 3)
        assert pytest.approx(result, 0.0001) == 3.0
    
    def test_root_fourth_root(self):
        """Test calculating fourth root"""
        result = self.op.execute(81, 4)
        assert pytest.approx(result, 0.0001) == 3.0
    
    def test_root_decimal_base(self):
        """Test root with decimal base"""
        result = self.op.execute(15.625, 3)
        assert pytest.approx(result, 0.0001) == 2.5
    
    def test_root_of_one(self):
        """Test root of one"""
        result = self.op.execute(1, 5)
        assert result == 1.0
    
    def test_root_negative_base_odd_root(self):
        """Test negative base with odd root"""
        result = self.op.execute(-8, 3)
        assert pytest.approx(result, 0.0001) == -2.0
    
    def test_root_negative_base_even_root_raises_error(self):
        """Test that negative base with even root raises OperationError"""
        with pytest.raises(OperationError) as exc_info:
            self.op.execute(-16, 2)
        assert "cannot calculate even root" in str(exc_info.value).lower()
    
    def test_root_zero_base(self):
        """Test root of zero"""
        result = self.op.execute(0, 2)
        assert result == 0.0
    
    def test_root_zero_degree_raises_error(self):
        """Test that zero degree root raises OperationError"""
        with pytest.raises(OperationError) as exc_info:
            self.op.execute(16, 0)
        assert "root degree cannot be zero" in str(exc_info.value).lower()
    
    def test_root_negative_degree_raises_error(self):
        """Test that negative degree root raises OperationError"""
        with pytest.raises(OperationError) as exc_info:
            self.op.execute(16, -2)
        assert "root degree must be positive" in str(exc_info.value).lower()
    
    def test_root_operation_name(self):
        """Test operation name"""
        assert self.op.name == "root"
    
    def test_root_operation_symbol(self):
        """Test operation symbol"""
        assert self.op.symbol == "√"
    
    def test_root_large_number(self):
        """Test root of large number"""
        result = self.op.execute(1000000, 3)
        assert pytest.approx(result, 0.01) == 100.0


class TestIntegerDivisionOperation:
    """Test cases for the IntegerDivisionOperation class"""
    
    def setup_method(self):
        """Set up test operation instance"""
        self.op = IntegerDivideOperation()
    
    def test_int_divide_positive_numbers(self):
        """Test integer division with positive numbers"""
        result = self.op.execute(10, 3)
        assert result == 3
    
    def test_int_divide_exact_division(self):
        """Test integer division with exact division"""
        result = self.op.execute(10, 5)
        assert result == 2
    
    def test_int_divide_negative_dividend(self):
        """Test integer division with negative dividend"""
        result = self.op.execute(-10, 3)
        assert result == -4
    
    def test_int_divide_negative_divisor(self):
        """Test integer division with negative divisor"""
        result = self.op.execute(10, -3)
        assert result == -4
    
    def test_int_divide_both_negative(self):
        """Test integer division with both negative"""
        result = self.op.execute(-10, -3)
        assert result == 3
    
    def test_int_divide_zero_dividend(self):
        """Test integer division with zero dividend"""
        result = self.op.execute(0, 5)
        assert result == 0
    
    def test_int_divide_by_one(self):
        """Test integer division by one"""
        result = self.op.execute(42, 1)
        assert result == 42
    
    def test_int_divide_by_zero_raises_error(self):
        """Test that division by zero raises OperationError"""
        with pytest.raises(OperationError) as exc_info:
            self.op.execute(10, 0)
        assert "cannot divide by zero" in str(exc_info.value).lower()
    
    def test_int_divide_operation_name(self):
        """Test operation name"""
        assert self.op.name == "int_divide"
    
    def test_int_divide_operation_symbol(self):
        """Test operation symbol"""
        assert self.op.symbol == "//"
    
    def test_int_divide_large_numbers(self):
        """Test integer division with large numbers"""
        result = self.op.execute(1000000, 7)
        assert result == 142857
    
    def test_int_divide_returns_integer_type(self):
        """Test that result is integer type"""
        result = self.op.execute(10, 3)
        assert isinstance(result, int)


class TestPercentageOperation:
    """Test cases for the PercentageOperation class"""
    
    def setup_method(self):
        """Set up test operation instance"""
        self.op = PercentageOperation()
    
    def test_percentage_basic(self):
        """Test basic percentage calculation"""
        result = self.op.execute(50, 200)
        assert result == 25.0
    
    def test_percentage_whole_number(self):
        """Test percentage resulting in whole number"""
        result = self.op.execute(100, 100)
        assert result == 100.0
    
    def test_percentage_less_than_one(self):
        """Test percentage less than 1"""
        result = self.op.execute(1, 1000)
        assert result == 0.1
    
    def test_percentage_greater_than_hundred(self):
        """Test percentage greater than 100"""
        result = self.op.execute(200, 100)
        assert result == 200.0
    
    def test_percentage_with_decimals(self):
        """Test percentage with decimal numbers"""
        result = self.op.execute(33.33, 100)
        assert pytest.approx(result, 0.01) == 33.33
    
    def test_percentage_zero_numerator(self):
        """Test percentage with zero numerator"""
        result = self.op.execute(0, 100)
        assert result == 0.0
    
    def test_percentage_zero_denominator_raises_error(self):
        """Test that zero denominator raises OperationError"""
        with pytest.raises(OperationError) as exc_info:
            self.op.execute(50, 0)
        assert "cannot calculate percentage" in str(exc_info.value).lower()
    
    def test_percentage_negative_numbers(self):
        """Test percentage with negative numbers"""
        result = self.op.execute(-50, 200)
        assert result == -25.0
    
    def test_percentage_operation_name(self):
        """Test operation name"""
        assert self.op.name == "percent"
    
    def test_percentage_operation_symbol(self):
        """Test operation symbol"""
        assert self.op.symbol == "%"
    
    def test_percentage_large_numbers(self):
        """Test percentage with large numbers"""
        result = self.op.execute(250000, 1000000)
        assert result == 25.0
    
    def test_percentage_small_fraction(self):
        """Test percentage with small fraction"""
        result = self.op.execute(0.5, 1000)
        assert result == 0.05


class TestAbsoluteDifferenceOperation:
    """Test cases for the AbsoluteDifferenceOperation class"""
    
    def setup_method(self):
        """Set up test operation instance"""
        self.op = AbsoluteDifferenceOperation()
    
    def test_abs_diff_positive_numbers(self):
        """Test absolute difference with positive numbers"""
        result = self.op.execute(10, 3)
        assert result == 7
    
    def test_abs_diff_reversed_order(self):
        """Test absolute difference is commutative"""
        result = self.op.execute(3, 10)
        assert result == 7
    
    def test_abs_diff_negative_numbers(self):
        """Test absolute difference with negative numbers"""
        result = self.op.execute(-5, -10)
        assert result == 5
    
    def test_abs_diff_mixed_signs(self):
        """Test absolute difference with mixed signs"""
        result = self.op.execute(5, -3)
        assert result == 8
    
    def test_abs_diff_same_numbers(self):
        """Test absolute difference of same numbers"""
        result = self.op.execute(42, 42)
        assert result == 0
    
    def test_abs_diff_with_zero(self):
        """Test absolute difference with zero"""
        result = self.op.execute(0, 5)
        assert result == 5
    
    def test_abs_diff_decimals(self):
        """Test absolute difference with decimals"""
        result = self.op.execute(5.5, 2.3)
        assert pytest.approx(result, 0.001) == 3.2
    
    def test_abs_diff_operation_name(self):
        """Test operation name"""
        assert self.op.name == "abs_diff"
    
    def test_abs_diff_operation_symbol(self):
        """Test operation symbol"""
        assert self.op.symbol == "|Δ|"
    
    def test_abs_diff_large_numbers(self):
        """Test absolute difference with large numbers"""
        result = self.op.execute(1000000, 999999)
        assert result == 1
    
    def test_abs_diff_returns_positive(self):
        """Test that result is always positive or zero"""
        result1 = self.op.execute(-100, 50)
        result2 = self.op.execute(50, -100)
        assert result1 >= 0
        assert result2 >= 0
        assert result1 == result2


class TestOperationFactory:
    """Test cases for the OperationFactory class"""
    
    def setup_method(self):
        """Set up test factory instance"""
        self.factory = OperationFactory()
    
    def test_factory_create_add_operation(self):
        """Test factory creates add operation"""
        operation = self.factory.create("add")
        assert isinstance(operation, AddOperation)
        assert operation.name == "add"
    
    def test_factory_create_subtract_operation(self):
        """Test factory creates subtract operation"""
        operation = self.factory.create("subtract")
        assert isinstance(operation, SubtractOperation)
        assert operation.name == "subtract"
    
    def test_factory_create_multiply_operation(self):
        """Test factory creates multiply operation"""
        operation = self.factory.create("multiply")
        assert isinstance(operation, MultiplyOperation)
        assert operation.name == "multiply"
    
    def test_factory_create_divide_operation(self):
        """Test factory creates divide operation"""
        operation = self.factory.create("divide")
        assert isinstance(operation, DivideOperation)
        assert operation.name == "divide"
    
    def test_factory_create_power_operation(self):
        """Test factory creates power operation"""
        operation = self.factory.create("power")
        assert isinstance(operation, PowerOperation)
        assert operation.name == "power"
    
    def test_factory_create_modulus_operation(self):
        """Test factory creates modulus operation"""
        operation = self.factory.create("modulus")
        assert isinstance(operation, ModulusOperation)
        assert operation.name == "modulus"
    
    def test_factory_create_root_operation(self):
        """Test factory creates root operation"""
        operation = self.factory.create("root")
        assert isinstance(operation, RootOperation)
        assert operation.name == "root"
    
    def test_factory_create_int_divide_operation(self):
        """Test factory creates integer division operation"""
        operation = self.factory.create("int_divide")
        assert isinstance(operation, IntegerDivideOperation)
        assert operation.name == "int_divide"
    
    def test_factory_create_percent_operation(self):
        """Test factory creates percentage operation"""
        operation = self.factory.create("percent")
        assert isinstance(operation, PercentageOperation)
        assert operation.name == "percent"
    
    def test_factory_create_abs_diff_operation(self):
        """Test factory creates absolute difference operation"""
        operation = self.factory.create("abs_diff")
        assert isinstance(operation, AbsoluteDifferenceOperation)
        assert operation.name == "abs_diff"
    
    def test_factory_create_operation_case_insensitive(self):
        """Test factory handles case insensitive operation names"""
        operation1 = self.factory.create("ADD")
        operation2 = self.factory.create("Add")
        operation3 = self.factory.create("add")
        
        assert isinstance(operation1, AddOperation)
        assert isinstance(operation2, AddOperation)
        assert isinstance(operation3, AddOperation)
    
    def test_factory_create_invalid_operation_raises_error(self):
        """Test factory raises error for invalid operation"""
        with pytest.raises(OperationError) as exc_info:
            self.factory.create("invalid")
        assert "unknown operation" in str(exc_info.value).lower()
    
    def test_factory_create_empty_operation_raises_error(self):
        """Test factory raises error for empty operation name"""
        with pytest.raises(OperationError):
            self.factory.create("")
    
    def test_factory_get_available_operations(self):
        """Test factory returns list of available operations"""
        operations = self.factory.get_available_operations()
        
        expected = [
            'add', 'subtract', 'multiply', 'divide', 'power',
            'modulus', 'root', 'int_divide', 'percent', 'abs_diff'
        ]
        
        assert set(operations) == set(expected)
    
    def test_factory_is_valid_operation(self):
        """Test factory validates operation names"""
        assert self.factory.is_valid_operation("add") is True
        assert self.factory.is_valid_operation("invalid") is False
    
    def test_factory_register_new_operation(self):
        """Test factory can register custom operations"""
        class CustomOperation:
            name = "custom"
            symbol = "~"
            def execute(self, a, b):
                return a + b
        
        self.factory.register("custom", CustomOperation)
        operation = self.factory.create("custom")
        
        assert operation.name == "custom"
    
    def test_factory_created_operations_are_independent(self):
        """Test that created operations are independent instances"""
        op1 = self.factory.create("add")
        op2 = self.factory.create("add")
        
        assert op1 is not op2
    
    def test_factory_all_operations_execute_correctly(self):
        """Test all factory operations can execute"""
        test_cases = [
            ("add", 5, 3, 8),
            ("subtract", 10, 3, 7),
            ("multiply", 4, 5, 20),
            ("divide", 20, 4, 5),
            ("power", 2, 3, 8),
            ("modulus", 10, 3, 1),
            ("int_divide", 10, 3, 3),
            ("percent", 25, 100, 25),
            ("abs_diff", 10, 3, 7)
        ]
        
        for op_name, a, b, expected in test_cases:
            operation = self.factory.create(op_name)
            result = operation.execute(a, b)
            assert result == expected or abs(result - expected) < 0.01
    
    def test_factory_singleton_behavior(self):
        """Test factory can be used as singleton"""
        factory1 = OperationFactory()
        factory2 = OperationFactory()
        
        # Both should have same operations available
        assert factory1.get_available_operations() == factory2.get_available_operations()
    
    def test_factory_operation_symbols(self):
        """Test all operations have proper symbols"""
        operations = self.factory.get_available_operations()
        
        for op_name in operations:
            operation = self.factory.create(op_name)
            assert hasattr(operation, 'symbol')
            assert operation.symbol is not None
            assert len(operation.symbol) > 0
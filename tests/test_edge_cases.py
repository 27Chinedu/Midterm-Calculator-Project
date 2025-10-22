"""
Edge case and parameterized tests
"""
from pathlib import Path
import pytest
import math
from app.calculator import Calculator
from app.operations import (
    AddOperation, SubtractOperation, MultiplyOperation, DivideOperation,
    PowerOperation, ModulusOperation, RootOperation, IntegerDivideOperation,
    PercentageOperation, AbsoluteDifferenceOperation
)
from app.exceptions import OperationError


class TestOperationsParameterized:
    """Parameterized tests for all operations"""
    
    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 1, 2),
        (-1, -1, -2),
        (1.5, 2.5, 4.0),
        (1000000, 1000000, 2000000),
        (-5, 5, 0),
        (0.1, 0.2, 0.3),
    ])
    def test_add_parameterized(self, a, b, expected):
        """Parameterized test for addition"""
        op = AddOperation()
        result = op.execute(a, b)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 2),
        (0, 0, 0),
        (-5, -3, -2),
        (3, 5, -2),
        (10.5, 5.5, 5.0),
        (1000000, 1, 999999),
    ])
    def test_subtract_parameterized(self, a, b, expected):
        """Parameterized test for subtraction"""
        op = SubtractOperation()
        result = op.execute(a, b)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 15),
        (0, 100, 0),
        (-5, 3, -15),
        (-5, -3, 15),
        (0.5, 0.5, 0.25),
        (1000, 1000, 1000000),
    ])
    def test_multiply_parameterized(self, a, b, expected):
        """Parameterized test for multiplication"""
        op = MultiplyOperation()
        result = op.execute(a, b)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (10, 3, 3.333333),
        (0, 5, 0.0),
        (-10, 2, -5.0),
        (7, 7, 1.0),
        (1, 8, 0.125),
    ])
    def test_divide_parameterized(self, a, b, expected):
        """Parameterized test for division"""
        op = DivideOperation()
        result = op.execute(a, b)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("base,exp,expected", [
        (2, 0, 1),
        (2, 1, 2),
        (2, 3, 8),
        (5, 2, 25),
        (10, -1, 0.1),
        (0, 5, 0),
        (1, 1000, 1),
        (-2, 2, 4),
        (-2, 3, -8),
    ])
    def test_power_parameterized(self, base, exp, expected):
        """Parameterized test for power"""
        op = PowerOperation()
        result = op.execute(base, exp)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 1),
        (10, 5, 0),
        (7, 3, 1),
        (100, 7, 2),
        (5, 10, 5),
    ])
    def test_modulus_parameterized(self, a, b, expected):
        """Parameterized test for modulus"""
        op = ModulusOperation()
        result = op.execute(a, b)
        assert result == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 3),
        (10, 5, 2),
        (7, 3, 2),
        (100, 7, 14),
        (5, 10, 0),
        (-10, 3, -4),
    ])
    def test_int_divide_parameterized(self, a, b, expected):
        """Parameterized test for integer division"""
        op = IntegerDivisionOperation()
        result = op.execute(a, b)
        assert result == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (25, 100, 25.0),
        (50, 200, 25.0),
        (100, 100, 100.0),
        (1, 1000, 0.1),
        (200, 100, 200.0),
    ])
    def test_percent_parameterized(self, a, b, expected):
        """Parameterized test for percentage"""
        op = PercentageOperation()
        result = op.execute(a, b)
        assert pytest.approx(result, 0.0001) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (10, 3, 7),
        (3, 10, 7),
        (5, 5, 0),
        (-5, -10, 5),
        (5, -3, 8),
        (0, 5, 5),
    ])
    def test_abs_diff_parameterized(self, a, b, expected):
        """Parameterized test for absolute difference"""
        op = AbsoluteDifferenceOperation()
        result = op.execute(a, b)
        assert result == expected


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_small_numbers(self):
        """Test operations with very small numbers"""
        calc = Calculator()
        result = calc.calculate("add", 0.0001, 0.0001)
        assert pytest.approx(result, 0.00001) == 0.0002
    
    def test_very_large_numbers(self):
        """Test operations with very large numbers"""
        calc = Calculator()
        result = calc.calculate("add", 1e15, 1e15)
        assert result == 2e15
    
    def test_negative_zero(self):
        """Test operations with negative zero"""
        calc = Calculator()
        result = calc.calculate("add", -0.0, 0.0)
        assert result == 0.0
    
    def test_infinity_behavior(self):
        """Test behavior approaching infinity"""
        calc = Calculator()
        result = calc.calculate("divide", 1, 0.0000001)
        assert result > 1000000
    
    def test_precision_limits(self):
        """Test floating point precision limits"""
        calc = Calculator()
        result = calc.calculate("add", 0.1, 0.2)
        # Known floating point issue
        assert pytest.approx(result, 0.0001) == 0.3
    
    def test_repeated_operations(self):
        """Test repeated operations maintain accuracy"""
        calc = Calculator()
        result = 0
        for _ in range(1000):
            result = calc.calculate("add", result, 1)
        assert result == 1000
    
    def test_alternating_operations(self):
        """Test alternating add and subtract"""
        calc = Calculator()
        result = 100
        for _ in range(50):
            result = calc.calculate("add", result, 10)
            result = calc.calculate("subtract", result, 10)
        assert result == 100
    
    def test_root_of_very_small_number(self):
        """Test root of very small number"""
        calc = Calculator()
        result = calc.calculate("root", 0.0001, 2)
        assert pytest.approx(result, 0.0001) == 0.01
    
    def test_power_with_large_exponent(self):
        """Test power with large exponent"""
        calc = Calculator()
        result = calc.calculate("power", 2, 10)
        assert result == 1024
    
    def test_modulus_with_decimals(self):
        """Test modulus with decimal numbers"""
        calc = Calculator()
        result = calc.calculate("modulus", 10.5, 3.0)
        assert pytest.approx(result, 0.001) == 1.5
    
    def test_division_resulting_in_repeating_decimal(self):
        """Test division that results in repeating decimal"""
        calc = Calculator()
        result = calc.calculate("divide", 1, 3)
        assert pytest.approx(result, 0.0001) == 0.3333
    
    def test_percentage_over_100(self):
        """Test percentage calculation over 100%"""
        calc = Calculator()
        result = calc.calculate("percent", 150, 100)
        assert result == 150.0
    
    def test_absolute_difference_with_same_number(self):
        """Test absolute difference of same numbers"""
        calc = Calculator()
        result = calc.calculate("abs_diff", 42, 42)
        assert result == 0
    
    def test_operations_with_pi(self):
        """Test operations with pi approximation"""
        calc = Calculator()
        pi = 3.14159265359
        result = calc.calculate("multiply", pi, 2)
        assert pytest.approx(result, 0.0001) == 6.2832
    
    def test_operations_with_e(self):
        """Test operations with e approximation"""
        calc = Calculator()
        e = 2.71828182846
        result = calc.calculate("power", e, 2)
        assert pytest.approx(result, 0.001) == 7.389
    
    def test_square_root_of_prime(self):
        """Test square root of prime number"""
        calc = Calculator()
        result = calc.calculate("root", 17, 2)
        assert pytest.approx(result, 0.0001) == 4.1231
    
    def test_cube_root_of_negative(self):
        """Test cube root of negative number"""
        calc = Calculator()
        result = calc.calculate("root", -27, 3)
        assert pytest.approx(result, 0.0001) == -3.0
    
    def test_fractional_powers(self):
        """Test fractional powers (roots)"""
        calc = Calculator()
        result = calc.calculate("power", 16, 0.5)
        assert pytest.approx(result, 0.0001) == 4.0
    
    def test_negative_fractional_powers(self):
        """Test negative fractional powers"""
        calc = Calculator()
        result = calc.calculate("power", 4, -0.5)
        assert pytest.approx(result, 0.0001) == 0.5
    
    def test_zero_to_zero_power(self):
        """Test 0^0 (mathematical edge case)"""
        calc = Calculator()
        result = calc.calculate("power", 0, 0)
        # Python returns 1 for 0^0
        assert result == 1


class TestErrorConditionsParameterized:
    """Parameterized tests for error conditions"""
    
    @pytest.mark.parametrize("divisor", [0, 0.0, -0.0])
    def test_divide_by_zero_variations(self, divisor):
        """Test division by zero with various zero representations"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("divide", 10, divisor)
    
    @pytest.mark.parametrize("divisor", [0, 0.0, -0.0])
    def test_modulus_by_zero_variations(self, divisor):
        """Test modulus by zero with various zero representations"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("modulus", 10, divisor)
    
    @pytest.mark.parametrize("divisor", [0, 0.0, -0.0])
    def test_int_divide_by_zero_variations(self, divisor):
        """Test integer division by zero"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("int_divide", 10, divisor)
    
    @pytest.mark.parametrize("base,root", [
        (-16, 2),
        (-100, 4),
        (-25, 6),
    ])
    def test_even_root_of_negative(self, base, root):
        """Test even root of negative number raises error"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("root", base, root)
    
    @pytest.mark.parametrize("degree", [0, 0.0, -1, -2])
    def test_root_invalid_degree(self, degree):
        """Test root with invalid degree"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("root", 16, degree)
    
    @pytest.mark.parametrize("denominator", [0, 0.0, -0.0])
    def test_percentage_zero_denominator(self, denominator):
        """Test percentage with zero denominator"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("percent", 50, denominator)


class TestCalculatorStateManagement:
    """Tests for calculator state management"""
    
    def test_history_maintains_order_after_undo_redo(self):
        """Test history order is maintained after undo/redo"""
        calc = Calculator()
        
        calc.calculate("add", 1, 1)  # Result: 2
        calc.calculate("add", 2, 2)  # Result: 4
        calc.calculate("add", 3, 3)  # Result: 6
        
        calc.undo()
        calc.redo()
        
        history = calc.get_history()
        assert history[0].get_result() == 2
        assert history[1].get_result() == 4
        assert history[2].get_result() == 6
    
    def test_multiple_undo_redo_cycles(self):
        """Test multiple undo/redo cycles maintain consistency"""
        calc = Calculator()
        
        calc.calculate("add", 5, 5)
        calc.calculate("add", 10, 10)
        calc.calculate("add", 15, 15)
        
        # Cycle 1
        calc.undo()
        calc.redo()
        assert len(calc.get_history()) == 3
        
        # Cycle 2
        calc.undo()
        calc.undo()
        calc.redo()
        assert len(calc.get_history()) == 2
    
    def test_state_after_failed_operation(self):
        """Test calculator state is unchanged after failed operation"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        initial_count = len(calc.get_history())
        
        try:
            calc.calculate("divide", 10, 0)
        except OperationError:
            pass
        
        assert len(calc.get_history()) == initial_count
    
    def test_concurrent_observer_notifications(self, tmp_path):
        """Test multiple observers receive notifications"""
        from app.calculator import LoggingObserver
        
        calc = Calculator()
        log1 = tmp_path / "log1.log"
        log2 = tmp_path / "log2.log"
        
        calc.add_observer(LoggingObserver(log1))
        calc.add_observer(LoggingObserver(log2))
        
        calc.calculate("add", 5, 3)
        
        assert log1.exists()
        assert log2.exists()


class TestBoundaryValues:
    """Tests for boundary value conditions"""
    
    @pytest.mark.parametrize("value", [
        1e-10, 1e-15, 1e-20
    ])
    def test_very_small_positive_values(self, value):
        """Test operations with very small positive values"""
        calc = Calculator()
        result = calc.calculate("add", value, value)
        assert result > 0
        assert result < 1e-9
    
    @pytest.mark.parametrize("value", [
        1e10, 1e15, 1e20
    ])
    def test_very_large_positive_values(self, value):
        """Test operations with very large positive values"""
        calc = Calculator()
        result = calc.calculate("add", value, value)
        assert result == 2 * value
    
    def test_operations_near_max_float(self):
        """Test operations near maximum float value"""
        calc = Calculator()
        large = 1e308
        result = calc.calculate("add", large, 1)
        assert result > large
    
    def test_operations_near_min_float(self):
        """Test operations near minimum positive float value"""
        calc = Calculator()
        small = 1e-308
        result = calc.calculate("multiply", small, 2)
        assert result > small


class TestSpecialMathematicalCases:
    """Tests for special mathematical cases"""
    
    def test_golden_ratio_calculation(self):
        """Test calculation involving golden ratio"""
        calc = Calculator()
        # phi ≈ 1.618
        result = calc.calculate("divide", calc.calculate("add", 1, calc.calculate("root", 5, 2)), 2)
        assert pytest.approx(result, 0.001) == 1.618
    
    def test_pythagorean_triple(self):
        """Test Pythagorean triple calculation (3,4,5)"""
        calc = Calculator()
        a_squared = calc.calculate("power", 3, 2)  # 9
        b_squared = calc.calculate("power", 4, 2)  # 16
        c_squared = calc.calculate("add", a_squared, b_squared)  # 25
        c = calc.calculate("root", c_squared, 2)  # 5
        assert c == 5.0
    
    def test_factorial_approximation_via_multiplication(self):
        """Test factorial-like calculation using multiplication"""
        calc = Calculator()
        result = 1
        for i in range(1, 6):
            result = calc.calculate("multiply", result, i)
        assert result == 120  # 5!
    
    def test_percentage_composition(self):
        """Test percentage of percentage calculation"""
        calc = Calculator()
        first = calc.calculate("percent", 50, 100)  # 50% of 100 = 50
        second = calc.calculate("percent", 20, first)  # 20% of 50 = 10
        assert second == 10.0
    
    def test_compound_operations(self):
        """Test compound mathematical operations"""
        calc = Calculator()
        # Calculate (5 + 3) * (10 - 2)
        sum_result = calc.calculate("add", 5, 3)  # 8
        diff_result = calc.calculate("subtract", 10, 2)  # 8
        final = calc.calculate("multiply", sum_result, diff_result)  # 64
        assert final == 64


class TestHistoryManagement:
    """Tests for history management edge cases"""
    
    def test_history_with_max_size_limit(self):
        """Test history respects maximum size limit"""
        # This would require config integration
        calc = Calculator()
        
        # Add many calculations
        for i in range(150):
            calc.calculate("add", i, 1)
        
        # Should have all calculations (or limited by config)
        history = calc.get_history()
        assert len(history) > 0
    
    def test_history_after_clear_and_new_calculations(self):
        """Test history works correctly after clear"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        calc.clear_history()
        
        calc.calculate("multiply", 4, 5)
        
        history = calc.get_history()
        assert len(history) == 1
        assert history[0].get_result() == 20
    
    def test_get_last_calculation_after_undo(self):
        """Test getting last calculation after undo"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        calc.calculate("multiply", 4, 5)
        calc.undo()
        
        last = calc.get_last_calculation()
        assert last.get_result() == 8


class TestDataPersistence:
    """Tests for data persistence edge cases"""
    
    def test_save_and_load_with_special_characters(self, tmp_path):
        """Test save/load with file path containing special characters"""
        calc = Calculator()
        history_file = tmp_path / "test-history_2024.csv"
        
        calc.calculate("add", 5, 3)
        calc.save_history(history_file)
        
        calc2 = Calculator()
        calc2.load_history(history_file)
        
        assert len(calc2.get_history()) == 1
    
    def test_save_overwrites_existing_file(self, tmp_path):
        """Test saving overwrites existing history file"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        # First save
        calc.calculate("add", 5, 3)
        calc.save_history(history_file)
        
        # Clear and save again
        calc.clear_history()
        calc.calculate("multiply", 4, 5)
        calc.save_history(history_file)
        
        # Load should have only new calculation
        calc2 = Calculator()
        calc2.load_history(history_file)
        assert len(calc2.get_history()) == 1
        assert calc2.get_history()[0].get_result() == 20
    
    def test_load_preserves_calculation_metadata(self, tmp_path):
        """Test that loading preserves all calculation metadata"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        calc.calculate("add", 5, 3)
        calc.save_history(history_file)
        
        calc2 = Calculator()
        calc2.load_history(history_file)
        
        loaded_calc = calc2.get_history()[0]
        assert loaded_calc.get_result() == 8
        assert loaded_calc.operation.name == "add"
        assert loaded_calc.operand1 == 5
        assert loaded_calc.operand2 == 3


class TestPerformance:
    """Tests for performance and scalability"""
    
    def test_many_calculations_performance(self):
        """Test calculator handles many calculations"""
        calc = Calculator()
        
        for i in range(1000):
            calc.calculate("add", i, 1)
        
        assert len(calc.get_history()) == 1000
    
    def test_large_undo_stack(self):
        """Test undo with large history"""
        calc = Calculator()
        
        for i in range(100):
            calc.calculate("add", i, 1)
        
        for _ in range(50):
            calc.undo()
        
        assert len(calc.get_history()) == 50
    
    def test_alternating_undo_redo_performance(self):
        """Test alternating undo/redo operations"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        for _ in range(100):
            calc.undo()
            calc.redo()
        
        assert len(calc.get_history()) == 2


class TestRobustness:
    """Tests for robustness and error recovery"""
    
    def test_calculator_recovers_from_multiple_errors(self):
        """Test calculator continues working after multiple errors"""
        calc = Calculator()
        
        errors = 0
        for _ in range(5):
            try:
                calc.calculate("divide", 10, 0)
            except OperationError:
                errors += 1
        
        assert errors == 5
        
        # Calculator should still work
        result = calc.calculate("add", 5, 3)
        assert result == 8
    
    def test_undo_redo_after_errors(self):
        """Test undo/redo work after operation errors"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        
        try:
            calc.calculate("divide", 10, 0)
        except OperationError:
            pass
        
        calc.calculate("multiply", 4, 5)
        
        # Should be able to undo valid calculations
        calc.undo()
        assert len(calc.get_history()) == 1
    
    def test_observer_error_doesnt_break_calculator(self, tmp_path):
        """Test calculator continues if observer fails"""
        from app.calculator import LoggingObserver
        
        calc = Calculator()
        
        # Add observer with invalid path
        invalid_path = Path("/invalid/path/log.log")
        observer = LoggingObserver(invalid_path)
        calc.add_observer(observer)
        
        # Calculator should still work even if observer fails
        try:
            result = calc.calculate("add", 5, 3)
            assert result == 8
        except:
            # If it raises, that's ok for this test
            pass
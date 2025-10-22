"""
Comprehensive tests for Calculator class
"""
import pytest
import pandas as pd
from pathlib import Path
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.operations import AddOperation, SubtractOperation
from app.exceptions import OperationError, HistoryError


class TestCalculatorComprehensive:
    """Comprehensive test cases for Calculator class"""
    
    def test_calculator_initialization(self):
        """Test calculator initializes with empty state"""
        calc = Calculator()
        assert calc is not None
        assert len(calc.get_history()) == 0
    
    def test_calculator_add_operation(self):
        """Test calculator add operation"""
        calc = Calculator()
        result = calc.calculate("add", 5, 3)
        assert result == 8
    
    def test_calculator_subtract_operation(self):
        """Test calculator subtract operation"""
        calc = Calculator()
        result = calc.calculate("subtract", 10, 3)
        assert result == 7
    
    def test_calculator_multiply_operation(self):
        """Test calculator multiply operation"""
        calc = Calculator()
        result = calc.calculate("multiply", 4, 5)
        assert result == 20
    
    def test_calculator_divide_operation(self):
        """Test calculator divide operation"""
        calc = Calculator()
        result = calc.calculate("divide", 20, 4)
        assert result == 5.0
    
    def test_calculator_power_operation(self):
        """Test calculator power operation"""
        calc = Calculator()
        result = calc.calculate("power", 2, 3)
        assert result == 8
    
    def test_calculator_modulus_operation(self):
        """Test calculator modulus operation"""
        calc = Calculator()
        result = calc.calculate("modulus", 10, 3)
        assert result == 1
    
    def test_calculator_root_operation(self):
        """Test calculator root operation"""
        calc = Calculator()
        result = calc.calculate("root", 16, 2)
        assert result == 4.0
    
    def test_calculator_int_divide_operation(self):
        """Test calculator integer division operation"""
        calc = Calculator()
        result = calc.calculate("int_divide", 10, 3)
        assert result == 3
    
    def test_calculator_percent_operation(self):
        """Test calculator percentage operation"""
        calc = Calculator()
        result = calc.calculate("percent", 25, 100)
        assert result == 25.0
    
    def test_calculator_abs_diff_operation(self):
        """Test calculator absolute difference operation"""
        calc = Calculator()
        result = calc.calculate("abs_diff", 10, 3)
        assert result == 7
    
    def test_calculator_invalid_operation(self):
        """Test calculator raises error for invalid operation"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("invalid", 5, 3)
    
    def test_calculator_divide_by_zero(self):
        """Test calculator handles division by zero"""
        calc = Calculator()
        with pytest.raises(OperationError):
            calc.calculate("divide", 10, 0)
    
    def test_calculator_history_tracking(self):
        """Test calculator tracks calculation history"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        history = calc.get_history()
        assert len(history) == 2
    
    def test_calculator_get_last_calculation(self):
        """Test getting last calculation"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("multiply", 4, 5)
        
        last = calc.get_last_calculation()
        assert last.get_result() == 20
    
    def test_calculator_clear_history(self):
        """Test clearing calculator history"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.clear_history()
        assert len(calc.get_history()) == 0
    
    def test_calculator_undo(self):
        """Test undo functionality"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.undo()
        assert len(calc.get_history()) == 1
    
    def test_calculator_undo_empty_history(self):
        """Test undo with no history raises error"""
        calc = Calculator()
        with pytest.raises(HistoryError):
            calc.undo()
    
    def test_calculator_redo(self):
        """Test redo functionality"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.undo()
        calc.redo()
        
        assert len(calc.get_history()) == 2
    
    def test_calculator_redo_nothing_to_redo(self):
        """Test redo with nothing to redo raises error"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        
        with pytest.raises(HistoryError):
            calc.redo()
    
    def test_calculator_multiple_undo(self):
        """Test multiple undo operations"""
        calc = Calculator()
        calc.calculate("add", 1, 1)
        calc.calculate("add", 2, 2)
        calc.calculate("add", 3, 3)
        
        calc.undo()
        calc.undo()
        
        assert len(calc.get_history()) == 1
    
    def test_calculator_multiple_redo(self):
        """Test multiple redo operations"""
        calc = Calculator()
        calc.calculate("add", 1, 1)
        calc.calculate("add", 2, 2)
        calc.calculate("add", 3, 3)
        
        calc.undo()
        calc.undo()
        calc.redo()
        
        assert len(calc.get_history()) == 2
    
    def test_calculator_undo_then_new_calculation_clears_redo(self):
        """Test that new calculation after undo clears redo stack"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.undo()
        calc.calculate("multiply", 4, 5)
        
        with pytest.raises(HistoryError):
            calc.redo()
    
    def test_calculator_add_observer(self):
        """Test adding observer to calculator"""
        calc = Calculator()
        observer = LoggingObserver(Path("test.log"))
        
        calc.add_observer(observer)
        assert observer in calc.observers
    
    def test_calculator_remove_observer(self):
        """Test removing observer from calculator"""
        calc = Calculator()
        observer = LoggingObserver(Path("test.log"))
        
        calc.add_observer(observer)
        calc.remove_observer(observer)
        
        assert observer not in calc.observers
    
    def test_calculator_notify_observers(self, tmp_path):
        """Test calculator notifies observers on calculation"""
        calc = Calculator()
        log_file = tmp_path / "test.log"
        observer = LoggingObserver(log_file)
        
        calc.add_observer(observer)
        calc.calculate("add", 5, 3)
        
        assert log_file.exists()
    
    def test_calculator_save_history(self, tmp_path):
        """Test saving calculation history to file"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.save_history(history_file)
        
        assert history_file.exists()
        df = pd.read_csv(history_file)
        assert len(df) == 2
    
    def test_calculator_load_history(self, tmp_path):
        """Test loading calculation history from file"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        # Create and save history
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        calc.save_history(history_file)
        
        # Load into new calculator
        calc2 = Calculator()
        calc2.load_history(history_file)
        
        assert len(calc2.get_history()) == 2
    
    def test_calculator_load_nonexistent_file(self, tmp_path):
        """Test loading from nonexistent file raises error"""
        calc = Calculator()
        history_file = tmp_path / "nonexistent.csv"
        
        with pytest.raises(FileNotFoundError):
            calc.load_history(history_file)
    
    def test_calculator_save_empty_history(self, tmp_path):
        """Test saving empty history creates empty file"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        calc.save_history(history_file)
        
        assert history_file.exists()
        df = pd.read_csv(history_file)
        assert len(df) == 0
    
    def test_calculator_with_negative_numbers(self):
        """Test calculator with negative numbers"""
        calc = Calculator()
        
        result1 = calc.calculate("add", -5, -3)
        assert result1 == -8
        
        result2 = calc.calculate("multiply", -5, 3)
        assert result2 == -15
    
    def test_calculator_with_decimals(self):
        """Test calculator with decimal numbers"""
        calc = Calculator()
        
        result1 = calc.calculate("add", 5.5, 3.2)
        assert pytest.approx(result1, 0.001) == 8.7
        
        result2 = calc.calculate("multiply", 2.5, 4.0)
        assert result2 == 10.0
    
    def test_calculator_with_zero(self):
        """Test calculator operations with zero"""
        calc = Calculator()
        
        result1 = calc.calculate("add", 0, 5)
        assert result1 == 5
        
        result2 = calc.calculate("multiply", 0, 5)
        assert result2 == 0
    
    def test_calculator_large_numbers(self):
        """Test calculator with large numbers"""
        calc = Calculator()
        
        result = calc.calculate("multiply", 1000000, 1000)
        assert result == 1000000000
    
    def test_calculator_history_order(self):
        """Test history maintains chronological order"""
        calc = Calculator()
        
        calc.calculate("add", 1, 1)
        calc.calculate("add", 2, 2)
        calc.calculate("add", 3, 3)
        
        history = calc.get_history()
        assert history[0].get_result() == 2
        assert history[1].get_result() == 4
        assert history[2].get_result() == 6
    
    def test_calculator_can_undo(self):
        """Test can_undo method"""
        calc = Calculator()
        
        assert calc.can_undo() is False
        
        calc.calculate("add", 5, 3)
        assert calc.can_undo() is True
    
    def test_calculator_can_redo(self):
        """Test can_redo method"""
        calc = Calculator()
        calc.calculate("add", 5, 3)
        
        assert calc.can_redo() is False
        
        calc.undo()
        assert calc.can_redo() is True
    
    def test_calculator_get_history_count(self):
        """Test getting history count"""
        calc = Calculator()
        
        assert calc.get_history_count() == 0
        
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        assert calc.get_history_count() == 2
    
    def test_calculator_precision_handling(self):
        """Test calculator handles precision correctly"""
        calc = Calculator()
        
        result = calc.calculate("divide", 10, 3)
        # Should have reasonable precision
        assert pytest.approx(result, 0.0001) == 3.3333
    
    def test_calculator_state_consistency_after_error(self):
        """Test calculator state remains consistent after error"""
        calc = Calculator()
        
        calc.calculate("add", 5, 3)
        
        try:
            calc.calculate("divide", 10, 0)
        except OperationError:
            pass
        
        # History should only contain valid calculation
        assert len(calc.get_history()) == 1
        
        # Calculator should still work
        result = calc.calculate("subtract", 10, 2)
        assert result == 8
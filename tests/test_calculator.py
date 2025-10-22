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
    
    def test_calculator_notify_observers(self, tmp_path: Path):
        """Test calculator notifies observers on calculation"""
        calc = Calculator()
        log_file = tmp_path / "test.log"
        observer = LoggingObserver(log_file)
        
        calc.add_observer(observer)
        calc.calculate("add", 5, 3)
        
        assert log_file.exists()
    
    def test_calculator_save_history(self, tmp_path: Path):
        """Test saving calculation history to file"""
        calc = Calculator()
        history_file = tmp_path / "history.csv"
        
        calc.calculate("add", 5, 3)
        calc.calculate("subtract", 10, 2)
        
        calc.save_history(history_file)
        
        assert history_file.exists()
        df = pd.read_csv(history_file)
        assert len(df) == 2
    
    def test_calculator_load_history(self, tmp_path: Path):
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
    
    def test_calculator_load_nonexistent_file(self, tmp_path: Path):
        """Test loading from nonexistent file raises error"""
        calc = Calculator()
        history_file = tmp_path / "nonexistent.csv"
        
        with pytest.raises(FileNotFoundError):
            calc.load_history(history_file)
    
    def test_calculator_save_empty_history(self, tmp_path: Path):
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

# Test REPL FUNCTIONS
"""
Tests for REPL (Read-Eval-Print Loop) functionality
"""
import pytest
from unittest.mock import MagicMock, patch
from io import StringIO
from app.calculator import run_repl
from app.calculator import Calculator


class TestREPL:
    """Test cases for the REPL class"""
    
    def setup_method(self):
        """Set up test REPL instance"""
        self.calculator = Calculator()
        self.repl = run_repl(self.calculator)
    
    def test_repl_initialization(self):
        """Test REPL initializes correctly"""
        assert self.repl is not None
        assert self.repl.calculator is self.calculator
        assert self.repl.running is False
    
    @patch('builtins.input', side_effect=['add 5 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_add_command(self, mock_stdout, mock_input):
        """Test REPL add command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '8' in output
    
    @patch('builtins.input', side_effect=['subtract 10 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_subtract_command(self, mock_stdout, mock_input):
        """Test REPL subtract command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '7' in output
    
    @patch('builtins.input', side_effect=['multiply 4 5', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_multiply_command(self, mock_stdout, mock_input):
        """Test REPL multiply command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '20' in output
    
    @patch('builtins.input', side_effect=['divide 20 4', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_divide_command(self, mock_stdout, mock_input):
        """Test REPL divide command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '5' in output
    
    @patch('builtins.input', side_effect=['power 2 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_power_command(self, mock_stdout, mock_input):
        """Test REPL power command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '8' in output
    
    @patch('builtins.input', side_effect=['modulus 10 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_modulus_command(self, mock_stdout, mock_input):
        """Test REPL modulus command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '1' in output
    
    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_history_command_empty(self, mock_stdout, mock_input):
        """Test REPL history command when empty"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'empty' in output.lower() or 'no history' in output.lower()
    
    @patch('builtins.input', side_effect=['add 5 3', 'history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_history_command_with_data(self, mock_stdout, mock_input):
        """Test REPL history command with calculations"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'add' in output.lower()
        assert '5' in output
        assert '3' in output
    
    @patch('builtins.input', side_effect=['add 5 3', 'clear', 'history', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_clear_command(self, mock_stdout, mock_input):
        """Test REPL clear command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'cleared' in output.lower()
    
    @patch('builtins.input', side_effect=['add 5 3', 'undo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_undo_command(self, mock_stdout, mock_input):
        """Test REPL undo command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'undo' in output.lower()
    
    @patch('builtins.input', side_effect=['add 5 3', 'undo', 'redo', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_redo_command(self, mock_stdout, mock_input):
        """Test REPL redo command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'redo' in output.lower()
    
    @patch('builtins.input', side_effect=['help', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_help_command(self, mock_stdout, mock_input):
        """Test REPL help command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'add' in output.lower()
        assert 'subtract' in output.lower()
        assert 'exit' in output.lower()
    
    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_exit_command(self, mock_stdout, mock_input):
        """Test REPL exit command"""
        self.repl.start()
        
        assert self.repl.running is False
    
    @patch('builtins.input', side_effect=['invalid_command', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_invalid_command(self, mock_stdout, mock_input):
        """Test REPL handles invalid commands"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'invalid' in output.lower() or 'error' in output.lower()
    
    @patch('builtins.input', side_effect=['add 5', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_insufficient_arguments(self, mock_stdout, mock_input):
        """Test REPL handles insufficient arguments"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'error' in output.lower() or 'invalid' in output.lower()
    
    @patch('builtins.input', side_effect=['add abc 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_non_numeric_arguments(self, mock_stdout, mock_input):
        """Test REPL handles non-numeric arguments"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'error' in output.lower() or 'invalid' in output.lower()
    
    @patch('builtins.input', side_effect=['divide 10 0', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_division_by_zero(self, mock_stdout, mock_input):
        """Test REPL handles division by zero"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert 'error' in output.lower() or 'zero' in output.lower()
    
    @patch('builtins.input', side_effect=['root 16 2', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_root_command(self, mock_stdout, mock_input):
        """Test REPL root command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '4' in output
    
    @patch('builtins.input', side_effect=['int_divide 10 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_int_divide_command(self, mock_stdout, mock_input):
        """Test REPL integer division command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '3' in output
    
    @patch('builtins.input', side_effect=['percent 25 100', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_percent_command(self, mock_stdout, mock_input):
        """Test REPL percentage command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '25' in output
    
    @patch('builtins.input', side_effect=['abs_diff 10 3', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_abs_diff_command(self, mock_stdout, mock_input):
        """Test REPL absolute difference command"""
        self.repl.start()
        output = mock_stdout.getvalue()
        
        assert '7' in output
    
    @patch('builtins.input', side_effect=['add 5 3', 'save', 'exit'])
    def test_repl_save_command(self, mock_input, tmp_path: Path):
        """Test REPL save command"""
        # This test would need proper file path setup
        self.repl.start()
        # Verify save was called
    
    @patch('builtins.input', side_effect=['load', 'exit'])
    def test_repl_load_command(self, mock_input, tmp_path: Path):
        """Test REPL load command"""
        # This test would need proper file path setup
        self.repl.start()
        # Verify load was called
    
    @patch('builtins.input', side_effect=['', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_empty_input(self, mock_stdout, mock_input):
        """Test REPL handles empty input"""
        self.repl.start()
        # Should not crash
        assert True
    
    @patch('builtins.input', side_effect=['   ', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_repl_whitespace_input(self, mock_stdout, mock_input):
        """Test REPL handles whitespace input"""
        self.repl.start()
        # Should not crash
        assert True
    
    def test_repl_parse_command_valid(self):
        """Test parsing valid command"""
        command, args = self.repl.parse_command("add 5 3")
        assert command == "add"
        assert args == ["5", "3"]
    
    def test_repl_parse_command_with_extra_spaces(self):
        """Test parsing command with extra spaces"""
        command, args = self.repl.parse_command("add   5   3")
        assert command == "add"
        assert args == ["5", "3"]
    
    def test_repl_parse_command_case_insensitive(self):
        """Test parsing command is case insensitive"""
        command, args = self.repl.parse_command("ADD 5 3")
        assert command == "add"
        assert args == ["5", "3"]
    
    def test_repl_welcome_message(self):
        """Test REPL displays welcome message"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('builtins.input', side_effect=['exit']):
                self.repl.start()
                output = mock_stdout.getvalue()
                assert 'calculator' in output.lower() or 'welcome' in output.lower()
"""
Comprehensive tests for REPL to achieve 100% coverage
"""
import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from io import StringIO

from app.calculator_repl import REPL
from app.calculator import Calculator
from app.exceptions import CalculatorError, OperationError, ValidationError, HistoryError
from app.calculation import Calculation
from app.operations import Operation


class TestREPLInitialization:
    """Test REPL initialization"""
    
    def test_init(self):
        """Test REPL initialization"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        assert repl.calculator is calc
        assert repl.running is False
        assert len(repl.commands) == 18
        assert 'add' in repl.commands
        assert 'help' in repl.commands


class TestREPLStart:
    """Test REPL start method"""
    
    def test_start_with_exit(self):
        """Test starting REPL and exiting"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.input', side_effect=['exit']):
            with patch('builtins.print') as mock_print:
                repl.start()
        
        assert repl.running is False
        assert any('Welcome' in str(call) for call in mock_print.call_args_list)
    
    def test_start_with_empty_input(self):
        """Test REPL with empty input"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.input', side_effect=['', '  ', 'exit']):
            with patch('builtins.print'):
                repl.start()
        
        assert repl.running is False
    
    def test_start_with_keyboard_interrupt(self):
        """Test REPL with KeyboardInterrupt"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit']):
            with patch('builtins.print') as mock_print:
                repl.start()
        
        assert any('exit' in str(call).lower() for call in mock_print.call_args_list)
    
    def test_start_with_eof_error(self):
        """Test REPL with EOFError"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.input', side_effect=EOFError()):
            with patch('builtins.print'):
                repl.start()
        
        assert repl.running is True  # Loop breaks but flag stays True


class TestParseCommand:
    """Test command parsing"""
    
    def test_parse_command_with_args(self):
        """Test parsing command with arguments"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        command, args = repl.parse_command("add 5 3")
        assert command == "add"
        assert args == ["5", "3"]
    
    def test_parse_command_without_args(self):
        """Test parsing command without arguments"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        command, args = repl.parse_command("history")
        assert command == "history"
        assert args == []
    
    def test_parse_command_empty_string(self):
        """Test parsing empty string"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        command, args = repl.parse_command("")
        assert command == ""
        assert args == []
    
    def test_parse_command_case_insensitive(self):
        """Test command parsing is case insensitive"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        command, args = repl.parse_command("ADD 5 3")
        assert command == "add"


class TestProcessInput:
    """Test input processing"""
    
    def test_process_unknown_command(self):
        """Test processing unknown command"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._process_input("unknown")
        
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        assert "Unknown command" in call_args


class TestHandleOperation:
    """Test operation handling"""
    
    def test_handle_operation_success(self):
        """Test successful operation"""
        calc = Mock(spec=Calculator)
        calc.calculate.return_value = 8
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('add', ['5', '3'])
        
        calc.calculate.assert_called_once_with('add', 5.0, 3.0)
        mock_print.assert_called_with("Result: 8")
    
    def test_handle_operation_wrong_arg_count(self):
        """Test operation with wrong number of arguments"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('add', ['5'])
        
        call_args = str(mock_print.call_args_list)
        assert "requires exactly 2 operands" in call_args
        assert "Usage:" in call_args
    
    def test_handle_operation_invalid_number(self):
        """Test operation with invalid number format"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('add', ['abc', '3'])
        
        mock_print.assert_called_with("Error: Invalid number format. Please enter valid numbers.")
    
    def test_handle_operation_operation_error(self):
        """Test operation raising OperationError"""
        calc = Mock(spec=Calculator)
        calc.calculate.side_effect = OperationError("Division by zero")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('divide', ['5', '0'])
        
        mock_print.assert_called_with("Operation Error: Division by zero")
    
    def test_handle_operation_validation_error(self):
        """Test operation raising ValidationError"""
        calc = Mock(spec=Calculator)
        calc.calculate.side_effect = ValidationError("Invalid operand")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('add', ['5', '3'])
        
        mock_print.assert_called_with("Validation Error: Invalid operand")
    
    def test_handle_operation_calculator_error(self):
        """Test operation raising CalculatorError"""
        calc = Mock(spec=Calculator)
        calc.calculate.side_effect = CalculatorError("General error")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_operation('add', ['5', '3'])
        
        mock_print.assert_called_with("Calculator Error: General error")


class TestHandleHistory:
    """Test history handling"""
    
    def test_handle_history_empty(self):
        """Test displaying empty history"""
        calc = Mock(spec=Calculator)
        calc.get_history.return_value = []
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_history('history', [])
        
        mock_print.assert_called_with("History is empty.")
    
    def test_handle_history_with_calculations(self):
        """Test displaying history with calculations"""
        calc = Mock(spec=Calculator)
        
        # Create mock calculations
        mock_calc1 = Mock(spec=Calculation)
        mock_calc1.operation = Mock(spec=Operation)
        mock_calc1.operation.name = "add"
        mock_calc1.operation.symbol = "+"
        mock_calc1.operand1 = 5
        mock_calc1.operand2 = 3
        mock_calc1.result = 8
        
        mock_calc2 = Mock(spec=Calculation)
        mock_calc2.operation = Mock(spec=Operation)
        mock_calc2.operation.name = "multiply"
        mock_calc2.operation.symbol = "*"
        mock_calc2.operand1 = 4
        mock_calc2.operand2 = 2
        mock_calc2.result = 8
        
        calc.get_history.return_value = [mock_calc1, mock_calc2]
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_history('history', [])
        
        call_args = str(mock_print.call_args_list)
        assert "CALCULATION HISTORY" in call_args
        assert "1. 5 + 3 = 8 (add)" in call_args
        assert "2. 4 * 2 = 8 (multiply)" in call_args


class TestHandleClear:
    """Test clear handling"""
    
    def test_handle_clear(self):
        """Test clearing history"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_clear('clear', [])
        
        calc.clear_history.assert_called_once()
        mock_print.assert_called_with("History cleared successfully.")


class TestHandleUndo:
    """Test undo handling"""
    
    def test_handle_undo_success(self):
        """Test successful undo"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_undo('undo', [])
        
        calc.undo.assert_called_once()
        mock_print.assert_called_with("Undid last calculation.")
    
    def test_handle_undo_error(self):
        """Test undo with HistoryError"""
        calc = Mock(spec=Calculator)
        calc.undo.side_effect = HistoryError("Nothing to undo")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_undo('undo', [])
        
        mock_print.assert_called_with("Error: Nothing to undo")


class TestHandleRedo:
    """Test redo handling"""
    
    def test_handle_redo_success(self):
        """Test successful redo"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_redo('redo', [])
        
        calc.redo.assert_called_once()
        mock_print.assert_called_with("Redid last calculation.")
    
    def test_handle_redo_error(self):
        """Test redo with HistoryError"""
        calc = Mock(spec=Calculator)
        calc.redo.side_effect = HistoryError("Nothing to redo")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_redo('redo', [])
        
        mock_print.assert_called_with("Error: Nothing to redo")


class TestHandleSave:
    """Test save handling"""
    
    def test_handle_save_default_filename(self):
        """Test saving with default filename"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_save('save', [])
        
        calc.save_history.assert_called_once()
        call_args = calc.save_history.call_args[0][0]
        assert str(call_args) == "history.csv"
        
        call_str = str(mock_print.call_args_list)
        assert "History saved to" in call_str
    
    def test_handle_save_custom_filename(self):
        """Test saving with custom filename"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_save('save', ['custom.csv'])
        
        calc.save_history.assert_called_once()
        call_args = calc.save_history.call_args[0][0]
        assert str(call_args) == "custom.csv"
    
    def test_handle_save_error(self):
        """Test save with exception"""
        calc = Mock(spec=Calculator)
        calc.save_history.side_effect = Exception("Write error")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_save('save', [])
        
        mock_print.assert_called_with("Error saving history: Write error")


class TestHandleLoad:
    """Test load handling"""
    
    def test_handle_load_default_filename(self):
        """Test loading with default filename"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_load('load', [])
        
        calc.load_history.assert_called_once()
        call_args = calc.load_history.call_args[0][0]
        assert str(call_args) == "history.csv"
        
        call_str = str(mock_print.call_args_list)
        assert "History loaded from" in call_str
    
    def test_handle_load_custom_filename(self):
        """Test loading with custom filename"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_load('load', ['custom.csv'])
        
        calc.load_history.assert_called_once()
        call_args = calc.load_history.call_args[0][0]
        assert str(call_args) == "custom.csv"
    
    def test_handle_load_file_not_found(self):
        """Test load with FileNotFoundError"""
        calc = Mock(spec=Calculator)
        calc.load_history.side_effect = FileNotFoundError()
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_load('load', ['missing.csv'])
        
        mock_print.assert_called_with("Error: File 'missing.csv' not found.")
    
    def test_handle_load_general_error(self):
        """Test load with general exception"""
        calc = Mock(spec=Calculator)
        calc.load_history.side_effect = Exception("Read error")
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_load('load', [])
        
        mock_print.assert_called_with("Error loading history: Read error")


class TestHandleHelp:
    """Test help handling"""
    
    def test_handle_help(self):
        """Test displaying help"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._handle_help('help', [])
        
        call_args = str(mock_print.call_args_list)
        assert "AVAILABLE COMMANDS" in call_args
        assert "add <a> <b>" in call_args
        assert "subtract <a> <b>" in call_args
        assert "multiply <a> <b>" in call_args
        assert "divide <a> <b>" in call_args
        assert "power <a> <b>" in call_args
        assert "modulus <a> <b>" in call_args
        assert "root <a> <b>" in call_args
        assert "int_divide <a> <b>" in call_args
        assert "percent <a> <b>" in call_args
        assert "abs_diff <a> <b>" in call_args
        assert "history" in call_args
        assert "clear" in call_args
        assert "undo" in call_args
        assert "redo" in call_args
        assert "save" in call_args
        assert "load" in call_args
        assert "exit" in call_args


class TestHandleExit:
    """Test exit handling"""
    
    def test_handle_exit(self):
        """Test exiting REPL"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        repl.running = True
        
        with patch('builtins.print') as mock_print:
            repl._handle_exit('exit', [])
        
        assert repl.running is False
        call_args = str(mock_print.call_args_list)
        assert "Thank you" in call_args
        assert "Goodbye" in call_args


class TestGetLogger:
    """Test get_logger method"""
    
    def test_get_logger_none(self):
        """Test get_logger when no logger exists"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        logger = repl.get_logger()
        assert logger is None
    
    def test_get_logger_exists(self):
        """Test get_logger when logger exists"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        mock_logger = Mock()
        repl.logger = mock_logger
        
        logger = repl.get_logger()
        assert logger is mock_logger


class TestPrintWelcome:
    """Test print welcome method"""
    
    def test_print_welcome(self):
        """Test printing welcome message"""
        calc = Mock(spec=Calculator)
        repl = REPL(calc)
        
        with patch('builtins.print') as mock_print:
            repl._print_welcome()
        
        call_args = str(mock_print.call_args_list)
        assert "Welcome" in call_args
        assert "Advanced Calculator" in call_args
        assert "help" in call_args


class TestAllOperations:
    """Test all operation commands are properly mapped"""
    
    @pytest.mark.parametrize("operation", [
        'add', 'subtract', 'multiply', 'divide', 'power', 
        'modulus', 'root', 'int_divide', 'percent', 'abs_diff'
    ])
    def test_all_operations_mapped(self, operation):
        """Test that all operations are properly handled"""
        calc = Mock(spec=Calculator)
        calc.calculate.return_value = 42
        repl = REPL(calc)
        
        with patch('builtins.print'):
            repl._handle_operation(operation, ['10', '5'])
        
        calc.calculate.assert_called_once_with(operation, 10.0, 5.0)

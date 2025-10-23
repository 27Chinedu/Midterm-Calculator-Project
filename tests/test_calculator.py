"""
Comprehensive tests for Calculator class - 100% coverage
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
from app.calculator import (
    Calculator, 
    CalculatorObserver, 
    LoggingObserver, 
    AutoSaveObserver
)
from app.calculation import Calculation
from app.exceptions import CalculatorError


class TestCalculatorObserver:
    """Tests for CalculatorObserver abstract base class"""
    
    def test_observer_is_abstract(self):
        """Test that CalculatorObserver cannot be instantiated"""
        with pytest.raises(TypeError):
            CalculatorObserver()
    
    def test_observer_requires_update_method(self):
        """Test that concrete observers must implement update"""
        class InvalidObserver(CalculatorObserver):
            pass
        
        with pytest.raises(TypeError):
            InvalidObserver()


class TestLoggingObserver:
    """Tests for LoggingObserver"""
    
    def test_logging_observer_initialization(self):
        """Test LoggingObserver initializes with logger"""
        observer = LoggingObserver()
        
        assert observer is not None
        assert hasattr(observer, 'logger')
        assert observer.logger is not None
    
    @patch('app.calculator.Logger')
    def test_logging_observer_update_logs_calculation(self, mock_logger_class):
        """Test that update method logs calculation"""
        mock_logger = Mock()
        mock_logger_class.return_value = mock_logger
        
        observer = LoggingObserver()
        calc = Calculation("add", 5.0, 3.0, 8.0)
        
        observer.update(calc)
        
        mock_logger.log_calculation.assert_called_once_with(calc)
    
    def test_logging_observer_is_calculator_observer(self):
        """Test that LoggingObserver is a CalculatorObserver"""
        observer = LoggingObserver()
        assert isinstance(observer, CalculatorObserver)


class TestAutoSaveObserver:
    """Tests for AutoSaveObserver"""
    
    def test_autosave_observer_initialization(self):
        """Test AutoSaveObserver initializes with history manager"""
        mock_history = Mock()
        observer = AutoSaveObserver(mock_history)
        
        assert observer is not None
        assert observer.history_manager is mock_history
        assert hasattr(observer, 'logger')
    
    @patch('app.calculator.config')
    def test_autosave_observer_update_when_enabled(self, mock_config):
        """Test update saves when auto_save is enabled"""
        mock_config.auto_save = True
        mock_history = Mock()
        observer = AutoSaveObserver(mock_history)
        
        calc = Calculation("add", 5.0, 3.0, 8.0)
        observer.update(calc)
        
        mock_history.save_to_csv.assert_called_once()
    
    @patch('app.calculator.config')
    def test_autosave_observer_update_when_disabled(self, mock_config):
        """Test update does not save when auto_save is disabled"""
        mock_config.auto_save = False
        mock_history = Mock()
        observer = AutoSaveObserver(mock_history)
        
        calc = Calculation("add", 5.0, 3.0, 8.0)
        observer.update(calc)
        
        mock_history.save_to_csv.assert_not_called()
    
    @patch('app.calculator.config')
    def test_autosave_observer_handles_save_exception(self, mock_config):
        """Test update handles exceptions during save"""
        mock_config.auto_save = True
        mock_history = Mock()
        mock_history.save_to_csv.side_effect = Exception("Save failed")
        
        observer = AutoSaveObserver(mock_history)
        calc = Calculation("add", 5.0, 3.0, 8.0)
        
        # Should not raise exception
        observer.update(calc)
        
        mock_history.save_to_csv.assert_called_once()
    
    def test_autosave_observer_is_calculator_observer(self):
        """Test that AutoSaveObserver is a CalculatorObserver"""
        mock_history = Mock()
        observer = AutoSaveObserver(mock_history)
        assert isinstance(observer, CalculatorObserver)


class TestCalculatorInitialization:
    """Tests for Calculator initialization"""
    
    def test_calculator_initialization(self):
        """Test calculator initializes with all components"""
        calc = Calculator()
        
        assert calc is not None
        assert hasattr(calc, 'history_manager')
        assert hasattr(calc, 'memento_caretaker')
        assert hasattr(calc, 'logger')
        assert hasattr(calc, '_observers')
    
    def test_calculator_registers_default_observers(self):
        """Test calculator registers default observers on init"""
        calc = Calculator()
        
        assert len(calc._observers) == 2
        assert any(isinstance(obs, LoggingObserver) for obs in calc._observers)
        assert any(isinstance(obs, AutoSaveObserver) for obs in calc._observers)
    
    @patch('app.calculator.MementoCaretaker')
    def test_calculator_saves_initial_state(self, mock_caretaker_class):
        """Test calculator saves initial state on creation"""
        mock_caretaker = Mock()
        mock_caretaker_class.return_value = mock_caretaker
        
        calc = Calculator()
        
        # Should save initial state
        assert mock_caretaker.save.called


class TestCalculatorObserverManagement:
    """Tests for observer registration and management"""
    
    def test_register_observer(self):
        """Test registering a new observer"""
        calc = Calculator()
        initial_count = len(calc._observers)
        
        mock_observer = Mock(spec=CalculatorObserver)
        calc.register_observer(mock_observer)
        
        assert len(calc._observers) == initial_count + 1
        assert mock_observer in calc._observers
    
    def test_unregister_observer(self):
        """Test unregistering an existing observer"""
        calc = Calculator()
        mock_observer = Mock(spec=CalculatorObserver)
        calc.register_observer(mock_observer)
        
        calc.unregister_observer(mock_observer)
        
        assert mock_observer not in calc._observers
    
    def test_unregister_nonexistent_observer(self):
        """Test unregistering observer not in list does not raise error"""
        calc = Calculator()
        mock_observer = Mock(spec=CalculatorObserver)
        
        # Should not raise exception
        calc.unregister_observer(mock_observer)
    
    def test_notify_observers(self):
        """Test notifying all observers"""
        calc = Calculator()
        
        mock_obs1 = Mock(spec=CalculatorObserver)
        mock_obs2 = Mock(spec=CalculatorObserver)
        
        calc.register_observer(mock_obs1)
        calc.register_observer(mock_obs2)
        
        test_calc = Calculation("add", 5.0, 3.0, 8.0)
        calc._notify_observers(test_calc)
        
        mock_obs1.update.assert_called_with(test_calc)
        mock_obs2.update.assert_called_with(test_calc)
    
    def test_notify_observers_handles_exceptions(self):
        """Test observer exceptions don't stop notification"""
        calc = Calculator()
        
        mock_obs1 = Mock(spec=CalculatorObserver)
        mock_obs1.update.side_effect = Exception("Observer 1 failed")
        
        mock_obs2 = Mock(spec=CalculatorObserver)
        
        calc.register_observer(mock_obs1)
        calc.register_observer(mock_obs2)
        
        test_calc = Calculation("add", 5.0, 3.0, 8.0)
        calc._notify_observers(test_calc)
        
        # Both should be called despite first one failing
        mock_obs1.update.assert_called()
        mock_obs2.update.assert_called()


class TestCalculatorCalculate:
    """Tests for calculate method"""
    
    @patch('app.calculator.OperationFactory')
    def test_calculate_basic_operation(self, mock_factory):
        """Test basic calculation"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        result = calc.calculate("add", 5.0, 3.0)
        
        assert result == 8.0
        mock_factory.create_operation.assert_called_with("add")
        mock_operation.execute.assert_called_with(5.0, 3.0)
    
    @patch('app.calculator.OperationFactory')
    @patch('app.calculator.config')
    def test_calculate_rounds_to_precision(self, mock_config, mock_factory):
        """Test result is rounded to configured precision"""
        mock_config.precision = 2
        
        mock_operation = Mock()
        mock_operation.execute.return_value = 3.33333333
        mock_operation.get_symbol.return_value = "÷"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        result = calc.calculate("divide", 10.0, 3.0)
        
        assert result == 3.33
    
    @patch('app.calculator.OperationFactory')
    def test_calculate_adds_to_history(self, mock_factory):
        """Test calculation is added to history"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        initial_history_len = len(calc.get_history())
        
        calc.calculate("add", 5.0, 3.0)
        
        assert len(calc.get_history()) == initial_history_len + 1
    
    @patch('app.calculator.OperationFactory')
    def test_calculate_saves_state(self, mock_factory):
        """Test calculation saves state for undo/redo"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        
        # Should be able to undo
        assert calc.memento_caretaker.can_undo()
    
    @patch('app.calculator.OperationFactory')
    def test_calculate_notifies_observers(self, mock_factory):
        """Test calculation notifies observers"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        mock_observer = Mock(spec=CalculatorObserver)
        calc.register_observer(mock_observer)
        
        calc.calculate("add", 5.0, 3.0)
        
        assert mock_observer.update.called
    
    @patch('app.calculator.OperationFactory')
    def test_calculate_raises_on_error(self, mock_factory):
        """Test calculation raises exception on error"""
        mock_factory.create_operation.side_effect = Exception("Invalid operation")
        
        calc = Calculator()
        
        with pytest.raises(Exception):
            calc.calculate("invalid", 5.0, 3.0)


class TestCalculatorUndo:
    """Tests for undo functionality"""
    
    @patch('app.calculator.OperationFactory')
    def test_undo_successful(self, mock_factory):
        """Test successful undo operation"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        
        result = calc.undo()
        
        assert result is True
    
    def test_undo_when_nothing_to_undo(self):
        """Test undo returns False when nothing to undo"""
        calc = Calculator()
        
        # Undo initial state
        calc.undo()
        
        # Try to undo again
        result = calc.undo()
        
        assert result is False
    
    @patch('app.calculator.OperationFactory')
    def test_undo_restores_history(self, mock_factory):
        """Test undo restores previous history state"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        initial_len = len(calc.get_history())
        
        calc.calculate("add", 5.0, 3.0)
        after_calc_len = len(calc.get_history())
        
        calc.undo()
        after_undo_len = len(calc.get_history())
        
        assert after_calc_len > initial_len
        assert after_undo_len == initial_len
    
    @patch('app.calculator.MementoCaretaker')
    def test_undo_when_memento_returns_none(self, mock_caretaker_class):
        """Test undo handles None memento"""
        mock_caretaker = Mock()
        mock_caretaker.can_undo.return_value = True
        mock_caretaker.undo.return_value = None
        mock_caretaker_class.return_value = mock_caretaker
        
        calc = Calculator()
        result = calc.undo()
        
        assert result is False


class TestCalculatorRedo:
    """Tests for redo functionality"""
    
    @patch('app.calculator.OperationFactory')
    def test_redo_successful(self, mock_factory):
        """Test successful redo operation"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        calc.undo()
        
        result = calc.redo()
        
        assert result is True
    
    def test_redo_when_nothing_to_redo(self):
        """Test redo returns False when nothing to redo"""
        calc = Calculator()
        
        result = calc.redo()
        
        assert result is False
    
    @patch('app.calculator.OperationFactory')
    def test_redo_restores_history(self, mock_factory):
        """Test redo restores undone history"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        after_calc_len = len(calc.get_history())
        
        calc.undo()
        after_undo_len = len(calc.get_history())
        
        calc.redo()
        after_redo_len = len(calc.get_history())
        
        assert after_undo_len < after_calc_len
        assert after_redo_len == after_calc_len
    
    @patch('app.calculator.MementoCaretaker')
    def test_redo_when_memento_returns_none(self, mock_caretaker_class):
        """Test redo handles None memento"""
        mock_caretaker = Mock()
        mock_caretaker.can_redo.return_value = True
        mock_caretaker.redo.return_value = None
        mock_caretaker_class.return_value = mock_caretaker
        
        calc = Calculator()
        result = calc.redo()
        
        assert result is False


class TestCalculatorHistory:
    """Tests for history management"""
    
    def test_get_history(self):
        """Test getting calculation history"""
        calc = Calculator()
        
        history = calc.get_history()
        
        assert isinstance(history, list)
    
    @patch('app.calculator.OperationFactory')
    def test_get_history_returns_calculations(self, mock_factory):
        """Test get_history returns actual calculations"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        
        history = calc.get_history()
        
        assert len(history) > 0
        assert isinstance(history[0], Calculation)
    
    def test_clear_history(self):
        """Test clearing history"""
        calc = Calculator()
        calc.clear_history()
        
        assert len(calc.get_history()) == 0
    
    @patch('app.calculator.OperationFactory')
    def test_clear_history_removes_all(self, mock_factory):
        """Test clear_history removes all calculations"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        calc.calculate("add", 5.0, 3.0)
        calc.calculate("add", 10.0, 2.0)
        
        calc.clear_history()
        
        assert len(calc.get_history()) == 0
    
    def test_clear_history_saves_state(self):
        """Test clear_history saves state for undo"""
        calc = Calculator()
        calc.clear_history()
        
        # Should be able to undo clear
        assert calc.memento_caretaker.can_undo()

class TestCalculatorFilePersistence:
    """Tests for save/load history"""
    
    def test_save_history_with_filepath(self, tmp_path):
        """Test saving history with specified filepath"""
        filepath = str(tmp_path / "history.csv")
        
        calc = Calculator()
        
        # Add some calculations to history first
        with patch('app.calculator.OperationFactory') as mock_factory:
            mock_operation = Mock()
            mock_operation.execute.return_value = 8.0
            mock_operation.get_symbol.return_value = "+"
            mock_factory.create_operation.return_value = mock_operation
            
            calc.calculate("add", 5.0, 3.0)
        
        # Save history
        calc.save_history(filepath)
        
        # File should exist
        assert Path(filepath).exists()
    
    def test_save_history_without_filepath(self):
        """Test saving history with default filepath"""
        calc = Calculator()
        
        # Should not raise exception
        calc.save_history(None)
    
    def test_save_history_calls_history_manager(self):
        """Test save_history delegates to history manager"""
        calc = Calculator()
        
        # Mock the history manager's save_to_csv method
        with patch.object(calc.history_manager, 'save_to_csv') as mock_save:
            calc.save_history("test.csv")
            
            # Verify the method was called with a Path object
            mock_save.assert_called_once()
            call_arg = mock_save.call_args[0][0]
            assert isinstance(call_arg, Path)
            assert call_arg.name == "test.csv"
    
    def test_load_history_with_filepath(self, tmp_path):
        """Test loading history with specified filepath"""
        filepath = str(tmp_path / "history.csv")
        
        # Create a dummy file
        Path(filepath).touch()
        
        calc = Calculator()
        
        # Mock the history manager's load_from_csv method
        with patch.object(calc.history_manager, 'load_from_csv') as mock_load:
            calc.load_history(filepath)
            
            # Verify the method was called with a Path object
            mock_load.assert_called_once()
            call_arg = mock_load.call_args[0][0]
            assert isinstance(call_arg, Path)
            assert call_arg.name == "history.csv"
    
    def test_load_history_without_filepath(self):
        """Test loading history with default filepath"""
        calc = Calculator()
        
        # Mock the history manager's load_from_csv method
        with patch.object(calc.history_manager, 'load_from_csv') as mock_load:
            calc.load_history(None)
            
            # Verify the method was called with None
            mock_load.assert_called_once_with(None)
    
    def test_load_history_saves_state(self):
        """Test load_history saves state after loading"""
        calc = Calculator()
        
        # Mock both the history manager and _save_state
        with patch.object(calc.history_manager, 'load_from_csv') as mock_load, \
             patch.object(calc, '_save_state') as mock_save:
            
            calc.load_history("test.csv")
            
            # Should call load_from_csv and then save_state
            mock_load.assert_called_once()
            mock_save.assert_called_once()
    
    def test_save_history_converts_string_to_path(self):
        """Test save_history converts string to Path"""
        calc = Calculator()
        
        with patch.object(calc.history_manager, 'save_to_csv') as mock_save:
            calc.save_history("test.csv")
            
            # Should be called with Path object
            call_arg = mock_save.call_args[0][0]
            assert isinstance(call_arg, Path)
            assert call_arg.name == "test.csv"
    
    def test_load_history_converts_string_to_path(self):
        """Test load_history converts string to Path"""
        calc = Calculator()
        
        with patch.object(calc.history_manager, 'load_from_csv') as mock_load:
            calc.load_history("test.csv")
            
            # Should be called with Path object
            call_arg = mock_load.call_args[0][0]
            assert isinstance(call_arg, Path)
            assert call_arg.name == "test.csv"
    
    def test_save_history_creates_actual_file(self, tmp_path):
        """Test that save_history actually creates a file with content"""
        filepath = str(tmp_path / "actual_history.csv")
        
        calc = Calculator()
        
        # Add a calculation to have something to save
        with patch('app.calculator.OperationFactory') as mock_factory:
            mock_operation = Mock()
            mock_operation.execute.return_value = 15.0
            mock_operation.get_symbol.return_value = "+"
            mock_factory.create_operation.return_value = mock_operation
            
            calc.calculate("add", 10.0, 5.0)
        
        # Save to file
        calc.save_history(filepath)
        
        # Verify file was created and has content
        assert Path(filepath).exists()
        
        # Read the file to verify it has content
        with open(filepath, 'r') as f:
            content = f.read()
            assert len(content) > 0
            # Should contain CSV headers or data
            assert 'operation' in content or 'operand1' in content
    
    def test_load_history_from_actual_file(self, tmp_path):
        """Test loading history from an actual file"""
        filepath = str(tmp_path / "load_history.csv")
        
        # Create a valid CSV file with calculation data
        csv_content = """operation,operand1,operand2,result,timestamp
add,5.0,3.0,8.0,2024-01-01T10:00:00
subtract,10.0,4.0,6.0,2024-01-01T10:01:00"""
        
        with open(filepath, 'w') as f:
            f.write(csv_content)
        
        calc = Calculator()
        
        # Load from the file
        calc.load_history(filepath)
        
        # Verify history was loaded
        history = calc.get_history()
        assert len(history) == 2
        assert history[0].operation == "add"
        assert history[0].result == 8.0
        assert history[1].operation == "subtract"
        assert history[1].result == 6.

class TestCalculatorIntegration:
    """Integration tests for Calculator"""
    
    @patch('app.calculator.OperationFactory')
    def test_full_workflow(self, mock_factory):
        """Test complete workflow: calculate, undo, redo, clear"""
        mock_operation = Mock()
        mock_operation.execute.return_value = 8.0
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        
        # Calculate
        result = calc.calculate("add", 5.0, 3.0)
        assert result == 8.0
        assert len(calc.get_history()) > 0
        
        # Undo
        calc.undo()
        assert len(calc.get_history()) == 0
        
        # Redo
        calc.redo()
        assert len(calc.get_history()) > 0
        
        # Clear
        calc.clear_history()
        assert len(calc.get_history()) == 0
    
    @patch('app.calculator.OperationFactory')
    def test_multiple_calculations(self, mock_factory):
        """Test multiple calculations"""
        mock_operation = Mock()
        mock_operation.execute.side_effect = [8.0, 7.0, 20.0]
        mock_operation.get_symbol.return_value = "+"
        mock_factory.create_operation.return_value = mock_operation
        
        calc = Calculator()
        
        calc.calculate("add", 5.0, 3.0)
        calc.calculate("add", 4.0, 3.0)
        calc.calculate("add", 10.0, 10.0)
        
        assert len(calc.get_history()) == 3
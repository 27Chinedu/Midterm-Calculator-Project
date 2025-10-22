"""
Pytest configuration and shared fixtures
"""
import pytest
import os
from pathlib import Path
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory


@pytest.fixture
def calculator():
    """Fixture to provide a fresh calculator instance"""
    return Calculator()


@pytest.fixture
def operation_factory():
    """Fixture to provide an operation factory instance"""
    return OperationFactory()


@pytest.fixture
def temp_log_file(tmp_path):
    """Fixture to provide a temporary log file path"""
    return tmp_path / "test.log"


@pytest.fixture
def temp_history_file(tmp_path):
    """Fixture to provide a temporary history file path"""
    return tmp_path / "history.csv"


@pytest.fixture
def temp_config_dir(tmp_path):
    """Fixture to provide temporary config directories"""
    log_dir = tmp_path / "logs"
    history_dir = tmp_path / "history"
    log_dir.mkdir()
    history_dir.mkdir()
    return {
        'log_dir': log_dir,
        'history_dir': history_dir
    }


@pytest.fixture
def clean_environment(monkeypatch):
    """Fixture to provide clean environment variables"""
    # Clear any existing calculator environment variables
    env_vars = [
        'CALCULATOR_LOG_DIR',
        'CALCULATOR_HISTORY_DIR',
        'CALCULATOR_MAX_HISTORY_SIZE',
        'CALCULATOR_AUTO_SAVE',
        'CALCULATOR_PRECISION',
        'CALCULATOR_MAX_INPUT_VALUE',
        'CALCULATOR_DEFAULT_ENCODING'
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def sample_calculations():
    """Fixture to provide sample calculation data"""
    from app.calculation import Calculation
    from app.operations import AddOperation, SubtractOperation, MultiplyOperation
    
    return [
        Calculation(AddOperation(), 5, 3),
        Calculation(SubtractOperation(), 10, 2),
        Calculation(MultiplyOperation(), 4, 5)
    ]


@pytest.fixture
def mock_config(tmp_path, monkeypatch):
    """Fixture to provide a mock configuration"""
    log_dir = tmp_path / "logs"
    history_dir = tmp_path / "history"
    
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(history_dir))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
    monkeypatch.setenv("CALCULATOR_PRECISION", "6")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
    
    return CalculatorConfig()


@pytest.fixture(autouse=True)
def reset_singletons():
    """Fixture to reset any singleton instances between tests"""
    # This ensures each test gets a fresh state
    yield
    # Cleanup code here if needed


@pytest.fixture
def calculation_history_data():
    """Fixture to provide sample history data for CSV operations"""
    return [
        {'operation': 'add', 'operand1': 5, 'operand2': 3, 'result': 8, 'timestamp': '2024-01-01 12:00:00'},
        {'operation': 'subtract', 'operand1': 10, 'operand2': 2, 'result': 8, 'timestamp': '2024-01-01 12:01:00'},
        {'operation': 'multiply', 'operand1': 4, 'operand2': 5, 'result': 20, 'timestamp': '2024-01-01 12:02:00'}
    ]


@pytest.fixture
def populated_calculator(calculator, sample_calculations):
    """Fixture to provide a calculator with existing calculations"""
    for calc in sample_calculations:
        calculator.history.add(calc)
    return calculator
"""
Tests for calculator configuration management
"""
import pytest
import os
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


class TestCalculatorConfig:
    """Test cases for the CalculatorConfig class"""
    
    def test_config_initialization_with_defaults(self):
        """Test config initializes with default values"""
        config = CalculatorConfig()
        
        assert config.log_dir is not None
        assert config.history_dir is not None
        assert config.max_history_size == 100
        assert config.precision == 10
        assert config.max_input_value == 1e10
        assert config.auto_save is True
        assert config.default_encoding == 'utf-8'
    
    def test_config_load_from_env(self, monkeypatch):
        """Test config loads values from environment variables"""
        monkeypatch.setenv("CALCULATOR_LOG_DIR", "/tmp/logs")
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "/tmp/history")
        monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "200")
        monkeypatch.setenv("CALCULATOR_PRECISION", "4")
        monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "999999")
        monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
        
        config = CalculatorConfig()
        
        assert str(config.log_dir) == "/tmp/logs"
        assert str(config.history_dir) == "/tmp/history"
        assert config.max_history_size == 200
        assert config.precision == 4
        assert config.max_input_value == 999999
        assert config.auto_save is True
    
    def test_config_auto_save_false(self, monkeypatch):
        """Test auto_save set to False"""
        monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
        config = CalculatorConfig()
        assert config.auto_save is False
    
    def test_config_invalid_max_history_size(self, monkeypatch):
        """Test invalid max_history_size raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "not_a_number")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
    
    def test_config_invalid_precision(self, monkeypatch):
        """Test invalid precision raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_PRECISION", "not_a_number")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
    
    def test_config_invalid_max_input_value(self, monkeypatch):
        """Test invalid max_input_value raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "not_a_number")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
    
    def test_config_creates_directories(self, tmp_path, monkeypatch):
        """Test config creates log and history directories"""
        log_dir = tmp_path / "logs"
        history_dir = tmp_path / "history"
        
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(history_dir))
        
        config = CalculatorConfig()
        
        assert log_dir.exists()
        assert history_dir.exists()
    
    def test_config_log_file_path(self, tmp_path, monkeypatch):
        """Test config returns correct log file path"""
        log_dir = tmp_path / "logs"
        monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
        
        config = CalculatorConfig()
        log_file = config.get_log_file_path()
        
        assert log_file.parent == log_dir
        assert log_file.name == "calculator.log"
    
    def test_config_history_file_path(self, tmp_path, monkeypatch):
        """Test config returns correct history file path"""
        history_dir = tmp_path / "history"
        monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(history_dir))
        
        config = CalculatorConfig()
        history_file = config.get_history_file_path()
        
        assert history_file.parent == history_dir
        assert history_file.name == "history.csv"
    
    def test_config_default_encoding(self):
        """Test config has default encoding"""
        config = CalculatorConfig()
        assert config.default_encoding == "utf-8"
    
    def test_config_custom_encoding(self, monkeypatch):
        """Test config with custom encoding"""
        monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "ascii")
        config = CalculatorConfig()
        assert config.default_encoding == "ascii"
    
    def test_config_validate_all_settings(self):
        """Test config validation succeeds with valid settings"""
        config = CalculatorConfig()
        # Should not raise any exception
        config.validate()
    
    def test_config_negative_max_history_size(self, monkeypatch):
        """Test negative max_history_size raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-100")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
    
    def test_config_zero_precision(self, monkeypatch):
        """Test zero precision raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_PRECISION", "0")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
    
    def test_config_negative_max_input_value(self, monkeypatch):
        """Test negative max_input_value raises ConfigurationError"""
        monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "-1000")
        
        with pytest.raises(ConfigurationError):
            CalculatorConfig()
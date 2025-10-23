"""
Configuration management for the calculator application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from app.exceptions import ConfigurationError

class CalculatorConfig:
    """Manages calculator configuration settings."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        self.load_configuration()
        self.validate()  # Call validate after loading
    
    def load_configuration(self):
        """Load configuration from environment variables with defaults."""
        # Base Directories
        self.log_dir = Path(os.getenv('CALCULATOR_LOG_DIR', 'logs'))
        self.history_dir = Path(os.getenv('CALCULATOR_HISTORY_DIR', 'history'))
        
        # Create directories if they don't exist
        self.log_dir.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
        
        # History Settings - FIXED DEFAULT FROM 1000 to 100
        self.max_history_size = self._safe_int_getenv('CALCULATOR_MAX_HISTORY_SIZE', 100)
        self.auto_save = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() == 'true'
        
        # Calculation Settings
        self.precision = self._safe_int_getenv('CALCULATOR_PRECISION', 10)
        self.max_input_value = self._safe_float_getenv('CALCULATOR_MAX_INPUT_VALUE', 1e10)
        self.default_encoding = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
        
        # File paths
        self.log_file = self.log_dir / 'calculator.log'
        self.history_file = self.history_dir / 'history.csv'
    
    def _safe_int_getenv(self, key: str, default: int) -> int:
        """Safely get integer from environment variable."""
        try:
            value = os.getenv(key)
            if value is None:
                return default
            return int(value)
        except ValueError:
            raise ConfigurationError(f"Invalid integer value for {key}: {os.getenv(key)}")
    
    def _safe_float_getenv(self, key: str, default: float) -> float:
        """Safely get float from environment variable."""
        try:
            value = os.getenv(key)
            if value is None:
                return default
            return float(value)
        except ValueError:
            raise ConfigurationError(f"Invalid float value for {key}: {os.getenv(key)}")
    
    def validate(self):
        """Validate configuration values."""
        if self.max_history_size < 1:
            raise ConfigurationError("CALCULATOR_MAX_HISTORY_SIZE must be at least 1")
        
        if self.precision < 0:
            raise ConfigurationError("CALCULATOR_PRECISION must be non-negative")
        
        if self.max_input_value <= 0:
            raise ConfigurationError("CALCULATOR_MAX_INPUT_VALUE must be positive")
    
    def get_log_file_path(self) -> Path:
        """Get the log file path."""
        return self.log_file
    
    def get_history_file_path(self) -> Path:
        """Get the history file path."""
        return self.history_file

# Global configuration instance
config = CalculatorConfig()
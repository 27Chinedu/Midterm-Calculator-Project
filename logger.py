"""
Logging configuration and Logger class for the calculator application.
"""

import logging
from pathlib import Path
from typing import Optional
from app.calculator_config import config

class Logger:
    """Custom logger for the calculator application."""
    
    _instance: Optional['Logger'] = None
    
    def __new__(cls):
        """Ensure only one logger instance exists (singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with configuration."""
        self.logger = logging.getLogger('CalculatorApp')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Create file handler
        file_handler = logging.FileHandler(
            config.log_file,
            encoding=config.default_encoding
        )
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def log_calculation(self, calculation):
        """Log a calculation."""
        self.info(f"Calculation performed: {calculation}")
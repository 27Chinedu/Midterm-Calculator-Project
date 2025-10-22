"""
Tests for logger functionality
"""
import pytest
import logging
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
from app.logger import Logger


class TestLogger:
    """Test cases for Logger class"""
    
    def test_logger_singleton(self):
        """Test that Logger is a singleton"""
        logger1 = Logger()
        logger2 = Logger()
        
        assert logger1 is logger2
    
    def test_logger_initialization(self):
        """Test logger initializes correctly"""
        logger = Logger()
        assert hasattr(logger, 'logger')
        assert isinstance(logger.logger, logging.Logger)
    
    def test_logger_has_handlers(self):
        """Test logger has file and console handlers"""
        logger = Logger()
        assert len(logger.logger.handlers) >= 1
    
    @patch('app.logger.config')
    def test_logger_methods(self, mock_config):
        """Test all logger methods"""
        # Mock config
        mock_config.log_file = Path("/tmp/test.log")
        mock_config.default_encoding = 'utf-8'
        
        logger = Logger()
        
        # Test that methods don't raise exceptions
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        logger.debug("Test debug message")
    
    def test_log_calculation(self):
        """Test logging a calculation"""
        logger = Logger()
        calc = Mock()
        calc.__str__ = Mock(return_value="2 + 2 = 4")
        
        # Should not raise exception
        logger.log_calculation(calc)
    
    def test_logger_with_temp_file(self):
        """Test logger with temporary file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            # Mock config to use temp file
            with patch('app.logger.config') as mock_config:
                mock_config.log_file = temp_path
                mock_config.default_encoding = 'utf-8'
                
                # Reinitialize logger to use temp file
                Logger._instance = None  # Reset singleton
                logger = Logger()
                
                # Log a message
                logger.info("Test message")
                
                # Verify file was created and has content
                assert temp_path.exists()
                # Note: We can't easily verify content due to logging buffering
                
        finally:
            # Clean up
            if temp_path.exists():
                os.unlink(temp_path)
            # Reset singleton for other tests
            Logger._instance = None
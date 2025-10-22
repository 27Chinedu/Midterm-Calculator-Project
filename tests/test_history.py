"""
Tests for history management functionality
"""
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from app.history import HistoryManager
from app.calculation import Calculation
from app.operations import AddOperation
from app.exceptions import FileOperationError


class TestHistoryManager:
    """Test cases for the HistoryManager class"""
    
    def setup_method(self):
        """Set up test history instance"""
        self.history = HistoryManager()
    
    def test_history_initialization(self):
        """Test history initializes empty"""
        assert len(self.history.get_history()) == 0
        assert bool(self.history) == False
    
    def test_add_calculation_to_history(self):
        """Test adding a calculation to history"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        assert len(self.history.get_history()) == 1
        assert self.history.get_history()[0] == calc
        assert bool(self.history) == True
    
    def test_history_max_size_limit(self, monkeypatch):
        """Test history respects max size limit"""
        # Mock config to have small max size for testing
        mock_config = Mock()
        mock_config.max_history_size = 3
        monkeypatch.setattr('app.history.config', mock_config)
        
        history = HistoryManager()
        for i in range(5):
            calc = Calculation(AddOperation(), i, 1)
            history.add_calculation(calc)
        
        assert len(history.get_history()) == 3
        # Should keep the most recent calculations
        recent_calcs = history.get_history()
        assert recent_calcs[0].operand1 == 2  # Third calculation
        assert recent_calcs[1].operand1 == 3  # Fourth calculation
        assert recent_calcs[2].operand1 == 4  # Fifth calculation
    
    def test_clear_history(self):
        """Test clearing all history"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        self.history.clear_history()
        assert len(self.history.get_history()) == 0
    
    def test_get_recent_calculations(self):
        """Test getting the most recent calculations"""
        calcs = [Calculation(AddOperation(), i, 1) for i in range(5)]
        for calc in calcs:
            self.history.add_calculation(calc)
        
        recent = self.history.get_recent(3)
        assert len(recent) == 3
        assert recent[0].operand1 == 2
        assert recent[1].operand1 == 3
        assert recent[2].operand1 == 4
    
    def test_get_recent_with_default_count(self):
        """Test getting recent calculations with default count"""
        calcs = [Calculation(AddOperation(), i, 1) for i in range(15)]
        for calc in calcs:
            self.history.add_calculation(calc)
        
        recent = self.history.get_recent()
        assert len(recent) == 10  # Default count
    
    def test_get_recent_from_empty_history(self):
        """Test getting recent calculations from empty history"""
        recent = self.history.get_recent(5)
        assert len(recent) == 0
    
    def test_history_length_method(self):
        """Test __len__ method"""
        assert len(self.history) == 0
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        assert len(self.history) == 1
    
    def test_history_bool_method(self):
        """Test __bool__ method"""
        assert bool(self.history) == False
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        assert bool(self.history) == True
    
    def test_save_to_csv_success(self):
        """Test successful save to CSV"""
        # Create test calculations
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(AddOperation(), 10, 2)
        self.history.add_calculation(calc1)
        self.history.add_calculation(calc2)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            # Save to CSV
            self.history.save_to_csv(temp_path)
            
            # Verify file was created and has content
            assert temp_path.exists()
            
            # Read back the CSV to verify content
            df = pd.read_csv(temp_path)
            assert len(df) == 2
            assert df.iloc[0]['operand1'] == 5.0
            assert df.iloc[1]['operand1'] == 10.0
            
        finally:
            # Clean up
            if temp_path.exists():
                os.unlink(temp_path)
    
    def test_save_to_csv_empty_history(self):
        """Test saving empty history to CSV"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
        
        try:
            # This should not create a file or raise an error
            self.history.save_to_csv(temp_path)
            
            # File might not exist or be empty, both are acceptable
            if temp_path.exists():
                # If file exists, it should be valid CSV (possibly with just headers)
                df = pd.read_csv(temp_path)
                # Should have no data rows
                assert len(df) == 0
            
        finally:
            if temp_path.exists():
                os.unlink(temp_path)
    
    def test_save_to_csv_error(self):
        """Test error handling during CSV save"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        
        # Use an invalid path to trigger an error
        invalid_path = Path("/invalid/path/history.csv")
        
        with pytest.raises(FileOperationError):
            self.history.save_to_csv(invalid_path)
    
    def test_load_from_csv_success(self):
        """Test successful load from CSV"""
        # First create a test CSV file
        test_data = [
            {'operation': 'add', 'operand1': 5.0, 'operand2': 3.0, 'result': 8.0, 'timestamp': '2023-01-01 10:00:00'},
            {'operation': 'add', 'operand1': 10.0, 'operand2': 2.0, 'result': 12.0, 'timestamp': '2023-01-01 10:01:00'}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            df = pd.DataFrame(test_data)
            df.to_csv(temp_path, index=False)
        
        try:
            # Load from CSV
            self.history.load_from_csv(temp_path)
            
            # Verify history was loaded correctly
            assert len(self.history) == 2
            history_calcs = self.history.get_history()
            assert history_calcs[0].operand1 == 5.0
            assert history_calcs[1].operand1 == 10.0
            
        finally:
            if temp_path.exists():
                os.unlink(temp_path)
    
    def test_load_from_csv_file_not_found(self):
        """Test loading from non-existent CSV file"""
        non_existent_path = Path("/non/existent/path/history.csv")
        
        # This should not raise an error, just log a warning
        self.history.load_from_csv(non_existent_path)
        assert len(self.history) == 0  # History should remain empty
    
    def test_load_from_csv_empty_file(self):
        """Test loading from empty CSV file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            # Create empty file
            temp_file.write("")
        
        try:
            # This should not raise an error
            self.history.load_from_csv(temp_path)
            assert len(self.history) == 0  # History should remain empty
            
        finally:
            if temp_path.exists():
                os.unlink(temp_path)
    
    def test_load_from_csv_error(self):
        """Test error handling during CSV load with corrupted file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            # Write invalid CSV content
            temp_file.write("invalid,csv,content\nmore,invalid,data")
        
        try:
            with pytest.raises(FileOperationError):
                self.history.load_from_csv(temp_path)
            
        finally:
            if temp_path.exists():
                os.unlink(temp_path)
    
    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not the original list"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        
        history_copy = self.history.get_history()
        history_copy.append("not a calculation")  # This should not affect original
        
        assert len(self.history.get_history()) == 1
        assert len(history_copy) == 2  # Our modified copy has 2 items


# Additional tests for edge cases
class TestHistoryManagerEdgeCases:
    """Test edge cases for HistoryManager"""
    
    def setup_method(self):
        self.history = HistoryManager()
    
    def test_add_none_calculation(self):
        """Test adding None to history (should raise error)"""
        with pytest.raises(AttributeError):
            self.history.add_calculation(None)
    
    def test_get_recent_with_negative_count(self):
        """Test getting recent with negative count"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        
        # Negative count should return empty list
        recent = self.history.get_recent(-1)
        assert recent == []
    
    def test_get_recent_with_zero_count(self):
        """Test getting recent with zero count"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add_calculation(calc)
        
        # Zero count should return empty list
        recent = self.history.get_recent(0)
        assert recent == []
    
    def test_get_recent_with_larger_count_than_history(self):
        """Test getting recent with count larger than history size"""
        calcs = [Calculation(AddOperation(), i, 1) for i in range(3)]
        for calc in calcs:
            self.history.add_calculation(calc)
        
        # Request more items than available
        recent = self.history.get_recent(10)
        assert len(recent) == 3  # Should return all available items


# Mock tests for external dependencies
class TestHistoryManagerWithMocks:
    """Test HistoryManager with mocked dependencies"""
    
    def test_save_to_csv_with_mock_config(self):
        """Test save_to_csv uses config when no filepath provided"""
        history = HistoryManager()
        calc = Calculation(AddOperation(), 5, 3)
        history.add_calculation(calc)
        
        mock_config = Mock()
        mock_config.history_file = Path("/mock/path/history.csv")
        mock_config.default_encoding = 'utf-8'
        
        with patch('app.history.config', mock_config), \
             patch('app.history.pd.DataFrame') as mock_dataframe, \
             patch('app.history.Path.exists', return_value=True):
            
            mock_df_instance = Mock()
            mock_dataframe.return_value = mock_df_instance
            
            history.save_to_csv()  # No filepath provided, should use config
            
            # Verify config history_file was used
            mock_df_instance.to_csv.assert_called_once_with(
                mock_config.history_file, 
                index=False, 
                encoding=mock_config.default_encoding
            )
    
    def test_load_from_csv_with_mock_config(self):
        """Test load_from_csv uses config when no filepath provided"""
        history = HistoryManager()
        
        mock_config = Mock()
        mock_config.history_file = Path("/mock/path/history.csv")
        mock_config.default_encoding = 'utf-8'
        
        mock_df = Mock()
        mock_df.iterrows.return_value = []  # Empty dataframe
        
        with patch('app.history.config', mock_config), \
             patch('app.history.pd.read_csv', return_value=mock_df), \
             patch('app.history.Path.exists', return_value=True):
            
            history.load_from_csv()  # No filepath provided, should use config
            
            # Verify config history_file was used
            pd.read_csv.assert_called_once_with(
                mock_config.history_file, 
                encoding=mock_config.default_encoding
            )
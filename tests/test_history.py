"""
Tests for history management functionality
"""
import pytest
from app.history import History
from app.calculation import Calculation
from app.operations import AddOperation


class TestHistory:
    """Test cases for the History class"""
    
    def setup_method(self):
        """Set up test history instance"""
        self.history = History(max_size=5)
    
    def test_history_initialization(self):
        """Test history initializes empty"""
        assert len(self.history.get_all()) == 0
    
    def test_add_calculation_to_history(self):
        """Test adding a calculation to history"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add(calc)
        assert len(self.history.get_all()) == 1
        assert self.history.get_all()[0] == calc
    
    def test_history_max_size_limit(self):
        """Test history respects max size limit"""
        for i in range(10):
            calc = Calculation(AddOperation(), i, 1)
            self.history.add(calc)
        assert len(self.history.get_all()) == 5
    
    def test_clear_history(self):
        """Test clearing all history"""
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add(calc)
        self.history.clear()
        assert len(self.history.get_all()) == 0
    
    def test_get_last_calculation(self):
        """Test getting the most recent calculation"""
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(AddOperation(), 10, 2)
        self.history.add(calc1)
        self.history.add(calc2)
        assert self.history.get_last() == calc2
    
    def test_get_last_from_empty_history(self):
        """Test getting last calculation from empty history"""
        assert self.history.get_last() is None
    
    def test_history_iteration(self):
        """Test iterating over history"""
        calcs = [Calculation(AddOperation(), i, 1) for i in range(3)]
        for calc in calcs:
            self.history.add(calc)
        
        history_list = list(self.history.get_all())
        assert len(history_list) == 3
    
    def test_history_remove_calculation(self):
        """Test removing a specific calculation from history"""
        calc1 = Calculation(AddOperation(), 5, 3)
        calc2 = Calculation(AddOperation(), 10, 2)
        self.history.add(calc1)
        self.history.add(calc2)
        
        self.history.remove(calc1)
        assert len(self.history.get_all()) == 1
        assert calc1 not in self.history.get_all()
    
    def test_history_count(self):
        """Test getting count of history entries"""
        assert self.history.count() == 0
        calc = Calculation(AddOperation(), 5, 3)
        self.history.add(calc)
        assert self.history.count() == 1
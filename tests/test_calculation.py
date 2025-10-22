"""
Tests for Calculation class 
"""
import pytest
from datetime import datetime
from app.calculation import Calculation


class TestCalculation:
    """Comprehensive tests for Calculation class"""
    
    def test_init_with_timestamp(self):
        """Test initialization with explicit timestamp"""
        timestamp = datetime(2024, 1, 1, 12, 0, 0)
        calc = Calculation("add", 5.0, 3.0, 8.0, timestamp)
        
        assert calc.operation == "add"
        assert calc.operand1 == 5.0
        assert calc.operand2 == 3.0
        assert calc.result == 8.0
        assert calc.timestamp == timestamp
    
    def test_init_without_timestamp(self):
        """Test initialization without timestamp - uses datetime.now()"""
        before = datetime.now()
        calc = Calculation("subtract", 10.0, 3.0, 7.0)
        after = datetime.now()
        
        assert calc.operation == "subtract"
        assert calc.operand1 == 10.0
        assert calc.operand2 == 3.0
        assert calc.result == 7.0
        assert before <= calc.timestamp <= after
    
    def test_init_with_none_timestamp(self):
        """Test initialization with None timestamp - uses datetime.now()"""
        calc = Calculation("multiply", 4.0, 5.0, 20.0, None)
        
        assert calc.operation == "multiply"
        assert isinstance(calc.timestamp, datetime)
    
    def test_str_method(self):
        """Test __str__ method"""
        calc = Calculation("add", 5.0, 3.0, 8.0)
        result = str(calc)
        
        assert result == "5.0 add 3.0 = 8.0"
    
    def test_str_with_different_operation(self):
        """Test __str__ with different operation"""
        calc = Calculation("divide", 20.0, 4.0, 5.0)
        result = str(calc)
        
        assert result == "20.0 divide 4.0 = 5.0"
    
    def test_repr_method(self):
        """Test __repr__ method"""
        timestamp = datetime(2024, 1, 1, 12, 0, 0)
        calc = Calculation("power", 2.0, 3.0, 8.0, timestamp)
        result = repr(calc)
        
        assert "Calculation(" in result
        assert "operation='power'" in result
        assert "operand1=2.0" in result
        assert "operand2=3.0" in result
        assert "result=8.0" in result
        assert "timestamp=" in result
    
    def test_to_dict_method(self):
        """Test to_dict method"""
        timestamp = datetime(2024, 6, 15, 14, 30, 0)
        calc = Calculation("modulus", 10.0, 3.0, 1.0, timestamp)
        result = calc.to_dict()
        
        assert result['operation'] == "modulus"
        assert result['operand1'] == 10.0
        assert result['operand2'] == 3.0
        assert result['result'] == 1.0
        assert result['timestamp'] == "2024-06-15T14:30:00"
    
    def test_to_dict_with_microseconds(self):
        """Test to_dict preserves microseconds in timestamp"""
        timestamp = datetime(2024, 1, 1, 12, 0, 0, 123456)
        calc = Calculation("add", 1.0, 2.0, 3.0, timestamp)
        result = calc.to_dict()
        
        assert result['timestamp'] == "2024-01-01T12:00:00.123456"
    
    def test_from_dict_method(self):
        """Test from_dict class method"""
        data = {
            'operation': 'subtract',
            'operand1': 15.0,
            'operand2': 7.0,
            'result': 8.0,
            'timestamp': '2024-03-20T10:15:30'
        }
        
        calc = Calculation.from_dict(data)
        
        assert calc.operation == 'subtract'
        assert calc.operand1 == 15.0
        assert calc.operand2 == 7.0
        assert calc.result == 8.0
        assert calc.timestamp == datetime(2024, 3, 20, 10, 15, 30)
    
    def test_from_dict_converts_string_numbers(self):
        """Test from_dict converts string numbers to float"""
        data = {
            'operation': 'multiply',
            'operand1': '4.5',
            'operand2': '2.0',
            'result': '9.0',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        calc = Calculation.from_dict(data)
        
        assert calc.operand1 == 4.5
        assert calc.operand2 == 2.0
        assert calc.result == 9.0
        assert isinstance(calc.operand1, float)
        assert isinstance(calc.operand2, float)
        assert isinstance(calc.result, float)
    
    def test_from_dict_with_microseconds(self):
        """Test from_dict parses microseconds correctly"""
        data = {
            'operation': 'divide',
            'operand1': 10.0,
            'operand2': 3.0,
            'result': 3.333,
            'timestamp': '2024-12-25T18:45:30.654321'
        }
        
        calc = Calculation.from_dict(data)
        
        assert calc.timestamp == datetime(2024, 12, 25, 18, 45, 30, 654321)
        assert calc.timestamp.microsecond == 654321
    
    def test_round_trip_to_dict_from_dict(self):
        """Test complete round trip: to_dict then from_dict"""
        original = Calculation(
            "root",
            16.0,
            2.0,
            4.0,
            datetime(2024, 7, 4, 9, 30, 15)
        )
        
        # Convert to dict
        data = original.to_dict()
        
        # Convert back from dict
        restored = Calculation.from_dict(data)
        
        assert restored.operation == original.operation
        assert restored.operand1 == original.operand1
        assert restored.operand2 == original.operand2
        assert restored.result == original.result
        assert restored.timestamp == original.timestamp
    
    def test_with_negative_numbers(self):
        """Test with negative operands"""
        calc = Calculation("add", -5.0, -3.0, -8.0)
        
        assert calc.operand1 == -5.0
        assert calc.operand2 == -3.0
        assert calc.result == -8.0
        assert str(calc) == "-5.0 add -3.0 = -8.0"
    
    def test_with_zero_values(self):
        """Test with zero values"""
        calc = Calculation("multiply", 0.0, 100.0, 0.0)
        
        assert calc.operand1 == 0.0
        assert calc.operand2 == 100.0
        assert calc.result == 0.0
    
    def test_with_decimal_precision(self):
        """Test with high decimal precision"""
        calc = Calculation("divide", 10.123456789, 3.987654321, 2.54)
        
        assert calc.operand1 == 10.123456789
        assert calc.operand2 == 3.987654321
        assert calc.result == 2.54
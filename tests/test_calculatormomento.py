"""
Tests for calculator memento pattern
"""
import pytest
from app.calculator_momento import CalculatorMemento, MementoCaretaker
from app.calculation import Calculation
from app.operations import AddOperation


class TestCalculatorMemento:
    """Test cases for CalculatorMemento"""
    
    def test_memento_creation(self):
        """Test creating a memento"""
        calculations = [Calculation("add", 1, 2, 3)]
        memento = CalculatorMemento(calculations)
        assert memento is not None
    
    def test_memento_get_state(self):
        """Test getting state from memento"""
        calculations = [Calculation("add", 1, 2, 3), Calculation("subtract", 5, 3, 2)]
        memento = CalculatorMemento(calculations)
        state = memento.get_state()
        
        assert len(state) == 2
        assert state[0].result == 3
        assert state[1].result == 2
    
    def test_memento_state_is_copy(self):
        """Test that memento state is a copy"""
        original_calcs = [Calculation("add", 1, 2, 3)]
        memento = CalculatorMemento(original_calcs)
        
        # Modify original
        original_calcs.append(Calculation("multiply", 2, 3, 6))
        
        # Memento state should not be affected
        assert len(memento.get_state()) == 1


class TestMementoCaretaker:
    """Test cases for MementoCaretaker"""
    
    def test_caretaker_initialization(self):
        """Test caretaker initializes correctly"""
        caretaker = MementoCaretaker()
        assert caretaker._current_index == -1
        assert len(caretaker._mementos) == 0
    
    def test_save_memento(self):
        """Test saving a memento"""
        caretaker = MementoCaretaker()
        calculations = [Calculation("add", 1, 2, 3)]
        memento = CalculatorMemento(calculations)
        
        caretaker.save(memento)
        
        assert len(caretaker._mementos) == 1
        assert caretaker._current_index == 0
    
    def test_save_multiple_mementos(self):
        """Test saving multiple mementos"""
        caretaker = MementoCaretaker()
        
        memento1 = CalculatorMemento([Calculation("add", 1, 2, 3)])
        memento2 = CalculatorMemento([Calculation("subtract", 5, 3, 2)])
        
        caretaker.save(memento1)
        caretaker.save(memento2)
        
        assert len(caretaker._mementos) == 2
        assert caretaker._current_index == 1
    
    def test_undo_redo_workflow(self):
        """Test complete undo/redo workflow"""
        caretaker = MementoCaretaker()
        
        memento1 = CalculatorMemento([Calculation("add", 1, 2, 3)])
        memento2 = CalculatorMemento([Calculation("subtract", 5, 3, 2)])
        
        caretaker.save(memento1)
        caretaker.save(memento2)
        
        # Test undo
        assert caretaker.can_undo() == True
        undone = caretaker.undo()
        assert undone == memento1
        assert caretaker._current_index == 0
        
        # Test redo
        assert caretaker.can_redo() == True
        redone = caretaker.redo()
        assert redone == memento2
        assert caretaker._current_index == 1
    
    def test_undo_when_nothing_to_undo(self):
        """Test undo when no mementos available"""
        caretaker = MementoCaretaker()
        
        assert caretaker.can_undo() == False
        assert caretaker.undo() is None
    
    def test_redo_when_nothing_to_redo(self):
        """Test redo when no mementos available"""
        caretaker = MementoCaretaker()
        
        assert caretaker.can_redo() == False
        assert caretaker.redo() is None
    
    def test_save_after_undo_clears_redo(self):
        """Test that saving after undo clears redo stack"""
        caretaker = MementoCaretaker()
        
        memento1 = CalculatorMemento([Calculation("add", 1, 2, 3)])
        memento2 = CalculatorMemento([Calculation("subtract", 5, 3, 2)])
        memento3 = CalculatorMemento([Calculation("multiply", 2, 3, 6)])
        
        caretaker.save(memento1)
        caretaker.save(memento2)
        caretaker.undo()  # Now at memento1
        
        # Save new memento - should clear memento2 from redo stack
        caretaker.save(memento3)
        
        assert len(caretaker._mementos) == 2  # memento1 and memento3
        assert caretaker._current_index == 1
        assert caretaker.can_redo() == False
    
    def test_can_undo_can_redo_edge_cases(self):
        """Test edge cases for can_undo and can_redo"""
        caretaker = MementoCaretaker()
        
        # Empty caretaker
        assert caretaker.can_undo() == False
        assert caretaker.can_redo() == False
        
        # One memento
        memento = CalculatorMemento([Calculation("add", 1, 2, 3)])
        caretaker.save(memento)
        
        assert caretaker.can_undo() == False  # Only one state, can't undo to before initial
        assert caretaker.can_redo() == False
        
        # Two mementos
        memento2 = CalculatorMemento([Calculation("subtract", 5, 3, 2)])
        caretaker.save(memento2)
        
        assert caretaker.can_undo() == True
        assert caretaker.can_redo() == False
        
        caretaker.undo()
        assert caretaker.can_undo() == False
        assert caretaker.can_redo() == True
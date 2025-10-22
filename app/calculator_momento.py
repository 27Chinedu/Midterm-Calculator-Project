"""
Memento pattern implementation for undo/redo functionality.
"""

from typing import List, Optional
from app.calculation import Calculation

class CalculatorMemento:
    """Memento class to store calculator state."""
    
    def __init__(self, state: List[Calculation]):
        """Initialize memento with a state."""
        self._state = state.copy()
    
    def get_state(self) -> List[Calculation]:
        """Get the stored state."""
        return self._state.copy()

class MementoCaretaker:
    """Manages memento objects for undo/redo functionality."""
    
    def __init__(self):
        """Initialize the caretaker."""
        self._mementos: List[CalculatorMemento] = []
        self._current_index: int = -1
    
    def save(self, memento: CalculatorMemento):
        """Save a new memento."""
        # Remove any mementos after current index (for new branch after undo)
        self._mementos = self._mementos[:self._current_index + 1]
        self._mementos.append(memento)
        self._current_index = len(self._mementos) - 1
    
    def undo(self) -> Optional[CalculatorMemento]:
        """Get the previous memento."""
        if self._current_index > 0:
            self._current_index -= 1
            return self._mementos[self._current_index]
        return None
    
    def redo(self) -> Optional[CalculatorMemento]:
        """Get the next memento."""
        if self._current_index < len(self._mementos) - 1:
            self._current_index += 1
            return self._mementos[self._current_index]
        return None
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return self._current_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return self._current_index < len(self._mementos) - 1
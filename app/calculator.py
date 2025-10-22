"""
Main Calculator class with observer pattern implementation.
"""

from pathlib import Path
from typing import List, Optional
from abc import ABC, abstractmethod
from calculation import Calculation
from operations import OperationFactory
from history import HistoryManager
from calculator_momento import CalculatorMemento, MementoCaretaker
from input_validator import InputValidator
from calculator_config import config
from logger import Logger
from exceptions import CalculatorError
import pandas as pd

class CalculatorObserver(ABC):
    """Abstract base class for calculator observers."""
    
    @abstractmethod
    def update(self, calculation: Calculation):
        """Called when a new calculation is performed."""
        pass

class LoggingObserver(CalculatorObserver):
    """Observer that logs calculations."""
    
    def __init__(self):
        self.logger = Logger()
    
    def update(self, calculation: Calculation):
        """Log the calculation."""
        self.logger.log_calculation(calculation)

class AutoSaveObserver(CalculatorObserver):
    """Observer that auto-saves history to CSV."""
    
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager
        self.logger = Logger()
    
    def update(self, calculation: Calculation):
        """Auto-save history if enabled."""
        if config.auto_save:
            try:
                self.history_manager.save_to_csv()
                self.logger.debug("History auto-saved")
            except Exception as e:
                self.logger.error(f"Auto-save failed: {e}")

class Calculator:
    """Main calculator class with observer pattern."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.history_manager = HistoryManager()
        self.memento_caretaker = MementoCaretaker()
        self.logger = Logger()
        self._observers: List[CalculatorObserver] = []
        
        # Register default observers
        self.register_observer(LoggingObserver())
        self.register_observer(AutoSaveObserver(self.history_manager))
        
        # Save initial state
        self._save_state()
    
    def register_observer(self, observer: CalculatorObserver):
        """Register an observer."""
        self._observers.append(observer)
    
    def unregister_observer(self, observer: CalculatorObserver):
        """Unregister an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, calculation: Calculation):
        """Notify all observers of a new calculation."""
        for observer in self._observers:
            try:
                observer.update(calculation)
            except Exception as e:
                self.logger.error(f"Observer notification failed: {e}")
    
    def _save_state(self):
        """Save current state to memento."""
        memento = CalculatorMemento(self.history_manager.get_history())
        self.memento_caretaker.save(memento)
    
    def calculate(self, operation_name: str, operand1: float, operand2: float) -> float:
        """
        Perform a calculation.
        
        Args:
            operation_name: Name of the operation
            operand1: First operand
            operand2: Second operand
            
        Returns:
            Result of the calculation
            
        Raises:
            CalculatorError: If calculation fails
        """
        try:
            # Create operation using factory
            operation = OperationFactory.create_operation(operation_name)
            
            # Execute operation
            result = operation.execute(operand1, operand2)
            
            # Round to configured precision
            result = round(result, config.precision)
            
            # Create calculation record
            calculation = Calculation(
                operation=operation.get_symbol(),
                operand1=operand1,
                operand2=operand2,
                result=result
            )
            
            # Add to history
            self.history_manager.add_calculation(calculation)
            
            # Save state for undo/redo
            self._save_state()
            
            # Notify observers
            self._notify_observers(calculation)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Calculation failed: {e}")
            raise
    
    def undo(self) -> bool:
        """
        Undo the last calculation.
        
        Returns:
            True if undo was successful
        """
        if not self.memento_caretaker.can_undo():
            self.logger.warning("Nothing to undo")
            return False
        
        memento = self.memento_caretaker.undo()
        if memento:
            self.history_manager._history = memento.get_state()
            self.logger.info("Undo performed")
            return True
        return False
    
    def redo(self) -> bool:
        """
        Redo the last undone calculation.
        
        Returns:
            True if redo was successful
        """
        if not self.memento_caretaker.can_redo():
            self.logger.warning("Nothing to redo")
            return False
        
        memento = self.memento_caretaker.redo()
        if memento:
            self.history_manager._history = memento.get_state()
            self.logger.info("Redo performed")
            return True
        return False
    
    def get_history(self) -> List[Calculation]:
        """Get calculation history."""
        return self.history_manager.get_history()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history_manager.clear_history()
        self._save_state()
    
    def save_history(self, filepath: Optional[str] = None):
        """Save history to file."""
        path = None if filepath is None else Path(filepath)
        self.history_manager.save_to_csv(path)
    
    def load_history(self, filepath: Optional[str] = None):
        """Load history from file."""
        path = None if filepath is None else Path(filepath)
        self.history_manager.load_from_csv(path)
        self._save_state()
    
    def run_repl(self):
        """Run the calculator REPL (Read-Eval-Print Loop)."""
        print("\n" + "="*50)
        print("Welcome to Chinedu's Brand New Calculator!")
        print("="*50)
        print("\nType 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("Calculator> ").strip()
                
                if not user_input:
                    continue
                
                # Parse input
                command, operand1, operand2 = InputValidator.parse_calculation_input(user_input)
                
                # Handle non-calculation commands
                if command == 'exit':
                    print("Thank you for using Chinedu's Calculator!")
                    break
                    
                elif command == 'help':
                    self._show_help()
                    
                elif command == 'history':
                    self._show_history()
                    
                elif command == 'clear':
                    self.clear_history()
                    print("History cleared.")
                    
                elif command == 'undo':
                    if self.undo():
                        print("Undo successful.")
                    else:
                        print("Nothing to undo.")
                        
                elif command == 'redo':
                    if self.redo():
                        print("Redo successful.")
                    else:
                        print("Nothing to redo.")
                
                else:
                    # Assume it's a calculation command
                    try:
                        result = self.calculate(command, operand1, operand2)
                        print(f"Result: {result}")
                    except CalculatorError as e:
                        print(f"Calculation error: {e}")
                    except Exception as e:
                        self.logger.error(f"Unexpected error during calculation: {e}")
                        print("An unexpected error occurred. See logs for details.")
            
            except (KeyboardInterrupt, EOFError):
                # Graceful exit on Ctrl-C / EOF
                print("\nExiting calculator. Goodbye!")
                break
            except Exception as e:
                # Catch-all for unexpected exceptions in the REPL loop
                self.logger.error(f"REPL error: {e}")
                print(f"Error: {e}")
                continue
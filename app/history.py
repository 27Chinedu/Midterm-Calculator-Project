"""
History management for the calculator application.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from app.calculation import Calculation
from app.calculator_config import config
from app.exceptions import HistoryError, FileOperationError
from app.logger import Logger

class HistoryManager:
    """Manages calculation history with persistence."""
    
    def __init__(self):
        """Initialize the history manager."""
        self._history: List[Calculation] = []
        self.logger = Logger()
    
    def add_calculation(self, calculation: Calculation):
        """Add a calculation to history."""
        self._history.append(calculation)
        
        # Enforce maximum history size
        if len(self._history) > config.max_history_size:
            self._history.pop(0)
    
    def get_history(self) -> List[Calculation]:
        """Get all calculations in history."""
        return self._history.copy()
    
    def clear_history(self):
        """Clear all history."""
        self._history.clear()
        self.logger.info("History cleared")
    
    def save_to_csv(self, filepath: Optional[Path] = None):
        """
        Save history to CSV file using pandas.
        
        Args:
            filepath: Optional custom filepath
        """
        filepath = filepath or config.history_file
        
        try:
            if not self._history:
                self.logger.warning("No history to save")
                return
            
            # Convert calculations to dictionaries
            data = [calc.to_dict() for calc in self._history]
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Save to CSV
            df.to_csv(filepath, index=False, encoding=config.default_encoding)
            
            self.logger.info(f"History saved to {filepath}")
            
        except Exception as e:
            error_msg = f"Failed to save history: {e}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg)
    
    def load_from_csv(self, filepath: Optional[Path] = None):
        """
        Load history from CSV file using pandas.
        
        Args:
            filepath: Optional custom filepath
        """
        filepath = filepath or config.history_file
        
        try:
            if not filepath.exists():
                self.logger.warning(f"History file not found: {filepath}")
                return
            
            # Read CSV
            df = pd.read_csv(filepath, encoding=config.default_encoding)
            
            # Clear current history
            self._history.clear()
            
            # Convert DataFrame rows to Calculation objects
            for _, row in df.iterrows():
                calc_dict = row.to_dict()
                calculation = Calculation.from_dict(calc_dict)
                self._history.append(calculation)
            
            self.logger.info(f"Loaded {len(self._history)} calculations from {filepath}")
            
        except pd.errors.EmptyDataError:
            self.logger.warning("History file is empty")
        except Exception as e:
            error_msg = f"Failed to load history: {e}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg)
    
    def get_recent(self, count: int = 10) -> List[Calculation]:
        """Get the most recent calculations."""
        return self._history[-count:] if self._history else []
    
    def __len__(self) -> int:
        """Get the number of calculations in history."""
        return len(self._history)
    
    def __bool__(self) -> bool:
        """Check if history has any calculations."""
        return bool(self._history)
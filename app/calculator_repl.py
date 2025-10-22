"""
REPL (Read-Eval-Print Loop) interface for the calculator
"""
from typing import Tuple, List
from app.calculator import Calculator
from app.exceptions import CalculatorError, OperationError, ValidationError, HistoryError


class REPL:
    """Command-line interface for the calculator"""
    
    def __init__(self, calculator: Calculator):
        """
        Initialize REPL with a calculator instance
        
        Args:
            calculator: Calculator instance to use
        """
        self.calculator = calculator
        self.running = False
        self.commands = {
            'add': self._handle_operation,
            'subtract': self._handle_operation,
            'multiply': self._handle_operation,
            'divide': self._handle_operation,
            'power': self._handle_operation,
            'modulus': self._handle_operation,
            'root': self._handle_operation,
            'int_divide': self._handle_operation,
            'percent': self._handle_operation,
            'abs_diff': self._handle_operation,
            'history': self._handle_history,
            'clear': self._handle_clear,
            'undo': self._handle_undo,
            'redo': self._handle_redo,
            'save': self._handle_save,
            'load': self._handle_load,
            'help': self._handle_help,
            'exit': self._handle_exit,
        }
    
    def start(self):
        """Start the REPL"""
        self.running = True
        self._print_welcome()
        
        while self.running:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                self._process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit the calculator.")
            except EOFError:
                break
    
    def _print_welcome(self):
        """Print welcome message"""
        print("\nWelcome to Chinedu's Brand New Advanced Calculator!")
        print("Type 'help' for available commands or 'exit' to quit.\n")
    
    def _process_input(self, user_input: str):
        """
        Process user input
        
        Args:
            user_input: User's input string
        """
        command, args = self.parse_command(user_input)
        
        if command in self.commands:
            self.commands[command](command, args)
        else:
            print(f"Error: Unknown command '{command}'. Type 'help' for available commands.")
    
    def parse_command(self, user_input: str) -> Tuple[str, List[str]]:
        """
        Parse user input into command and arguments
        
        Args:
            user_input: User's input string
            
        Returns:
            Tuple of (command, arguments)
        """
        parts = user_input.split()
        command = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        return command, args
    
    def _handle_operation(self, command: str, args: List[str]):
        """
        Handle arithmetic operation
        
        Args:
            command: Operation name
            args: List of operands
        """
        if len(args) != 2:
            print(f"Error: '{command}' requires exactly 2 operands.")
            print(f"Usage: {command} <number1> <number2>")
            return
        
        try:
            operand1 = float(args[0])
            operand2 = float(args[1])
            
            result = self.calculator.calculate(command, operand1, operand2)
            print(f"Result: {result}")
            
        except ValueError:
            print("Error: Invalid number format. Please enter valid numbers.")
        except OperationError as e:
            print(f"Operation Error: {e}")
        except ValidationError as e:
            print(f"Validation Error: {e}")
        except CalculatorError as e:
            print(f"Calculator Error: {e}")
    
    def _handle_history(self, command: str, args: List[str]):
        """Display calculation history"""
        history = self.calculator.get_history()
        
        if not history:
            print("History is empty.")
            return
        
        print("\n" + "=" * 60)
        print("CALCULATION HISTORY")
        print("=" * 60)
        
        for i, calc in enumerate(history, 1):
            op_name = calc.operation.name
            op_symbol = calc.operation.symbol
            result = calc.get_result()
            
            print(f"{i}. {calc.operand1} {op_symbol} {calc.operand2} = {result} ({op_name})")
        
        print("=" * 60)
    
    def _handle_clear(self, command: str, args: List[str]):
        """Clear calculation history"""
        self.calculator.clear_history()
        print("History cleared successfully.")
    
    def _handle_undo(self, command: str, args: List[str]):
        """Undo last calculation"""
        try:
            self.calculator.undo()
            print("Undid last calculation.")
        except HistoryError as e:
            print(f"Error: {e}")
    
    def _handle_redo(self, command: str, args: List[str]):
        """Redo last undone calculation"""
        try:
            self.calculator.redo()
            print("Redid last calculation.")
        except HistoryError as e:
            print(f"Error: {e}")
    
    def _handle_save(self, command: str, args: List[str]):
        """Save calculation history to file"""
        try:
            from pathlib import Path
            
            filename = args[0] if args else "history.csv"
            filepath = Path(filename)
            
            self.calculator.save_history(filepath)
            print(f"History saved to {filepath}")
            
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def _handle_load(self, command: str, args: List[str]):
        """Load calculation history from file"""
        try:
            from pathlib import Path
            
            filename = args[0] if args else "history.csv"
            filepath = Path(filename)
            
            self.calculator.load_history(filepath)
            print(f"History loaded from {filepath}")
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def _handle_help(self, command: str, args: List[str]):
        """Display help information"""
        print("\n" + "=" * 60)
        print("AVAILABLE COMMANDS")
        print("=" * 60)
        print("\nArithmetic Operations:")
        print("  add <a> <b>         - Add two numbers")
        print("  subtract <a> <b>    - Subtract b from a")
        print("  multiply <a> <b>    - Multiply two numbers")
        print("  divide <a> <b>      - Divide a by b")
        print("  power <a> <b>       - Raise a to the power of b")
        print("  modulus <a> <b>     - Calculate a modulo b")
        print("  root <a> <b>        - Calculate bth root of a")
        print("  int_divide <a> <b>  - Integer division of a by b")
        print("  percent <a> <b>     - Calculate a as percentage of b")
        print("  abs_diff <a> <b>    - Absolute difference between a and b")
        
        print("\nHistory Commands:")
        print("  history             - Display calculation history")
        print("  clear               - Clear calculation history")
        print("  undo                - Undo last calculation")
        print("  redo                - Redo last undone calculation")
        
        print("\nFile Operations:")
        print("  save [filename]     - Save history to file (default: history.csv)")
        print("  load [filename]     - Load history from file (default: history.csv)")
        
        print("\nOther Commands:")
        print("  help                - Display this help message")
        print("  exit                - Exit the calculator")
        print("=" * 60)
    
    def _handle_exit(self, command: str, args: List[str]):
        """Exit the calculator"""
        print("\nThank you for using the Advanced Calculator. Goodbye!")
        self.running = False
    
    def get_logger(self):
        """Get logger instance (for testing)"""
        return getattr(self, 'logger', None)
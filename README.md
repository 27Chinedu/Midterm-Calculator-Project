# Advanced Python Calculator
A sophisticated, feature-rich calculator application built with Python that demonstrates modern software engineering practices including design patterns, comprehensive testing, and CI/CD integration.

## FEATURES
Basic Operations: Addition, Subtraction, Multiplication, Division

### Advanced Operations:
- Power and root calculations
- Modulus and integer division
- Percentage calculations
- Absolute difference
- Precision Control: Configurable decimal precision for results
- Input Validation: Robust validation with custom error handling

### Advanced Features
- Calculation History: Persistent storage with configurable size limits
- Undo/Redo Functionality: Memento pattern implementation for state management
- Observer Pattern: Real-time notifications for calculations
- Auto-save: Automatic history persistence to CSV files
- Comprehensive Logging: Structured logging with configurable levels
- Configuration Management: Environment-based configuration system
- Design Patterns: Observer, Memento, Factory, Singleton patterns
- CI/CD Pipeline: GitHub Actions for automated testing

### 🛠️ Installation Instructions
- Prerequisites
    - Python 3.8 or higher
    - pip (Python package manager)

# Environment
- Directory Configuration
    - CALCULATOR_LOG_DIR=logs
    - CALCULATOR_HISTORY_DIR=history
    - CALCULATOR_MAX_HISTORY_SIZE=100
    - CALCULATOR_AUTO_SAVE=true
    - CALCULATOR_PRECISION=10
    - CALCULATOR_MAX_INPUT_VALUE=10000000000.0
    - CALCULATOR_DEFAULT_ENCODING=utf-8

# Configuration Options Explained
CALCULATOR_LOG_DIR: Directory for log files (default: logs)

CALCULATOR_HISTORY_DIR: Directory for history CSV files (default: history)

CALCULATOR_MAX_HISTORY_SIZE: Maximum number of calculations to store (default: 100)

CALCULATOR_AUTO_SAVE: Automatically save history after each calculation (default: true)

CALCULATOR_PRECISION: Decimal precision for results (default: 10)

CALCULATOR_MAX_INPUT_VALUE: Maximum allowed input value (default: 10,000,000,000)

CALCULATOR_DEFAULT_ENCODING: File encoding for logs and history (default: utf-8)

# Logging Configuration
The application automatically configures logging with:

File Handler: Writes to logs/calculator.log

Console Handler: Outputs warnings and errors to console

Structured Format: Timestamp, logger name, level, and message

Rotation: Log files are automatically created and managed

# Usage Guide
Command-Line Interface
The calculator supports interactive command-line usage with the following commands:

Addition (add 5 3)

Output: 8.0

Subtraction (subtract 10 4)

Output: 6.0

Multiplication (multiply 7 6)

Output: 42.0

Division (divide 15 3)

Output: 5.0

Power calculation (power 2 8)

Output: 256.0

Root calculation (nth root) root 16 2

Output: 4.0 (square root)

or root 27 3  

Output: 3.0 (cube root)

Modulus operation (modulus 10 3)

Output: 1.0

Integer division (int_divide 10 3)

Output: 3.0

Percentage calculation (percent 25 100)

Output: 25.0

Absolute difference (abs_diff 10 3)

Output: 7.0

# History Management Commands

view calculation history = history

clear history = clear

Get recent calculations (last 5) = recent 5

Undo last calculation = undo

Redo undone calculation = redo

### File Operations

Save history to specific file = save /path/to/history.csv

Load history from file = load /path/to/history.csv

Export history = export

Import calculations = import

Display help = help

Exit application = exit

# Example Session
python -m app.calculator

Calculator Started. Type 'help' for commands.

> add 10 5
15.0

> multiply 3 7
21.0

> power 2 10
1024.0

> history
1: 10.0 + 5.0 = 15.0
2: 3.0 * 7.0 = 21.0  
3: 2.0 ^ 10.0 = 1024.0

> undo
Undo performed

> history
1: 10.0 + 5.0 = 15.0
2: 3.0 * 7.0 = 21.0

> exit
Goodbye!

# CI/CD Information

GitHub Actions Workflow
The project includes automated CI/CD pipelines in .github/workflows/:

python-tests.yml
Trigger: On push to main branch and pull requests

## Workflow Features
Automated Testing: Runs complete test suite on every commit

Multi-version Support: Ensures compatibility across Python versions

Coverage Reporting: Tracks test coverage trends

Quality Gates: Prevents merging of failing code

Artifact Uploads: Stores test results and coverage reports


# Design Patterns Implemented

Observer Pattern
Purpose: Decouple calculation execution from side effects

Implementation: CalculatorObserver with LoggingObserver and AutoSaveObserver

Benefits: Easy extension with new observers without modifying core logic

Memento Pattern
Purpose: Enable undo/redo functionality

Implementation: CalculatorMemento and MementoCaretaker

Benefits: Clean state management and history tracking

Factory Pattern
Purpose: Dynamic operation creation

Implementation: OperationFactory class

Benefits: Easy addition of new operations without modifying existing code

Singleton Pattern
Purpose: Single configuration and logging instances

Implementation: Logger class with __new__ method

Benefits: Consistent configuration across the application

# Advanced Python Calculator

A sophisticated, feature-rich calculator application built with Python that demonstrates modern software engineering practices including design patterns, comprehensive testing, and CI/CD integration.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Testing](#testing)
- [Design Patterns](#design-patterns)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)


## Features

### Basic Operations
- Addition
- Subtraction
- Multiplication
- Division

### Advanced Operations
- Power calculations (x^y)
- Root calculations (nth root)
- Modulus operations
- Integer division
- Percentage calculations
- Absolute difference

### Advanced Features
- **Calculation History**: Persistent storage with configurable size limits
- **Undo/Redo**: Full state management using Memento pattern
- **Observer Pattern**: Real-time notifications for calculations
- **Auto-save**: Automatic history persistence to CSV files
- **Comprehensive Logging**: Structured logging with configurable levels
- **Configuration Management**: Environment-based configuration system
- **Design Patterns**: Observer, Memento, Factory, and Singleton patterns
- **CI/CD Pipeline**: Automated testing with GitHub Actions
- **90% Test Coverage**: Comprehensive unit and integration tests

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/calculator-app.git
cd calculator-app
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -m pytest tests/ -v
```

If all tests pass, the installation is successful!

## Configuration

### Environment Variables Setup

Create a `.env` file in the project root directory:

```bash
touch .env  # On macOS/Linux
type nul > .env  # On Windows
```

### Configuration Options

Add the following environment variables to your `.env` file:

```env
# Directory Configuration
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history

# History Settings
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true

# Calculation Settings
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=10000000000.0
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Configuration Details

| Variable | Description | Default | Valid Values |
|----------|-------------|---------|--------------|
| `CALCULATOR_LOG_DIR` | Directory for log files | `logs` | Any valid path |
| `CALCULATOR_HISTORY_DIR` | Directory for history CSV files | `history` | Any valid path |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum calculations to store | `100` | Positive integer |
| `CALCULATOR_AUTO_SAVE` | Auto-save after each calculation | `true` | `true` or `false` |
| `CALCULATOR_PRECISION` | Decimal places for results | `10` | Non-negative integer |
| `CALCULATOR_MAX_INPUT_VALUE` | Maximum allowed input value | `1e10` | Positive number |
| `CALCULATOR_DEFAULT_ENCODING` | File encoding for logs/history | `utf-8` | Valid encoding name |

### Logging Configuration

The application automatically configures logging with:

- **File Handler**: Writes to `logs/calculator.log`
- **Console Handler**: Outputs warnings and errors to console
- **Structured Format**: `timestamp - name - level - message`
- **Log Rotation**: Automatically managed by Python logging

## Usage Guide

### Starting the Calculator

Run the calculator in interactive mode:

```bash
python main.py
```

Or using the module:

```bash
python -m app.calculator
```

### Command-Line Interface

The calculator supports interactive command-line usage with the following commands:

#### Arithmetic Operations

```bash
# Addition
> add 5 3
Result: 8.0

# Subtraction
> subtract 10 4
Result: 6.0

# Multiplication
> multiply 7 6
Result: 42.0

# Division
> divide 15 3
Result: 5.0

# Power (x^y)
> power 2 8
Result: 256.0

# Root (nth root of x)
> root 16 2
Result: 4.0  # Square root

> root 27 3
Result: 3.0  # Cube root

# Modulus
> modulus 10 3
Result: 1.0

# Integer Division
> int_divide 10 3
Result: 3.0

# Percentage (a as percentage of b)
> percent 25 100
Result: 25.0

# Absolute Difference
> abs_diff 10 3
Result: 7.0
```

#### History Management

```bash
# View calculation history
> history
==============================================================
CALCULATION HISTORY
==============================================================
1. 5.0 + 3.0 = 8.0 (add)
2. 10.0 - 4.0 = 6.0 (subtract)
3. 7.0 * 6.0 = 42.0 (multiply)
==============================================================

# Clear history
> clear
History cleared successfully.

# Undo last calculation
> undo
Undid last calculation.

# Redo undone calculation
> redo
Redid last calculation.
```

#### File Operations

```bash
# Save history to default location (history/history.csv)
> save
History saved to history/history.csv

# Save to custom location
> save /path/to/my_history.csv
History saved to /path/to/my_history.csv

# Load history from default location
> load
History loaded from history/history.csv

# Load from custom location
> load /path/to/my_history.csv
History loaded from /path/to/my_history.csv
```

#### Other Commands

```bash
# Display help
> help

# Exit application
> exit
Thank you for using the Advanced Calculator. Goodbye!
```

### Example Session

```bash
$ python main.py

Welcome to Chinedu's Brand New Advanced Calculator!
Type 'help' for available commands or 'exit' to quit.

> add 10 5
Result: 15.0

> multiply 3 7
Result: 21.0

> power 2 10
Result: 1024.0

> history
==============================================================
CALCULATION HISTORY
==============================================================
1. 10.0 + 5.0 = 15.0 (add)
2. 3.0 * 7.0 = 21.0 (multiply)
3. 2.0 ^ 10.0 = 1024.0 (power)
==============================================================

> undo
Undid last calculation.

> history
==============================================================
CALCULATION HISTORY
==============================================================
1. 10.0 + 5.0 = 15.0 (add)
2. 3.0 * 7.0 = 21.0 (multiply)
==============================================================

> save
History saved to history/history.csv

> exit
Thank you for using the Advanced Calculator. Goodbye!
```

## Testing

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/test_calculator.py -v
```

**Run tests with coverage report:**
```bash
pytest tests/ --cov=app --cov-report=html
```

**View coverage report:**
```bash
# On macOS/Linux
open htmlcov/index.html

# On Windows
start htmlcov/index.html
```

### Test Structure

```
tests/
├── conftest.py                    # Shared fixtures
├── test_calculation.py            # Calculation class tests
├── test_calculator.py             # Calculator class tests (90% coverage)
├── test_calculator_momento.py     # Memento pattern tests
├── test_config.py                 # Configuration tests
├── test_edge_cases.py             # Edge cases and boundary tests
├── test_exceptions.py             # Custom exception tests
├── test_fixed_edge_case.py        # Additional edge case tests
├── test_history.py                # History management tests (90% coverage)
├── test_logger.py                 # Logger tests
├── test_operation.py              # Operation classes tests
└── test_validators.py             # Input validation tests
```

### Test Coverage

The project maintains **90% test coverage** across all modules:

- Calculation class
- Calculator class with Observer pattern
- History management
- Memento pattern (Undo/Redo)
- Operations and Factory pattern
- Configuration management
- Input validation
- Custom exceptions
- Logger singleton
- Edge cases and boundary conditions

### Running Specific Test Categories

```bash
# Run only unit tests
pytest tests/test_operations.py tests/test_calculation.py -v

# Run integration tests
pytest tests/test_calculator.py -v

# Run edge case tests
pytest tests/test_edge_cases.py -v

# Run with markers (if defined)
pytest -m "not slow" -v
```

## Design Patterns

### 1. Observer Pattern

**Purpose**: Decouple calculation execution from side effects

**Implementation**:
- `CalculatorObserver`: Abstract base class
- `LoggingObserver`: Logs calculations
- `AutoSaveObserver`: Auto-saves history

**Benefits**:
- Easy to add new observers without modifying calculator
- Loose coupling between components
- Single Responsibility Principle

**Example**:
```python
# Custom observer
class CustomObserver(CalculatorObserver):
    def update(self, calculation: Calculation):
        print(f"Calculation performed: {calculation}")

# Register observer
calculator.register_observer(CustomObserver())
```

### 2. Memento Pattern

**Purpose**: Enable undo/redo functionality

**Implementation**:
- `CalculatorMemento`: Stores calculator state
- `MementoCaretaker`: Manages memento history

**Benefits**:
- Clean state management
- Encapsulation of state details
- Time-travel debugging capability

**Example**:
```python
calculator.calculate("add", 5, 3)
calculator.undo()  # Reverts to previous state
calculator.redo()  # Restores undone state
```

### 3. Factory Pattern

**Purpose**: Dynamic operation creation

**Implementation**:
- `OperationFactory`: Creates operation instances
- Operation classes: `AddOperation`, `SubtractOperation`, etc.

**Benefits**:
- Easy addition of new operations
- Open/Closed Principle compliance
- Centralized operation management

**Example**:
```python
# Add new operation
class CustomOperation(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b + a / b
    
    def get_symbol(self) -> str:
        return "⊕"

# Register in factory
OperationFactory._operations['custom'] = CustomOperation
```

### 4. Singleton Pattern

**Purpose**: Single configuration and logging instances

**Implementation**:
- `Logger`: Single logger instance
- `CalculatorConfig`: Single configuration instance

**Benefits**:
- Consistent state across application
- Reduced memory footprint
- Global access point

**Example**:
```python
logger1 = Logger()
logger2 = Logger()
assert logger1 is logger2  # Same instance
```

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes automated CI/CD in `.github/workflows/python-tests.yml`

**Triggers**:
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

**Workflow Steps**:
1. Checkout code
2. Set up Python environment (3.8, 3.9, 3.10, 3.11, 3.12)
3. Install dependencies
4. Run linters (flake8, pylint)
5. Execute test suite
6. Generate coverage report
7. Upload artifacts

**Features**:
- Multi-version Python support
- Automated testing on every commit
- Coverage reporting
- Quality gates
- Artifact uploads (test results, coverage reports)

**Viewing Results**:
1. Navigate to repository on GitHub
2. Click "Actions" tab
3. Select workflow run
4. View logs and artifacts

### Local CI Simulation

Run the same checks locally:

```bash
# Linting
flake8 app tests --max-line-length=100

# Type checking (if mypy is installed)
mypy app

# Testing with coverage
pytest tests/ --cov=app --cov-report=term-missing
```

## Project Structure

```
calculator-app/
├── .github/
│   └── workflows/
│       └── python-tests.yml       # CI/CD pipeline
├── app/
│   ├── __init__.py
│   ├── calculation.py             # Calculation data class
│   ├── calculator.py              # Main calculator with Observer pattern
│   ├── calculator_config.py       # Configuration management
│   ├── calculator_momento.py      # Memento pattern implementation
│   ├── calculator_repl.py         # Command-line interface
│   ├── exceptions.py              # Custom exception classes
│   ├── history.py                 # History management
│   ├── input_validator.py         # Input validation
│   ├── logger.py                  # Logging singleton
│   └── operations.py              # Operation classes and factory
├── tests/
│   ├── conftest.py                # Pytest fixtures
│   ├── test_calculation.py
│   ├── test_calculator.py
│   ├── test_calculatormomento.py
│   ├── test_config.py
│   ├── test_edge_cases.py
│   ├── test_exceptions.py
│   ├── test_fixed_edge_case.py
│   ├── test_history.py
│   ├── test_logger.py
│   ├── test_operation.py
│   └── test_validators.py
├── logs/                          # Log files (created automatically)
├── history/                       # History CSV files (created automatically)
├── .env                           # Environment configuration
├── .gitignore                     # Git ignore rules
├── main.py                        # Application entry point
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

### Testing Requirements

- All new features must include tests
- Tests must pass before merging
- Coverage must remain at 90% minimum
- Edge cases should be tested


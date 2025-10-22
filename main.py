from app.calculator import Calculator
from app.calculator_repl import REPL


def main():  # pragma: no cover
    """Main entry point"""
    calculator = Calculator()
    repl = REPL(calculator)
    repl.start()


if __name__ == "__main__":  # pragma: no cover
    main()
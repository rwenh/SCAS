"""
demo.py — small end-to-end walkthrough of the CAS pipeline.

Not part of the test suite. Run manually once the modules are implemented:
    python -m examples.demo

This exists so you have one script that exercises parse -> simplify ->
differentiate -> print together, since the unit tests only exercise each
module in isolation.
"""

from src.parser import parse
from src.simplifier import simplify
from src.differentiator import differentiate
from src.printer import to_string


def run_demo(expression: str, var: str = 'x') -> None:
    """
    Pseudocode:
        print(f"Original:    {expression}")

        tree = parse(expression)
        print(f"Parsed:      {to_string(tree)}")

        simplified = simplify(tree)
        print(f"Simplified:  {to_string(simplified)}")

        derivative = differentiate(simplified, var)
        print(f"d/d{var}:       {to_string(derivative)}")

        derivative_simplified = simplify(derivative)
        print(f"Simplified:  {to_string(derivative_simplified)}")

        print()
    """
    raise NotImplementedError


if __name__ == '__main__':
    examples = [
        "x^2 + 2*x + 1",
        "sin(x) * cos(x)",
        "x^3 / x",
        "(x + 1) * (x - 1)",
    ]
    for expr in examples:
        run_demo(expr)

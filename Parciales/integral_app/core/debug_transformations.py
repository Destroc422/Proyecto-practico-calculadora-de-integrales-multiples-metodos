#!/usr/bin/env python3
"""
Debug the transformation process step by step
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def debug_transformations():
    """Debug the transformation process step by step"""
    engine = MicrosoftMathEngine()
    
    test_expr = "sin(x)"
    
    print(f"Original expression: {test_expr}")
    print()
    
    # Step by step transformations
    expr = test_expr
    print(f"Step 0 - Original: {expr}")
    
    # Clean expression
    cleaned = engine._clean_expression(expr)
    print(f"Step 1 - Cleaned: {cleaned}")
    
    # Transform integrals
    integrated = engine._transform_integrals(cleaned)
    print(f"Step 2 - Integrals: {integrated}")
    
    # Transform functions
    functions = engine._transform_functions(integrated)
    print(f"Step 3 - Functions: {functions}")
    
    # Transform powers
    powered = engine._transform_powers(functions)
    print(f"Step 4 - Powers: {powered}")
    
    # Transform fractions
    fractioned = engine._transform_fractions(powered)
    print(f"Step 5 - Fractions: {fractioned}")
    
    # Transform operators
    operators = engine._transform_operators(fractioned)
    print(f"Step 6 - Operators: {operators}")
    
    # Handle implicit multiplication
    multiplied = engine._handle_implicit_multiplication(operators)
    print(f"Step 7 - Implicit Multiplication: {multiplied}")
    
    print()
    print("=== Testing the full parse method ===")
    try:
        result = engine.parse_natural_math(test_expr)
        print(f"Full parse result: {result}")
    except Exception as e:
        print(f"Full parse error: {e}")

if __name__ == "__main__":
    debug_transformations()

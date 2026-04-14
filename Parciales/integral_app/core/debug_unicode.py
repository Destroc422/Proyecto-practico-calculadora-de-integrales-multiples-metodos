#!/usr/bin/env python3
"""
Debug Unicode character handling
"""
import sys
import os
import unicodedata

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def debug_unicode():
    """Debug Unicode character handling"""
    engine = MicrosoftMathEngine()
    
    test_expr = "int (x² + 1)/(x) dx"
    
    print(f"Original expression: {test_expr}")
    print(f"Length: {len(test_expr)}")
    
    # Print each character with its Unicode info
    for i, char in enumerate(test_expr):
        print(f"{i}: '{char}' - {unicodedata.name(char, 'UNKNOWN')} - U+{ord(char):04X}")
    
    print("\n" + "=" * 60)
    
    # Test step by step transformations
    expr = test_expr
    print(f"Step 0 - Original: {expr}")
    
    # Clean expression
    cleaned = engine._clean_expression(expr)
    print(f"Step 1 - Cleaned: {cleaned}")
    
    # Transform powers
    powered = engine._transform_powers(cleaned)
    print(f"Step 2 - Powers: {powered}")
    
    # Transform integrals
    integrated = engine._transform_integrals(powered)
    print(f"Step 3 - Integrals: {integrated}")
    
    # Transform fractions
    fractioned = engine._transform_fractions(integrated)
    print(f"Step 4 - Fractions: {fractioned}")

if __name__ == "__main__":
    debug_unicode()

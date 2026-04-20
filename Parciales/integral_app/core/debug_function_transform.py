#!/usr/bin/env python3
"""
Debug the function transformation specifically
"""
import sys
import os
import re

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def debug_function_transform():
    """Debug the function transformation specifically"""
    engine = MicrosoftMathEngine()
    
    test_expr = "sin(x)"
    
    print(f"Testing function transformation for: {test_expr}")
    print()
    
    # Check function mappings
    print("Function mappings keys:")
    for key in engine.function_mappings.keys():
        print(f"  {key}")
    print()
    
    # Test function patterns
    print("Function patterns:")
    for pattern in engine.function_patterns:
        print(f"  {pattern}")
        match = re.search(pattern, test_expr)
        if match:
            print(f"    MATCHED! Groups: {match.groups()}")
        else:
            print(f"    No match")
    print()
    
    # Test the function transformation method directly
    result = engine._transform_functions(test_expr)
    print(f"Function transformation result: {result}")
    
    # Test if the function name is recognized
    pattern = r'([a-zA-Z]+)\(([^)]+)\)'
    match = re.search(pattern, test_expr)
    if match:
        func_name = match.group(1)
        print(f"Function name extracted: {func_name}")
        print(f"Is in mappings: {func_name.lower() in [f.lower() for f in engine.function_mappings.keys()]}")

if __name__ == "__main__":
    debug_function_transform()

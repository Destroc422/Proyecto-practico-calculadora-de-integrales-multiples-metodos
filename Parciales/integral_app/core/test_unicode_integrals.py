#!/usr/bin/env python3
"""
Test script for Unicode integral patterns
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def test_unicode_integrals():
    """Test the Unicode integral patterns"""
    engine = MicrosoftMathEngine()
    
    # Test cases for Unicode integrals
    test_cases = [
        # Unicode indefinite integrals
        "int (x² + 1)/(x) dx",
        "integral (x² + 1)/(x) dx",
        "int (x²)/(x) dx",
        "integral (x²)/(x) dx",
        
        # Unicode integral symbol
        "int (x² + 1)/(x) dx",
        "integral (x² + 1)/(x) dx",
        "int (x²)/(x) dx",
        "integral (x²)/(x) dx",
    ]
    
    print("Testing Unicode integral patterns...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\nTest {i}: {test_case}")
            result = engine.parse_natural_math(test_case)
            print(f"  Parsed successfully: {result}")
            
            # Try to solve the integral
            if "integrate" in str(result):
                try:
                    solved = sp.integrate(result)
                    print(f"  Solved: {solved}")
                except Exception as e:
                    print(f"  Solve error: {e}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    import sympy as sp
    test_unicode_integrals()

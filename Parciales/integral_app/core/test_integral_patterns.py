#!/usr/bin/env python3
"""
Test script for new integral patterns with fractions
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def test_integral_patterns():
    """Test the new integral patterns with fractions"""
    engine = MicrosoftMathEngine()
    
    # Test cases for integrals with fractions
    test_cases = [
        # Basic fraction integrals
        "int (x^2+1)/(x+1) dx",
        "integral (x^2+1)/(x+1) dx",
        "int x^2/x dx",
        "integral x^2/x dx",
        
        # Definite integrals with fractions
        "0 to 1 int (x^2+1)/(x+1) dx",
        "0 to 1 integral (x^2+1)/(x+1) dx",
        "0 to 1 int x^2/x dx",
        "0 to 1 integral x^2/x dx",
        
        # Unicode integrals with fractions
        "int (x^2+1)/(x+1) dx",
        "int x^2/x dx",
        
        # Complex nested fractions
        "int ((x^2+1)/(x+1)) dx",
        "integral ((x^2+1)/(x+1)) dx",
    ]
    
    print("Testing new integral patterns with fractions...")
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
    test_integral_patterns()

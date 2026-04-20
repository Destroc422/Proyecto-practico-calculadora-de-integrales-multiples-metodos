#!/usr/bin/env python3
"""
Debug integral parsing step by step
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine

def debug_integral_parsing():
    """Debug integral parsing step by step"""
    engine = MicrosoftMathEngine()
    
    test_expr = "int (3x + 5) dx"
    
    print(f"Debugging: {test_expr}")
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
    
    # Test what happens if we apply implicit multiplication to the integrand
    print(f"Step 3 - Testing implicit multiplication on integrand...")
    
    # Extract integrand from the integrate expression
    import re
    match = re.search(r'integrate\(([^,]+),', integrated)
    if match:
        integrand = match.group(1)
        print(f"  Extracted integrand: {integrand}")
        
        # Apply implicit multiplication to integrand
        multiplied = engine._handle_implicit_multiplication(integrand)
        print(f"  After implicit multiplication: {multiplied}")
        
        # Reconstruct the integrate expression
        final_expr = integrated.replace(integrand, multiplied)
        print(f"  Final expression: {final_expr}")
        
        # Try to parse it
        try:
            import sympy as sp
            x = sp.symbols('x')
            result = sp.sympify(final_expr)
            print(f"  SymPy parsing: SUCCESS -> {result}")
            
            # Try to integrate
            integrated_result = sp.integrate(result, x)
            print(f"  Integration result: {integrated_result}")
        except Exception as e:
            print(f"  SymPy parsing: ERROR -> {e}")

if __name__ == "__main__":
    debug_integral_parsing()

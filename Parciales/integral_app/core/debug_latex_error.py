#!/usr/bin/env python3
"""
Debug script to identify the LaTeX parsing error
"""
import sys
import os
import re

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.latex_renderer_fixed import ProfessionalLaTeXRenderer
    import sympy as sp
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def debug_latex_parsing():
    """Debug the LaTeX parsing error"""
    
    renderer = ProfessionalLaTeXRenderer()
    
    print("=== Debug de LaTeX Parsing Error ===")
    print()
    
    # Test expressions that might cause the error
    test_expressions = [
        "3*x**2/2 + 5*x",
        "x**3/2 + 5*x**2/2",
        "x**2 + 2*x + 1",
        "sin(x) + cos(x)",
        "int (3x + 5) dx"
    ]
    
    for i, expr in enumerate(test_expressions, 1):
        print(f"Test {i}: {expr}")
        
        try:
            # Convert to SymPy expression
            if isinstance(expr, str):
                sympy_expr = sp.sympify(expr)
            else:
                sympy_expr = expr
            
            print(f"  SymPy: {sympy_expr}")
            
            # Get LaTeX
            latex_expr = sp.latex(sympy_expr)
            print(f"  LaTeX: {latex_expr}")
            
            # Test convert_to_text_format
            try:
                text_format = renderer.convert_to_text_format(sympy_expr)
                print(f"  Text format: {text_format}")
            except Exception as e:
                print(f"  Text format ERROR: {e}")
                # Try to identify the problematic part
                print(f"  Problematic LaTeX: {latex_expr}")
                
                # Test individual LaTeX cleaning
                try:
                    cleaned = renderer._clean_latex_for_text_display(latex_expr)
                    print(f"  Cleaned LaTeX: {cleaned}")
                except Exception as e2:
                    print(f"  LaTeX cleaning ERROR: {e2}")
            
            print()
            
        except Exception as e:
            print(f"  ERROR: {e}")
            print()
    
    # Test the specific error case from logs
    print("=== Test del Error Específico ===")
    print()
    
    # The error seems to be related to: \int \frac{3 x^{2}}{2} dx + \int 5 x dx
    problematic_latex = r"\int \frac{3 x^{2}}{2} dx + \int 5 x dx"
    print(f"LaTeX problemático: {problematic_latex}")
    
    try:
        cleaned = renderer._clean_latex_for_text_display(problematic_latex)
        print(f"Cleaned: {cleaned}")
    except Exception as e:
        print(f"ERROR: {e}")
        
        # Try to identify the problematic pattern
        print("Análisis del patrón problemático:")
        patterns = [
            r'\int \frac{([^}]+)}{([^}]+)} dx',
            r'\int ([^ ]+) dx',
            r'\+',
            r'\$'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, problematic_latex)
            if matches:
                print(f"  Patrón '{pattern}' -> {matches}")

if __name__ == "__main__":
    debug_latex_parsing()

#!/usr/bin/env python3
"""
Simple debug script for LaTeX parsing error
"""
import re
import sympy as sp

def test_latex_patterns():
    """Test LaTeX patterns that might cause parsing errors"""
    
    print("=== Debug de LaTeX Parsing Error ===")
    print()
    
    # Test the specific problematic pattern from logs
    problematic_latex = r"\int \frac{3 x^{2}}{2} dx + \int 5 x dx"
    print(f"LaTeX problemático: {problematic_latex}")
    
    # Test regex patterns that might be causing issues
    patterns = [
        (r'\int \frac{([^}]+)}{([^}]+)} dx', 'Integral con fracción'),
        (r'\int ([^ ]+) dx', 'Integral simple'),
        (r'\+', 'Operador suma'),
        (r'\$', 'Dólar'),
        (r'\\frac{([^}]+)}{([^}]+)}', 'Fracción'),
        (r'\\int', 'Integral'),
    ]
    
    print("\nAnálisis de patrones:")
    for pattern, description in patterns:
        try:
            matches = re.findall(pattern, problematic_latex)
            if matches:
                print(f"  '{pattern}' ({description}): {matches}")
            else:
                print(f"  '{pattern}' ({description}): No matches")
        except Exception as e:
            print(f"  '{pattern}' ({description}): ERROR - {e}")
    
    # Test LaTeX cleaning function similar to the renderer
    def clean_latex_for_text(latex_str):
        """Clean LaTeX string for text display"""
        try:
            conversions = {
                # Powers
                r'\*\*': '^',
                
                # Fractions
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\\dfrac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                
                # Integrals
                r'\\int': 'integral',
                r'\\int_': 'integral_',
                r'\\int\^': 'integral^',
                
                # Constants
                r'\\pi': 'pi',
                r'\\e': 'e',
                
                # Functions
                r'\\sin': 'sin',
                r'\\cos': 'cos',
                r'\\tan': 'tan',
                r'\\log': 'log',
                r'\\ln': 'ln',
                
                # Parentheses
                r'\\left\(': '(',
                r'\\right\)': ')',
                
                # Spaces
                r'\\,': ' ',
                r'\\;': '  ',
                
                # Clean up remaining backslashes
                r'\\': '',
            }
            
            result = latex_str
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            return result
            
        except Exception as e:
            print(f"Error in LaTeX cleaning: {e}")
            return latex_str
    
    print(f"\nLaTeX original: {problematic_latex}")
    try:
        cleaned = clean_latex_for_text(problematic_latex)
        print(f"LaTeX limpio: {cleaned}")
    except Exception as e:
        print(f"ERROR en limpieza: {e}")
    
    # Test specific problematic parts
    print("\nTest de partes problemáticas:")
    parts = [
        r"\int \frac{3 x^{2}}{2} dx",
        r"\int 5 x dx",
        r"\frac{3 x^{2}}{2}",
        r"3 x^{2}",
        r"5 x"
    ]
    
    for part in parts:
        try:
            cleaned_part = clean_latex_for_text(part)
            print(f"  '{part}' -> '{cleaned_part}'")
        except Exception as e:
            print(f"  '{part}' -> ERROR: {e}")

def test_sympy_latex():
    """Test SymPy LaTeX generation"""
    
    print("\n=== Test SymPy LaTeX Generation ===")
    
    # Test expressions
    expressions = [
        "3*x**2/2 + 5*x",
        "x**3/2 + 5*x**2/2",
        "sp.integrate(3*x**2/2 + 5*x, sp.Symbol('x'))"
    ]
    
    for expr_str in expressions:
        try:
            if expr_str.startswith("sp."):
                # Evaluate the expression
                expr = eval(expr_str)
            else:
                expr = sp.sympify(expr_str)
            
            latex = sp.latex(expr)
            print(f"Expression: {expr}")
            print(f"LaTeX: {latex}")
            print()
            
        except Exception as e:
            print(f"ERROR con '{expr_str}': {e}")
            print()

if __name__ == "__main__":
    test_latex_patterns()
    test_sympy_latex()

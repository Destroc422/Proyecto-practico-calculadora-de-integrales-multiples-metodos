#!/usr/bin/env python3
"""
Test the LaTeX renderer fix
"""
import re
import sympy as sp

def test_latex_renderer_fix():
    """Test the fixed LaTeX renderer patterns"""
    
    print("=== Test LaTeX Renderer Fix ===")
    print()
    
    # Simulate the fixed _clean_latex_for_text_display method
    def clean_latex_for_text_display(latex_str):
        """Clean LaTeX string for text-based mathematical display"""
        try:
            # Text-based mathematical conversions
            conversions = {
                # Powers (Keep ** for text clarity)
                r'\*\*': '^',
                
                # Fractions (text format)
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\\dfrac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                
                # Roots (text format)
                r'\\sqrt{([^}]+)}': r'sqrt(\1)',
                r'\\sqrt\[3\]{([^}]+)}': r'cbrt(\1)',
                r'\\sqrt\[n\]{([^}]+)}': r'nroot(\1)',
                
                # Integrals (text format) - FIXED PATTERNS
                r'\\int': 'integral',
                r'\\int_': 'integral_',
                r'\\int\\^': 'integral^',
                r'\\int_{([^}]+)}\\^{([^}]+)}': r'integral_{\1}^{\2}',
                r'\\int_{([^}]+)}': r'integral_{\1}',
                r'\\int\\^{([^}]+)}': r'integral^{\1}',
                
                # Summation and products (text format) - FIXED PATTERNS
                r'\\sum': 'sum',
                r'\\sum_': 'sum_',
                r'\\sum\\^': 'sum^',
                r'\\prod': 'product',
                r'\\prod_': 'product_',
                r'\\prod\\^': 'product^',
                
                # Constants (text format)
                r'\\pi': 'pi',
                r'\\e': 'e',
                r'\\infty': 'infinity',
                r'\\mathrm{e}': 'e',
                
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
    
    # Test the problematic LaTeX from logs
    test_cases = [
        r"\frac{3 x^{2}}{2} + 5 x",
        r"\int \frac{3 x^{2}}{2} dx + \int 5 x dx",
        r"\frac{x^{3}}{2} + \frac{5 x^{2}}{2}",
        r"\sin(x) + \cos(x)",
        r"\int \sin(x) dx"
    ]
    
    for i, latex_str in enumerate(test_cases, 1):
        print(f"Test {i}: {latex_str}")
        try:
            cleaned = clean_latex_for_text_display(latex_str)
            print(f"  Result: {cleaned}")
            print("  Status: SUCCESS")
        except Exception as e:
            print(f"  ERROR: {e}")
            print("  Status: FAILED")
        print()
    
    # Test individual patterns to identify the exact problem
    print("=== Test Individual Patterns ===")
    
    patterns_to_test = [
        (r'\\frac{([^}]+)}{([^}]+)}', r'\frac{3 x^{2}}{2}'),
        (r'\\int', r'\int'),
        (r'\\int', r'\int \frac{3 x^{2}}{2} dx'),
        (r'\\int\\^', r'\int^'),
        (r'\\sum', r'\sum'),
        (r'\\sum\\^', r'\sum^'),
    ]
    
    for pattern, test_str in patterns_to_test:
        try:
            result = re.sub(pattern, 'REPLACED', test_str)
            print(f"Pattern '{pattern}' on '{test_str}' -> '{result}'")
        except Exception as e:
            print(f"ERROR with pattern '{pattern}': {e}")
    
    print()
    print("=== Test Complete ===")

if __name__ == "__main__":
    test_latex_renderer_fix()

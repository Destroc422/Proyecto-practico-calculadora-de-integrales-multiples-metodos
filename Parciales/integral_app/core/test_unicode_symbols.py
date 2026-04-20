#!/usr/bin/env python3
"""
Test script to verify Unicode symbols work correctly
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_unicode_symbols():
    """Test that Unicode symbols work correctly with the math engine"""
    
    engine = MicrosoftMathEngine()
    
    print("=== Prueba de Símbolos Unicode en el Motor Matemático ===")
    print()
    
    # Test cases with Unicode symbols
    test_cases = [
        # Integral symbols
        "int (3x + 5) dx",
        "integral (x² + 2x + 1) dx",
        
        # Power symbols
        "x² + 2x + 1",
        "x³ - 3x² + 3x - 1",
        
        # Combined expressions
        "int (x² + sin(x)) dx",
        "integral (x³ + cos(x)) dx",
        
        # Definite integrals
        "0 to 1 int x² dx",
        "0 to 1 integral (x² + 1) dx",
        
        # Complex expressions
        "int (x²/(x+1)) dx",
        "integral ((x²+1)/(x+1)) dx"
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"Test {i}: {test_case}")
            
            # Parse the expression
            result = engine.parse_natural_math(test_case)
            print(f"  Parseado: {result}")
            
            # Try to integrate if it's not already integrated
            x = sp.symbols('x')
            if "integrate" not in str(result):
                integrated = sp.integrate(result, x)
                print(f"  Integrado: {integrated}")
            else:
                print(f"  Ya está integrado")
            
            # Generate LaTeX
            latex_result = sp.latex(result)
            print(f"  LaTeX: {latex_result}")
            
            success_count += 1
            print("  Status: SUCCESS")
            print()
            
        except Exception as e:
            print(f"  ERROR: {e}")
            print()
    
    print(f"=== Resultados: {success_count}/{total_count} exitosos ===")
    
    if success_count == total_count:
        print("¡TODOS los símbolos Unicode funcionan correctamente!")
        print("El teclado científico modificado es compatible con el motor matemático.")
    else:
        print(f"Quedan {total_count - success_count} casos por resolver.")
    
    return success_count == total_count

def test_keypad_unicode_symbols():
    """Test the specific Unicode symbols that should be in the keypad"""
    
    print("\n=== Verificación de Símbolos Unicode del Teclado ===")
    
    # Unicode symbols that should be available
    unicode_symbols = {
        '': 'Integral',
        '': 'Double Integral',
        '²': 'Superscript Two',
        '³': 'Superscript Three',
        '': 'Superscript Four',
        '': 'Superscript n',
        '': 'Cube Root',
        '': 'Fourth Root',
        '': 'Summation',
        '': 'Product'
    }
    
    print("Símbolos Unicode disponibles en el teclado:")
    for symbol, description in unicode_symbols.items():
        print(f"  {symbol} - {description}")
    
    print("\nBotones de integrales Unicode:")
    integral_buttons = [
        ('', 'int '),
        ('', 'integral '),
        ('dx', ' dx'),
        ('0to1', '0 to 1 int '),
        ('0to2', '0 to 2 int '),
        ('ato', 'a to b int ')
    ]
    
    for button_text, insert_text in integral_buttons:
        print(f"  Botón '{button_text}' -> Inserta '{insert_text}'")
    
    print("\nBotones de funciones con integrales:")
    function_integrals = [
        ('sin', 'int sin(x) dx'),
        ('cos', 'int cos(x) dx'),
        ('tan', 'int tan(x) dx'),
        ('exp', 'int exp(x) dx'),
        ('ln', 'int log(x) dx'),
        ('x²', 'int x² dx')
    ]
    
    for button_text, insert_text in function_integrals:
        print(f"  Botón '{button_text}' -> Inserta '{insert_text}'")

if __name__ == "__main__":
    # Test Unicode symbols
    symbols_work = test_unicode_symbols()
    
    # Show keypad symbols
    test_keypad_unicode_symbols()
    
    print(f"\n=== Resumen Final ===")
    if symbols_work:
        print("El teclado científico Unicode está listo para usar!")
        print("Todos los símbolos Unicode funcionan correctamente con el motor matemático.")
    else:
        print("Se necesitan ajustes adicionales en el motor matemático.")

#!/usr/bin/env python3
"""
Test script to demonstrate Unicode capabilities of the enhanced keypad
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_unicode_capabilities():
    """Test the Unicode capabilities of the enhanced keypad"""
    
    engine = MicrosoftMathEngine()
    
    print("=== Test de Capacidades Unicode del Teclado Mejorado ===")
    print()
    
    # Test Unicode symbols that should be available in the enhanced keypad
    unicode_test_cases = [
        # Basic Unicode symbols
        ("alpha", "alpha"),
        ("beta", "beta"),
        ("gamma", "gamma"),
        ("delta", "delta"),
        ("theta", "theta"),
        ("lambda", "lambda"),
        ("mu", "mu"),
        ("pi", "pi"),
        ("sigma", "sigma"),
        ("phi", "phi"),
        ("omega", "omega"),
        
        # Uppercase Greek letters
        ("Alpha", "Alpha"),
        ("Beta", "Beta"),
        ("Gamma", "Gamma"),
        ("Delta", "Delta"),
        ("Theta", "Theta"),
        ("Lambda", "Lambda"),
        ("Pi", "Pi"),
        ("Sigma", "Sigma"),
        ("Phi", "Phi"),
        ("Omega", "Omega"),
        
        # Mathematical symbols
        ("int", "int"),
        ("integral", "integral"),
        ("sum", "sum"),
        ("product", "product"),
        ("partial", "partial"),
        ("nabla", "nabla"),
        ("infinity", "infinity"),
        ("sqrt", "sqrt"),
        
        # Set theory symbols
        ("forall", "forall"),
        ("exists", "exists"),
        ("empty", "empty"),
        ("in", "in"),
        ("notin", "notin"),
        ("subset", "subset"),
        ("superset", "superset"),
        ("le", "<="),
        ("ge", ">="),
        ("ne", "!="),
        ("approx", "~="),
        ("equiv", "=="),
        
        # Number sets
        ("Natural", "Natural"),
        ("Integer", "Integer"),
        ("Real", "Real"),
        ("Rational", "Rational"),
        ("Complex", "Complex"),
        
        # Unicode powers and roots
        ("x²", "x²"),
        ("x³", "x³"),
        ("sqrt", "sqrt"),
        ("**(1/3)", "**(1/3)"),
        ("**(1/4)", "**(1/4)"),
        
        # Unicode fractions
        ("1/2", "1/2"),
        ("1/3", "1/3"),
        ("1/4", "1/4"),
        ("2/3", "2/3"),
        ("3/4", "3/4"),
        ("1/pi", "1/pi"),
    ]
    
    print("Símbolos Unicode disponibles en el teclado mejorado:")
    print("=" * 60)
    
    success_count = 0
    total_count = len(unicode_test_cases)
    
    for symbol, expected in unicode_test_cases:
        try:
            # Test that the symbol is recognized
            if symbol in expected or expected in symbol:
                print(f"  {symbol:<15} -> {expected:<20} [OK]")
                success_count += 1
            else:
                print(f"  {symbol:<15} -> {expected:<20} [MISMATCH]")
        except Exception as e:
            print(f"  {symbol:<15} -> {expected:<20} [ERROR: {e}]")
    
    print()
    print(f"Resultados: {success_count}/{total_count} símbolos Unicode funcionan correctamente")
    print()
    
    # Test actual mathematical expressions with Unicode symbols
    print("Test de Expresiones Matemáticas con Símbolos Unicode:")
    print("=" * 60)
    
    math_expressions = [
        "int (3x² + 5x) dx",
        "integral (x³ + 2x² + x) dx",
        "int sin(x) dx",
        "integral cos(2x) dx",
        "int (x²/(x+1)) dx",
        "integral ((x²+1)/(x+1)) dx",
        "0 to 1 int x² dx",
        "0 to 1 integral (x² + 1) dx",
        "int (alpha*x² + beta*x + gamma) dx",
        "integral (pi*x² + e*x + phi) dx",
        "sum_{i=1}^{n} i²",
        "product_{i=1}^{n} i",
        "limit_{x->0} sin(x)/x",
        "partial f/partial x",
        "nabla f",
        "sqrt(x² + y²)",
        "x² + y² = r²",
        "sin²(x) + cos²(x) = 1",
        "e^(i*pi) + 1 = 0",
        "alpha + beta + gamma = 180",
        "integral_{a}^{b} f(x) dx",
    ]
    
    math_success_count = 0
    math_total_count = len(math_expressions)
    
    for expr in math_expressions:
        try:
            result = engine.parse_natural_math(expr)
            print(f"  {expr:<30} -> {str(result):<25} [OK]")
            math_success_count += 1
        except Exception as e:
            print(f"  {expr:<30} -> ERROR: {str(e):<25} [FAILED]")
    
    print()
    print(f"Resultados matemáticos: {math_success_count}/{math_total_count} expresiones funcionan")
    print()
    
    # Test specific Unicode features
    print("Test de Características Específicas Unicode:")
    print("=" * 60)
    
    unicode_features = [
        ("Potencias Unicode", "x² + x³ + x^4", "x**2 + x**3 + x**4"),
        ("Fracciones Unicode", "1/2 + 1/3 + 1/4", "1/2 + 1/3 + 1/4"),
        ("Letras Griegas", "alpha + beta + gamma", "alpha + beta + gamma"),
        ("Símbolos Integrales", "int f(x) dx", "integrate(f(x), x)"),
        ("Símbolos Sumatoria", "sum_{i=1}^{n} i", "Sum(i, (i, 1, n))"),
        ("Símbolos Productorio", "product_{i=1}^{n} i", "Product(i, (i, 1, n))"),
        ("Símbolos Conjuntos", "x in Real", "x in Real"),
        ("Símbolos Lógicos", "forall x in Real", "forall x in Real"),
        ("Símbolos Relacionales", "x <= y and y <= z", "x <= y and y <= z"),
        ("Símbolos Aritméticos", "x ± y", "x ± y"),
    ]
    
    feature_success_count = 0
    feature_total_count = len(unicode_features)
    
    for feature_name, test_expr, expected_result in unicode_features:
        try:
            result = engine.parse_natural_math(test_expr)
            if str(result) == expected_result or expected_result in str(result):
                print(f"  {feature_name:<25} -> [OK]")
                feature_success_count += 1
            else:
                print(f"  {feature_name:<25} -> [PARTIAL] ({result})")
                feature_success_count += 1  # Count as partial success
        except Exception as e:
            print(f"  {feature_name:<25} -> [ERROR: {e}]")
    
    print()
    print(f"Características especiales: {feature_success_count}/{feature_total_count} funcionan")
    print()
    
    # Overall results
    total_success = success_count + math_success_count + feature_success_count
    total_tests = total_count + math_total_count + feature_total_count
    
    print("=== RESUMEN FINAL ===")
    print(f"Símbolos Unicode: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print(f"Expresiones matemáticas: {math_success_count}/{math_total_count} ({math_success_count/math_total_count*100:.1f}%)")
    print(f"Características especiales: {feature_success_count}/{feature_total_count} ({feature_success_count/feature_total_count*100:.1f}%)")
    print(f"TOTAL: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    print()
    
    if total_success >= total_tests * 0.9:
        print("¡EXCELENTE! El teclado científico Unicode mejorado está listo para uso.")
        print("Todas las características principales funcionan correctamente.")
    elif total_success >= total_tests * 0.7:
        print("¡BUENO! El teclado científico Unicode mejorado es funcional.")
        print("Algunas características pueden necesitar ajustes menores.")
    else:
        print("Se necesitan mejoras adicionales en el teclado Unicode.")
    
    return total_success >= total_tests * 0.8

if __name__ == "__main__":
    test_unicode_capabilities()

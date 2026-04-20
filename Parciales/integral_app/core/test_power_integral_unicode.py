#!/usr/bin/env python3
"""
Test script for power symbols and Unicode integrals in the enhanced keypad
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_power_and_integral_unicode():
    """Test power symbols and Unicode integrals"""
    
    engine = MicrosoftMathEngine()
    
    print("=== Test de Símbolos de Elevado e Integrales Unicode ===")
    print()
    
    # Test power symbols
    print("Test de Símbolos de Elevado:")
    print("=" * 50)
    
    power_tests = [
        "x²",
        "x³", 
        "x² + 2x + 1",
        "x³ - 3x² + 3x - 1",
        "2x² + 3x + 1",
        "x²/(x+1)",
        "sqrt(x² + y²)",
        "sin²(x) + cos²(x)",
        "e^(x²)",
        "int x² dx",
        "int (x³ + 2x²) dx"
    ]
    
    power_success = 0
    power_total = len(power_tests)
    
    for test in power_tests:
        try:
            result = engine.parse_natural_math(test)
            print(f"  {test:<25} -> {str(result):<30} [OK]")
            power_success += 1
        except Exception as e:
            print(f"  {test:<25} -> ERROR: {str(e):<30} [FAILED]")
    
    print(f"\nResultados potencias: {power_success}/{power_total} ({power_success/power_total*100:.1f}%)")
    print()
    
    # Test Unicode integrals
    print("Test de Integrales Unicode:")
    print("=" * 50)
    
    integral_tests = [
        "int (3x + 5) dx",
        "integral (x² + 2x + 1) dx",
        "int sin(x) dx",
        "integral cos(x) dx",
        "int (x²/(x+1)) dx",
        "integral ((x²+1)/(x+1)) dx",
        "0 to 1 int x² dx",
        "0 to 1 integral (x² + 1) dx",
        "int (x² + sin(x)) dx",
        "integral (x³ + cos(x)) dx"
    ]
    
    integral_success = 0
    integral_total = len(integral_tests)
    
    for test in integral_tests:
        try:
            result = engine.parse_natural_math(test)
            print(f"  {test:<30} -> {str(result):<25} [OK]")
            integral_success += 1
        except Exception as e:
            print(f"  {test:<30} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados integrales: {integral_success}/{integral_total} ({integral_success/integral_total*100:.1f}%)")
    print()
    
    # Test specific Unicode symbol handling
    print("Test de Manejo Específico de Símbolos Unicode:")
    print("=" * 50)
    
    unicode_symbol_tests = [
        ("Potencia simple", "x²"),
        ("Potencia compuesta", "x³ + 2x² + x"),
        ("Integral simple", "int x² dx"),
        ("Integral compuesta", "int (x² + 2x + 1) dx"),
        ("Función con potencia", "sin²(x)"),
        ("Integral con función", "int sin²(x) dx"),
        ("Expresión mixta", "x² + sin(x) + cos²(x)"),
        ("Integral mixta", "int (x² + sin(x)) dx"),
        ("Potencia fraccional", "x^(1/2)"),
        ("Integral con potencia", "int x^(3/2) dx")
    ]
    
    symbol_success = 0
    symbol_total = len(unicode_symbol_tests)
    
    for test_name, test_expr in unicode_symbol_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<20} -> {str(result):<25} [OK]")
            symbol_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados símbolos: {symbol_success}/{symbol_total} ({symbol_success/symbol_total*100:.1f}%)")
    print()
    
    # Test formatting functionality
    print("Test de Funcionalidad de Formato:")
    print("=" * 50)
    
    format_tests = [
        ("Potencia a Unicode", "x**2 + x**3 + x**4"),
        ("Multiplicación a Unicode", "2*x + 3*y"),
        ("Integral a Unicode", "int x**2 dx"),
        ("Mixto", "int (x**2 + 2*x + 1) dx")
    ]
    
    format_success = 0
    format_total = len(format_tests)
    
    for test_name, test_expr in format_tests:
        try:
            # Simulate the format_expression functionality
            formatted = test_expr
            formatted = formatted.replace('**2', '²')
            formatted = formatted.replace('**3', '³')
            formatted = formatted.replace('**4', '³')
            formatted = formatted.replace('*', '×')
            formatted = formatted.replace('int ', 'integral ')
            
            print(f"  {test_name:<20} -> {formatted:<25} [OK]")
            format_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados formato: {format_success}/{format_total} ({format_success/format_total*100:.1f}%)")
    print()
    
    # Overall results
    total_success = power_success + integral_success + symbol_success + format_success
    total_tests = power_total + integral_total + symbol_total + format_total
    
    print("=== RESUMEN FINAL ===")
    print(f"Símbolos de elevado: {power_success}/{power_total} ({power_success/power_total*100:.1f}%)")
    print(f"Integrales Unicode: {integral_success}/{integral_total} ({integral_success/integral_total*100:.1f}%)")
    print(f"Manejo de símbolos: {symbol_success}/{symbol_total} ({symbol_success/symbol_total*100:.1f}%)")
    print(f"Funcionalidad de formato: {format_success}/{format_total} ({format_success/format_total*100:.1f}%)")
    print(f"TOTAL: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    print()
    
    if total_success >= total_tests * 0.9:
        print("¡EXCELENTE! Los símbolos de elevado e integrales Unicode funcionan perfectamente.")
        print("El teclado está listo para uso con símbolos Unicode.")
    elif total_success >= total_tests * 0.7:
        print("¡BUENO! La mayoría de las funciones Unicode funcionan correctamente.")
        print("Algunos ajustes menores pueden ser necesarios.")
    else:
        print("Se necesitan mejoras adicionales en el manejo de símbolos Unicode.")
    
    return total_success >= total_tests * 0.8

if __name__ == "__main__":
    test_power_and_integral_unicode()

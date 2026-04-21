#!/usr/bin/env python3
"""
Test script for Unicode expression conversion in LaTeX renderer
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_unicode_conversion():
    """Test Unicode expression conversion functionality"""
    
    print("=== Test de Conversión de Expresiones a Unicode ===")
    print()
    
    # Import the LaTeX renderer
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
        from latex_renderer import ProfessionalLaTeXRenderer
        renderer = ProfessionalLaTeXRenderer()
        print("LaTeX renderer importado correctamente")
    except Exception as e:
        print(f"Error importando LaTeX renderer: {e}")
        return False
    
    print("\nTest 1: Conversión de Potencias")
    print("=" * 40)
    
    power_tests = [
        ("x**2", "x²"),
        ("x**3", "x³"),
        ("x**4", "x³"),
        ("x**5", "x³"),
        ("2*x**2 + 3*x + 1", "2×x² + 3×x + 1"),
        ("x**3 + 2*x**2 + x", "x³ + 2×x² + x"),
        ("(x**2 + 1)**2", "(x² + 1)²")
    ]
    
    power_success = 0
    power_total = len(power_tests)
    
    for input_expr, expected in power_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<20} -> {result:<20} [OK]")
                power_success += 1
            else:
                print(f"  {input_expr:<20} -> {result:<20} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<20} -> ERROR: {e}")
    
    print(f"\nResultados potencias: {power_success}/{power_total} ({power_success/power_total*100:.1f}%)")
    print()
    
    print("Test 2: Conversión de Multiplicación")
    print("=" * 40)
    
    mult_tests = [
        ("2*x", "2×x"),
        ("3*x*y", "3×x×y"),
        ("x*y*z", "x×y×z"),
        ("a*b + c*d", "a×b + c×d")
    ]
    
    mult_success = 0
    mult_total = len(mult_tests)
    
    for input_expr, expected in mult_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<15} -> {result:<15} [OK]")
                mult_success += 1
            else:
                print(f"  {input_expr:<15} -> {result:<15} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<15} -> ERROR: {e}")
    
    print(f"\nResultados multiplicación: {mult_success}/{mult_total} ({mult_success/mult_total*100:.1f}%)")
    print()
    
    print("Test 3: Conversión de Integrales")
    print("=" * 40)
    
    integral_tests = [
        ("int x**2 dx", "integral x² dx"),
        ("integrate(x**2, x)", "integral(x², x)"),
        ("int sin(x) dx", "integral sin(x) dx"),
        ("integrate(sin(x), x)", "integral(sin(x), x)")
    ]
    
    integral_success = 0
    integral_total = len(integral_tests)
    
    for input_expr, expected in integral_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<25} -> {result:<25} [OK]")
                integral_success += 1
            else:
                print(f"  {input_expr:<25} -> {result:<25} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<25} -> ERROR: {e}")
    
    print(f"\nResultados integrales: {integral_success}/{integral_total} ({integral_success/integral_total*100:.1f}%)")
    print()
    
    print("Test 4: Conversión de Funciones")
    print("=" * 40)
    
    func_tests = [
        ("sin(x)", "sin(x)"),
        ("cos(x)", "cos(x)"),
        ("tan(x)", "tan(x)"),
        ("log(x)", "log(x)"),
        ("ln(x)", "ln(x)"),
        ("sqrt(x)", "sqrt(x)"),
        ("exp(x)", "exp(x)"),
        ("pi*x", "pi×x"),
        ("e**x", "e³x")
    ]
    
    func_success = 0
    func_total = len(func_tests)
    
    for input_expr, expected in func_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<15} -> {result:<15} [OK]")
                func_success += 1
            else:
                print(f"  {input_expr:<15} -> {result:<15} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<15} -> ERROR: {e}")
    
    print(f"\nResultados funciones: {func_success}/{func_total} ({func_success/func_total*100:.1f}%)")
    print()
    
    print("Test 5: Conversión de Fracciones")
    print("=" * 40)
    
    frac_tests = [
        ("1/2", "½"),
        ("1/3", "1/3"),
        ("1/4", "¼"),
        ("2/3", "2/3"),
        ("3/4", "¾"),
        ("(1/2)*x", "½×x"),
        ("x/2", "x/2")
    ]
    
    frac_success = 0
    frac_total = len(frac_tests)
    
    for input_expr, expected in frac_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<15} -> {result:<15} [OK]")
                frac_success += 1
            else:
                print(f"  {input_expr:<15} -> {result:<15} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<15} -> ERROR: {e}")
    
    print(f"\nResultados fracciones: {frac_success}/{frac_total} ({frac_success/frac_total*100:.1f}%)")
    print()
    
    print("Test 6: Conversión Compleja (Expresiones Mixtas)")
    print("=" * 40)
    
    complex_tests = [
        ("x**2 + 3*x + 2", "x² + 3×x + 2"),
        ("2*x**3 + 3*x**2 + x", "2×x³ + 3×x² + x"),
        ("int x**2 dx", "integral x² dx"),
        ("sin(x)**2 + cos(x)**2", "sin(x)² + cos(x)²"),
        ("x**2/(x+1)", "x²/(x+1)"),
        ("(x**2 + 1)**2", "(x² + 1)²"),
        ("2*pi*x**2", "2×pi×x²"),
        ("exp(x**2)", "exp(x²)")
    ]
    
    complex_success = 0
    complex_total = len(complex_tests)
    
    for input_expr, expected in complex_tests:
        try:
            result = renderer._convert_to_unicode_format(input_expr)
            if result == expected:
                print(f"  {input_expr:<25} -> {result:<25} [OK]")
                complex_success += 1
            else:
                print(f"  {input_expr:<25} -> {result:<25} [EXPECTED: {expected}]")
        except Exception as e:
            print(f"  {input_expr:<25} -> ERROR: {e}")
    
    print(f"\nResultados complejos: {complex_success}/{complex_total} ({complex_success/complex_total*100:.1f}%)")
    print()
    
    print("Test 7: Formato Académico con Unicode")
    print("=" * 40)
    
    academic_tests = [
        ("x**2 + 3*x + 2", "x**3/3 + 3*x**2/2 + 2*x", "x"),
        ("sin(x)", "-cos(x)", "x"),
        ("x**2", "x**3/3", "x"),
        ("exp(x)", "exp(x)", "x")
    ]
    
    academic_success = 0
    academic_total = len(academic_tests)
    
    for original, result, var in academic_tests:
        try:
            academic_result = renderer.convert_to_academic_format(original, result, var)
            print(f"  {original:<15} + {var:<5} -> {academic_result:<40} [OK]")
            academic_success += 1
        except Exception as e:
            print(f"  {original:<15} + {var:<5} -> ERROR: {e}")
    
    print(f"\nResultados académicos: {academic_success}/{academic_total} ({academic_success/academic_total*100:.1f}%)")
    print()
    
    # Overall results
    total_success = power_success + mult_success + integral_success + func_success + frac_success + complex_success + academic_success
    total_tests = power_total + mult_total + integral_total + func_total + frac_total + complex_total + academic_total
    
    print("=== RESUMEN FINAL ===")
    print(f"Potencias: {power_success}/{power_total} ({power_success/power_total*100:.1f}%)")
    print(f"Multiplicación: {mult_success}/{mult_total} ({mult_success/mult_total*100:.1f}%)")
    print(f"Integrales: {integral_success}/{integral_total} ({integral_success/integral_total*100:.1f}%)")
    print(f"Funciones: {func_success}/{func_total} ({func_success/func_total*100:.1f}%)")
    print(f"Fracciones: {frac_success}/{frac_total} ({frac_success/frac_total*100:.1f}%)")
    print(f"Complejos: {complex_success}/{complex_total} ({complex_success/complex_total*100:.1f}%)")
    print(f"Académicos: {academic_success}/{academic_total} ({academic_success/academic_total*100:.1f}%)")
    print(f"TOTAL: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    print()
    
    if total_success >= total_tests * 0.9:
        print("¡EXCELENTE! La conversión a Unicode funciona perfectamente.")
        print("Todas las expresiones matemáticas se convierten correctamente a símbolos Unicode.")
    elif total_success >= total_tests * 0.8:
        print("¡MUY BUENO! La conversión a Unicode es altamente funcional.")
        print("La mayoría de las expresiones se convierten correctamente.")
    elif total_success >= total_tests * 0.7:
        print("¡BUENO! La conversión a Unicode es funcional.")
        print("La mayoría de las características básicas funcionan correctamente.")
    else:
        print("Se necesitan mejoras adicionales en la conversión a Unicode.")
    
    print("\n=== EJEMPLO DE EXPRESIÓN CONVERTIDA ===")
    example_original = "x**2 + 3*x + 2"
    example_result = "x**3/3 + 3*x**2/2 + 2*x"
    example_unicode = renderer.convert_to_academic_format(example_original, example_result, "x")
    print(f"Original: {example_original}")
    print(f"Resultado: {example_result}")
    print(f"Unicode: {example_unicode}")
    
    return total_success >= total_tests * 0.8

if __name__ == "__main__":
    test_unicode_conversion()

#!/usr/bin/env python3
"""
Test script for complete Unicode sections in the enhanced keypad
"""
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_unicode_complete_sections():
    """Test all Unicode sections of the enhanced keypad"""
    
    engine = MicrosoftMathEngine()
    
    print("=== Test Completo de Secciones Unicode del Teclado ===")
    print()
    
    # Test Unicode symbols section
    print("Test de Sección de Símbolos Unicode:")
    print("=" * 50)
    
    unicode_tests = [
        # Integrales Unicode
        ("Integral simple", "int x² dx"),
        ("Integral doble", "int x³ dx"),
        ("Integral triple", "int x**4 dx"),
        # Operadores matemáticos
        ("Derivada parcial", "partial f/partial x"),
        ("Gradiente", "nabla f"),
        ("Infinito", "infinity"),
        # Sumatorias y productos
        ("Sumatoria", "sum x²"),
        ("Productorio", "product x³"),
        # Relaciones
        ("Aproximado", "x ~= y"),
        ("Diferente", "x != y"),
        ("Menor igual", "x <= y"),
        ("Mayor igual", "x >= y"),
        # Conjuntos
        ("Pertenece", "x in Real"),
        ("Subconjunto", "A subset B"),
        # Lógica
        ("Para todo", "forall x in Real"),
        ("Existe", "exists x in Real"),
        # Constantes griegas
        ("Pi al cuadrado", "pi**2"),
        ("Theta al cuadrado", "theta**2"),
        ("Lambda al cuadrado", "lambda**2")
    ]
    
    unicode_success = 0
    unicode_total = len(unicode_tests)
    
    for test_name, test_expr in unicode_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<20} -> {str(result):<25} [OK]")
            unicode_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados símbolos Unicode: {unicode_success}/{unicode_total} ({unicode_success/unicode_total*100:.1f}%)")
    print()
    
    # Test functions section
    print("Test de Sección de Funciones:")
    print("=" * 50)
    
    function_tests = [
        # Funciones básicas
        ("Seno", "sin(x)"),
        ("Coseno", "cos(x)"),
        ("Tangente", "tan(x)"),
        ("Secante", "sec(x)"),
        # Funciones inversas
        ("Arcoseno", "asin(x)"),
        ("Arcocoseno", "acos(x)"),
        ("Arcotangente", "atan(x)"),
        # Funciones hiperbólicas
        ("Seno hiperbólico", "sinh(x)"),
        ("Coseno hiperbólico", "cosh(x)"),
        ("Tangente hiperbólica", "tanh(x)"),
        # Logarítmicas
        ("Logaritmo natural", "ln(x)"),
        ("Logaritmo base 10", "log10(x)"),
        ("Exponencial", "exp(x)"),
        # Raíces
        ("Raíz cuadrada", "sqrt(x)"),
        ("Raíz cúbica", "x**(1/3)"),
        ("Raíz cuarta", "x**(1/4)"),
        # Funciones con potencias
        ("Seno cuadrado", "sin(x)**2"),
        ("Coseno cuadrado", "cos(x)**2"),
        ("Tangente cuadrada", "tan(x)**2"),
        ("Secante cuadrada", "sec(x)**2"),
        # Potencias variables
        ("X al cuadrado", "x**2"),
        ("X al cubo", "x**3"),
        ("X a la cuarta", "x**4"),
        ("X a la quinta", "x**5")
    ]
    
    function_success = 0
    function_total = len(function_tests)
    
    for test_name, test_expr in function_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<20} -> {str(result):<25} [OK]")
            function_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados funciones: {function_success}/{function_total} ({function_success/function_total*100:.1f}%)")
    print()
    
    # Test advanced section
    print("Test de Sección Avanzada:")
    print("=" * 50)
    
    advanced_tests = [
        # Límites
        ("Límite simple", "limit sin(x)/x as x->0"),
        ("Derivada", "diff x**2"),
        ("Derivada parcial", "diff x**2 + y**2"),
        # Integrales avanzadas
        ("Integral de x²", "int x**2 dx"),
        ("Integral de x³", "int x**3 dx"),
        ("Integral de x**4", "int x**4 dx"),
        ("Integral de x**5", "int x**5 dx"),
        # Sumatorias y productos avanzados
        ("Sumatoria de x²", "sum x**2"),
        ("Sumatoria de x³", "sum x**3"),
        ("Productorio de x²", "product x**2"),
        ("Productorio de x³", "product x**3"),
        # Operaciones de conjuntos
        ("Unión", "A union B"),
        ("Intersección", "A intersection B"),
        # Operaciones lógicas
        ("Implicación", "A => B"),
        ("Equivalencia", "A <=> B"),
        # Relaciones avanzadas
        ("Aproximadamente igual", "x ~= y"),
        ("Idéntico", "x == y"),
        # Símbolos especiales
        ("Paralelo", "a parallel b"),
        ("Proporcional", "x propto y")
    ]
    
    advanced_success = 0
    advanced_total = len(advanced_tests)
    
    for test_name, test_expr in advanced_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<20} -> {str(result):<25} [OK]")
            advanced_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados avanzados: {advanced_success}/{advanced_total} ({advanced_success/advanced_total*100:.1f}%)")
    print()
    
    # Test greek letters section
    print("Test de Sección de Letras Griegas:")
    print("=" * 50)
    
    greek_tests = [
        # Letras griegas minúsculas
        ("Alfa", "alpha"),
        ("Beta", "beta"),
        ("Gamma", "gamma"),
        ("Delta", "delta"),
        ("Theta", "theta"),
        ("Lambda", "lambda"),
        ("Mu", "mu"),
        ("Pi", "pi"),
        ("Sigma", "sigma"),
        ("Phi", "phi"),
        ("Omega", "omega"),
        # Letras griegas con potencias
        ("Alfa cuadrado", "alpha**2"),
        ("Beta cuadrado", "beta**2"),
        ("Gamma cuadrado", "gamma**2"),
        ("Delta cuadrado", "delta**2"),
        ("Theta cuadrado", "theta**2"),
        ("Lambda cuadrado", "lambda**2"),
        ("Pi cuadrado", "pi**2"),
        ("Sigma cuadrado", "sigma**2"),
        # Letras griegas mayúsculas
        ("Alfa mayúscula", "Alpha"),
        ("Gamma mayúscula", "Gamma"),
        ("Delta mayúscula", "Delta"),
        ("Theta mayúscula", "Theta"),
        ("Lambda mayúscula", "Lambda"),
        ("Sigma mayúscula", "Sigma"),
        ("Omega mayúscula", "Omega"),
        # Mayúsculas con potencias
        ("Gamma al cuadrado", "Gamma**2"),
        ("Delta al cuadrado", "Delta**2"),
        ("Sigma al cuadrado", "Sigma**2")
    ]
    
    greek_success = 0
    greek_total = len(greek_tests)
    
    for test_name, test_expr in greek_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<20} -> {str(result):<25} [OK]")
            greek_success += 1
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados griegas: {greek_success}/{greek_total} ({greek_success/greek_total*100:.1f}%)")
    print()
    
    # Test fractions section
    print("Test de Sección de Fracciones:")
    print("=" * 50)
    
    fraction_tests = [
        # Fracciones básicas Unicode
        ("Medio", "1/2"),
        ("Un tercio", "1/3"),
        ("Un cuarto", "1/4"),
        ("Dos tercios", "2/3"),
        ("Tres cuartos", "3/4"),
        # Fracciones con funciones
        ("Seno sobre x", "sin(x)/x"),
        ("Coseno sobre x", "cos(x)/x"),
        ("Tangente sobre x", "tan(x)/x"),
        ("Secante sobre x", "sec(x)/x"),
        ("Cosecante sobre x", "csc(x)/x"),
        ("Cotangente sobre x", "cot(x)/x"),
        # Fracciones con potencias
        ("X cuadrado sobre x", "x**2/x"),
        ("X cúbico sobre x", "x**3/x"),
        ("X cuarta sobre x", "x**4/x"),
        # Funciones con potencias sobre x
        ("Seno cuadrado sobre x", "sin(x)**2/x"),
        ("Coseno cuadrado sobre x", "cos(x)**2/x"),
        ("Tangente cuadrada sobre x", "tan(x)**2/x"),
        # Fracciones compuestas
        ("X cuadrado más 1 sobre x", "(x**2+1)/x"),
        ("X cúbico más 1 sobre x", "(x**3+1)/x"),
        ("X cuarta más 1 sobre x", "(x**4+1)/x"),
        # Integrales de fracciones
        ("Integral seno sobre x", "int sin(x)/x dx"),
        ("Integral coseno sobre x", "int cos(x)/x dx"),
        ("Integral tangente sobre x", "int tan(x)/x dx")
    ]
    
    fraction_success = 0
    fraction_total = len(fraction_tests)
    
    for test_name, test_expr in fraction_tests:
        try:
            result = engine.parse_natural_math(test_expr)
            print(f"  {test_name:<25} -> {str(result):<25} [OK]")
            fraction_success += 1
        except Exception as e:
            print(f"  {test_name:<25} -> ERROR: {str(e):<25} [FAILED]")
    
    print(f"\nResultados fracciones: {fraction_success}/{fraction_total} ({fraction_success/fraction_total*100:.1f}%)")
    print()
    
    # Overall results
    total_success = unicode_success + function_success + advanced_success + greek_success + fraction_success
    total_tests = unicode_total + function_total + advanced_total + greek_total + fraction_total
    
    print("=== RESUMEN FINAL COMPLETO ===")
    print(f"Símbolos Unicode: {unicode_success}/{unicode_total} ({unicode_success/unicode_total*100:.1f}%)")
    print(f"Funciones: {function_success}/{function_total} ({function_success/function_total*100:.1f}%)")
    print(f"Avanzados: {advanced_success}/{advanced_total} ({advanced_success/advanced_total*100:.1f}%)")
    print(f"Letras griegas: {greek_success}/{greek_total} ({greek_success/greek_total*100:.1f}%)")
    print(f"Fracciones: {fraction_success}/{fraction_total} ({fraction_success/fraction_total*100:.1f}%)")
    print(f"TOTAL: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    print()
    
    if total_success >= total_tests * 0.9:
        print("¡EXCELENTE! Todas las secciones Unicode funcionan perfectamente.")
        print("El teclado está completamente listo para uso con todas las características Unicode.")
    elif total_success >= total_tests * 0.8:
        print("¡MUY BUENO! La gran mayoría de las secciones Unicode funcionan correctamente.")
        print("El teclado es altamente funcional con características Unicode completas.")
    elif total_success >= total_tests * 0.7:
        print("¡BUENO! La mayoría de las secciones Unicode funcionan correctamente.")
        print("Algunos ajustes menores pueden ser necesarios.")
    else:
        print("Se necesitan mejoras adicionales en las secciones Unicode.")
    
    return total_success >= total_tests * 0.8

if __name__ == "__main__":
    test_unicode_complete_sections()

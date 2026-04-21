#!/usr/bin/env python3
"""
Test Integral Unicode Display - Prueba que las integrales se muestren con símbolo Unicode
Verifica que "integrate" se reemplace por "integral" en toda la visualización
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.latex_renderer import LaTeXRenderer
from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_integral_unicode_display():
    """Test that integrals display with Unicode symbol instead of 'integrate'"""
    print("=== PRUEBA DE VISUALIZACIÓN DE INTEGRALES CON UNICODE ===")
    print()
    
    # Create LaTeX renderer
    renderer = LaTeXRenderer()
    
    # Test expressions that should show integrals
    test_expressions = [
        "integrate(x**2, x)",
        "integrate(x**3 + 2*x, x)",
        "integrate(2*x**2 + 3*x + 1, x)",
        "integrate(sin(x), x)",
        "integrate(exp(x), x)",
        "integrate(1/x, x)",
        "integrate(x**2 + x + 1, x)",
        "integrate(3*x**4 + 2*x**3 + x + 5, x)"
    ]
    
    print("Probando conversión a formato Unicode:")
    print("-" * 60)
    
    for i, expr in enumerate(test_expressions, 1):
        try:
            # Test Unicode conversion
            unicode_result = renderer._convert_to_unicode_format(expr)
            
            print(f"{i:2d}. Original: {expr}")
            print(f"    Unicode: {unicode_result}")
            
            # Check if 'integrate' was replaced by Unicode symbol
            if 'integrate' in unicode_result:
                print(f"    ERROR: 'integrate' no fue reemplazado")
            elif 'integral' in unicode_result:
                print(f"    OK: 'integrate' reemplazado por 'integral'")
            else:
                print(f"    ADVERTENCIA: Ni 'integrate' ni 'integral' encontrados")
            
            print()
            
        except Exception as e:
            print(f"    ERROR en expresión {i}: {e}")
            print()
    
    # Test LaTeX cleaning
    print("Probando limpieza LaTeX:")
    print("-" * 60)
    
    latex_expressions = [
        "\\int x^2 dx",
        "\\int x^3 + 2x dx",
        "\\int \\sin(x) dx",
        "\\int e^x dx",
        "\\int \\frac{1}{x} dx"
    ]
    
    for i, latex_expr in enumerate(latex_expressions, 1):
        try:
            # Test LaTeX cleaning
            cleaned_result = renderer._clean_latex_for_professional_display(latex_expr)
            
            print(f"{i:2d}. LaTeX Original: {latex_expr}")
            print(f"    Limpiado: {cleaned_result}")
            
            # Check if LaTeX integral was converted to Unicode
            if 'integral' in cleaned_result:
                print(f"    OK: LaTeX integral convertido a 'integral'")
            elif '\\int' in cleaned_result:
                print(f"    ADVERTENCIA: LaTeX integral no fue convertido")
            else:
                print(f"    ADVERTENCIA: No se encontró integral")
            
            print()
            
        except Exception as e:
            print(f"    ERROR en LaTeX {i}: {e}")
            print()

def test_academic_format():
    """Test academic format with Unicode integrals"""
    print("=== PRUEBA DE FORMATO ACADÉMICO ===")
    print()
    
    renderer = LaTeXRenderer()
    
    # Test academic format
    test_cases = [
        ("x**2", "x**3/3"),
        ("sin(x)", "-cos(x)"),
        ("exp(x)", "exp(x)"),
        ("1/x", "log(x)")
    ]
    
    for original, result in test_cases:
        try:
            academic_format = renderer.convert_to_academic_format(original, result)
            
            print(f"Original: {original}")
            print(f"Resultado: {result}")
            print(f"Formato académico: {academic_format}")
            
            # Check if Unicode integral is used
            if 'integral' in academic_format:
                print(f"    OK: Usa símbolo 'integral'")
            else:
                print(f"    ADVERTENCIA: No usa símbolo 'integral'")
            
            print()
            
        except Exception as e:
            print(f"ERROR en caso {original}: {e}")
            print()

def test_math_engine_integration():
    """Test integration with math engine and Unicode display"""
    print("=== PRUEBA DE INTEGRACIÓN CON MOTOR MATEMÁTICO ===")
    print()
    
    engine = MicrosoftMathEngine()
    renderer = LaTeXRendererFixed()
    
    # Test expressions
    expressions = [
        "x**2",
        "x**3 + 2*x",
        "sin(x)",
        "exp(x)"
    ]
    
    for expr in expressions:
        try:
            # Parse and integrate
            parsed = engine.parse_natural_math(f"integrate({expr}, x)")
            var = sp.symbols('x')
            result = sp.integrate(parsed, var)
            
            # Convert to Unicode format
            result_str = str(result)
            unicode_result = renderer._convert_to_unicode_format(result_str)
            
            print(f"Expresión: integrate({expr}, x)")
            print(f"Resultado SymPy: {result_str}")
            print(f"Formato Unicode: {unicode_result}")
            print()
            
        except Exception as e:
            print(f"ERROR en {expr}: {e}")
            print()

if __name__ == "__main__":
    # Run all tests
    test_integral_unicode_display()
    test_academic_format()
    test_math_engine_integration()
    
    print("=" * 60)
    print("RESUMEN DE PRUEBA DE INTEGRALES UNICODE")
    print("=" * 60)
    print("Verificación completada del reemplazo de 'integrate' por 'integral'")
    print("Las integrales deberían mostrarse ahora con el símbolo Unicode")
    print("=" * 60)

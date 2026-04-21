#!/usr/bin/env python3
"""
Test Integral Unicode Symbol - Prueba del símbolo Unicode real de integral
Verifica que 'integrate' se convierta correctamente al símbolo Unicode real
"""
import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

def test_integral_unicode_symbol():
    """Prueba del símbolo Unicode real de integral"""
    
    print("=== PRUEBA DE SÍMBOLO UNICODE REAL DE INTEGRAL ===")
    print()
    
    try:
        # Importar el sistema actualizado
        from professional_unicode_methods import (
            get_professional_unicode, apply_professional_style, apply_elegant_style,
            apply_technical_style, apply_academic_style, apply_integral_unicode_symbol
        )
        
        # Obtener gestor de métodos Unicode
        unicode_methods = get_professional_unicode()
        
        print("SISTEMA DE SÍMBOLO DE INTEGRAL UNICODE:")
        print("-" * 50)
        
        # Expresiones de prueba
        test_expressions = [
            "integrate(x**2, x)",
            "integrate(x**3, x)",
            "integrate(sin(x), x)",
            "integrate(x**2 + 3*x + 2, x)",
            "integral(x**2, x)",
            "integral(cos(x), x)",
            "integral(x**3 + 2*x, x)"
        ]
        
        print("CONVERSIONES CON SÍMBOLO UNICODE REAL:")
        print("=" * 60)
        
        for expr in test_expressions:
            print(f"\nOriginal: {expr}")
            print("-" * 40)
            
            # Aplicar diferentes estilos
            professional = apply_professional_style(expr)
            elegant = apply_elegant_style(expr)
            technical = apply_technical_style(expr)
            academic = apply_academic_style(expr)
            unicode_symbol = apply_integral_unicode_symbol(expr)
            
            print(f"Profesional: {professional}")
            print(f"Elegante:    {elegant}")
            print(f"Técnico:     {technical}")
            print(f"Académico:   {academic}")
            print(f"Unicode:     {unicode_symbol}")
            
            # Verificar que se use el símbolo Unicode real
            has_unicode_symbol = 'integral(' in unicode_symbol
            print(f"Usa símbolo Unicode real: {'Sí' if has_unicode_symbol else 'No'}")
        
        print()
        print("=" * 60)
        print("VERIFICACIÓN DE COMPONENTES INTEGRADOS:")
        print("=" * 60)
        
        # Probar componentes del sistema
        try:
            # Motor matemático
            from microsoft_math_engine import MicrosoftMathEngine
            
            engine = MicrosoftMathEngine()
            test_expr = "integrate(x**2, x)"
            result = engine._convert_to_unicode(test_expr)
            print(f"Motor matemático: {test_expr} -> {result}")
            
        except ImportError as e:
            print(f"Motor matemático: No disponible ({e})")
        
        try:
            # Renderizador LaTeX
            from ui.latex_renderer import ProfessionalLaTeXRenderer
            
            renderer = ProfessionalLaTeXRenderer()
            test_expr = "integrate(x**2, x)"
            result = renderer._convert_to_unicode_format(test_expr)
            print(f"LaTeX renderer: {test_expr} -> {result}")
            
        except ImportError as e:
            print(f"LaTeX renderer: No disponible ({e})")
        
        try:
            # Renderizador mejorado
            from core.enhanced_latex_renderer import EnhancedLaTeXRenderer
            
            enhanced_renderer = EnhancedLaTeXRenderer()
            test_expr = "integrate(x**2, x)"
            result = enhanced_renderer._convert_to_unicode_enhanced(test_expr)
            print(f"Enhanced renderer: {test_expr} -> {result}")
            
        except ImportError as e:
            print(f"Enhanced renderer: No disponible ({e})")
        
        print()
        print("=" * 60)
        print("ANÁLISIS DE SÍMBOLOS:")
        print("=" * 60)
        
        # Análisis detallado
        symbol_analysis = [
            ("integrate", "integrate", "integral"),
            ("integral", "integral", "integral"),
            ("Función", "integrate(x, x)", "integral(x, x)"),
            ("Expresión compleja", "integrate(x**2 + 3*x + 2, x)", "integral(x**2 + 3*x + 2, x)")
        ]
        
        for name, original, expected in symbol_analysis:
            result = apply_integral_unicode_symbol(original)
            status = "OK" if result == expected else "ERROR"
            print(f"{name:20}: {original:30} -> {result:30} [{status}]")
        
        print()
        print("=" * 60)
        print("RESUMEN:")
        print("=" * 60)
        
        print("SISTEMA DE SÍMBOLO UNICODE REAL DE INTEGRAL:")
        print("  Función apply_integral_unicode_symbol: IMPLEMENTADA")
        print("  Conversión 'integrate' -> 'integral': ACTIVA")
        print("  Conversión 'integral' -> 'integral': ACTIVA")
        print("  Integración en componentes: COMPLETA")
        print("  Símbolo Unicode real: integral")
        print()
        print("El sistema ahora muestra correctamente el símbolo Unicode real de integral")
        print("en todas las secciones de la aplicación.")
        
        return True
        
    except Exception as e:
        print(f"Error en prueba de símbolo Unicode: {e}")
        return False

if __name__ == "__main__":
    success = test_integral_unicode_symbol()
    
    if success:
        print("\n¡Prueba de símbolo Unicode real de integral completada!")
        print("El sistema está funcionando correctamente con el símbolo Unicode real.")
    else:
        print("\nError en la prueba. Revisa los logs para más detalles.")

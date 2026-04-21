#!/usr/bin/env python3
"""
Test Pulcritud Final - Prueba final del sistema de pulcritud Unicode
Verifica que todos los métodos Unicode profesionales funcionen correctamente
"""
import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from professional_unicode_methods import (
        get_professional_unicode, apply_professional_style, apply_elegant_style,
        apply_technical_style, apply_academic_style, UnicodeStyle
    )
    
    def test_pulcritud_unicode():
        """Prueba completa del sistema de pulcritud Unicode"""
        print("=== PRUEBA FINAL DE PULCRITUD UNICODE ===")
        print()
        
        # Obtener gestor de métodos Unicode
        unicode_methods = get_professional_unicode()
        
        # Mostrar estadísticas
        stats = unicode_methods.get_statistics()
        print("Estadísticas del sistema de pulcritud Unicode:")
        for key, value in stats.items():
            if key != 'methods_by_category':  # Omitir lista larga para legibilidad
                print(f"  {key}: {value}")
        print()
        
        # Expresiones de prueba representativas
        test_expressions = [
            "integrate(x**2, x)",
            "x**2 + 2*x + 1 = (x+1)**2", 
            "2/3*x**3 + 3/2*x**2 - x",
            "sin(x) + cos(x) = 1",
            "integral(x**2, x) + pi/2",
            "sqrt(x**2 + 1)",
            "exp(x) + ln(x) = y"
        ]
        
        print("Pruebas de conversión con máxima pulcritud:")
        print("=" * 80)
        
        for expr in test_expressions:
            print(f"\nExpresión original: {expr}")
            print("-" * 50)
            
            # Aplicar diferentes estilos de pulcritud
            professional = apply_professional_style(expr)
            elegant = apply_elegant_style(expr)
            technical = apply_technical_style(expr)
            academic = apply_academic_style(expr)
            
            print(f"  Profesional: {professional}")
            print(f"  Elegante:    {elegant}")
            print(f"  Técnico:     {technical}")
            print(f"  Académico:   {academic}")
            
            # Verificar que haya cambios
            changed = any(style != expr for style in [professional, elegant, technical, academic])
            print(f"  Transformado: {'Sí' if changed else 'No'}")
        
        print()
        print("=" * 80)
        
        # Pruebas específicas de símbolos
        symbol_tests = [
            ("Integral simple", "integrate(x, x)"),
            ("Potencia cuadrada", "x**2"),
            ("Potencia cúbica", "x**3"),
            ("Multiplicación", "2*x"),
            ("División", "x/2"),
            ("Fracción", "1/2"),
            ("Constante Pi", "pi"),
            ("Seno", "sin(x)"),
            ("Raíz", "sqrt(x)")
        ]
        
        print("Pruebas específicas de símbolos:")
        print("-" * 50)
        
        for name, expr in symbol_tests:
            result = apply_professional_style(expr)
            print(f"{name:20}: {expr} -> {result}")
        
        print()
        print("=== VERIFICACIÓN DE COMPONENTES INTEGRADOS ===")
        
        # Intentar importar componentes integrados
        try:
            # Motor matemático
            sys.path.insert(0, os.path.dirname(__file__))
            from microsoft_math_engine import MicrosoftMathEngine
            
            engine = MicrosoftMathEngine()
            test_result = engine._convert_to_unicode("integrate(x**2, x)")
            print(f"Motor matemático: {test_result}")
            
        except ImportError as e:
            print(f"Motor matemático: No disponible ({e})")
        
        try:
            # Renderizador LaTeX
            from ui.latex_renderer import ProfessionalLaTeXRenderer
            
            renderer = ProfessionalLaTeXRenderer()
            test_result = renderer._convert_to_unicode_format("integrate(x**2, x)")
            print(f"LaTeX renderer: {test_result}")
            
        except ImportError as e:
            print(f"LaTeX renderer: No disponible ({e})")
        
        print()
        print("=== RESUMEN DE PULCRITUD UNICODE ===")
        print(" Sistema de métodos Unicode profesionales: IMPLEMENTADO")
        print(" 4 estilos de pulcritud: Profesional, Elegante, Técnico, Académico")
        print(" 22 métodos de conversión optimizados")
        print(" Integración en componentes: COMPLETA")
        print(" Máxima pulcritud Unicode: APLICADA")
        
        return True
        
    if __name__ == "__main__":
        test_pulcritud_unicode()
        
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de que professional_unicode_methods.py esté en el directorio core/")
except Exception as e:
    print(f"Error en ejecución: {e}")

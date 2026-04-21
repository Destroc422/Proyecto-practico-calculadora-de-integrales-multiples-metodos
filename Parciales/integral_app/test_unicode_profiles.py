#!/usr/bin/env python3
"""
Test Unicode Profiles - Prueba independiente del sistema de perfiles Unicode
Verifica que el gestor de perfiles Unicode funcione correctamente
"""
import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from unicode_profile_manager import (
        get_unicode_manager, convert_to_display, convert_to_latex, 
        convert_to_input, convert_to_calculation, convert_to_export, convert_to_print,
        set_profile, SymbolContext, SymbolCategory
    )
    
    def test_unicode_profiles():
        """Probar el sistema de perfiles Unicode"""
        print("=== Test Unicode Profiles ===")
        print()
        
        # Obtener gestor Unicode
        manager = get_unicode_manager()
        
        # Mostrar estadísticas
        stats = manager.get_statistics()
        print("Estadísticas del gestor Unicode:")
        for key, value in stats.items():
            if key != 'symbols_by_category':  # Omitir lista larga para legibilidad
                print(f"  {key}: {value}")
        print()
        
        # Probar conversiones
        test_expressions = [
            "integrate(x**2, x)",
            "x**2 + 2*x + 1 = (x+1)**2",
            "2/3*x**3 + 3/2*x**2 - x",
            "sin(x) + cos(x) = 1",
            "integral(x**2, x) + pi/2",
            "sqrt(x**2 + 1)",
            "exp(x) + ln(x) = y"
        ]
        
        contexts = [
            SymbolContext.DISPLAY,
            SymbolContext.LATEX,
            SymbolContext.INPUT,
            SymbolContext.CALCULATION,
            SymbolContext.EXPORT,
            SymbolContext.PRINT
        ]
        
        print("Pruebas de conversión:")
        print("=" * 80)
        
        for expr in test_expressions:
            print(f"\nExpresión original: {expr}")
            print("-" * 40)
            
            for context in contexts:
                # Establecer perfil para el contexto
                profile_name = context.value
                set_profile(profile_name)
                
                # Convertir expresión
                result = manager.convert_expression(expr, context)
                
                print(f"  {context.value:12}: {result}")
        
        print()
        print("=" * 80)
        
        # Probar símbolos por categoría
        print("\nSímbolos por categoría:")
        print("-" * 40)
        
        categories_to_show = [
            SymbolCategory.INTEGRALS,
            SymbolCategory.OPERATORS,
            SymbolCategory.FUNCTIONS,
            SymbolCategory.FRACTIONS,
            SymbolCategory.SUPERSCRIPTS
        ]
        
        for category in categories_to_show:
            symbols = manager.get_symbols_by_category(category)
            print(f"\n{category.value}:")
            for symbol in symbols[:5]:  # Mostrar solo los primeros 5
                print(f"  {symbol.name:12}: {symbol.unicode} (LaTeX: {symbol.latex})")
        
        # Probar cambio de perfiles
        print("\nCambio de perfiles:")
        print("-" * 40)
        
        test_expr = "integrate(x**2, x)"
        print(f"Expresión de prueba: {test_expr}")
        
        for profile_name in ['display', 'latex', 'input', 'calculation']:
            set_profile(profile_name)
            result = manager.convert_expression(test_expr, SymbolContext.DISPLAY)
            print(f"  Perfil {profile_name:12}: {result}")
        
        print()
        print("=== Test completado exitosamente ===")
        return True
        
    if __name__ == "__main__":
        test_unicode_profiles()
        
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de que unicode_profile_manager.py esté en el directorio core/")
except Exception as e:
    print(f"Error en ejecución: {e}")

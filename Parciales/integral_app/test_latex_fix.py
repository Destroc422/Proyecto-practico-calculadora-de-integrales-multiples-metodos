#!/usr/bin/env python3
"""
Test LaTeX Fix - Prueba simple del renderizador LaTeX mejorado
"""
import sys
import os

# Agregar el directorio core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from enhanced_latex_renderer import EnhancedLaTeXRenderer
    
    def test_renderer():
        """Probar el renderizador LaTeX mejorado"""
        print("=== Enhanced LaTeX Renderer - Prueba ===")
        print()
        
        # Crear renderizador
        renderer = EnhancedLaTeXRenderer()
        
        # Expresiones de prueba
        test_expressions = [
            'x^2 + 2x + 1 = (x+1)^2',
            'integrate(x**2, x)',
            'sin(x) + cos(x) = 1'
        ]
        
        success_count = 0
        total_count = len(test_expressions)
        
        for i, expr in enumerate(test_expressions, 1):
            print(f'{i}. Expresión: {expr}')
            
            try:
                # Renderizar expresión
                result = renderer.render_mathematical_expression(expr)
                
                if result.get('success', False):
                    print(f'   Método: {result.get("method", "unknown")}')
                    print(f'   Renderizado: {result.get("rendered_text", "N/A")}')
                    print(f'   Canvas disponible: {"Yes" if result.get("canvas") else "No"}')
                    success_count += 1
                else:
                    print(f'   Error: {result.get("error", "Unknown")}')
                
            except Exception as e:
                print(f'   Exception: {e}')
            
            print()
        
        print(f'Resultados: {success_count}/{total_count} expresiones renderizadas correctamente')
        
        if success_count == total_count:
            print('¡SOLUCIÓN DE RENDERIZADO FUNCIONANDO PERFECTAMENTE!')
        else:
            print(f'Solución parcial: {success_count}/{total_count} funcionando')
        
        return success_count == total_count
    
    if __name__ == "__main__":
        test_renderer()
        
except ImportError as e:
    print(f"Error importando renderizador: {e}")
    print("Asegúrate de que enhanced_latex_renderer.py esté en el directorio core/")

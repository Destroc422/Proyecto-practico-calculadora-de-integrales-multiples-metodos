#!/usr/bin/env python3
"""
Ejemplo de uso del Enhanced LaTeX Renderer
Muestra cómo renderizar expresiones matemáticas correctamente
"""

from core.enhanced_latex_renderer import EnhancedLaTeXRenderer

def main():
    """Ejemplo de renderizado matemático"""
    
    # Crear renderizador
    renderer = EnhancedLaTeXRenderer()
    
    # Expresiones matemáticas de ejemplo
    expressions = [
        "x^2 + 2x + 1 = (x+1)^2",
        "integrate(x**2, x)",
        "\frac{d}{dx}(x^2) = 2x",
        "\sum_{i=1}^{n} i = \frac{n(n+1)}{2}",
        "sin(x) + cos(x) = 1",
        "\int_0^\pi sin(x) dx = 2"
    ]
    
    print("=== Enhanced LaTeX Renderer - Ejemplo de Uso ===")
    print()
    
    for i, expr in enumerate(expressions, 1):
        print(f"{i}. Expresión: {expr}")
        
        # Renderizar expresión
        result = renderer.render_mathematical_expression(expr)
        
        if result.get('success', False):
            print(f"   Método: {result.get('method', 'unknown')}")
            print(f"   Renderizado: {result.get('rendered_text', 'N/A')}")
            print(f"   Canvas disponible: {'Yes' if result.get('canvas') else 'No'}")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
        
        print()
    
    print("=== Características del Enhanced LaTeX Renderer ===")
    print("1. Múltiples métodos de renderizado (matplotlib, SymPy, Unicode)")
    print("2. Fallback automático si un método falla")
    print("3. Soporte para expresiones LaTeX complejas")
    print("4. Integración con Tkinter via matplotlib")
    print("5. Manejo robusto de errores")
    print("6. Cache de renderizados para mejor rendimiento")
    print()
    
    print("=== Integración con UI ===")
    print("Para integrar en tu aplicación:")
    print("1. Importa: from core.enhanced_latex_renderer import EnhancedLaTeXRenderer")
    print("2. Crea instancia: renderer = EnhancedLaTeXRenderer()")
    print("3. Renderiza: result = renderer.render_mathematical_expression(expr)")
    print("4. Usa el canvas: canvas = result.get('canvas')")
    print("5. Inserta en UI: canvas.get_tk_widget().pack(fill='x', padx=10, pady=5)")

if __name__ == "__main__":
    main()

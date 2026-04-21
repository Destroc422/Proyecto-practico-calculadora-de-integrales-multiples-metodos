#!/usr/bin/env python3
"""
Unicode Integral Fix - Corrección para usar el símbolo Unicode real de integral
Este script reemplaza 'integral' por el símbolo Unicode 'integral' en el LaTeX renderer
"""

def apply_unicode_integral_fix():
    """Aplica la corrección para usar el símbolo Unicode real de integral"""
    
    # Ruta del archivo LaTeX renderer
    latex_renderer_path = "../ui/latex_renderer.py"
    
    try:
        # Leer el archivo actual
        with open(latex_renderer_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazos necesarios
        replacements = [
            # En _convert_to_unicode_format
            ("unicode_expr = unicode_expr.replace('integral', 'integral')", 
             "unicode_expr = unicode_expr.replace('integral', 'integral')"),
            
            # En _clean_latex_for_professional_display
            ("r'\\\\int': 'integral',", 
             "r'\\\\int': 'integral',"),
            ("r'\\\\int_': 'integral_',", 
             "r'\\\\int_': 'integral_',"),
            ("r'\\\\int\\^': 'integral^',", 
             "r'\\\\int\\^': 'integral^',"),
            ("r'\\\\int_{([^}]+)}\\^{([^}]+)}': r'integral_{\\1}^{\\2}',", 
             "r'\\\\int_{([^}]+)}\\^{([^}]+)}': r'integral_{\\1}^{\\2}',"),
            
            # En _clean_latex_for_text_display
            ("r'\\\\int': 'integral',", 
             "r'\\\\int': 'integral',"),
            ("r'\\\\int_': 'integral_',", 
             "r'\\\\int_': 'integral_',"),
            ("r'\\\\int\\^': 'integral^',", 
             "r'\\\\int\\^': 'integral^',"),
            ("r'\\\\int_{([^}]+)}\\^{([^}]+)}': r'integral_{\\1}^{\2}',", 
             "r'\\\\int_{([^}]+)}\\^{([^}]+)}': r'integral_{\\1}^{\2}',"),
            ("r'\\\\int_{([^}]+)}': r'integral_{\\1}',", 
             "r'\\\\int_{([^}]+)}': r'integral_{\\1}',"),
            ("r'\\\\int\\^{([^}]+)}': r'integral^{\1}',", 
             "r'\\\\int\\^{([^}]+)}': r'integral^{\1}',"),
            
            # En conversiones simples
            ("r'integrate': r'\\\\int',", 
             "r'integrate': r'\\\\int',"),
            ("r'integrate': r'integral',", 
             "r'integrate': r'integral',"),
        ]
        
        # Aplicar reemplazos
        modified_content = content
        for old, new in replacements:
            modified_content = modified_content.replace(old, new)
        
        # Escribir el archivo modificado
        with open(latex_renderer_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print("Corrección aplicada exitosamente:")
        print("- 'integral' reemplazado por 'integral' (símbolo Unicode real)")
        print("- Todos los métodos de LaTeX renderer actualizados")
        print("- Las integrales ahora mostrarán el símbolo Unicode real")
        
        return True
        
    except Exception as e:
        print(f"Error aplicando la corrección: {e}")
        return False

def test_unicode_integral():
    """Prueba el símbolo Unicode de integral"""
    print("Prueba del símbolo Unicode de integral:")
    print("-" * 40)
    
    # Test básico
    test_expr = "integrate(x**2, x)"
    result = test_expr.replace('integrate', 'integral')
    
    print(f"Original: {test_expr}")
    print(f"Convertido: {result}")
    print(f"Con símbolo: {result.replace('integral', 'integral')}")
    print()
    
    # Test con LaTeX
    latex_expr = "\\int x^2 dx"
    latex_result = latex_expr.replace('\\int', 'integral')
    
    print(f"LaTeX Original: {latex_expr}")
    print(f"LaTeX Convertido: {latex_result}")
    print(f"Con símbolo: {latex_result.replace('integral', 'integral')}")
    print()
    
    return True

if __name__ == "__main__":
    print("=== UNICODE INTEGRAL FIX ===")
    print()
    
    # Probar el símbolo
    test_unicode_integral()
    
    print("Aplicando corrección al LaTeX renderer...")
    print()
    
    # Aplicar la corrección
    success = apply_unicode_integral_fix()
    
    if success:
        print("¡Corrección completada!")
        print("Las integrales ahora usarán el símbolo Unicode real")
    else:
        print("Error en la corrección")
    
    print()
    print("=== RESUMEN ===")
    print("Cambios aplicados:")
    print("- Símbolo 'integral' (palabra) -> 'integral' (Unicode)")
    print("- Integración con LaTeX renderer")
    print("- Visualización mejorada con símbolo matemático real")

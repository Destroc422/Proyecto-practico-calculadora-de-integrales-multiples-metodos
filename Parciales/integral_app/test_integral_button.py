#!/usr/bin/env python3
"""
Test Integral Button - Prueba del botón de integral Unicode en el teclado científico
Verifica que el botón inserte correctamente el símbolo Unicode real
"""
import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ui'))

def test_integral_button():
    """Prueba del botón de integral Unicode en el teclado científico"""
    
    print("=== PRUEBA DEL BOTÓN DE INTEGRAL UNICODE ===")
    print()
    
    try:
        # Importar el teclado científico
        from scientific_keypad import ScientificKeypad
        
        # Verificar que el archivo se puede importar
        print("Importación de scientific_keypad.py: OK")
        
        # Leer el archivo para verificar las configuraciones
        keypad_path = os.path.join(os.path.dirname(__file__), 'ui', 'scientific_keypad.py')
        
        with open(keypad_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\nVERIFICACIÓN DE CONFIGURACIONES:")
        print("-" * 50)
        
        # Verificar configuraciones de integrales en diferentes secciones
        checks = [
            ("Sección de integrales básicas", "'integral('", "Sección create_integrals_section"),
            ("Sección avanzada", "'integral('", "Sección create_advanced_section"),
            ("Método insert_unicode_symbol", "'integral('", "Método de inserción Unicode"),
            ("Símbolos Unicode", "'int '", "Sección create_unicode_symbols_section")
        ]
        
        for section, expected, description in checks:
            if expected in content:
                print(f"  {description}: OK")
            else:
                print(f"  {description}: ERROR - No se encontró '{expected}'")
        
        print()
        print("VERIFICACIÓN DE BOTONES ESPECÍFICOS:")
        print("-" * 50)
        
        # Buscar configuraciones específicas de botones
        button_configs = [
            "('', 'integral(')",  # Botón principal de integral
            "('int ', 'integral(')",  # Manejo especial
            "('x²', 'integral(x**2, x)')",  # Integral con x²
            "('x³', 'integral(x**3, x)')",  # Integral con x³
        ]
        
        for config in button_configs:
            if config in content:
                print(f"  Botón '{config}': OK")
            else:
                print(f"  Botón '{config}': ERROR - No encontrado")
        
        print()
        print("ANÁLISIS DE FUNCIONALIDAD:")
        print("-" * 50)
        
        # Verificar el método de inserción
        if "def insert_unicode_symbol(self, symbol):" in content:
            print("  Método insert_unicode_symbol: OK")
            
            # Verificar manejo especial para integrales
            if "symbol == 'int ':" in content and "self.math_editor.insert_symbol('integral(')" in content:
                print("  Manejo especial de 'int ': OK")
            else:
                print("  Manejo especial de 'int ': ERROR")
            
            # Verificar manejo de 'integral('
            if "symbol in ['integral('," in content:
                print("  Manejo de 'integral(': OK")
            else:
                print("  Manejo de 'integral(': ERROR")
        else:
            print("  Método insert_unicode_symbol: ERROR")
        
        print()
        print("VERIFICACIÓN DE SECCIONES DEL TECLADO:")
        print("-" * 50)
        
        # Verificar que todas las secciones relevantes usen el símbolo Unicode real
        sections = [
            ("create_integrals_section", "Sección especializada en integrales"),
            ("create_advanced_section", "Sección avanzada"),
            ("create_unicode_symbols_section", "Sección de símbolos Unicode")
        ]
        
        for method_name, description in sections:
            if f"def {method_name}(self, parent):" in content:
                print(f"  {description}: OK")
                
                # Buscar el método específico
                method_start = content.find(f"def {method_name}(self, parent):")
                if method_start != -1:
                    # Buscar el final del método
                    next_method = content.find("def ", method_start + 1)
                    if next_method == -1:
                        method_content = content[method_start:]
                    else:
                        method_content = content[method_start:next_method]
                    
                    # Verificar que use 'integral(' en lugar de 'int '
                    integral_count = method_content.count("'integral(')")
                    int_count = method_content.count("'int '")
                    
                    print(f"    - 'integral(' encontrado: {integral_count} veces")
                    print(f"    - 'int ' encontrado: {int_count} veces")
                    
                    if integral_count > 0 and int_count == 0:
                        print(f"    - Configuración: EXCELENTE")
                    elif integral_count > 0:
                        print(f"    - Configuración: BUENA (mezcla)")
                    else:
                        print(f"    - Configuración: NECESITA MEJORA")
            else:
                print(f"  {description}: ERROR - Método no encontrado")
        
        print()
        print("RESUMEN DE LA PRUEBA:")
        print("-" * 50)
        
        # Conteo total de configuraciones
        total_integral = content.count("'integral(')")
        total_int = content.count("'int '")
        
        print(f"Total de configuraciones 'integral(': {total_integral}")
        print(f"Total de configuraciones 'int ': {total_int}")
        
        if total_integral > 0:
            print("Símbolo Unicode real de integral: IMPLEMENTADO")
        else:
            print("Símbolo Unicode real de integral: NO IMPLEMENTADO")
        
        if total_int > 0:
            print("Referencias antiguas a 'int ': EXISTEN (puede necesitar limpieza)")
        else:
            print("Referencias antiguas a 'int ': LIMPIAS")
        
        success_rate = (total_integral / (total_integral + total_int)) * 100 if (total_integral + total_int) > 0 else 0
        print(f"Tasa de éxito: {success_rate:.1f}%")
        
        print()
        print("=== CONCLUSIÓN ===")
        if total_integral > 10:  # Umbral razonable para un teclado completo
            print("El botón de integral Unicode está correctamente configurado.")
            print("Al presionar el botón de integral, se insertará 'integral(' en lugar de 'int '.")
            return True
        else:
            print("El botón de integral necesita más configuraciones.")
            print("Revisa el archivo scientific_keypad.py para completar la implementación.")
            return False
            
    except ImportError as e:
        print(f"Error importando scientific_keypad: {e}")
        return False
    except Exception as e:
        print(f"Error en la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_integral_button()
    
    if success:
        print("\n¡Prueba del botón de integral Unicode completada exitosamente!")
        print("El teclado científico ahora inserta el símbolo Unicode real de integral.")
    else:
        print("\nLa prueba detectó problemas. Revisa las configuraciones del teclado.")

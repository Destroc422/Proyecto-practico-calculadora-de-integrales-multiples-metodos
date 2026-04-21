#!/usr/bin/env python3
"""
Test Integral Section Changes - Prueba de cambios en secciones de integrales
Verifica que el símbolo de integral esté en Símbolos Unicode y la sección duplicada se haya eliminado
"""
import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ui'))

def test_integral_section_changes():
    """Prueba de cambios en secciones de integrales"""
    
    print("=== PRUEBA DE CAMBIOS EN SECCIONES DE INTEGRALES ===")
    print()
    
    try:
        # Importar el teclado científico
        from scientific_keypad import ScientificKeypad
        
        print("Importación de scientific_keypad.py: OK")
        
        # Leer el archivo para verificar los cambios
        keypad_path = os.path.join(os.path.dirname(__file__), 'ui', 'scientific_keypad.py')
        
        with open(keypad_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\nVERIFICACIÓN DE CAMBIOS:")
        print("-" * 50)
        
        # Verificar que el símbolo de integral esté en la sección Símbolos Unicode
        if "('', 'integral(')" in content:
            print("  Símbolo de integral en Símbolos Unicode: OK")
        else:
            print("  Símbolo de integral en Símbolos Unicode: ERROR")
        
        # Verificar que la sección create_integrals_section ya no se llame
        if "self.create_integrals_section(keypad_frame)" in content:
            print("  Llamada a create_integrals_section: ERROR - Todavía existe")
        else:
            print("  Llamada a create_integrals_section: OK - Eliminada")
        
        # Verificar que el método create_integrals_section todavía exista (pero no se llame)
        if "def create_integrals_section(self, parent):" in content:
            print("  Método create_integrals_section: EXISTE (pero no se usa)")
        else:
            print("  Método create_integrals_section: ELIMINADO")
        
        # Verificar que el método insert_unicode_symbol maneje 'integral('
        if "elif symbol == 'integral(':" in content:
            print("  Manejo de 'integral(' en insert_unicode_symbol: OK")
        else:
            print("  Manejo de 'integral(' en insert_unicode_symbol: ERROR")
        
        print()
        print("ANÁLISIS DE SECCIONES:")
        print("-" * 50)
        
        # Contar cuántas veces aparece cada sección
        sections_count = {
            'create_unicode_symbols_section': content.count('create_unicode_symbols_section'),
            'create_integrals_section': content.count('create_integrals_section'),
            'create_advanced_section': content.count('create_advanced_section'),
            'create_greek_section': content.count('create_greek_section'),
            'create_fractions_section': content.count('create_fractions_section')
        }
        
        for section, count in sections_count.items():
            if 'create_' in section and '(' not in section:
                print(f"  {section}: {count} {'llamada(s)' if 'self.' in content else ''}")
        
        print()
        print("VERIFICACIÓN DE SÍMBOLOS DE INTEGRAL:")
        print("-" * 50)
        
        # Contar símbolos de integral en diferentes secciones
        integral_symbols = {
            "Símbolos Unicode": content.count("('', 'integral(')"),
            "Sección avanzada": content.count("'integral('") - content.count("('', 'integral(')"),
            "Total": content.count("'integral(')")
        }
        
        for location, count in integral_symbols.items():
            print(f"  {location}: {count} símbolo(s)")
        
        print()
        print("ESTADO FINAL:")
        print("-" * 50)
        
        # Verificar el estado final
        if "self.create_integrals_section(keypad_frame)" not in content:
            print("  Sección duplicada eliminada: OK")
        else:
            print("  Sección duplicada eliminada: ERROR")
        
        if "('', 'integral(')" in content:
            print("  Símbolo de integral agregado a Símbolos Unicode: OK")
        else:
            print("  Símbolo de integral agregado a Símbolos Unicode: ERROR")
        
        if "elif symbol == 'integral(':" in content:
            print("  Manejo del símbolo actualizado: OK")
        else:
            print("  Manejo del símbolo actualizado: ERROR")
        
        print()
        print("=== CONCLUSIÓN ===")
        
        # Evaluar el éxito general
        success_criteria = [
            "self.create_integrals_section(keypad_frame)" not in content,
            "('', 'integral(')" in content,
            "elif symbol == 'integral(':" in content
        ]
        
        success_count = sum(success_criteria)
        total_criteria = len(success_criteria)
        
        if success_count == total_criteria:
            print("Todos los cambios aplicados exitosamente:")
            print("  - Símbolo de integral agregado a Símbolos Unicode")
            print("  - Sección duplicada de Integrales eliminada")
            print("  - Manejo de símbolo actualizado")
            return True
        else:
            print(f"Cambios parciales: {success_count}/{total_criteria} completados")
            return False
            
    except ImportError as e:
        print(f"Error importando scientific_keypad: {e}")
        return False
    except Exception as e:
        print(f"Error en la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_integral_section_changes()
    
    if success:
        print("\n¡Prueba de cambios en secciones completada exitosamente!")
        print("El símbolo de integral ahora está en Símbolos Unicode y la sección duplicada fue eliminada.")
    else:
        print("\nLa prueba detectó problemas. Revisa los cambios realizados.")

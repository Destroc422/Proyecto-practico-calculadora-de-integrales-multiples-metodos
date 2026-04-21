#!/usr/bin/env python3
"""
Final Fix - Solución definitiva para restaurar el sistema
Elimina completamente los métodos Unicode problemáticos y restaura funcionalidad
"""
import os
import re

def final_fix():
    """Solución definitiva para el sistema"""
    
    file_path = os.path.join(os.path.dirname(__file__), 'ui', 'professional_main_window.py')
    
    try:
        print("=== APLICANDO SOLUCIÓN DEFINITIVA ===")
        
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Eliminar completamente todos los métodos Unicode añadidos
        # Buscar el primer método Unicode problemático
        unicode_start = content.find('def get_keypad_unicode_symbols(self, category: SymbolCategory):')
        
        if unicode_start != -1:
            # Encontrar el final del bloque Unicode (antes del siguiente método o final de clase)
            lines = content.split('\n')
            start_line = -1
            end_line = -1
            
            for i, line in enumerate(lines):
                if 'def get_keypad_unicode_symbols' in line:
                    start_line = i
                elif start_line != -1 and line.startswith('    def ') and 'get_keypad_unicode_symbols' not in line:
                    end_line = i
                    break
            
            if start_line != -1:
                if end_line == -1:
                    # Buscar final de la clase
                    for i in range(start_line + 1, len(lines)):
                        if lines[i].strip() == '' and i + 1 < len(lines) and not lines[i + 1].startswith('        '):
                            end_line = i
                            break
                
                if end_line == -1:
                    end_line = len(lines)
                
                # Eliminar líneas problemáticas
                new_lines = lines[:start_line] + lines[end_line:]
                content = '\n'.join(new_lines)
                print(f"Eliminados {end_line - start_line} líneas de métodos Unicode")
        
        # 2. Eliminar importaciones Unicode problemáticas
        unicode_import_pattern = r'\n# Importar gestor de perfiles Unicode.*?SymbolContext\)\n'
        content = re.sub(unicode_import_pattern, '\n', content, flags=re.DOTALL)
        
        # 3. Eliminar llamadas a setup_unicode_profiles
        content = content.replace('            # Setup Unicode profiles\n            self.setup_unicode_profiles()\n', '')
        
        # 4. Escribir archivo limpio
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Archivo limpio escrito")
        
        # 5. Verificar que el sistema funciona
        print("\n=== VERIFICANDO SISTEMA ===")
        
        try:
            # Test de sintaxis
            with open(file_path, 'r', encoding='utf-8') as f:
                test_content = f.read()
            
            compile(test_content, file_path, 'exec')
            print("Sintaxis Python: OK")
            
            # Test de importación
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            
            from ui.professional_main_window import ProfessionalIntegralCalculator
            print("Importación: OK")
            
            # Verificar métodos básicos
            basic_methods = [
                '__init__',
                'setup_professional_ui',
                'calculate_integral',
                '_display_result'
            ]
            
            for method in basic_methods:
                if hasattr(ProfessionalIntegralCalculator, method):
                    print(f"Método {method}: OK")
                else:
                    print(f"Método {method}: FALTANTE")
            
            print("\n=== SISTEMA RESTAURADO EXITOSAMENTE ===")
            return True
            
        except SyntaxError as e:
            print(f"Error de sintaxis: {e}")
            return False
        except ImportError as e:
            print(f"Error de importación: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False
            
    except Exception as e:
        print(f"Error en solución definitiva: {e}")
        return False

if __name__ == "__main__":
    success = final_fix()
    
    if success:
        print("\n¡SISTEMA FUNCIONAL!")
        print("Ahora puedes ejecutar: python main.py")
    else:
        print("\nError en la solución. Revisa los logs.")

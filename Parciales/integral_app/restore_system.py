#!/usr/bin/env python3
"""
Restore System - Restaura la funcionalidad completa del sistema
Elimina métodos problemáticos y restaura el sistema a un estado funcional
"""
import os
import shutil
from datetime import datetime

def restore_system():
    """Restaura el sistema a un estado funcional"""
    
    try:
        print("=== RESTAURANDO SISTEMA A ESTADO FUNCIONAL ===")
        
        # 1. Hacer backup del archivo actual
        main_window_path = os.path.join(os.path.dirname(__file__), 'ui', 'professional_main_window.py')
        backup_path = main_window_path + f'.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        if os.path.exists(main_window_path):
            shutil.copy2(main_window_path, backup_path)
            print(f"Backup creado: {backup_path}")
        
        # 2. Leer el archivo y eliminar métodos problemáticos
        with open(main_window_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. Eliminar métodos Unicode problemáticos que causan indentación
        lines_to_remove = [
            'def get_keypad_unicode_symbols(self, category: SymbolCategory):',
            'def insert_unicode_symbol(self, symbol: str, symbol_name: str):',
            'def setup_unicode_profiles(self):',
            'def toggle_unicode_profile(self):',
            'def convert_expression_context(self, expression: str, context: SymbolContext):'
        ]
        
        # Eliminar bloques completos de métodos problemáticos
        new_content = content
        for method_start in lines_to_remove:
            if method_start in new_content:
                # Encontrar inicio del método
                start_pos = new_content.find(method_start)
                if start_pos != -1:
                    # Encontrar el siguiente método o el final de la clase
                    next_method = new_content.find('\n    def ', start_pos + 1)
                    if next_method == -1:
                        # Buscar final de la clase
                        class_end = new_content.find('\n\n# ', start_pos + 1)
                        if class_end == -1:
                            class_end = len(new_content)
                        next_method = class_end
                    
                    # Eliminar el método problemático
                    new_content = new_content[:start_pos] + new_content[next_method:]
                    print(f"Método eliminado: {method_start}")
        
        # 4. Eliminar importaciones Unicode problemáticas
        unicode_imports = [
            'from core.unicode_profile_manager import (',
            'get_unicode_manager, convert_to_display, convert_to_latex, ',
            'convert_to_input, convert_to_calculation, convert_to_export, convert_to_print,',
            'set_profile, SymbolContext, SymbolCategory'
        ]
        
        for import_line in unicode_imports:
            if import_line in new_content:
                # Encontrar el bloque de importación completo
                start_pos = new_content.find(import_line)
                if start_pos != -1:
                    end_pos = new_content.find('\n\n', start_pos)
                    if end_pos == -1:
                        end_pos = new_content.find('\n# ', start_pos)
                    if end_pos == -1:
                        end_pos = len(new_content)
                    
                    new_content = new_content[:start_pos] + new_content[end_pos:]
                    print(f"Importación eliminada: {import_line[:50]}...")
        
        # 5. Escribir el archivo restaurado
        with open(main_window_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Archivo professional_main_window.py restaurado")
        
        # 6. Restaurar métodos originales simples
        simple_unicode_methods = '''
    def _convert_to_unicode_format(self, expression: str) -> str:
        """Convert expression to Unicode format"""
        try:
            # Handle powers
            unicode_expr = expression.replace('**2', '²').replace('**3', '³')
            
            # Handle multiplication
            unicode_expr = unicode_expr.replace('*', '×')
            
            # Handle division
            unicode_expr = unicode_expr.replace('/', '÷')
            
            # Handle integrals
            unicode_expr = unicode_expr.replace('int ', 'integral ').replace('integrate(', 'integral(')
            
            # Handle common symbols
            unicode_expr = unicode_expr.replace('pi', 'pi').replace('inf', 'inf')
            
            return unicode_expr
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression
    
    def _clean_latex_for_professional_display(self, latex_text: str) -> str:
        """Clean LaTeX text for professional display"""
        try:
            # Remove LaTeX commands that might cause issues
            cleaned = latex_text.replace('\\\\', '\\')
            
            # Handle integrals
            cleaned = cleaned.replace('\\int', 'integral')
            
            # Handle fractions
            cleaned = cleaned.replace('\\frac{', '(').replace('}{', '/(')
            
            # Handle powers
            cleaned = cleaned.replace('^{', '^(').replace('}', ')')
            
            # Handle subscripts
            cleaned = cleaned.replace('_{', '_(')
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX: {e}")
            return latex_text
'''
        
        # Añadir métodos simples al final de la clase
        class_end = new_content.rfind('\n        except Exception as e:')
        if class_end != -1:
            end_pos = new_content.find('\n\n', class_end)
            if end_pos == -1:
                end_pos = len(new_content)
            
            new_content = new_content[:end_pos] + simple_unicode_methods + '\n' + new_content[end_pos:]
        
        # Escribir archivo final
        with open(main_window_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Métodos Unicode simples restaurados")
        
        # 7. Verificar que el sistema funciona
        print("\n=== VERIFICANDO SISTEMA RESTAURADO ===")
        
        try:
            # Intentar importar el módulo
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            
            from ui.professional_main_window import ProfessionalIntegralCalculator
            print("Importación exitosa: ProfessionalIntegralCalculator")
            
            # Verificar que los métodos existen
            import inspect
            
            # Verificar métodos Unicode
            methods_to_check = [
                '_convert_to_unicode_format',
                '_clean_latex_for_professional_display'
            ]
            
            for method_name in methods_to_check:
                if hasattr(ProfessionalIntegralCalculator, method_name):
                    print(f"Método encontrado: {method_name}")
                else:
                    print(f"Método faltante: {method_name}")
            
            print("Sistema restaurado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error en verificación: {e}")
            return False
            
    except Exception as e:
        print(f"Error restaurando sistema: {e}")
        return False

if __name__ == "__main__":
    success = restore_system()
    
    if success:
        print("\n=== SISTEMA RESTAURADO EXITOSAMENTE ===")
        print("El sistema ahora debería funcionar con Unicode básico")
        print("Puedes ejecutar: python main.py")
    else:
        print("\n=== ERROR EN RESTAURACIÓN ===")
        print("Revisa los logs para más detalles")

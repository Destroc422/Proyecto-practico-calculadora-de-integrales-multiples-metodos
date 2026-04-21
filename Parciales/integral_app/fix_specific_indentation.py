#!/usr/bin/env python3
"""
Fix Specific Indentation - Corrige el problema específico de indentación
"""
import os

def fix_specific_indentation():
    """Corrige el problema específico de indentación en la línea 211"""
    
    file_path = os.path.join(os.path.dirname(__file__), 'ui', 'professional_main_window.py')
    
    try:
        # Leer archivo línea por línea
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Buscar y corregir la línea 211 (índice 210)
        for i, line in enumerate(lines):
            if i == 210:  # Línea 211 (índice 210)
                if 'def get_keypad_unicode_symbols' in line:
                    # Reemplazar la línea con indentación correcta (4 espacios)
                    lines[i] = '    def get_keypad_unicode_symbols(self, category: SymbolCategory):\n'
                    print(f"Línea {i+1} corregida: {repr(lines[i])}")
                    break
        
        # Escribir archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("Indentación específica corregida exitosamente")
        return True
        
    except Exception as e:
        print(f"Error corrigiendo indentación específica: {e}")
        return False

if __name__ == "__main__":
    fix_specific_indentation()

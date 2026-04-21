#!/usr/bin/env python3
"""
Fix Indentation - Corrige problemas de indentación en professional_main_window.py
"""
import os
import re

def fix_indentation():
    """Corrige la indentación del archivo professional_main_window.py"""
    
    file_path = os.path.join(os.path.dirname(__file__), 'ui', 'professional_main_window.py')
    
    try:
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar y corregir el problema específico
        # El problema es que el método get_keypad_unicode_symbols está fuera de la clase
        
        # Patrón para encontrar el método fuera de lugar
        pattern = r'(raise\s+\n\s+)(\s+)(def get_keypad_unicode_symbols)'
        
        # Reemplazar con indentación correcta
        replacement = r'\1    \3'
        
        new_content = re.sub(pattern, replacement, content)
        
        # Si no se encontró el patrón, intentar otro enfoque
        if new_content == content:
            # Buscar líneas específicas alrededor del problema
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if 'def get_keypad_unicode_symbols' in line and not line.startswith('    '):
                    # Corregir indentación
                    lines[i] = '    ' + line.strip()
                    break
            
            new_content = '\n'.join(lines)
        
        # Escribir archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Indentación corregida exitosamente")
        return True
        
    except Exception as e:
        print(f"Error corrigiendo indentación: {e}")
        return False

if __name__ == "__main__":
    fix_indentation()

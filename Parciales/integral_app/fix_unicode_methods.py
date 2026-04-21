#!/usr/bin/env python3
"""
Fix Unicode Methods - Corrige y completa los métodos Unicode en todos los componentes
"""
import os
import re

def fix_unicode_methods():
    """Corrige y completa los métodos Unicode"""
    
    try:
        print("=== CORRIGIENDO MÉTODOS UNICODE ===")
        
        # 1. Corregir Microsoft Math Engine
        engine_path = os.path.join(os.path.dirname(__file__), 'core', 'microsoft_math_engine.py')
        
        with open(engine_path, 'r', encoding='utf-8') as f:
            engine_content = f.read()
        
        # Verificar si el método _convert_to_unicode existe
        if '_convert_to_unicode' not in engine_content:
            # Añadir el método faltante
            unicode_method = '''
    def _convert_to_unicode(self, expression: str) -> str:
        """Convert expression to Unicode format with professional pulcritud"""
        try:
            from core.professional_unicode_methods import apply_professional_style
            return apply_professional_style(expression)
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression
'''
            
            # Insertar antes del último método
            last_method_pos = engine_content.rfind('def ')
            if last_method_pos != -1:
                engine_content = engine_content[:last_method_pos] + unicode_method + '\n' + engine_content[last_method_pos:]
            
            with open(engine_path, 'w', encoding='utf-8') as f:
                f.write(engine_content)
            
            print("Método _convert_to_unicode añadido a Microsoft Math Engine")
        
        # 2. Verificar y corregir LaTeX renderer
        renderer_path = os.path.join(os.path.dirname(__file__), 'ui', 'latex_renderer.py')
        
        with open(renderer_path, 'r', encoding='utf-8') as f:
            renderer_content = f.read()
        
        # Verificar si el método _convert_to_unicode_format existe
        if '_convert_to_unicode_format' not in renderer_content:
            # Añadir el método faltante
            unicode_method = '''
    def _convert_to_unicode_format(self, expression: str) -> str:
        """Convert expression to Unicode format with professional pulcritud"""
        try:
            from core.professional_unicode_methods import apply_professional_style
            return apply_professional_style(expression)
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression
'''
            
            # Insertar antes del último método
            last_method_pos = renderer_content.rfind('def ')
            if last_method_pos != -1:
                renderer_content = renderer_content[:last_method_pos] + unicode_method + '\n' + renderer_content[last_method_pos:]
            
            with open(renderer_path, 'w', encoding='utf-8') as f:
                f.write(renderer_content)
            
            print("Método _convert_to_unicode_format añadido a LaTeX renderer")
        
        # 3. Verificar Enhanced LaTeX renderer
        enhanced_path = os.path.join(os.path.dirname(__file__), 'core', 'enhanced_latex_renderer.py')
        
        if os.path.exists(enhanced_path):
            with open(enhanced_path, 'r', encoding='utf-8') as f:
                enhanced_content = f.read()
            
            # Verificar si el método _convert_to_unicode_enhanced existe
            if '_convert_to_unicode_enhanced' not in enhanced_content:
                # Añadir el método faltante
                unicode_method = '''
    def _convert_to_unicode_enhanced(self, expression: str) -> str:
        """Enhanced Unicode conversion with professional pulcritud"""
        try:
            from core.professional_unicode_methods import apply_elegant_style
            return apply_elegant_style(expression)
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression
'''
                
                # Insertar antes del último método
                last_method_pos = enhanced_content.rfind('def ')
                if last_method_pos != -1:
                    enhanced_content = enhanced_content[:last_method_pos] + unicode_method + '\n' + enhanced_content[last_method_pos:]
                
                with open(enhanced_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_content)
                
                print("Método _convert_to_unicode_enhanced añadido a Enhanced LaTeX renderer")
        
        print("Métodos Unicode corregidos y completados")
        return True
        
    except Exception as e:
        print(f"Error corrigiendo métodos Unicode: {e}")
        return False

if __name__ == "__main__":
    fix_unicode_methods()

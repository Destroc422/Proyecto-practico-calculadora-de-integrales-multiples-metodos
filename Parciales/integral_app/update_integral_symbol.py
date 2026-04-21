#!/usr/bin/env python3
"""
Update Integral Symbol - Actualiza todo el sistema para usar símbolo Unicode real de integral
Reemplaza 'integrate' y 'integral' por el símbolo Unicode real: integral
"""
import os
import re

def update_integral_symbol_system():
    """Actualiza todo el sistema para usar símbolo Unicode real de integral"""
    
    try:
        print("=== ACTUALIZANDO SÍMBOLO DE INTEGRAL UNICODE REAL ===")
        
        # 1. Actualizar professional_unicode_methods.py
        print("1. Actualizando professional_unicode_methods.py...")
        
        methods_path = os.path.join(os.path.dirname(__file__), 'core', 'professional_unicode_methods.py')
        
        with open(methods_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar 'integral(' por 'integral(' con símbolo Unicode real
        content = content.replace("replacement='integral('", "replacement='integral('")
        
        # Añadir método específico para símbolo Unicode real
        unicode_integral_method = '''
        # Símbolo real de integral Unicode
        self.methods['integral_unicode_symbol'] = UnicodeMethod(
            name='integral_unicode_symbol',
            pattern=r'\\bintegral\\s*\\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Integral con símbolo Unicode real',
            category='integrals'
        )
        
        # Reemplazar integrate por símbolo Unicode real
        self.methods['integrate_to_unicode'] = UnicodeMethod(
            name='integrate_to_unicode',
            pattern=r'\\bintegrate\\s*\\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Convertir integrate a símbolo Unicode real',
            category='integrals'
        )
'''
        
        # Insertar después de los métodos existentes
        insert_pos = content.find('# Potencias - Estilo Profesional')
        if insert_pos != -1:
            content = content[:insert_pos] + unicode_integral_method + content[insert_pos:]
        
        with open(methods_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   professional_unicode_methods.py actualizado")
        
        # 2. Actualizar unicode_profile_manager.py
        print("2. Actualizando unicode_profile_manager.py...")
        
        profile_path = os.path.join(os.path.dirname(__file__), 'core', 'unicode_profile_manager.py')
        
        with open(profile_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Actualizar mapeo de integrales para usar símbolo Unicode real
        content = content.replace("'integrate': 'integral'", "'integrate': 'integral'")
        content = content.replace("'integral': 'integral'", "'integral': 'integral'")
        
        # Añadir mapeo específico para símbolo Unicode real
        if "'integral': 'integral'" not in content:
            # Buscar la sección de mapeos de integrales
            integral_section = '''
        # Integrales con símbolo Unicode real
        'integrate': 'integral',
        'integral': 'integral',
'''
            
            # Insertar en la sección de mapeos
            mappings_pos = content.find("# Integrales")
            if mappings_pos != -1:
                end_pos = content.find('\n\n', mappings_pos)
                if end_pos == -1:
                    end_pos = content.find('\n    #', mappings_pos)
                if end_pos == -1:
                    end_pos = len(content)
                
                content = content[:mappings_pos] + integral_section + content[end_pos:]
        
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   unicode_profile_manager.py actualizado")
        
        # 3. Actualizar microsoft_math_engine.py
        print("3. Actualizando microsoft_math_engine.py...")
        
        engine_path = os.path.join(os.path.dirname(__file__), 'core', 'microsoft_math_engine.py')
        
        with open(engine_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Actualizar método _convert_to_unicode
        if '_convert_to_unicode' in content:
            # Reemplazar conversiones de integrales
            content = content.replace('unicode_expr = unicode_expr.replace(\'int \', \'integral \').replace(\'integrate(\', \'integral(\')', 
                                      'unicode_expr = unicode_expr.replace(\'int \', \'integral \').replace(\'integrate(\', \'integral(\').replace(\'integral(\', \'integral(\')')
        
        with open(engine_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   microsoft_math_engine.py actualizado")
        
        # 4. Actualizar latex_renderer.py
        print("4. Actualizando latex_renderer.py...")
        
        renderer_path = os.path.join(os.path.dirname(__file__), 'ui', 'latex_renderer.py')
        
        with open(renderer_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Actualizar método _convert_to_unicode_format
        if '_convert_to_unicode_format' in content:
            content = content.replace('unicode_expr = unicode_expr.replace(\'int \', \'integral \').replace(\'integrate(\', \'integral(\')', 
                                      'unicode_expr = unicode_expr.replace(\'int \', \'integral \').replace(\'integrate(\', \'integral(\').replace(\'integral(\', \'integral(\')')
        
        with open(renderer_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   latex_renderer.py actualizado")
        
        # 5. Actualizar enhanced_latex_renderer.py
        print("5. Actualizando enhanced_latex_renderer.py...")
        
        enhanced_path = os.path.join(os.path.dirname(__file__), 'core', 'enhanced_latex_renderer.py')
        
        if os.path.exists(enhanced_path):
            with open(enhanced_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Actualizar método _convert_to_unicode_enhanced
            if '_convert_to_unicode_enhanced' in content:
                content = content.replace('unicode_expr = unicode_expr.replace(\'integrate(\', \'integral(\').replace(\'int \', \'integral \')', 
                                          'unicode_expr = unicode_expr.replace(\'integrate(\', \'integral(\').replace(\'int \', \'integral \').replace(\'integral(\', \'integral(\')')
            
            with open(enhanced_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   enhanced_latex_renderer.py actualizado")
        
        # 6. Crear nuevo método de conversión para símbolo Unicode real
        print("6. Creando nueva función para símbolo Unicode real...")
        
        # Añadir función de conveniencia
        unicode_function = '''
# Función para convertir a símbolo Unicode real de integral
def apply_integral_unicode_symbol(expression: str) -> str:
    """Aplica símbolo Unicode real de integral a expresiones"""
    unicode_methods = get_professional_unicode()
    
    # Reemplazar 'integrate(' y 'integral(' por 'integral('
    expression = expression.replace('integrate(', 'integral(')
    expression = expression.replace('integral(', 'integral(')
    
    return expression
'''
        
        # Añadir al final de professional_unicode_methods.py
        with open(methods_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'apply_integral_unicode_symbol' not in content:
            content += unicode_function
        
        with open(methods_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   Función apply_integral_unicode_symbol creada")
        
        print("\n=== ACTUALIZACIÓN COMPLETADA ===")
        print("El sistema ahora usa el símbolo Unicode real de integral: integral")
        print("Todos los componentes han sido actualizados para mostrar el símbolo correcto.")
        
        return True
        
    except Exception as e:
        print(f"Error actualizando símbolo de integral: {e}")
        return False

if __name__ == "__main__":
    success = update_integral_symbol_system()
    
    if success:
        print("\n¡Símbolo de integral Unicode actualizado exitosamente!")
        print("Ahora 'integrate' se mostrará como 'integral' en toda la aplicación.")
    else:
        print("\nError en la actualización. Revisa los logs para más detalles.")

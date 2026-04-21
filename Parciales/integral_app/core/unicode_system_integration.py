#!/usr/bin/env python3
"""
Unicode System Integration - Integración del gestor de perfiles Unicode
Integra el sistema de perfiles Unicode en todos los componentes del sistema
"""
import sys
import os
import logging
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar directorios al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicode_profile_manager import (
    UnicodeProfileManager, SymbolContext, SymbolCategory,
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, convert_to_export, convert_to_print,
    set_profile, get_symbol_info, get_symbols_by_category
)


class UnicodeSystemIntegration:
    """Integración del sistema Unicode en todos los componentes"""
    
    def __init__(self):
        self.unicode_manager = get_unicode_manager()
        self.integration_log = []
        
    def integrate_latex_renderer(self):
        """Integrar perfiles Unicode en el renderizador LaTeX"""
        try:
            logger.info("Integrando perfiles Unicode en LaTeX renderer")
            
            # Ruta del archivo LaTeX renderer
            renderer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        'ui', 'latex_renderer.py')
            
            # Leer archivo actual
            with open(renderer_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación del gestor Unicode
            import_code = '''
# Importar gestor de perfiles Unicode
from core.unicode_profile_manager import (
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, set_profile,
    SymbolContext
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode_format
            old_method = '''    def _convert_to_unicode_format(self, expression: str) -> str:
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
            return expression'''
            
            new_method = '''    def _convert_to_unicode_format(self, expression: str) -> str:
        """Convert expression to Unicode format using profile manager"""
        try:
            unicode_manager = get_unicode_manager()
            
            # Establecer perfil para visualización
            set_profile('display')
            
            # Convertir usando el gestor de perfiles
            return convert_to_display(expression)
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode_format actualizado")
            
            # Reemplazar método _clean_latex_for_professional_display
            old_clean_method = '''    def _clean_latex_for_professional_display(self, latex_text: str) -> str:
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
            return latex_text'''
            
            new_clean_method = '''    def _clean_latex_for_professional_display(self, latex_text: str) -> str:
        """Clean LaTeX text for professional display using profile manager"""
        try:
            unicode_manager = get_unicode_manager()
            
            # Establecer perfil para visualización
            set_profile('display')
            
            # Convertir LaTeX a visualización
            return convert_to_display(latex_text)
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX: {e}")
            return latex_text'''
            
            if old_clean_method in content:
                content = content.replace(old_clean_method, new_clean_method)
                logger.info("Método _clean_latex_for_professional_display actualizado")
            
            # Escribir archivo modificado
            with open(renderer_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("LaTeX renderer integrado con perfiles Unicode")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando LaTeX renderer: {e}")
            return False
    
    def integrate_microsoft_math_engine(self):
        """Integrar perfiles Unicode en el motor matemático"""
        try:
            logger.info("Integrando perfiles Unicode en Microsoft Math Engine")
            
            # Ruta del archivo
            engine_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'core', 'microsoft_math_engine.py')
            
            # Leer archivo actual
            with open(engine_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación del gestor Unicode
            import_code = '''
# Importar gestor de perfiles Unicode
from core.unicode_profile_manager import (
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, set_profile,
    SymbolContext
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode
            old_method = '''    def _convert_to_unicode(self, expression: str) -> str:
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
            return expression'''
            
            new_method = '''    def _convert_to_unicode(self, expression: str) -> str:
        """Convert expression to Unicode format using profile manager"""
        try:
            unicode_manager = get_unicode_manager()
            
            # Establecer perfil para visualización
            set_profile('display')
            
            # Convertir usando el gestor de perfiles
            return convert_to_display(expression)
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode actualizado")
            
            # Escribir archivo modificado
            with open(engine_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Microsoft Math Engine integrado con perfiles Unicode")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Microsoft Math Engine: {e}")
            return False
    
    def integrate_professional_main_window(self):
        """Integrar perfiles Unicode en la ventana principal"""
        try:
            logger.info("Integrando perfiles Unicode en Professional Main Window")
            
            # Ruta del archivo
            window_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(window_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación del gestor Unicode
            import_code = '''
# Importar gestor de perfiles Unicode
from core.unicode_profile_manager import (
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, convert_to_export, convert_to_print,
    set_profile, SymbolContext, SymbolCategory
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Añadir método para gestión de perfiles Unicode
            unicode_management_method = '''
    def setup_unicode_profiles(self):
        """Setup Unicode profile management"""
        try:
            self.unicode_manager = get_unicode_manager()
            
            # Establecer perfil inicial según el contexto
            set_profile('display')
            
            # Añadir atajos de teclado para cambiar perfiles
            self.root.bind('<Control-Alt-U>', lambda e: self.toggle_unicode_profile())
            self.root.bind('<Control-Alt-D>', lambda e: set_profile('display'))
            self.root.bind('<Control-Alt-L>', lambda e: set_profile('latex'))
            self.root.bind('<Control-Alt-I>', lambda e: set_profile('input'))
            
            logger.info("Unicode profiles setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up Unicode profiles: {e}")
    
    def toggle_unicode_profile(self):
        """Toggle between Unicode profiles"""
        try:
            current_profile = self.unicode_manager.get_active_profile()
            if current_profile:
                profiles = list(self.unicode_manager.profiles.keys())
                current_index = profiles.index(current_profile.name)
                next_index = (current_index + 1) % len(profiles)
                next_profile = profiles[next_index]
                
                set_profile(next_profile)
                self.update_status(f"Perfil Unicode: {next_profile}", "#3498db")
                
                # Actualizar visualización actual si hay resultado
                if hasattr(self, 'current_result') and self.current_result:
                    self._display_result(self.current_result)
                
        except Exception as e:
            logger.error(f"Error toggling Unicode profile: {e}")
    
    def convert_expression_context(self, expression: str, context: SymbolContext) -> str:
        """Convert expression using Unicode profiles"""
        try:
            return self.unicode_manager.convert_expression(expression, context)
        except Exception as e:
            logger.error(f"Error converting expression: {e}")
            return expression
    
    def get_unicode_symbols_for_category(self, category: SymbolCategory):
        """Get Unicode symbols for a specific category"""
        try:
            return self.unicode_manager.get_symbols_by_category(category)
        except Exception as e:
            logger.error(f"Error getting symbols for category: {e}")
            return []
'''
            
            # Insertar método después del __init__
            init_end = content.find('def setup_professional_ui(self):')
            if init_end != -1:
                content = content[:init_end] + unicode_management_method + '\n' + content[init_end:]
            
            # Modificar método _display_result para usar perfiles Unicode
            display_method_pattern = r'(def _display_result\(self, result: Dict\[str, Any\]):.*?logger\.info\("Resultados mostrados correctamente"\))'
            
            # Buscar el método y añadir llamada a setup_unicode_profiles
            setup_call = '''
            # Setup Unicode profiles
            self.setup_unicode_profiles()'''
            
            # Buscar el final del método __init__
            init_end = content.find('def setup_professional_ui(self):')
            if init_end != -1:
                # Encontrar el final del bloque try anterior
                try_end = content.rfind('raise', 0, init_end)
                if try_end != -1:
                    line_end = content.find('\n', try_end)
                    if line_end != -1:
                        content = content[:line_end] + setup_call + '\n' + content[line_end:]
            
            # Escribir archivo modificado
            with open(window_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Professional Main Window integrado con perfiles Unicode")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Professional Main Window: {e}")
            return False
    
    def integrate_enhanced_latex_renderer(self):
        """Integrar perfiles Unicode en el renderizador LaTeX mejorado"""
        try:
            logger.info("Integrando perfiles Unicode en Enhanced LaTeX Renderer")
            
            # Ruta del archivo
            renderer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        'core', 'enhanced_latex_renderer.py')
            
            # Leer archivo actual
            with open(renderer_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación del gestor Unicode
            import_code = '''
# Importar gestor de perfiles Unicode
from core.unicode_profile_manager import (
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, set_profile,
    SymbolContext
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode_enhanced
            old_method = '''    def _convert_to_unicode_enhanced(self, expression: str) -> str:
        """Enhanced Unicode conversion with comprehensive symbol support"""
        try:
            unicode_expr = expression
            
            # Powers and superscripts
            unicode_expr = unicode_expr.replace('**2', '²').replace('**3', '³').replace('**n', '**n')
            
            # Multiplication and division
            unicode_expr = unicode_expr.replace('*', '×').replace('/', '÷')
            
            # Integrals
            unicode_expr = unicode_expr.replace('integrate(', 'integral(').replace('int ', 'integral ')
            unicode_expr = unicode_expr.replace('integrate', 'integral')
            
            # Common mathematical symbols
            unicode_expr = unicode_expr.replace('pi', 'pi').replace('inf', 'inf')
            unicode_expr = unicode_expr.replace('sqrt(', 'sqrt(')
            
            # Trigonometric functions
            unicode_expr = unicode_expr.replace('sin(', 'sin(').replace('cos(', 'cos(').replace('tan(', 'tan(')
            
            # Logarithmic functions
            unicode_expr = unicode_expr.replace('ln(', 'ln(').replace('log(', 'log(')
            
            # Exponential functions
            unicode_expr = unicode_expr.replace('exp(', 'exp(')
            
            # Common fractions
            unicode_expr = unicode_expr.replace('1/2', '½').replace('1/3', '1/3').replace('2/3', '2/3')
            unicode_expr = unicode_expr.replace('1/4', '¼').replace('3/4', '¾')
            
            return unicode_expr
            
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression'''
            
            new_method = '''    def _convert_to_unicode_enhanced(self, expression: str) -> str:
        """Enhanced Unicode conversion using profile manager"""
        try:
            unicode_manager = get_unicode_manager()
            
            # Establecer perfil para visualización
            set_profile('display')
            
            # Convertir usando el gestor de perfiles
            return convert_to_display(expression)
            
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode_enhanced actualizado")
            
            # Escribir archivo modificado
            with open(renderer_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Enhanced LaTeX Renderer integrado con perfiles Unicode")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Enhanced LaTeX Renderer: {e}")
            return False
    
    def integrate_keypad_system(self):
        """Integrar perfiles Unicode en el sistema de teclado"""
        try:
            logger.info("Integrando perfiles Unicode en sistema de teclado")
            
            # Ruta del archivo
            keypad_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(keypad_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Modificar método create_enhanced_algebra_tab para usar perfiles Unicode
            algebra_tab_pattern = r'(def create_enhanced_algebra_tab\(self\):.*?logger\.error\(f"Error creating enhanced algebra tab: \{str\(e\)\}")'
            
            # Añadir método para obtener símbolos Unicode del teclado
            keypad_symbols_method = '''
    def get_keypad_unicode_symbols(self, category: SymbolCategory):
        """Get Unicode symbols for keypad from profile manager"""
        try:
            symbols = get_symbols_by_category(category)
            return [(s.unicode, s.name) for s in symbols if s.unicode]
        except Exception as e:
            logger.error(f"Error getting keypad symbols: {e}")
            return []
    
    def insert_unicode_symbol(self, symbol: str, symbol_name: str):
        """Insert Unicode symbol into input field"""
        try:
            if hasattr(self, 'input_field'):
                current_text = self.input_field.get()
                cursor_pos = self.input_field.index(tk.INSERT)
                
                # Insertar símbolo
                new_text = current_text[:cursor_pos] + symbol + current_text[cursor_pos:]
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, new_text)
                
                # Mover cursor después del símbolo
                self.input_field.icursor(cursor_pos + len(symbol))
                
                # Actualizar estado
                self.update_status(f"Símbolo insertado: {symbol_name} ({symbol})", "#27ae60")
                
        except Exception as e:
            logger.error(f"Error inserting Unicode symbol: {e}")
'''
            
            # Insertar método después de setup_professional_ui
            setup_end = content.find('def create_professional_toolbar(self):')
            if setup_end != -1:
                content = content[:setup_end] + keypad_symbols_method + '\n' + content[setup_end:]
            
            # Escribir archivo modificado
            with open(keypad_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Sistema de teclado integrado con perfiles Unicode")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando sistema de teclado: {e}")
            return False
    
    def integrate_all_components(self):
        """Integrar perfiles Unicode en todos los componentes"""
        logger.info("=== INICIANDO INTEGRACIÓN COMPLETA DE PERFILES UNICODE ===")
        
        integrations = [
            ("LaTeX Renderer", self.integrate_latex_renderer),
            ("Microsoft Math Engine", self.integrate_microsoft_math_engine),
            ("Professional Main Window", self.integrate_professional_main_window),
            ("Enhanced LaTeX Renderer", self.integrate_enhanced_latex_renderer),
            ("Keypad System", self.integrate_keypad_system)
        ]
        
        success_count = 0
        
        for name, integration_func in integrations:
            try:
                logger.info(f"Integrando: {name}")
                if integration_func():
                    success_count += 1
                    logger.info(f"  OK: {name}")
                else:
                    logger.warning(f"  ERROR: {name}")
            except Exception as e:
                logger.error(f"  EXCEPTION: {name} - {e}")
        
        logger.info(f"Integración completada: {success_count}/{len(integrations)} componentes")
        
        # Guardar log de integración
        self.save_integration_log()
        
        return success_count == len(integrations)
    
    def save_integration_log(self):
        """Guardar log de integración"""
        try:
            log_file = os.path.join(os.path.dirname(__file__), 'unicode_integration_log.json')
            
            import json
            from datetime import datetime
            
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'integrations': self.integration_log,
                'unicode_manager_stats': self.unicode_manager.get_statistics()
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Log de integración guardado")
            
        except Exception as e:
            logger.error(f"Error guardando log de integración: {e}")
    
    def test_integration(self):
        """Probar la integración de perfiles Unicode"""
        logger.info("=== PROBANDO INTEGRACIÓN DE PERFILES UNICODE ===")
        
        try:
            # Importar componentes modificados
            from ui.latex_renderer import ProfessionalLaTeXRenderer
            from core.microsoft_math_engine import MicrosoftMathEngine
            from core.enhanced_latex_renderer import EnhancedLaTeXRenderer
            
            # Expresiones de prueba
            test_expressions = [
                "integrate(x**2, x)",
                "x**2 + 2*x + 1 = (x+1)**2",
                "2/3*x**3 + 3/2*x**2 - x",
                "sin(x) + cos(x) = 1",
                "integral(x**2, x) + pi/2"
            ]
            
            # Probar conversiones
            for expr in test_expressions:
                logger.info(f"Probando expresión: {expr}")
                
                # Prueba de conversión a diferentes contextos
                display_result = convert_to_display(expr)
                latex_result = convert_to_latex(expr)
                input_result = convert_to_input(expr)
                calc_result = convert_to_calculation(expr)
                
                logger.info(f"  Display: {display_result}")
                logger.info(f"  LaTeX: {latex_result}")
                logger.info(f"  Input: {input_result}")
                logger.info(f"  Calculation: {calc_result}")
                logger.info("-" * 50)
            
            # Probar motor matemático
            engine = MicrosoftMathEngine()
            test_result = engine._convert_to_unicode("integrate(x**2, x)")
            logger.info(f"Motor matemático - Unicode: {test_result}")
            
            # Probar renderizador LaTeX
            renderer = ProfessionalLaTeXRenderer()
            test_result = renderer._convert_to_unicode_format("integrate(x**2, x)")
            logger.info(f"LaTeX renderer - Unicode: {test_result}")
            
            # Probar renderizador mejorado
            enhanced_renderer = EnhancedLaTeXRenderer()
            test_result = enhanced_renderer._convert_to_unicode_enhanced("integrate(x**2, x)")
            logger.info(f"Enhanced renderer - Unicode: {test_result}")
            
            logger.info("Pruebas de integración completadas exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en pruebas de integración: {e}")
            return False


def main():
    """Función principal"""
    try:
        print("=== Unicode System Integration ===")
        print("Integración del gestor de perfiles Unicode en todo el sistema")
        print()
        
        # Crear instancia de integración
        integration = UnicodeSystemIntegration()
        
        # Integrar todos los componentes
        success = integration.integrate_all_components()
        
        print()
        if success:
            print("Todos los componentes integrados exitosamente")
        else:
            print("Algunos componentes no pudieron integrarse")
        
        print()
        # Probar integración
        test_success = integration.test_integration()
        
        print()
        print("=== RESUMEN ===")
        print(f"Integración: {'Exitosa' if success else 'Parcial'}")
        print(f"Pruebas: {'Exitosas' if test_success else 'Fallidas'}")
        
        if success and test_success:
            print("El sistema de perfiles Unicode está completamente integrado y funcionando")
        else:
            print("Revisa los logs para detalles de los problemas")
        
        # Mostrar log de integración
        print()
        print("Log de integración:")
        for log_entry in integration.integration_log:
            print(f"  - {log_entry}")
        
        return success and test_success
        
    except Exception as e:
        print(f"Error en ejecución: {e}")
        return False


if __name__ == "__main__":
    main()

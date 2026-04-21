#!/usr/bin/env python3
"""
Unicode Pulcritud Integration - Integración de Pulcritud Unicode en Todas las Secciones
Implementa métodos Unicode profesionales con máxima pulcritud en toda la aplicación
"""
import sys
import os
import logging
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar directorios al path
sys.path.insert(0, os.path.dirname(__file__))

from professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)


class UnicodePulcritudIntegration:
    """Integración de pulcritud Unicode en todas las secciones"""
    
    def __init__(self):
        self.unicode_methods = get_professional_unicode()
        self.integration_log = []
        
        logger.info("Unicode Pulcritud Integration inicializado")
    
    def integrate_latex_renderer(self):
        """Integrar métodos Unicode profesionales en LaTeX renderer"""
        try:
            logger.info("Integrando pulcritud Unicode en LaTeX renderer")
            
            # Ruta del archivo LaTeX renderer
            renderer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        'ui', 'latex_renderer.py')
            
            # Leer archivo actual
            with open(renderer_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación de métodos Unicode profesionales
            import_code = '''
# Importar métodos Unicode profesionales para máxima pulcritud
from core.professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode_format con versión profesional
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
        """Convert expression to Unicode format with professional pulcritud"""
        try:
            unicode_methods = get_professional_unicode()
            
            # Aplicar estilo profesional para máxima pulcritud
            return apply_professional_style(expression)
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode_format actualizado con pulcritud profesional")
            
            # Escribir archivo modificado
            with open(renderer_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("LaTeX renderer con pulcritud Unicode profesional")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando LaTeX renderer: {e}")
            return False
    
    def integrate_microsoft_math_engine(self):
        """Integrar métodos Unicode profesionales en motor matemático"""
        try:
            logger.info("Integrando pulcritud Unicode en Microsoft Math Engine")
            
            # Ruta del archivo
            engine_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'core', 'microsoft_math_engine.py')
            
            # Leer archivo actual
            with open(engine_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación de métodos Unicode profesionales
            import_code = '''
# Importar métodos Unicode profesionales para máxima pulcritud
from core.professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode con versión profesional
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
        """Convert expression to Unicode format with professional pulcritud"""
        try:
            unicode_methods = get_professional_unicode()
            
            # Aplicar estilo profesional para máxima pulcritud
            return apply_professional_style(expression)
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode actualizado con pulcritud profesional")
            
            # Escribir archivo modificado
            with open(engine_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Microsoft Math Engine con pulcritud Unicode profesional")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Microsoft Math Engine: {e}")
            return False
    
    def integrate_professional_main_window(self):
        """Integrar métodos Unicode profesionales en ventana principal"""
        try:
            logger.info("Integrando pulcritud Unicode en Professional Main Window")
            
            # Ruta del archivo
            window_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(window_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación de métodos Unicode profesionales
            import_code = '''
# Importar métodos Unicode profesionales para máxima pulcritud
from core.professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Añadir métodos de pulcritud Unicode
            pulcritud_methods = '''
    def apply_unicode_pulcritud(self, expression: str, style: str = 'professional') -> str:
        """Aplica pulcritud Unicode profesional a expresiones"""
        try:
            unicode_methods = get_professional_unicode()
            
            if style == 'professional':
                return apply_professional_style(expression)
            elif style == 'elegant':
                return apply_elegant_style(expression)
            elif style == 'technical':
                return apply_technical_style(expression)
            elif style == 'academic':
                return apply_academic_style(expression)
            else:
                return apply_professional_style(expression)
                
        except Exception as e:
            logger.error(f"Error aplicando pulcritud Unicode: {e}")
            return expression
    
    def format_result_with_pulcritud(self, result: str) -> str:
        """Formatea resultado con pulcritud Unicode profesional"""
        return self.apply_unicode_pulcritud(result, 'professional')
    
    def format_steps_with_pulcritud(self, steps: list) -> list:
        """Formatea pasos con pulcritud Unicode elegante"""
        formatted_steps = []
        for step in steps:
            if isinstance(step, str):
                formatted_step = self.apply_unicode_pulcritud(step, 'elegant')
                formatted_steps.append(formatted_step)
            elif isinstance(step, dict) and 'expression' in step:
                step['expression'] = self.apply_unicode_pulcritud(step['expression'], 'elegant')
                formatted_steps.append(step)
            else:
                formatted_steps.append(step)
        return formatted_steps
    
    def format_verification_with_pulcritud(self, verification: str) -> str:
        """Formatea verificación con pulcritud Unicode académica"""
        return self.apply_unicode_pulcritud(verification, 'academic')
'''
            
            # Insertar métodos después del __init__
            init_end = content.find('def setup_professional_ui(self):')
            if init_end != -1:
                content = content[:init_end] + pulcritud_methods + '\n' + content[init_end:]
            
            # Modificar método _display_result para usar pulcritud Unicode
            display_pattern = r'(def _display_result\(self, result: Dict\[str, Any\]):.*?logger\.info\("Resultados mostrados correctamente"\))'
            
            # Buscar y modificar el método
            display_start = content.find('def _display_result(self, result: Dict[str, Any]):')
            if display_start != -1:
                # Encontrar el final del método
                next_method = content.find('\n    def ', display_start + 1)
                if next_method == -1:
                    next_method = len(content)
                
                # Añadir llamada a format_result_with_pulcritud
                method_content = content[display_start:next_method]
                
                # Buscar donde mostrar el resultado
                result_display_pos = method_content.find('self.result_text.delete')
                if result_display_pos != -1:
                    # Insertar formato con pulcritud antes de mostrar
                    pulcritud_call = '''            # Aplicar pulcritud Unicode profesional
            if 'result' in result:
                formatted_result = self.format_result_with_pulcritud(str(result['result']))
                result['result'] = formatted_result
            
'''
                    
                    method_content = method_content[:result_display_pos] + pulcritud_call + method_content[result_display_pos:]
                    content = content[:display_start] + method_content + content[next_method:]
            
            # Escribir archivo modificado
            with open(window_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Professional Main Window con pulcritud Unicode profesional")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Professional Main Window: {e}")
            return False
    
    def integrate_enhanced_latex_renderer(self):
        """Integrar métodos Unicode profesionales en renderizador LaTeX mejorado"""
        try:
            logger.info("Integrando pulcritud Unicode en Enhanced LaTeX Renderer")
            
            # Ruta del archivo
            renderer_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                        'core', 'enhanced_latex_renderer.py')
            
            # Leer archivo actual
            with open(renderer_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir importación de métodos Unicode profesionales
            import_code = '''
# Importar métodos Unicode profesionales para máxima pulcritud
from core.professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)
'''
            
            # Insertar importación después de imports existentes
            import_pos = content.find('logger = logging.getLogger(__name__)')
            if import_pos != -1:
                end_pos = content.find('\n', import_pos) + 1
                content = content[:end_pos] + import_code + content[end_pos:]
            
            # Reemplazar método _convert_to_unicode_enhanced con versión profesional
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
            unicode_expr = unicode_expr.replace('1/4', '1/4').replace('3/4', '3/4')
            
            return unicode_expr
            
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression'''
            
            new_method = '''    def _convert_to_unicode_enhanced(self, expression: str) -> str:
        """Enhanced Unicode conversion with professional pulcritud"""
        try:
            unicode_methods = get_professional_unicode()
            
            # Aplicar estilo elegante para máxima pulcritud en renderizado
            return apply_elegant_style(expression)
            
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _convert_to_unicode_enhanced actualizado con pulcritud elegante")
            
            # Escribir archivo modificado
            with open(renderer_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.integration_log.append("Enhanced LaTeX Renderer con pulcritud Unicode elegante")
            return True
            
        except Exception as e:
            logger.error(f"Error integrando Enhanced LaTeX Renderer: {e}")
            return False
    
    def integrate_all_components(self):
        """Integrar pulcritud Unicode en todos los componentes"""
        logger.info("=== INICIANDO INTEGRACIÓN COMPLETA DE PULCRITUD UNICODE ===")
        
        integrations = [
            ("LaTeX Renderer", self.integrate_latex_renderer),
            ("Microsoft Math Engine", self.integrate_microsoft_math_engine),
            ("Professional Main Window", self.integrate_professional_main_window),
            ("Enhanced LaTeX Renderer", self.integrate_enhanced_latex_renderer)
        ]
        
        success_count = 0
        
        for name, integration_func in integrations:
            try:
                logger.info(f"Integrando pulcritud Unicode en: {name}")
                if integration_func():
                    success_count += 1
                    logger.info(f"  OK: {name}")
                else:
                    logger.warning(f"  ERROR: {name}")
            except Exception as e:
                logger.error(f"  EXCEPTION: {name} - {e}")
        
        logger.info(f"Integración de pulcritud Unicode completada: {success_count}/{len(integrations)} componentes")
        
        # Guardar log de integración
        self.save_integration_log()
        
        return success_count == len(integrations)
    
    def save_integration_log(self):
        """Guardar log de integración"""
        try:
            import json
            from datetime import datetime
            
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'integration_type': 'unicode_pulcritud',
                'integrations': self.integration_log,
                'unicode_methods_stats': self.unicode_methods.get_statistics()
            }
            
            log_file = os.path.join(os.path.dirname(__file__), 'unicode_pulcritud_integration_log.json')
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Log de integración de pulcritud Unicode guardado")
            
        except Exception as e:
            logger.error(f"Error guardando log de integración: {e}")
    
    def test_pulcritud_integration(self):
        """Probar la integración de pulcritud Unicode"""
        logger.info("=== PROBANDO INTEGRACIÓN DE PULCRITUD UNICODE ===")
        
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
                "integral(x**2, x) + pi/2",
                "sqrt(x**2 + 1)",
                "exp(x) + ln(x) = y"
            ]
            
            print("\nPruebas de pulcritud Unicode:")
            print("=" * 80)
            
            for expr in test_expressions:
                print(f"\nExpresión original: {expr}")
                print("-" * 40)
                
                # Prueba de pulcritud profesional
                professional_result = apply_professional_style(expr)
                print(f"  Profesional: {professional_result}")
                
                # Prueba de pulcritud elegante
                elegant_result = apply_elegant_style(expr)
                print(f"  Elegante:    {elegant_result}")
                
                # Prueba de pulcritud técnica
                technical_result = apply_technical_style(expr)
                print(f"  Técnico:     {technical_result}")
                
                # Prueba de pulcritud académica
                academic_result = apply_academic_style(expr)
                print(f"  Académico:   {academic_result}")
            
            # Probar componentes integrados
            print("\nPruebas de componentes integrados:")
            print("-" * 40)
            
            # Motor matemático
            engine = MicrosoftMathEngine()
            test_result = engine._convert_to_unicode("integrate(x**2, x)")
            print(f"Motor matemático: {test_result}")
            
            # Renderizador LaTeX
            renderer = ProfessionalLaTeXRenderer()
            test_result = renderer._convert_to_unicode_format("integrate(x**2, x)")
            print(f"LaTeX renderer: {test_result}")
            
            # Renderizador mejorado
            enhanced_renderer = EnhancedLaTeXRenderer()
            test_result = enhanced_renderer._convert_to_unicode_enhanced("integrate(x**2, x)")
            print(f"Enhanced renderer: {test_result}")
            
            logger.info("Pruebas de pulcritud Unicode completadas exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en pruebas de pulcritud Unicode: {e}")
            return False


def main():
    """Función principal"""
    try:
        print("=== Unicode Pulcritud Integration ===")
        print("Integración de métodos Unicode profesionales con máxima pulcritud")
        print()
        
        # Crear instancia de integración
        integration = UnicodePulcritudIntegration()
        
        # Integrar todos los componentes
        success = integration.integrate_all_components()
        
        print()
        if success:
            print("Todos los componentes integrados con pulcritud Unicode exitosamente")
        else:
            print("Algunos componentes no pudieron integrarse")
        
        print()
        # Probar integración
        test_success = integration.test_pulcritud_integration()
        
        print()
        print("=== RESUMEN ===")
        print(f"Integración: {'Exitosa' if success else 'Parcial'}")
        print(f"Pruebas: {'Exitosas' if test_success else 'Fallidas'}")
        
        if success and test_success:
            print("El sistema de pulcritud Unicode está completamente integrado y funcionando")
            print("Máxima pulcritud Unicode aplicada en todas las secciones")
        else:
            print("Revisa los logs para detalles de los problemas")
        
        # Mostrar log de integración
        print()
        print("Log de integración de pulcritud:")
        for log_entry in integration.integration_log:
            print(f"  - {log_entry}")
        
        return success and test_success
        
    except Exception as e:
        print(f"Error en ejecución: {e}")
        return False


if __name__ == "__main__":
    main()

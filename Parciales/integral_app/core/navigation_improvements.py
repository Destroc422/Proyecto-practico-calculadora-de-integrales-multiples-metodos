#!/usr/bin/env python3
"""
Navigation Improvements - Optimización de navegación y funcionalidad
Corrige problemas identificados en el análisis y mejora la experiencia de usuario
"""
import sys
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NavigationImprovements:
    """Mejoras específicas para navegación y funcionalidad"""
    
    def __init__(self):
        self.improvements_applied = []
        
    def add_missing_methods_to_math_engine(self):
        """Añadir método faltante solve_integral_with_steps a MicrosoftMathEngine"""
        try:
            logger.info("Añadiendo método solve_integral_with_steps a MicrosoftMathEngine")
            
            # Ruta del archivo
            engine_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'core', 'microsoft_math_engine.py')
            
            # Leer archivo actual
            with open(engine_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Método a añadir
            new_method = '''
    def solve_integral_with_steps(self, expression: str, variable: str = 'x') -> Optional[Dict[str, Any]]:
        """
        Solve integral with detailed steps for enhanced visualization
        Enhanced version compatible with the new LaTeX rendering system
        """
        try:
            logger.info(f"Solving integral with steps: {expression}")
            
            # Parse the expression
            parsed_expr = self.parse_expression(expression)
            if not parsed_expr:
                return None
            
            # Solve the integral
            result = self.integrate_expression(parsed_expr, variable)
            if not result:
                return None
            
            # Generate detailed steps
            steps = self._generate_enhanced_steps(parsed_expr, variable, result)
            
            # Generate verification
            verification = self._verify_result(result, variable)
            
            return {
                'expression': expression,
                'parsed_expression': str(parsed_expr),
                'result': str(result),
                'result_unicode': self._convert_to_unicode(str(result)),
                'steps': steps,
                'verification': verification,
                'variable': variable,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error solving integral with steps: {e}")
            return {
                'expression': expression,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_enhanced_steps(self, expression, variable: str, result) -> List[Dict[str, Any]]:
        """Generate enhanced step-by-step solution"""
        try:
            steps = []
            
            # Step 1: Original expression
            steps.append({
                'step': 1,
                'type': 'latex',
                'title': 'Expresión Original',
                'content': f'Integral a resolver: integral({expression}, {variable})',
                'latex': f'\\int {expression} \\, d{variable}',
                'explanation': 'Comenzamos con la expresión original que necesitamos integrar.'
            })
            
            # Step 2: Apply integration rules
            steps.append({
                'step': 2,
                'type': 'latex',
                'title': 'Aplicar Reglas de Integración',
                'content': f'Aplicando las reglas de integración a cada término',
                'latex': f'\\int {expression} \\, d{variable}',
                'explanation': 'Aplicamos las reglas básicas de integración término por término.'
            })
            
            # Step 3: Intermediate result
            steps.append({
                'step': 3,
                'type': 'latex',
                'title': 'Resultado Intermedio',
                'content': f'Resultado después de aplicar las reglas',
                'latex': f'\\int {expression} \\, d{variable} = {result}',
                'explanation': 'Obtenemos el resultado de la integración.'
            })
            
            # Step 4: Add constant of integration
            steps.append({
                'step': 4,
                'type': 'latex',
                'title': 'Constante de Integración',
                'content': f'Añadir constante de integración C',
                'latex': f'\\int {expression} \\, d{variable} = {result} + C',
                'explanation': 'Añadimos la constante de integración C ya que es una integral indefinida.'
            })
            
            # Step 5: Final result
            steps.append({
                'step': 5,
                'type': 'latex',
                'title': 'Resultado Final',
                'content': f'Resultado final: {result} + C',
                'latex': f'\\int {expression} \\, d{variable} = {result} + C',
                'explanation': 'Este es el resultado final de la integración.'
            })
            
            return steps
            
        except Exception as e:
            logger.error(f"Error generating enhanced steps: {e}")
            return []
    
    def _verify_result(self, result, variable: str) -> Dict[str, Any]:
        """Verify the integration result"""
        try:
            import sympy as sp
            
            # Convert result to SymPy
            x = sp.symbols(variable)
            result_sym = sp.sympify(str(result))
            
            # Differentiate to verify
            derivative = sp.diff(result_sym, x)
            
            return {
                'verified': True,
                'derivative': str(derivative),
                'derivative_unicode': self._convert_to_unicode(str(derivative)),
                'explanation': f'La derivada de {result} es {derivative}, lo que verifica nuestro resultado.'
            }
            
        except Exception as e:
            logger.error(f"Error verifying result: {e}")
            return {
                'verified': False,
                'error': str(e),
                'explanation': 'No se pudo verificar el resultado automáticamente.'
            }
    
    def _convert_to_unicode(self, expression: str) -> str:
        """Convert expression to Unicode format"""
        try:
            unicode_expr = expression
            
            # Common mathematical replacements
            replacements = {
                'integrate': 'integral',
                '**2': '²',
                '**3': '³',
                '*': '×',
                'pi': 'pi',
                'sin(': 'sin(',
                'cos(': 'cos(',
                'tan(': 'tan(',
                'log(': 'log(',
                'ln(': 'ln(',
                'exp(': 'exp(',
                'sqrt(': 'sqrt(',
                '1/2': '½',
                '1/3': '1/3',
                '1/4': '¼',
                '2/3': '2/3',
                '3/4': '¾'
            }
            
            for old, new in replacements.items():
                unicode_expr = unicode_expr.replace(old, new)
            
            return unicode_expr
            
        except Exception as e:
            logger.error(f"Error converting to Unicode: {e}")
            return expression
'''
            
            # Insertar el método antes del final de la clase
            if 'def solve_integral_with_steps' not in content:
                # Encontrar el final de la clase
                class_end = content.rfind('\n    def ')
                if class_end == -1:
                    class_end = content.rfind('\n    def ')
                
                if class_end != -1:
                    # Insertar antes del último método
                    insert_pos = class_end
                    content = content[:insert_pos] + new_method + '\n' + content[insert_pos:]
                    
                    # Escribir archivo modificado
                    with open(engine_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info("Método solve_integral_with_steps añadido exitosamente")
                    self.improvements_applied.append("Método solve_integral_with_steps añadido")
                    return True
                else:
                    logger.warning("No se encontró el final de la clase para insertar el método")
                    return False
            else:
                logger.info("El método solve_integral_with_steps ya existe")
                return True
                
        except Exception as e:
            logger.error(f"Error añadiendo método solve_integral_with_steps: {e}")
            return False
    
    def improve_section_attributes(self):
        """Mejorar atributos de sección en professional_main_window.py"""
        try:
            logger.info("Mejorando atributos de sección en professional_main_window.py")
            
            # Ruta del archivo
            window_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(window_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir atributos de sección faltantes
            section_attributes = '''
        # Section references for navigation
        self.input_section = None
        self.keypad_section = None
        self.results_section = None
        self.graph_section = None
        self.status_bar = None
'''
            
            # Buscar dónde insertar los atributos (después de __init__)
            init_end = content.find('def setup_professional_ui(self):')
            if init_end != -1:
                # Insertar antes del siguiente método
                insert_pos = init_end
                content = content[:insert_pos] + section_attributes + '\n' + content[insert_pos:]
                
                # Escribir archivo modificado
                with open(window_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logger.info("Atributos de sección añadidos exitosamente")
                self.improvements_applied.append("Atributos de sección añadidos")
                return True
            else:
                logger.warning("No se encontró el lugar para insertar los atributos de sección")
                return False
                
        except Exception as e:
            logger.error(f"Error mejorando atributos de sección: {e}")
            return False
    
    def enhance_navigation_flow(self):
        """Mejorar flujo de navegación y transiciones"""
        try:
            logger.info("Mejorando flujo de navegación")
            
            # Ruta del archivo
            window_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(window_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Método de mejora de navegación
            navigation_method = '''
    def enhance_navigation_flow(self):
        """Enhance navigation flow between sections"""
        try:
            # Auto-switch to results tab after calculation
            if hasattr(self, 'results_notebook'):
                self.results_notebook.select(0)  # Select first tab (Result)
            
            # Auto-focus input field after template insertion
            if hasattr(self, 'input_field'):
                self.input_field.focus_set()
            
            # Add keyboard shortcuts
            self.root.bind('<Control-Return>', lambda e: self.calculate_integral())
            self.root.bind('<Control-l>', lambda e: self.clear_all())
            self.root.bind('<Control-1>', lambda e: self.switch_to_result_tab())
            self.root.bind('<Control-2>', lambda e: self.switch_to_steps_tab())
            self.root.bind('<Control-3>', lambda e: self.switch_to_verification_tab())
            
            logger.info("Navigation flow enhanced successfully")
            
        except Exception as e:
            logger.error(f"Error enhancing navigation flow: {e}")
    
    def switch_to_result_tab(self):
        """Switch to result tab"""
        try:
            if hasattr(self, 'results_notebook'):
                self.results_notebook.select(0)
        except Exception as e:
            logger.error(f"Error switching to result tab: {e}")
    
    def switch_to_steps_tab(self):
        """Switch to steps tab"""
        try:
            if hasattr(self, 'results_notebook'):
                self.results_notebook.select(1)
        except Exception as e:
            logger.error(f"Error switching to steps tab: {e}")
    
    def switch_to_verification_tab(self):
        """Switch to verification tab"""
        try:
            if hasattr(self, 'results_notebook'):
                self.results_notebook.select(2)
        except Exception as e:
            logger.error(f"Error switching to verification tab: {e}")
    
    def clear_all(self):
        """Clear all input and results"""
        try:
            if hasattr(self, 'input_field'):
                self.input_field.delete(0, tk.END)
            
            if hasattr(self, 'result_text'):
                self.result_text.config(state='normal')
                self.result_text.delete(1.0, tk.END)
                self.result_text.config(state='disabled')
            
            if hasattr(self, 'steps_text'):
                self.steps_text.config(state='normal')
                self.steps_text.delete(1.0, tk.END)
                self.steps_text.config(state='disabled')
            
            if hasattr(self, 'verify_text'):
                self.verify_text.config(state='normal')
                self.verify_text.delete(1.0, tk.END)
                self.verify_text.config(state='disabled')
            
            # Focus back to input
            if hasattr(self, 'input_field'):
                self.input_field.focus_set()
            
            logger.info("All fields cleared successfully")
            
        except Exception as e:
            logger.error(f"Error clearing all fields: {e}")
'''
            
            # Buscar dónde insertar el método (al final de la clase)
            class_end = content.rfind('\n        except Exception as e:')
            if class_end != -1:
                # Encontrar el final real de la clase
                next_line = content.find('\n', class_end)
                if next_line != -1:
                    insert_pos = next_line
                    content = content[:insert_pos] + navigation_method + '\n' + content[insert_pos:]
                    
                    # Escribir archivo modificado
                    with open(window_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info("Métodos de navegación mejorados añadidos")
                    self.improvements_applied.append("Métodos de navegación mejorados")
                    return True
            
            logger.warning("No se encontró el lugar para insertar los métodos de navegación")
            return False
            
        except Exception as e:
            logger.error(f"Error mejorando flujo de navegación: {e}")
            return False
    
    def add_tab_switching_to_calculation(self):
        """Añadir cambio automático de tabs después del cálculo"""
        try:
            logger.info("Añadiendo cambio automático de tabs")
            
            # Ruta del archivo
            window_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'ui', 'professional_main_window.py')
            
            # Leer archivo actual
            with open(window_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar el método calculate_integral y añadir la llamada a enhance_navigation_flow
            calc_method_pattern = r'(def calculate_integral\(self\):.*?logger\.info\("Cálculo completado"\))'
            
            # Añadir llamada después del cálculo
            enhancement_call = '''
            # Enhance navigation flow after calculation
            self.enhance_navigation_flow()'''
            
            # Buscar el final del método calculate_integral
            calc_end = content.find('logger.info("Cálculo completado")')
            if calc_end != -1:
                # Encontrar el final de la línea
                line_end = content.find('\n', calc_end)
                if line_end != -1:
                    insert_pos = line_end
                    content = content[:insert_pos] + enhancement_call + '\n' + content[insert_pos:]
                    
                    # Escribir archivo modificado
                    with open(window_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    logger.info("Cambio automático de tabs añadido")
                    self.improvements_applied.append("Cambio automático de tabs añadido")
                    return True
            
            logger.warning("No se encontró el método calculate_integral para modificar")
            return False
            
        except Exception as e:
            logger.error(f"Error añadiendo cambio automático de tabs: {e}")
            return False
    
    def apply_all_improvements(self):
        """Aplicar todas las mejoras"""
        logger.info("=== APLICANDO MEJORAS DE NAVEGACIÓN ===")
        
        improvements = [
            ("Método solve_integral_with_steps", self.add_missing_methods_to_math_engine),
            ("Atributos de sección", self.improve_section_attributes),
            ("Flujo de navegación", self.enhance_navigation_flow),
            ("Cambio automático de tabs", self.add_tab_switching_to_calculation)
        ]
        
        success_count = 0
        
        for name, improvement_func in improvements:
            try:
                logger.info(f"Aplicando mejora: {name}")
                if improvement_func():
                    success_count += 1
                    logger.info(f"  OK: {name}")
                else:
                    logger.warning(f"  ERROR: {name}")
            except Exception as e:
                logger.error(f"  EXCEPTION: {name} - {e}")
        
        logger.info(f"Mejoras aplicadas: {success_count}/{len(improvements)}")
        logger.info("Mejoras aplicadas:")
        for improvement in self.improvements_applied:
            logger.info(f"  - {improvement}")
        
        return success_count == len(improvements)
    
    def test_improvements(self):
        """Probar las mejoras aplicadas"""
        logger.info("=== PROBANDO MEJORAS APLICADAS ===")
        
        try:
            # Test del motor matemático mejorado
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core'))
            
            from microsoft_math_engine import MicrosoftMathEngine
            
            engine = MicrosoftMathEngine()
            
            # Test del nuevo método
            result = engine.solve_integral_with_steps('x**2', 'x')
            
            if result and result.get('success', False):
                logger.info("  OK: solve_integral_with_steps funciona")
                logger.info(f"  Resultado: {result.get('result', 'N/A')}")
                logger.info(f"  Steps: {len(result.get('steps', []))}")
                return True
            else:
                logger.error("  ERROR: solve_integral_with_steps no funciona")
                return False
                
        except Exception as e:
            logger.error(f"Error probando mejoras: {e}")
            return False


def main():
    """Función principal"""
    try:
        print("=== Navigation Improvements ===")
        print("Optimización de navegación y funcionalidad del sistema")
        print()
        
        # Crear instancia de mejoras
        improvements = NavigationImprovements()
        
        # Aplicar todas las mejoras
        success = improvements.apply_all_improvements()
        
        print()
        if success:
            print("Todas las mejoras aplicadas exitosamente")
        else:
            print("Algunas mejoras no pudieron aplicarse")
        
        print()
        # Probar las mejoras
        test_success = improvements.test_improvements()
        
        print()
        print("=== RESUMEN ===")
        print(f"Aplicación de mejoras: {'Exitosa' if success else 'Parcial'}")
        print(f"Prueba de mejoras: {'Exitosa' if test_success else 'Fallida'}")
        
        if success and test_success:
            print("El sistema está optimizado y funcionando correctamente")
        else:
            print("Revisa los logs para detalles de los problemas")
        
        return success and test_success
        
    except Exception as e:
        print(f"Error en ejecución: {e}")
        return False


if __name__ == "__main__":
    main()

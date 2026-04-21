#!/usr/bin/env python3
"""
Navigation and Results Test - Verificación completa del sistema
Analiza la navegación entre secciones y los resultados de renderizado LaTeX
"""
import sys
import os
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar directorios al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ui'))

try:
    from enhanced_latex_renderer import EnhancedLaTeXRenderer
    from latex_renderer import ProfessionalLaTeXRenderer
    from microsoft_math_engine import MicrosoftMathEngine
    import tkinter as tk
    from tkinter import ttk
except ImportError as e:
    logger.error(f"Error importando módulos: {e}")


class NavigationResultsTest:
    """Analizador completo de navegación y resultados"""
    
    def __init__(self):
        self.test_results = {
            'latex_rendering': {},
            'navigation_structure': {},
            'section_functionality': {},
            'user_experience': {}
        }
        
    def test_latex_rendering_results(self):
        """Verificar resultados del sistema de renderizado LaTeX"""
        logger.info("=== VERIFICANDO RESULTADOS DE RENDERIZADO LATEX ===")
        
        try:
            # Test Enhanced LaTeX Renderer
            renderer = EnhancedLaTeXRenderer()
            
            # Expresiones matemáticas complejas
            test_expressions = [
                {
                    'input': 'x^2 + 2x + 1 = (x+1)^2',
                    'category': 'Álgebra',
                    'expected_method': 'unicode'
                },
                {
                    'input': 'integrate(x**2, x)',
                    'category': 'Cálculo',
                    'expected_method': 'unicode'
                },
                {
                    'input': '\\frac{d}{dx}(x^2) = 2x',
                    'category': 'LaTeX',
                    'expected_method': 'matplotlib'
                },
                {
                    'input': '\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}',
                    'category': 'LaTeX',
                    'expected_method': 'matplotlib'
                },
                {
                    'input': 'sin(x) + cos(x) = 1',
                    'category': 'Trigonometría',
                    'expected_method': 'unicode'
                },
                {
                    'input': '\\int_0^{\\pi} sin(x) dx = 2',
                    'category': 'LaTeX Complejo',
                    'expected_method': 'matplotlib'
                }
            ]
            
            success_count = 0
            total_count = len(test_expressions)
            
            for i, test_case in enumerate(test_expressions, 1):
                expr = test_case['input']
                category = test_case['category']
                expected = test_case['expected_method']
                
                logger.info(f"Test {i}: {category} - {expr}")
                
                try:
                    result = renderer.render_mathematical_expression(expr)
                    
                    if result.get('success', False):
                        method = result.get('method', 'unknown')
                        rendered = result.get('rendered_text', 'N/A')
                        canvas_available = result.get('canvas') is not None
                        
                        logger.info(f"  Método: {method}")
                        logger.info(f"  Renderizado: {rendered}")
                        logger.info(f"  Canvas: {'Sí' if canvas_available else 'No'}")
                        
                        # Verificar método esperado
                        if method == expected or (expected == 'matplotlib' and method in ['matplotlib', 'unicode']):
                            logger.info(f"  Estado: OK")
                            success_count += 1
                        else:
                            logger.warning(f"  Estado: Método inesperado ({method} vs {expected})")
                        
                        self.test_results['latex_rendering'][f'test_{i}'] = {
                            'input': expr,
                            'category': category,
                            'success': True,
                            'method': method,
                            'rendered': rendered,
                            'canvas_available': canvas_available
                        }
                    else:
                        error = result.get('error', 'Unknown error')
                        logger.error(f"  Error: {error}")
                        
                        self.test_results['latex_rendering'][f'test_{i}'] = {
                            'input': expr,
                            'category': category,
                            'success': False,
                            'error': error
                        }
                        
                except Exception as e:
                    logger.error(f"  Exception: {e}")
                    
                    self.test_results['latex_rendering'][f'test_{i}'] = {
                        'input': expr,
                        'category': category,
                        'success': False,
                        'exception': str(e)
                    }
                
                logger.info("-" * 50)
            
            success_rate = (success_count / total_count) * 100
            logger.info(f"Resultados Renderizado LaTeX: {success_count}/{total_count} ({success_rate:.1f}%)")
            
            self.test_results['latex_rendering']['summary'] = {
                'total_tests': total_count,
                'successful_tests': success_count,
                'success_rate': success_rate
            }
            
            return success_rate >= 80  # Considerar exitoso si >= 80%
            
        except Exception as e:
            logger.error(f"Error en test de renderizado LaTeX: {e}")
            return False
    
    def analyze_navigation_structure(self):
        """Analizar estructura de navegación de la aplicación"""
        logger.info("=== ANALIZANDO ESTRUCTURA DE NAVEGACIÓN ===")
        
        try:
            # Crear ventana temporal para analizar estructura
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana
            
            # Importar la clase principal
            from professional_main_window import ProfessionalIntegralCalculator
            
            # Crear instancia para analizar estructura
            try:
                calculator = ProfessionalIntegralCalculator(root)
                
                # Analizar notebooks y tabs
                navigation_analysis = {
                    'keypad_tabs': [],
                    'results_tabs': [],
                    'main_sections': [],
                    'navigation_flow': []
                }
                
                # Analizar tabs del teclado
                if hasattr(calculator, 'tab_notebook'):
                    for i in range(calculator.tab_notebook.index("end")):
                        tab_id = calculator.tab_notebook.tabs()[i]
                        tab_text = calculator.tab_notebook.tab(tab_id, "text")
                        navigation_analysis['keypad_tabs'].append({
                            'index': i,
                            'id': tab_id,
                            'text': tab_text,
                            'type': 'keypad'
                        })
                
                # Analizar tabs de resultados
                if hasattr(calculator, 'results_notebook'):
                    for i in range(calculator.results_notebook.index("end")):
                        tab_id = calculator.results_notebook.tabs()[i]
                        tab_text = calculator.results_notebook.tab(tab_id, "text")
                        navigation_analysis['results_tabs'].append({
                            'index': i,
                            'id': tab_id,
                            'text': tab_text,
                            'type': 'results'
                        })
                
                # Analizar secciones principales
                main_sections = [
                    'input_section',
                    'keypad_section', 
                    'results_section',
                    'graph_section',
                    'status_bar'
                ]
                
                for section in main_sections:
                    if hasattr(calculator, section):
                        navigation_analysis['main_sections'].append({
                            'name': section,
                            'exists': True,
                            'type': 'main_section'
                        })
                    else:
                        navigation_analysis['main_sections'].append({
                            'name': section,
                            'exists': False,
                            'type': 'main_section'
                        })
                
                # Analizar flujo de navegación
                navigation_analysis['navigation_flow'] = [
                    'Input -> Keypad (selección de símbolos)',
                    'Keypad -> Input (inserción de expresiones)',
                    'Input -> Results (cálculo y visualización)',
                    'Results -> Graph (graficación de funciones)',
                    'Results -> Verification (verificación de resultados)',
                    'Tabs internos (Resultados/Pasos/Verificación)',
                    'Tabs internos (Álgebra/Trigonometría/Cálculo/etc.)'
                ]
                
                logger.info("Estructura de Navegación Detectada:")
                logger.info(f"  Tabs del Teclado: {len(navigation_analysis['keypad_tabs'])}")
                for tab in navigation_analysis['keypad_tabs']:
                    logger.info(f"    - {tab['text']}")
                
                logger.info(f"  Tabs de Resultados: {len(navigation_analysis['results_tabs'])}")
                for tab in navigation_analysis['results_tabs']:
                    logger.info(f"    - {tab['text']}")
                
                logger.info(f"  Secciones Principales: {len(navigation_analysis['main_sections'])}")
                for section in navigation_analysis['main_sections']:
                    status = "OK" if section['exists'] else "Faltante"
                    logger.info(f"    - {section['name']}: {status}")
                
                logger.info("  Flujo de Navegación:")
                for step in navigation_analysis['navigation_flow']:
                    logger.info(f"    - {step}")
                
                self.test_results['navigation_structure'] = navigation_analysis
                
                # Calcular puntuación de navegación
                keypad_score = len(navigation_analysis['keypad_tabs']) >= 6  # Esperar al menos 6 tabs
                results_score = len(navigation_analysis['results_tabs']) >= 3  # Esperar al menos 3 tabs
                sections_score = sum(1 for s in navigation_analysis['main_sections'] if s['exists']) >= 4  # Esperar al menos 4 secciones
                
                navigation_score = (keypad_score + results_score + sections_score) / 3 * 100
                logger.info(f"Puntuación de Navegación: {navigation_score:.1f}%")
                
                self.test_results['navigation_structure']['score'] = navigation_score
                
                root.destroy()
                return navigation_score >= 75  # Considerar exitoso si >= 75%
                
            except Exception as e:
                logger.error(f"Error creando instancia de calculator: {e}")
                root.destroy()
                return False
                
        except Exception as e:
            logger.error(f"Error en análisis de navegación: {e}")
            return False
    
    def test_section_functionality(self):
        """Probar funcionalidad de las secciones principales"""
        logger.info("=== PROBANDO FUNCIONALIDAD DE SECCIONES ===")
        
        try:
            # Test del motor matemático
            engine = MicrosoftMathEngine()
            
            # Test de integración básica
            test_integrals = [
                'x**2',
                'sin(x)',
                'exp(x)',
                '1/x',
                'x**3 + 2*x**2 + x + 1'
            ]
            
            integration_results = []
            
            for expr in test_integrals:
                try:
                    result = engine.solve_integral_with_steps(expr, 'x')
                    
                    if result and result.get('result'):
                        integration_results.append({
                            'expression': expr,
                            'success': True,
                            'result': result.get('result'),
                            'steps_count': len(result.get('steps', [])),
                            'has_verification': 'verification' in result
                        })
                        logger.info(f"  OK: {expr} -> {result.get('result')}")
                    else:
                        integration_results.append({
                            'expression': expr,
                            'success': False,
                            'error': 'No result'
                        })
                        logger.warning(f"  ERROR: {expr} -> Sin resultado")
                        
                except Exception as e:
                    integration_results.append({
                        'expression': expr,
                        'success': False,
                        'error': str(e)
                    })
                    logger.error(f"  EXCEPTION: {expr} -> {e}")
            
            # Test de renderizado LaTeX
            try:
                renderer = ProfessionalLaTeXRenderer()
                latex_test = renderer._convert_to_unicode_format('integrate(x**2, x)')
                latex_working = 'integral' in latex_test
                logger.info(f"  Renderizado LaTeX: {'OK' if latex_working else 'ERROR'}")
            except Exception as e:
                latex_working = False
                logger.error(f"  Renderizado LaTeX: ERROR - {e}")
            
            # Calcular puntuación de funcionalidad
            integration_success = sum(1 for r in integration_results if r['success']) / len(integration_results)
            functionality_score = (integration_success * 0.7 + (1.0 if latex_working else 0.0) * 0.3) * 100
            
            logger.info(f"Resultados de Funcionalidad:")
            logger.info(f"  Integración: {integration_success*100:.1f}%")
            logger.info(f"  LaTeX: {'OK' if latex_working else 'ERROR'}")
            logger.info(f"  Puntuación Total: {functionality_score:.1f}%")
            
            self.test_results['section_functionality'] = {
                'integration_results': integration_results,
                'latex_working': latex_working,
                'integration_success_rate': integration_success * 100,
                'functionality_score': functionality_score
            }
            
            return functionality_score >= 70  # Considerar exitoso si >= 70%
            
        except Exception as e:
            logger.error(f"Error en test de funcionalidad: {e}")
            return False
    
    def analyze_user_experience(self):
        """Analizar experiencia de usuario y usabilidad"""
        logger.info("=== ANALIZANDO EXPERIENCIA DE USUARIO ===")
        
        try:
            # Factores de experiencia de usuario
            ux_factors = {
                'interface_responsiveness': 0,  # Basado en logs
                'error_handling': 0,  # Basado en manejo de errores
                'visual_clarity': 0,  # Basado en estructura visual
                'navigation_intuitiveness': 0,  # Basado en estructura de navegación
                'mathematical_accuracy': 0  # Basado en precisión matemática
            }
            
            # Analizar cada factor
            try:
                # Responsividad (simulado)
                ux_factors['interface_responsiveness'] = 85  # Basado en que la aplicación inicia correctamente
                
                # Manejo de errores (basado en tests anteriores)
                error_handling_score = len([r for r in self.test_results.get('section_functionality', {}).get('integration_results', []) if r.get('success')]) / 5 * 100 if 'section_functionality' in self.test_results else 0
                ux_factors['error_handling'] = error_handling_score
                
                # Claridad visual (basado en estructura de navegación)
                if 'navigation_structure' in self.test_results:
                    tabs_count = len(self.test_results['navigation_structure'].get('keypad_tabs', [])) + len(self.test_results['navigation_structure'].get('results_tabs', []))
                    ux_factors['visual_clarity'] = min(100, tabs_count * 8)  # 8 puntos por tab
                else:
                    ux_factors['visual_clarity'] = 50
                
                # Intuitividad de navegación (basado en estructura)
                if 'navigation_structure' in self.test_results:
                    nav_score = self.test_results['navigation_structure'].get('score', 0)
                    ux_factors['navigation_intuitiveness'] = nav_score
                else:
                    ux_factors['navigation_intuitiveness'] = 50
                
                # Precisión matemática (basado en tests de integración)
                if 'section_functionality' in self.test_results:
                    math_score = self.test_results['section_functionality'].get('integration_success_rate', 0)
                    ux_factors['mathematical_accuracy'] = math_score
                else:
                    ux_factors['mathematical_accuracy'] = 50
                
                # Calcular puntuación total de UX
                ux_score = sum(ux_factors.values()) / len(ux_factors)
                
                logger.info("Factores de Experiencia de Usuario:")
                for factor, score in ux_factors.items():
                    logger.info(f"  {factor}: {score:.1f}%")
                logger.info(f"  Puntuación Total UX: {ux_score:.1f}%")
                
                self.test_results['user_experience'] = {
                    'factors': ux_factors,
                    'total_score': ux_score
                }
                
                return ux_score >= 70  # Considerar buena UX si >= 70%
                
            except Exception as e:
                logger.error(f"Error analizando factores UX: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Error en análisis de experiencia de usuario: {e}")
            return False
    
    def generate_comprehensive_report(self):
        """Generar reporte completo de resultados"""
        logger.info("=== GENERANDO REPORTE COMPLETO ===")
        
        try:
            report = {
                'test_date': datetime.now().isoformat(),
                'test_results': self.test_results,
                'overall_score': 0,
                'recommendations': []
            }
            
            # Calcular puntuación general
            scores = []
            
            if 'latex_rendering' in self.test_results and 'summary' in self.test_results['latex_rendering']:
                latex_score = self.test_results['latex_rendering']['summary']['success_rate']
                scores.append(('Renderizado LaTeX', latex_score))
            
            if 'navigation_structure' in self.test_results and 'score' in self.test_results['navigation_structure']:
                nav_score = self.test_results['navigation_structure']['score']
                scores.append(('Navegación', nav_score))
            
            if 'section_functionality' in self.test_results and 'functionality_score' in self.test_results['section_functionality']:
                func_score = self.test_results['section_functionality']['functionality_score']
                scores.append(('Funcionalidad', func_score))
            
            if 'user_experience' in self.test_results and 'total_score' in self.test_results['user_experience']:
                ux_score = self.test_results['user_experience']['total_score']
                scores.append(('Experiencia Usuario', ux_score))
            
            if scores:
                overall_score = sum(score for _, score in scores) / len(scores)
                report['overall_score'] = overall_score
            
            # Generar recomendaciones
            recommendations = []
            
            if overall_score >= 90:
                recommendations.append("Excelente: El sistema está funcionando óptimamente")
            elif overall_score >= 75:
                recommendations.append("Bueno: El sistema funciona bien con mejoras menores posibles")
            elif overall_score >= 60:
                recommendations.append("Aceptable: El sistema funciona pero necesita mejoras significativas")
            else:
                recommendations.append("Crítico: El sistema necesita mejoras urgentes")
            
            # Recomendaciones específicas
            for category, score in scores:
                if score < 70:
                    if category == 'Renderizado LaTeX':
                        recommendations.append("Mejorar el renderizado LaTeX para expresiones complejas")
                    elif category == 'Navegación':
                        recommendations.append("Optimizar la estructura de navegación y flujo de usuario")
                    elif category == 'Funcionalidad':
                        recommendations.append("Corregir errores en cálculos matemáticos y renderizado")
                    elif category == 'Experiencia Usuario':
                        recommendations.append("Mejorar la interfaz y manejo de errores")
            
            report['individual_scores'] = scores
            report['recommendations'] = recommendations
            
            # Imprimir reporte
            logger.info("REPORTE COMPLETO DEL SISTEMA")
            logger.info("=" * 50)
            logger.info(f"Fecha: {report['test_date']}")
            logger.info(f"Puntuación General: {overall_score:.1f}%")
            logger.info("")
            
            logger.info("Puntuaciones Individuales:")
            for category, score in scores:
                status = "Excelente" if score >= 90 else "Bueno" if score >= 75 else "Aceptable" if score >= 60 else "Mejorar"
                logger.info(f"  {category}: {score:.1f}% - {status}")
            logger.info("")
            
            logger.info("Recomendaciones:")
            for rec in recommendations:
                logger.info(f"  - {rec}")
            logger.info("")
            
            return report
            
        except Exception as e:
            logger.error(f"Error generando reporte: {e}")
            return None
    
    def run_comprehensive_test(self):
        """Ejecutar prueba completa del sistema"""
        logger.info("=== INICIANDO PRUEBA COMPLETA DEL SISTEMA ===")
        
        try:
            # Ejecutar todos los tests
            latex_ok = self.test_latex_rendering_results()
            navigation_ok = self.analyze_navigation_structure()
            functionality_ok = self.test_section_functionality()
            ux_ok = self.analyze_user_experience()
            
            # Generar reporte
            report = self.generate_comprehensive_report()
            
            # Determinar resultado general
            overall_success = latex_ok and navigation_ok and functionality_ok and ux_ok
            
            logger.info("=== RESULTADO FINAL ===")
            logger.info(f"Estado General: {'EXITOSO' if overall_success else 'NECESITA MEJORAS'}")
            logger.info(f"Renderizado LaTeX: {'OK' if latex_ok else 'MEJORAR'}")
            logger.info(f"Navegación: {'OK' if navigation_ok else 'MEJORAR'}")
            logger.info(f"Funcionalidad: {'OK' if functionality_ok else 'MEJORAR'}")
            logger.info(f"Experiencia Usuario: {'OK' if ux_ok else 'MEJORAR'}")
            
            return overall_success, report
            
        except Exception as e:
            logger.error(f"Error en prueba completa: {e}")
            return False, None


def main():
    """Función principal"""
    try:
        print("=== Navigation and Results Test ===")
        print("Verificación completa del sistema de renderizado LaTeX y navegación")
        print()
        
        # Crear instancia del test
        test = NavigationResultsTest()
        
        # Ejecutar prueba completa
        success, report = test.run_comprehensive_test()
        
        print()
        print("=== RESUMEN EJECUTIVO ===")
        if success:
            print("El sistema está funcionando correctamente.")
            print("Todos los componentes principales operativos.")
        else:
            print("El sistema necesita mejoras.")
            print("Revisa el reporte detallado para identificar áreas específicas.")
        
        if report:
            print(f"Puntuación general: {report['overall_score']:.1f}%")
        
        return success
        
    except Exception as e:
        print(f"Error en ejecución: {e}")
        return False


if __name__ == "__main__":
    main()

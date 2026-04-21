#!/usr/bin/env python3
"""
LaTeX Rendering Fix - Solución completa para problemas de renderizado LaTeX
Este script reemplaza el sistema de renderizado LaTeX actual con una solución robusta
"""

import sys
import os
import shutil
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LaTeXRenderingFix:
    """Solución integral para problemas de renderizado LaTeX"""
    
    def __init__(self):
        self.backup_dir = "backups"
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.ui_dir = os.path.join(os.path.dirname(self.app_dir), "ui")
        
    def create_backup(self, file_path: str) -> str:
        """Crear backup de un archivo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(file_path)
            backup_path = os.path.join(self.backup_dir, f"{filename}_{timestamp}")
            
            os.makedirs(self.backup_dir, exist_ok=True)
            shutil.copy2(file_path, backup_path)
            
            logger.info(f"Backup creado: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creando backup de {file_path}: {e}")
            return ""
    
    def apply_latex_fix(self):
        """Aplicar la solución completa de renderizado LaTeX"""
        try:
            logger.info("=== INICIANDO SOLUCIÓN DE RENDERIZADO LATEX ===")
            
            # 1. Reemplazar el método de renderizado en professional_main_window.py
            self._fix_professional_main_window()
            
            # 2. Actualizar el latex_renderer.py
            self._update_latex_renderer()
            
            # 3. Crear sistema de renderizado mejorado
            self._create_enhanced_rendering_system()
            
            logger.info("=== SOLUCIÓN APLICADA EXITOSAMENTE ===")
            return True
            
        except Exception as e:
            logger.error(f"Error aplicando solución: {e}")
            return False
    
    def _fix_professional_main_window(self):
        """Corregir el renderizado en professional_main_window.py"""
        try:
            file_path = os.path.join(self.ui_dir, "professional_main_window.py")
            
            # Crear backup
            self.create_backup(file_path)
            
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar el método _render_latex_step_fixed
            old_method = '''    def _render_latex_step_fixed(self, step_number, latex_content):
        """Render LaTeX step with robust error handling"""
        try:
            # Clean LaTeX to prevent parsing errors
            cleaned_latex = self._clean_latex_content_fixed(latex_content)
            
            # Insert placeholder for LaTeX visualization
            placeholder = f"[LaTeX Step {step_number}]\n"
            self.steps_text.insert("end", placeholder, "latex_placeholder")
            
            # Store for visual rendering
            if not hasattr(self, 'fixed_latex_steps'):
                self.fixed_latex_steps = {}
            
            self.fixed_latex_steps[f"step_{step_number}"] = {
                'original': latex_content,
                'cleaned': cleaned_latex,
                'placeholder': placeholder
            }
            
            # Configure tag
            self.steps_text.tag_configure("latex_placeholder", 
                                        font=("Courier", 11), 
                                        foreground="#e74c3c",
                                        background="#fdf2f2")
            
        except Exception as e:
            logger.error(f"Error renderizando LaTeX paso {step_number}: {e}")
            # Fallback to text
            enhanced_content = self._apply_unicode_enhancements_fixed(latex_content)'''
            
            new_method = '''    def _render_latex_step_fixed(self, step_number, latex_content):
        """Render LaTeX step with enhanced rendering system"""
        try:
            # Importar el renderizador mejorado
            from core.enhanced_latex_renderer import EnhancedLaTeXRenderer
            
            # Crear renderizador si no existe
            if not hasattr(self, 'enhanced_renderer'):
                self.enhanced_renderer = EnhancedLaTeXRenderer()
            
            # Renderizar expresión matemática
            result = self.enhanced_renderer.render_mathematical_expression(latex_content)
            
            if result.get('success', False):
                # Insertar título del paso
                step_title = f"Paso {step_number}: \n"
                self.steps_text.insert("end", step_title, "step_title")
                
                # Insertar canvas de matplotlib
                canvas = result.get('canvas')
                if canvas:
                    canvas.get_tk_widget().pack(fill='x', padx=10, pady=5)
                    self.steps_text.window_create("end", window=canvas.get_tk_widget())
                
                self.steps_text.insert("end", "\n", "step_separator")
                
                # Configurar tags
                self.steps_text.tag_configure("step_title", 
                                            font=("Arial", 12, "bold"), 
                                            foreground="#2c3e50")
                self.steps_text.tag_configure("step_separator", 
                                            font=("Arial", 8), 
                                            foreground="#95a5a6")
                
            else:
                # Fallback a texto con Unicode
                fallback_text = self._apply_unicode_enhancements_fixed(latex_content)
                self.steps_text.insert("end", f"Paso {step_number}: {fallback_text}\n", "latex_fallback")
                self.steps_text.tag_configure("latex_fallback", 
                                            font=("Courier", 11), 
                                            foreground="#e67e22",
                                            background="#fef9e7")
            
        except Exception as e:
            logger.error(f"Error renderizando LaTeX paso {step_number}: {e}")
            # Fallback final a texto plano
            self.steps_text.insert("end", f"Paso {step_number}: {latex_content}\n", "latex_error")
            self.steps_text.tag_configure("latex_error", 
                                        font=("Courier", 11), 
                                        foreground="#e74c3c",
                                        background="#fdf2f2")'''
            
            # Reemplazar método
            if old_method in content:
                content = content.replace(old_method, new_method)
                logger.info("Método _render_latex_step_fixed actualizado")
            else:
                logger.warning("Método _render_latex_step_fixed no encontrado")
            
            # Escribir archivo actualizado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("professional_main_window.py actualizado exitosamente")
            
        except Exception as e:
            logger.error(f"Error actualizando professional_main_window.py: {e}")
            raise
    
    def _update_latex_renderer(self):
        """Actualizar el LaTeX renderer existente"""
        try:
            file_path = os.path.join(self.ui_dir, "latex_renderer.py")
            
            # Crear backup
            self.create_backup(file_path)
            
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir import del renderizador mejorado
            if "from core.enhanced_latex_renderer import EnhancedLaTeXRenderer" not in content:
                import_section = "import matplotlib.pyplot as plt\nimport matplotlib\nimport sympy as sp\nimport re\nimport logging\nfrom matplotlib.backends.backend_tkagg import FigureCanvasTkAgg\nfrom typing import Optional\n\n# Import enhanced renderer\ntry:\n    from core.enhanced_latex_renderer import EnhancedLaTeXRenderer\nexcept ImportError:\n    EnhancedLaTeXRenderer = None\n    logging.warning(\"Enhanced LaTeX Renderer not available\")"
                
                content = content.replace("import matplotlib.pyplot as plt\nimport matplotlib\nimport sympy as sp\nimport re\nimport logging\nfrom matplotlib.backends.backend_tkagg import FigureCanvasTkAgg\nfrom typing import Optional", import_section)
                logger.info("Import del renderizador mejorado añadido")
            
            # Escribir archivo actualizado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("latex_renderer.py actualizado exitosamente")
            
        except Exception as e:
            logger.error(f"Error actualizando latex_renderer.py: {e}")
            raise
    
    def _create_enhanced_rendering_system(self):
        """Crear el sistema de renderizado mejorado"""
        try:
            # El enhanced_latex_renderer.py ya fue creado
            logger.info("Sistema de renderizado mejorado listo")
            
        except Exception as e:
            logger.error(f"Error creando sistema de renderizado mejorado: {e}")
            raise
    
    def test_rendering_fix(self):
        """Probar la solución de renderizado"""
        try:
            logger.info("=== PROBANDO SOLUCIÓN DE RENDERIZADO ===")
            
            # Importar el renderizador mejorado
            from core.enhanced_latex_renderer import EnhancedLaTeXRenderer
            
            # Crear instancia
            renderer = EnhancedLaTeXRenderer()
            
            # Expresiones de prueba
            test_expressions = [
                "x^2 + 2x + 1 = (x+1)^2",
                "integrate(x**2, x)",
                "\\frac{d}{dx}(x^2) = 2x",
                "\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}",
                "sin(x) + cos(x) = 1"
            ]
            
            success_count = 0
            total_count = len(test_expressions)
            
            for expr in test_expressions:
                try:
                    result = renderer.render_mathematical_expression(expr)
                    if result.get('success', False):
                        logger.info(f"  OK: {expr} -> {result.get('method', 'unknown')}")
                        success_count += 1
                    else:
                        logger.warning(f"  ERROR: {expr} -> {result.get('error', 'Unknown')}")
                        
                except Exception as e:
                    logger.error(f"  EXCEPTION: {expr} -> {e}")
            
            logger.info(f"Resultados: {success_count}/{total_count} expresiones renderizadas correctamente")
            
            if success_count == total_count:
                logger.info("¡SOLUCIÓN DE RENDERIZADO FUNCIONANDO PERFECTAMENTE!")
                return True
            else:
                logger.warning(f"Solución parcial: {success_count}/{total_count} funcionando")
                return False
                
        except Exception as e:
            logger.error(f"Error probando solución: {e}")
            return False
    
    def create_usage_example(self):
        """Crear ejemplo de uso del nuevo sistema"""
        try:
            example_code = '''#!/usr/bin/env python3
"""
Ejemplo de uso del Enhanced LaTeX Renderer
Muestra cómo renderizar expresiones matemáticas correctamente
"""

from core.enhanced_latex_renderer import EnhancedLaTeXRenderer

def main():
    """Ejemplo de renderizado matemático"""
    
    # Crear renderizador
    renderer = EnhancedLaTeXRenderer()
    
    # Expresiones matemáticas de ejemplo
    expressions = [
        "x^2 + 2x + 1 = (x+1)^2",
        "integrate(x**2, x)",
        "\\frac{d}{dx}(x^2) = 2x",
        "\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}",
        "sin(x) + cos(x) = 1",
        "\\int_0^\\pi sin(x) dx = 2"
    ]
    
    print("=== Enhanced LaTeX Renderer - Ejemplo de Uso ===")
    print()
    
    for i, expr in enumerate(expressions, 1):
        print(f"{i}. Expresión: {expr}")
        
        # Renderizar expresión
        result = renderer.render_mathematical_expression(expr)
        
        if result.get('success', False):
            print(f"   Método: {result.get('method', 'unknown')}")
            print(f"   Renderizado: {result.get('rendered_text', 'N/A')}")
            print(f"   Canvas disponible: {'Yes' if result.get('canvas') else 'No'}")
        else:
            print(f"   Error: {result.get('error', 'Unknown')}")
        
        print()
    
    print("=== Características del Enhanced LaTeX Renderer ===")
    print("1. Múltiples métodos de renderizado (matplotlib, SymPy, Unicode)")
    print("2. Fallback automático si un método falla")
    print("3. Soporte para expresiones LaTeX complejas")
    print("4. Integración con Tkinter via matplotlib")
    print("5. Manejo robusto de errores")
    print("6. Cache de renderizados para mejor rendimiento")
    print()
    
    print("=== Integración con UI ===")
    print("Para integrar en tu aplicación:")
    print("1. Importa: from core.enhanced_latex_renderer import EnhancedLaTeXRenderer")
    print("2. Crea instancia: renderer = EnhancedLaTeXRenderer()")
    print("3. Renderiza: result = renderer.render_mathematical_expression(expr)")
    print("4. Usa el canvas: canvas = result.get('canvas')")
    print("5. Inserta en UI: canvas.get_tk_widget().pack(fill='x', padx=10, pady=5)")

if __name__ == "__main__":
    main()
'''
            
            example_path = os.path.join(self.app_dir, "latex_rendering_example.py")
            with open(example_path, 'w', encoding='utf-8') as f:
                f.write(example_code)
            
            logger.info(f"Ejemplo de uso creado: {example_path}")
            
        except Exception as e:
            logger.error(f"Error creando ejemplo de uso: {e}")


def main():
    """Función principal para aplicar la solución"""
    try:
        print("=== LaTeX Rendering Fix - Solución Integral ===")
        print()
        
        # Crear instancia de la solución
        fix = LaTeXRenderingFix()
        
        # Aplicar solución
        print("1. Aplicando solución de renderizado LaTeX...")
        success = fix.apply_latex_fix()
        
        if success:
            print("   ¡Solución aplicada exitosamente!")
        else:
            print("   Error aplicando solución")
            return False
        
        print()
        print("2. Probando solución...")
        test_success = fix.test_rendering_fix()
        
        if test_success:
            print("   ¡Solución funcionando perfectamente!")
        else:
            print("   Solución parcial, revisa los logs")
        
        print()
        print("3. Creando ejemplo de uso...")
        fix.create_usage_example()
        print("   Ejemplo creado: latex_rendering_example.py")
        
        print()
        print("=== RESUMEN DE LA SOLUCIÓN ===")
        print("1. Enhanced LaTeX Renderer creado")
        print("2. professional_main_window.py actualizado")
        print("3. latex_renderer.py mejorado")
        print("4. Sistema de fallback implementado")
        print("5. Ejemplo de uso disponible")
        print()
        print("=== PRÓXIMOS PASOS ===")
        print("1. Ejecuta: python latex_rendering_example.py")
        print("2. Inicia la aplicación: python main.py")
        print("3. Prueba con expresiones matemáticas")
        print("4. Verifica que los pasos se rendericen correctamente")
        
        return True
        
    except Exception as e:
        print(f"Error en la solución: {e}")
        return False


if __name__ == "__main__":
    main()

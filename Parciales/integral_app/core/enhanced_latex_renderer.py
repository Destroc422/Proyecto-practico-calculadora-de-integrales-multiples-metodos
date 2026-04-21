#!/usr/bin/env python3
"""
Enhanced LaTeX Renderer - Solución completa para renderizado matemático
Soporta múltiples métodos de renderizado: matplotlib, MathJax (web), y Unicode fallback
"""
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
import re
import logging
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional, Dict, Any, Tuple
import tkinter as tk
from tkinter import ttk

# Configurar matplotlib para mejor renderizado matemático
matplotlib.rcParams.update({
    'font.size': 16,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.titlesize': 20,
    'font.family': 'DejaVu Sans',
    'mathtext.fontset': 'dejavusans',
    'text.usetex': False,  # Desactivar TeX nativo para evitar dependencias
    'mathtext.default': 'regular'
})

logger = logging.getLogger(__name__)

# Importar métodos Unicode profesionales para máxima pulcritud
from core.professional_unicode_methods import (
    get_professional_unicode, apply_professional_style, apply_elegant_style,
    apply_technical_style, apply_academic_style, UnicodeStyle
)

# Importar gestor de perfiles Unicode
from core.unicode_profile_manager import (
    get_unicode_manager, convert_to_display, convert_to_latex, 
    convert_to_input, convert_to_calculation, set_profile,
    SymbolContext
)


class EnhancedLaTeXRenderer:
    """Renderizador LaTeX mejorado con múltiples métodos de fallback"""
    
    def __init__(self):
        """Inicializar el renderizador mejorado"""
        try:
            # Colores profesionales
            self.colors = {
                'background': '#ffffff',
                'text': '#2c3e50',
                'highlight': '#3498db',
                'success': '#27ae60',
                'warning': '#f39c12',
                'error': '#e74c3c',
                'title': '#34495e',
                'math': '#2c3e50'
            }
            
            # Cache para renderizados
            self.render_cache = {}
            
            # Configuración de métodos de renderizado
            self.render_methods = {
                'matplotlib': self._render_with_matplotlib,
                'sympy': self._render_with_sympy,
                'unicode': self._render_with_unicode
            }
            
            logger.info("Enhanced LaTeX Renderer initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Enhanced LaTeX Renderer: {e}")
            raise
    
    def render_mathematical_expression(self, expression: str, method: str = 'auto') -> Dict[str, Any]:
        """
        Renderizar expresión matemática con el mejor método disponible
        
        Args:
            expression: Expresión matemática o LaTeX
            method: Método específico ('auto', 'matplotlib', 'sympy', 'unicode')
            
        Returns:
            Diccionario con resultado del renderizado
        """
        try:
            # Limpiar expresión
            cleaned_expr = self._clean_expression(expression)
            
            # Elegir método
            if method == 'auto':
                render_method = self._choose_best_method(cleaned_expr)
            else:
                render_method = self.render_methods.get(method, self._render_with_unicode)
            
            # Intentar renderizado
            result = render_method(cleaned_expr)
            
            # Si falla, intentar fallback
            if not result.get('success', False):
                logger.warning(f"Primary method failed for: {expression}, trying fallback")
                result = self._render_with_unicode(cleaned_expr)
            
            return result
            
        except Exception as e:
            logger.error(f"Error rendering expression '{expression}': {e}")
            return self._create_error_result(expression, str(e))
    
    def _choose_best_method(self, expression: str) -> callable:
        """Elegir el mejor método de renderizado basado en la expresión"""
        
        # Si contiene LaTeX complejo, usar matplotlib
        if re.search(r'\\[a-zA-Z]+|\\begin|\\end|\{.*\}|_\{|\^\{', expression):
            return self._render_with_matplotlib
        
        # Si es expresión SymPy simple, usar SymPy
        elif self._is_sympy_expression(expression):
            return self._render_with_sympy
        
        # Default: Unicode
        else:
            return self._render_with_unicode
    
    def _render_with_matplotlib(self, expression: str) -> Dict[str, Any]:
        """Renderizar usando matplotlib con math text"""
        try:
            # Crear figura
            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            ax.set_axis_off()
            
            # Preparar LaTeX para matplotlib
            matplotlib_latex = self._prepare_for_matplotlib(expression)
            
            # Renderizar
            ax.text(0.05, 0.5, matplotlib_latex,
                   transform=ax.transAxes,
                   fontsize=16,
                   color=self.colors['math'],
                   ha='left', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", 
                            facecolor=self.colors['background'],
                            edgecolor=self.colors['highlight'],
                            alpha=0.8))
            
            # Crear canvas
            canvas = FigureCanvasTkAgg(fig, master=None)
            canvas.draw()
            
            return {
                'success': True,
                'method': 'matplotlib',
                'canvas': canvas,
                'figure': fig,
                'expression': expression,
                'rendered_text': matplotlib_latex
            }
            
        except Exception as e:
            logger.warning(f"Matplotlib rendering failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _render_with_sympy(self, expression: str) -> Dict[str, Any]:
        """Renderizar usando SymPy"""
        try:
            # Intentar parsear con SymPy
            sympy_expr = sp.sympify(expression, evaluate=False)
            
            # Crear figura
            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            ax.set_axis_off()
            
            # Obtener LaTeX de SymPy
            latex_str = sp.latex(sympy_expr)
            
            # Renderizar
            ax.text(0.05, 0.5, f'${latex_str}$',
                   transform=ax.transAxes,
                   fontsize=16,
                   color=self.colors['math'],
                   ha='left', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", 
                            facecolor=self.colors['background'],
                            edgecolor=self.colors['success'],
                            alpha=0.8))
            
            # Crear canvas
            canvas = FigureCanvasTkAgg(fig, master=None)
            canvas.draw()
            
            return {
                'success': True,
                'method': 'sympy',
                'canvas': canvas,
                'figure': fig,
                'expression': expression,
                'sympy_expr': sympy_expr,
                'rendered_text': latex_str
            }
            
        except Exception as e:
            logger.warning(f"SymPy rendering failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _render_with_unicode(self, expression: str) -> Dict[str, Any]:
        """Renderizar usando Unicode mathematical symbols"""
        try:
            # Convertir a Unicode
            unicode_text = self._convert_to_unicode(expression)
            
            # Crear figura simple
            fig, ax = plt.subplots(1, 1, figsize=(12, 2))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            ax.set_axis_off()
            
            # Renderizar texto Unicode
            ax.text(0.05, 0.5, unicode_text,
                   transform=ax.transAxes,
                   fontsize=14,
                   color=self.colors['math'],
                   ha='left', va='center',
                   bbox=dict(boxstyle="round,pad=0.3", 
                            facecolor=self.colors['background'],
                            edgecolor=self.colors['warning'],
                            alpha=0.8))
            
            # Crear canvas
            canvas = FigureCanvasTkAgg(fig, master=None)
            canvas.draw()
            
            return {
                'success': True,
                'method': 'unicode',
                'canvas': canvas,
                'figure': fig,
                'expression': expression,
                'rendered_text': unicode_text
            }
            
        except Exception as e:
            logger.error(f"Unicode rendering failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _prepare_for_matplotlib(self, expression: str) -> str:
        """Preparar expresión para matplotlib math text"""
        try:
            # Limpiar y preparar
            cleaned = expression.strip()
            
            # Reemplazar comandos LaTeX comunes
            replacements = [
                (r'\\int', r'\int'),
                (r'\\sum', r'\sum'),
                (r'\\prod', r'\prod'),
                (r'\\frac{([^}]+)}{([^}]+)}', r'\frac{\1}{\2}'),
                (r'\\sqrt{([^}]+)}', r'\sqrt{\1}'),
                (r'\\infty', r'\infty'),
                (r'\\pi', r'\pi'),
                (r'\\alpha', r'\alpha'),
                (r'\\beta', r'\beta'),
                (r'\\gamma', r'\gamma'),
                (r'\\delta', r'\delta'),
                (r'\\theta', r'\theta'),
                (r'\\lambda', r'\lambda'),
                (r'\\mu', r'\mu'),
                (r'\\sigma', r'\sigma'),
                (r'\\phi', r'\phi'),
                (r'\\omega', r'\omega'),
                (r'\\sin', r'\sin'),
                (r'\\cos', r'\cos'),
                (r'\\tan', r'\tan'),
                (r'\\log', r'\log'),
                (r'\\ln', r'\ln'),
                (r'\\exp', r'\exp'),
                (r'\*\*', '^'),
                (r'\^', '^'),
                (r'_', '_')
            ]
            
            # Aplicar reemplazos
            for pattern, replacement in replacements:
                cleaned = re.sub(pattern, replacement, cleaned)
            
            # Envolver en $$ si no está envuelto
            if not cleaned.startswith('$$') and not cleaned.startswith('$'):
                cleaned = f'${cleaned}$'
            
            return cleaned
            
        except Exception as e:
            logger.warning(f"Error preparing for matplotlib: {e}")
            return expression
    
    def _convert_to_unicode(self, expression: str) -> str:
        """Convertir expresión a Unicode mathematical symbols"""
        try:
            unicode_expr = expression
            
            # Reemplazos matemáticos comunes
            replacements = {
                'integrate': 'integral',
                '**2': '²',
                '**3': '³',
                '**4': '³',
                '**5': '³',
                '**6': '³',
                '**7': '³',
                '**8': '³',
                '**9': '³',
                '*': '×',
                'pi': 'pi',
                'sqrt(': 'sqrt(',
                'log(': 'log(',
                'ln(': 'ln(',
                'sin(': 'sin(',
                'cos(': 'cos(',
                'tan(': 'tan(',
                '1/2': '½',
                '1/3': '1/3',
                '1/4': '¼',
                '2/3': '2/3',
                '3/4': '¾',
                'infinity': 'infinity',
                '->': '->',
                '<=': '<=',
                '>=': '>='
            }
            
            # Aplicar reemplazos
            for old, new in replacements.items():
                unicode_expr = unicode_expr.replace(old, new)
            
            return unicode_expr
            
        except Exception as e:
            logger.warning(f"Error converting to Unicode: {e}")
            return expression
    
    def _is_sympy_expression(self, expression: str) -> bool:
        """Verificar si es una expresión SymPy válida"""
        try:
            sp.sympify(expression, evaluate=False)
            return True
        except:
            return False
    
    def _clean_expression(self, expression: str) -> str:
        """Limpiar expresión para renderizado"""
        try:
            # Eliminar espacios extra
            cleaned = re.sub(r'\s+', ' ', expression.strip())
            
            # Eliminar caracteres problemáticos
            cleaned = re.sub(r'[^\w\s\-\+\*\/\(\)\[\]\{\}\^\_\=\.<>!|\\]', '', cleaned)
            
            return cleaned
            
        except Exception as e:
            logger.warning(f"Error cleaning expression: {e}")
            return expression
    
    def _create_error_result(self, expression: str, error: str) -> Dict[str, Any]:
        """Crear resultado de error"""
        return {
            'success': False,
            'method': 'error',
            'expression': expression,
            'error': error,
            'rendered_text': f"Error: {expression}"
        }
    
    def create_step_visualization(self, step_data: Dict[str, Any]) -> Optional[FigureCanvasTkAgg]:
        """
        Crear visualización para un paso matemático
        
        Args:
            step_data: Diccionario con datos del paso
            
        Returns:
            Canvas de matplotlib o None si falla
        """
        try:
            # Obtener contenido matemático
            math_content = step_data.get('latex', '') or step_data.get('content', '')
            
            if not math_content:
                logger.warning("No mathematical content found in step data")
                return None
            
            # Renderizar
            result = self.render_mathematical_expression(math_content)
            
            if result.get('success', False):
                return result.get('canvas')
            else:
                logger.warning(f"Failed to render step: {result.get('error', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating step visualization: {e}")
            return None
    
    def render_multiple_steps(self, steps_data: Dict[str, Dict[str, Any]]) -> Dict[str, FigureCanvasTkAgg]:
        """
        Renderizar múltiples pasos matemáticos
        
        Args:
            steps_data: Diccionario de datos de pasos
            
        Returns:
            Diccionario de canvases renderizados
        """
        rendered_steps = {}
        
        for step_key, step_data in steps_data.items():
            try:
                canvas = self.create_step_visualization(step_data)
                if canvas:
                    rendered_steps[step_key] = canvas
                else:
                    logger.warning(f"Failed to render step {step_key}")
                    
            except Exception as e:
                logger.error(f"Error rendering step {step_key}: {e}")
        
        logger.info(f"Successfully rendered {len(rendered_steps)}/{len(steps_data)} steps")
        return rendered_steps


# Función de conveniencia para crear renderizador

    def _convert_to_unicode_enhanced(self, expression: str) -> str:
        """Enhanced Unicode conversion with professional pulcritud"""
        try:
            from core.professional_unicode_methods import apply_elegant_style
            return apply_elegant_style(expression)
        except Exception as e:
            logger.error(f"Error in enhanced Unicode conversion: {e}")
            return expression

def create_enhanced_renderer() -> EnhancedLaTeXRenderer:
    """Crear instancia del renderizador mejorado"""
    return EnhancedLaTeXRenderer()


# Ejemplo de uso
if __name__ == "__main__":
    # Test del renderizador
    renderer = EnhancedLaTeXRenderer()
    
    # Expresiones de prueba
    test_expressions = [
        "x^2 + 2x + 1 = (x+1)^2",
        "integrate(x**2, x)",
        "\\frac{d}{dx}(x^2) = 2x",
        "\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}",
        "sin(x) + cos(x) = 1"
    ]
    
    print("=== Enhanced LaTeX Renderer Test ===")
    print()
    
    for expr in test_expressions:
        print(f"Expression: {expr}")
        result = renderer.render_mathematical_expression(expr)
        print(f"Method: {result.get('method', 'unknown')}")
        print(f"Success: {result.get('success', False)}")
        print(f"Rendered: {result.get('rendered_text', 'N/A')}")
        print("-" * 50)

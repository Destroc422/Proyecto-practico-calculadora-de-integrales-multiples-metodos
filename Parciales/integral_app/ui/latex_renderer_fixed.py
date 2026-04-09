"""
Professional LaTeX Renderer - Single, optimized implementation
High-quality mathematical rendering without LaTeX dependencies
"""
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
import re
import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional

# Configure matplotlib for professional rendering
matplotlib.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'font.family': 'DejaVu Sans',
    'mathtext.fontset': 'dejavusans'
})

logger = logging.getLogger(__name__)


class ProfessionalLaTeXRenderer:
    """Professional LaTeX renderer with enhanced visual quality"""
    
    def __init__(self):
        """Initialize the renderer"""
        try:
            # Professional color scheme
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
            
            # Active canvases for cleanup
            self.active_canvases = {}
            
            logger.info("Professional LaTeX renderer initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LaTeX renderer: {str(e)}")
            raise
    
    def render_expression(self, expression, title: str = "", color: str = None, fontsize: int = 16):
        """
        Render a mathematical expression with professional formatting
        
        Args:
            expression: SymPy expression or LaTeX string
            title: Optional title
            color: Optional color
            fontsize: Font size
            
        Returns:
            matplotlib Figure
        """
        try:
            # Create figure with better proportions
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes for clean display
            ax.set_axis_off()
            
            # Convert expression to professional display format
            display_text = self._convert_to_professional_format(expression, title)
            
            # Set color
            text_color = color or self.colors['math']
            
            # Display title if provided
            if title:
                ax.text(0.5, 0.85, title, transform=ax.transAxes,
                       fontsize=fontsize+4, ha='center', va='center', 
                       color=self.colors['title'], weight='bold')
            
            # Display the main expression
            ax.text(0.5, 0.5, display_text, transform=ax.transAxes,
                   fontsize=fontsize+2, ha='center', va='center', 
                   color=text_color, family='DejaVu Sans', weight='normal')
            
            # Add subtle border
            rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, 
                               transform=ax.transAxes, 
                               fill=False, 
                               edgecolor=self.colors['text'], 
                               linewidth=0.5, 
                               alpha=0.3)
            ax.add_patch(rect)
            
            plt.tight_layout(pad=2.0)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering expression: {str(e)}")
            return self._render_error_text(str(e))
    
    def render_preview(self, expression: str):
        """
        Render a preview of an expression with compact formatting
        
        Args:
            expression: Raw expression string
            
        Returns:
            matplotlib Figure
        """
        try:
            # Create compact figure for preview
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes
            ax.set_axis_off()
            
            # Convert to professional format
            display_text = self._convert_to_professional_format(expression)
            
            # Display the expression
            ax.text(0.5, 0.5, display_text, transform=ax.transAxes,
                   fontsize=14, ha='center', va='center', 
                   color=self.colors['math'], family='DejaVu Sans')
            
            # Add subtle frame
            rect = plt.Rectangle((0.01, 0.01), 0.98, 0.98, 
                               transform=ax.transAxes, 
                               fill=False, 
                               edgecolor=self.colors['text'], 
                               linewidth=0.3, 
                               alpha=0.2)
            ax.add_patch(rect)
            
            plt.tight_layout(pad=1.0)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering preview: {str(e)}")
            return self._render_error_text(str(e))
    
    def display_expression_in_frame(self, expression, frame, title: str = "", 
                                  color: str = None, fontsize: int = 16):
        """
        Display an expression in a Tkinter frame with professional formatting
        
        Args:
            expression: SymPy expression or LaTeX string
            frame: Tkinter frame to display in
            title: Optional title
            color: Optional color
            fontsize: Font size
            
        Returns:
            FigureCanvasTkAgg widget
        """
        try:
            # Clear frame completely before rendering
            self._clear_frame_completely(frame)
            
            # Render expression with professional formatting
            fig = self.render_expression(expression, title, color, fontsize)
            
            # Create canvas
            canvas = self.get_canvas_widget(fig, frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
            
            # Store for cleanup
            frame_id = str(id(frame))
            self.active_canvases[frame_id] = canvas
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error displaying expression in frame: {str(e)}")
            # Show error message as fallback
            self._show_error_in_frame(frame, str(e))
            return None
    
    def display_preview(self, expression, frame):
        """
        Display a preview of an expression with professional formatting
        
        Args:
            expression: Raw expression string
            frame: Tkinter frame
            
        Returns:
            FigureCanvasTkAgg widget
        """
        try:
            # Clear frame completely before rendering
            self._clear_frame_completely(frame)
            
            # Render preview with professional formatting
            fig = self.render_preview(expression)
            
            # Create canvas
            canvas = self.get_canvas_widget(fig, frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            
            # Store for cleanup
            frame_id = str(id(frame))
            self.active_canvases[frame_id] = canvas
            
            return canvas
            
        except Exception as e:
            logger.error(f"Error displaying preview: {str(e)}")
            # Show error message as fallback
            self._show_error_in_frame(frame, str(e))
            return None
    
    def _convert_to_professional_format(self, expression, title: str = ""):
        """
        Convert expression to professional mathematical display format
        
        Args:
            expression: SymPy expression or string
            title: Optional title
            
        Returns:
            Formatted string with proper mathematical notation
        """
        try:
            # Handle different types of expressions
            if hasattr(expression, 'latex'):
                # SymPy expression
                try:
                    latex_str = expression.latex()
                    return self._clean_latex_for_professional_display(latex_str)
                except:
                    return str(expression)
            elif isinstance(expression, str):
                # String expression
                return self._clean_latex_for_professional_display(expression)
            else:
                # Fallback to string representation
                return str(expression)
                
        except Exception as e:
            logger.error(f"Error converting to professional format: {str(e)}")
            return str(expression)
    
    def convert_to_text_format(self, expression) -> str:
        """
        Convert expression to text-based mathematical format
        
        Args:
            expression: SymPy expression or LaTeX string
            
        Returns:
            Text-formatted string suitable for plain text display
        """
        try:
            # Handle different types of expressions
            if hasattr(expression, 'latex'):
                # SymPy expression
                try:
                    latex_str = expression.latex()
                    return self._clean_latex_for_text_display(latex_str)
                except:
                    return str(expression)
            elif isinstance(expression, str):
                # String expression
                return self._clean_latex_for_text_display(expression)
            else:
                # Fallback to string representation
                return str(expression)
                
        except Exception as e:
            logger.error(f"Error converting to text format: {str(e)}")
            return str(expression)
    
    def _clean_latex_for_professional_display(self, latex_str: str) -> str:
        """
        Clean LaTeX string for professional mathematical display
        
        Args:
            latex_str: LaTeX string
            
        Returns:
            Professionally formatted string
        """
        try:
            # Professional mathematical conversions
            conversions = {
                # Powers (CRITICAL FIX for ** to ^)
                r'\*\*': '^',
                
                # Fractions
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\\dfrac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                
                # Roots
                r'\\sqrt{([^}]+)}': r'sqrt(\1)',
                r'\\sqrt\[3\]{([^}]+)}': r'cbrt(\1)',
                r'\\sqrt\[n\]{([^}]+)}': r'nroot(\1)',
                
                # Integrals
                r'\\int': 'integral',
                r'\\int_': 'integral_',
                r'\\int\^': 'integral^',
                r'\\int_{([^}]+)}\^{([^}]+)}': r'integral_{\1}^{\2}',
                r'\\int_{([^}]+)}': r'integral_{\1}',
                r'\\int\^{([^}]+)}': r'integral^{\1}',
                
                # Summation and products
                r'\\sum': 'sum',
                r'\\sum_': 'sum_',
                r'\\sum\^': 'sum^',
                r'\\prod': 'product',
                r'\\prod_': 'product_',
                r'\\prod\^': 'product^',
                
                # Constants
                r'\\pi': 'pi',
                r'\\e': 'e',
                r'\\infty': 'infinity',
                r'\\mathrm{e}': 'e',
                
                # Greek letters (lowercase)
                r'\\alpha': 'alpha',
                r'\\beta': 'beta',
                r'\\gamma': 'gamma',
                r'\\delta': 'delta',
                r'\\epsilon': 'epsilon',
                r'\\zeta': 'zeta',
                r'\\eta': 'eta',
                r'\\theta': 'theta',
                r'\\iota': 'iota',
                r'\\kappa': 'kappa',
                r'\\lambda': 'lambda',
                r'\\mu': 'mu',
                r'\\nu': 'nu',
                r'\\xi': 'xi',
                r'\\pi': 'pi',
                r'\\rho': 'rho',
                r'\\sigma': 'sigma',
                r'\\tau': 'tau',
                r'\\upsilon': 'upsilon',
                r'\\phi': 'phi',
                r'\\chi': 'chi',
                r'\\psi': 'psi',
                r'\\omega': 'omega',
                
                # Greek letters (uppercase)
                r'\\Gamma': 'Gamma',
                r'\\Delta': 'Delta',
                r'\\Theta': 'Theta',
                r'\\Lambda': 'Lambda',
                r'\\Xi': 'Xi',
                r'\\Pi': 'Pi',
                r'\\Sigma': 'Sigma',
                r'\\Upsilon': 'Upsilon',
                r'\\Phi': 'Phi',
                r'\\Psi': 'Psi',
                r'\\Omega': 'Omega',
                
                # Functions
                r'\\sin': 'sin',
                r'\\cos': 'cos',
                r'\\tan': 'tan',
                r'\\cot': 'cot',
                r'\\sec': 'sec',
                r'\\csc': 'csc',
                r'\\arcsin': 'arcsin',
                r'\\arccos': 'arccos',
                r'\\arctan': 'arctan',
                r'\\sinh': 'sinh',
                r'\\cosh': 'cosh',
                r'\\tanh': 'tanh',
                r'\\log': 'log',
                r'\\ln': 'ln',
                r'\\lg': 'lg',
                r'\\exp': 'exp',
                r'\\sqrt': 'sqrt',
                r'\\abs': 'abs',
                r'\\mathrm{abs}': 'abs',
                
                # Operators and symbols (text format)
                r'\\le': '<=',
                r'\\ge': '>=',
                r'\\ne': '!=',
                r'\\neq': '!=',
                r'\\approx': 'approx',
                r'\\sim': 'sim',
                r'\\simeq': 'simeq',
                r'\\cong': 'cong',
                r'\\equiv': 'equiv',
                r'\\propto': 'propto',
                r'\\pm': '+/-',
                r'\\mp': '-/+',
                r'\\times': '*',
                r'\\div': '/',
                r'\\cdot': '*',
                r'\\circ': 'circ',
                r'\\oplus': 'oplus',
                r'\\otimes': 'otimes',
                r'\\wedge': 'and',
                r'\\vee': 'or',
                r'\\neg': 'not',
                r'\\implies': '=>',
                r'\\iff': '<=>',
                
                # Calculus (text format)
                r'\\partial': 'partial',
                r'\\nabla': 'nabla',
                r'\\Delta': 'Delta',
                r'\\delta': 'delta',
                
                # Sets (text format)
                r'\\cup': 'union',
                r'\\cap': 'intersection',
                r'\\subset': 'subset',
                r'\\supset': 'superset',
                r'\\subseteq': 'subseteq',
                r'\\supseteq': 'superseteq',
                r'\\in': 'in',
                r'\\notin': 'notin',
                r'\\ni': 'contains',
                r'\\emptyset': 'empty',
                r'\\varnothing': 'empty',
                
                # Number sets (text format)
                r'\\mathbb{R}': 'Real',
                r'\\mathbb{Z}': 'Integer',
                r'\\mathbb{N}': 'Natural',
                r'\\mathbb{C}': 'Complex',
                r'\\mathbb{Q}': 'Rational',
                r'\\mathbb{H}': 'Quaternion',
                
                # Parentheses and brackets
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\\[': '[',
                r'\\right\\]': ']',
                r'\\left\\{': '{',
                r'\\right\\}': '}',
                r'\\langle': '<',
                r'\\rangle': '>',
                
                # Spaces and formatting
                r'\\,': ' ',
                r'\\;': '  ',
                r'\\!': '',
                r'\\&': '  ',
                r'\\\\': '\n',
                r'\\quad': '    ',
                r'\\qquad': '        ',
                
                # Text formatting
                r'\\text{([^}]+)}': r'\1',
                r'\\mathrm{([^}]+)}': r'\1',
                r'\\mathit{([^}]+)}': r'\1',
                r'\\mathbf{([^}]+)}': r'**\1**',
                r'\\mathsf{([^}]+)}': r'\1',
                r'\\mathtt{([^}]+)}': r'\1',
                r'\\mathcal{([^}]+)}': r'cal(\1)',
                
                # Clean up any remaining backslashes
                r'\\': '',
            }
            
            # Apply conversions in order of priority
            result = latex_str
            
            # First handle complex patterns
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            # Handle special cases for powers
            result = re.sub(r'([a-zA-Z])\^([0-9]+)', r'\1^\2', result)
            result = re.sub(r'([a-zA-Z])\^({[^}]+})', r'\1^\2', result)
            
            # Handle subscripts
            result = re.sub(r'([a-zA-Z])_([0-9]+)', r'\1_\2', result)
            result = re.sub(r'([a-zA-Z])_({[^}]+})', r'\1_\2', result)
            
            # Clean up extra spaces
            result = re.sub(r'\s+', ' ', result)
            result = result.strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX for professional display: {str(e)}")
            return latex_str
    
    def _clean_latex_for_text_display(self, latex_str: str) -> str:
        """
        Clean LaTeX string for text-based mathematical display
        
        Args:
            latex_str: LaTeX string
            
        Returns:
            Text-formatted string suitable for plain text display
        """
        try:
            # Text-based mathematical conversions
            conversions = {
                # Powers (Keep ** for text clarity)
                r'\*\*': '^',
                
                # Fractions (text format)
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\\dfrac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                
                # Roots (text format)
                r'\\sqrt{([^}]+)}': r'sqrt(\1)',
                r'\\sqrt\[3\]{([^}]+)}': r'cbrt(\1)',
                r'\\sqrt\[n\]{([^}]+)}': r'nroot(\1)',
                
                # Integrals (text format)
                r'\\int': 'integral',
                r'\\int_': 'integral_',
                r'\\int\^': 'integral^',
                r'\\int_{([^}]+)}\^{([^}]+)}': r'integral_{\1}^{\2}',
                r'\\int_{([^}]+)}': r'integral_{\1}',
                r'\\int\^{([^}]+)}': r'integral^{\1}',
                
                # Summation and products (text format)
                r'\\sum': 'sum',
                r'\\sum_': 'sum_',
                r'\\sum\^': 'sum^',
                r'\\prod': 'product',
                r'\\prod_': 'product_',
                r'\\prod\^': 'product^',
                
                # Constants (text format)
                r'\\pi': 'pi',
                r'\\e': 'e',
                r'\\infty': 'infinity',
                r'\\mathrm{e}': 'e',
                
                # Greek letters (lowercase)
                r'\\alpha': 'alpha',
                r'\\beta': 'beta',
                r'\\gamma': 'gamma',
                r'\\delta': 'delta',
                r'\\epsilon': 'epsilon',
                r'\\zeta': 'zeta',
                r'\\eta': 'eta',
                r'\\theta': 'theta',
                r'\\iota': 'iota',
                r'\\kappa': 'kappa',
                r'\\lambda': 'lambda',
                r'\\mu': 'mu',
                r'\\nu': 'nu',
                r'\\xi': 'xi',
                r'\\pi': 'pi',
                r'\\rho': 'rho',
                r'\\sigma': 'sigma',
                r'\\tau': 'tau',
                r'\\upsilon': 'upsilon',
                r'\\phi': 'phi',
                r'\\chi': 'chi',
                r'\\psi': 'psi',
                r'\\omega': 'omega',
                
                # Greek letters (uppercase)
                r'\\Gamma': 'Gamma',
                r'\\Delta': 'Delta',
                r'\\Theta': 'Theta',
                r'\\Lambda': 'Lambda',
                r'\\Xi': 'Xi',
                r'\\Pi': 'Pi',
                r'\\Sigma': 'Sigma',
                r'\\Upsilon': 'Upsilon',
                r'\\Phi': 'Phi',
                r'\\Psi': 'Psi',
                r'\\Omega': 'Omega',
                
                # Functions
                r'\\sin': 'sin',
                r'\\cos': 'cos',
                r'\\tan': 'tan',
                r'\\cot': 'cot',
                r'\\sec': 'sec',
                r'\\csc': 'csc',
                r'\\arcsin': 'arcsin',
                r'\\arccos': 'arccos',
                r'\\arctan': 'arctan',
                r'\\sinh': 'sinh',
                r'\\cosh': 'cosh',
                r'\\tanh': 'tanh',
                r'\\log': 'log',
                r'\\ln': 'ln',
                r'\\lg': 'lg',
                r'\\exp': 'exp',
                r'\\sqrt': 'sqrt',
                r'\\abs': 'abs',
                r'\\mathrm{abs}': 'abs',
                
                # Operators and symbols (text format)
                r'\\le': '<=',
                r'\\ge': '>=',
                r'\\ne': '!=',
                r'\\neq': '!=',
                r'\\approx': 'approx',
                r'\\sim': 'sim',
                r'\\simeq': 'simeq',
                r'\\cong': 'cong',
                r'\\equiv': 'equiv',
                r'\\propto': 'propto',
                r'\\pm': '+/-',
                r'\\mp': '-/+',
                r'\\times': '*',
                r'\\div': '/',
                r'\\cdot': '*',
                r'\\circ': 'circ',
                r'\\oplus': 'oplus',
                r'\\otimes': 'otimes',
                r'\\wedge': 'and',
                r'\\vee': 'or',
                r'\\neg': 'not',
                r'\\implies': '=>',
                r'\\iff': '<=>',
                
                # Calculus (text format)
                r'\\partial': 'partial',
                r'\\nabla': 'nabla',
                r'\\Delta': 'Delta',
                r'\\delta': 'delta',
                
                # Sets (text format)
                r'\\cup': 'union',
                r'\\cap': 'intersection',
                r'\\subset': 'subset',
                r'\\supset': 'superset',
                r'\\subseteq': 'subseteq',
                r'\\supseteq': 'superseteq',
                r'\\in': 'in',
                r'\\notin': 'notin',
                r'\\ni': 'contains',
                r'\\emptyset': 'empty',
                r'\\varnothing': 'empty',
                
                # Number sets (text format)
                r'\\mathbb{R}': 'Real',
                r'\\mathbb{Z}': 'Integer',
                r'\\mathbb{N}': 'Natural',
                r'\\mathbb{C}': 'Complex',
                r'\\mathbb{Q}': 'Rational',
                r'\\mathbb{H}': 'Quaternion',
                
                # Parentheses and brackets
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\\[': '[',
                r'\\right\\]': ']',
                r'\\left\\{': '{',
                r'\\right\\}': '}',
                r'\\langle': '<',
                r'\\rangle': '>',
                
                # Spaces and formatting
                r'\\,': ' ',
                r'\\;': '  ',
                r'\\!': '',
                r'\\&': '  ',
                r'\\\\': '\n',
                r'\\quad': '    ',
                r'\\qquad': '        ',
                
                # Text formatting
                r'\\text{([^}]+)}': r'\1',
                r'\\mathrm{([^}]+)}': r'\1',
                r'\\mathit{([^}]+)}': r'\1',
                r'\\mathbf{([^}]+)}': r'**\1**',
                r'\\mathsf{([^}]+)}': r'\1',
                r'\\mathtt{([^}]+)}': r'\1',
                r'\\mathcal{([^}]+)}': r'cal(\1)',
                
                # Clean up any remaining backslashes
                r'\\': '',
            }
            
            # Apply conversions in order of priority
            result = latex_str
            
            # First handle complex patterns
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            # Handle special cases for powers
            result = re.sub(r'([a-zA-Z])\^([0-9]+)', r'\1^\2', result)
            result = re.sub(r'([a-zA-Z])\^({[^}]+})', r'\1^\2', result)
            
            # Handle subscripts
            result = re.sub(r'([a-zA-Z])_([0-9]+)', r'\1_\2', result)
            result = re.sub(r'([a-zA-Z])_({[^}]+})', r'\1_\2', result)
            
            # Clean up extra spaces
            result = re.sub(r'\s+', ' ', result)
            result = result.strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX for text display: {str(e)}")
            return latex_str
    
    def _render_error_text(self, error_msg: str) -> plt.Figure:
        """Render an error message with professional formatting"""
        try:
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes
            ax.set_axis_off()
            
            # Error message with professional formatting
            ax.text(0.5, 0.5, f'Error: {error_msg}', transform=ax.transAxes,
                   fontsize=14, ha='center', va='center', 
                   color=self.colors['error'], family='DejaVu Sans')
            
            # Add border
            rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, 
                               transform=ax.transAxes, 
                               fill=False, 
                               edgecolor=self.colors['error'], 
                               linewidth=1, 
                               alpha=0.5)
            ax.add_patch(rect)
            
            plt.tight_layout(pad=2.0)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering error text: {str(e)}")
            # Create minimal fallback figure
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.set_axis_off()
            return fig
    
    def get_canvas_widget(self, figure: plt.Figure, parent):
        """
        Get a canvas widget from a figure for embedding in Tkinter
        
        Args:
            figure: matplotlib Figure
            parent: Parent widget
            
        Returns:
            FigureCanvasTkAgg widget
        """
        try:
            canvas = FigureCanvasTkAgg(figure, parent)
            canvas.draw()
            return canvas
        except Exception as e:
            logger.error(f"Error creating canvas widget: {str(e)}")
            raise
    
    def clear_canvas(self, canvas_widget):
        """Clear a canvas widget"""
        try:
            if canvas_widget:
                canvas_widget.get_tk_widget().destroy()
        except Exception as e:
            logger.error(f"Error clearing canvas: {str(e)}")
    
    def _clear_frame_completely(self, frame):
        """Clear frame completely - this is the critical fix"""
        try:
            # Destroy all widgets in the frame
            for widget in frame.winfo_children():
                widget.destroy()
            
            # Clear canvas tracking
            frame_id = str(id(frame))
            if frame_id in self.active_canvases:
                del self.active_canvases[frame_id]
                
        except Exception as e:
            logger.error(f"Error clearing frame completely: {str(e)}")
    
    def _show_error_in_frame(self, frame, error_msg):
        """Show error message in frame as fallback"""
        try:
            # Clear frame first
            self._clear_frame_completely(frame)
            
            # Create error label
            error_label = tk.Label(frame, 
                                text=f"Error: {error_msg}",
                                font=('Segoe UI', 10),
                                fg=self.colors['error'], 
                                bg=self.colors['background'],
                                wraplength=400,
                                justify=tk.CENTER)
            error_label.pack(expand=True)
            
        except Exception as e:
            logger.error(f"Error showing error in frame: {str(e)}")

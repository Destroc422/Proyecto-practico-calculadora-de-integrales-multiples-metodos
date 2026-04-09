"""
Professional LaTeX Renderer - Enhanced visual quality
"""
import matplotlib.pyplot as plt
import matplotlib
import sympy as sp
import re
import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Optional

# Configure matplotlib for better text rendering
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
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            # Add subtle frame
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
                # Fractions
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\\dfrac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                
                # Roots
                r'\\sqrt{([^}]+)}': r'√(\1)',
                r'\\sqrt\[3\]{([^}]+)}': r'³√(\1)',
                r'\\sqrt\[n\]{([^}]+)}': r'ⁿ√(\1)',
                
                # Integrals
                r'\\int': '∫',
                r'\\int_': '∫',
                r'\\int\^': '∫',
                r'\\int_{([^}]+)}\^{([^}]+)}': r'∫_{\1}^{\2}',
                r'\\int_{([^}]+)}': r'∫_{\1}',
                r'\\int\^{([^}]+)}': r'∫^{\1}',
                
                # Summation and products
                r'\\sum': '∑',
                r'\\sum_': '∑',
                r'\\sum\^': '∑',
                r'\\prod': '∏',
                r'\\prod_': '∏',
                r'\\prod\^': '∏',
                
                # Constants
                r'\\pi': 'π',
                r'\\e': 'e',
                r'\\infty': '∞',
                r'\\mathrm{e}': 'e',
                
                # Greek letters (lowercase)
                r'\\alpha': 'α',
                r'\\beta': 'β',
                r'\\gamma': 'γ',
                r'\\delta': 'δ',
                r'\\epsilon': 'ε',
                r'\\zeta': 'ζ',
                r'\\eta': 'η',
                r'\\theta': 'θ',
                r'\\iota': 'ι',
                r'\\kappa': 'κ',
                r'\\lambda': 'λ',
                r'\\mu': 'μ',
                r'\\nu': 'ν',
                r'\\xi': 'ξ',
                r'\\pi': 'π',
                r'\\rho': 'ρ',
                r'\\sigma': 'σ',
                r'\\tau': 'τ',
                r'\\upsilon': 'υ',
                r'\\phi': 'φ',
                r'\\chi': 'χ',
                r'\\psi': 'ψ',
                r'\\omega': 'ω',
                
                # Greek letters (uppercase)
                r'\\Gamma': 'Γ',
                r'\\Delta': 'Δ',
                r'\\Theta': 'Θ',
                r'\\Lambda': 'Λ',
                r'\\Xi': 'Ξ',
                r'\\Pi': 'Π',
                r'\\Sigma': 'Σ',
                r'\\Upsilon': 'Υ',
                r'\\Phi': 'Φ',
                r'\\Psi': 'Ψ',
                r'\\Omega': 'Ω',
                
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
                r'\\sqrt': '√',
                r'\\abs': '|',
                r'\\mathrm{abs}': '|',
                
                # Operators and symbols
                r'\\le': '≤',
                r'\\ge': '≥',
                r'\\ne': '≠',
                r'\\neq': '≠',
                r'\\approx': '≈',
                r'\\sim': '∼',
                r'\\simeq': '≃',
                r'\\cong': '≅',
                r'\\equiv': '≡',
                r'\\propto': '∝',
                r'\\pm': '±',
                r'\\mp': '∓',
                r'\\times': '×',
                r'\\div': '÷',
                r'\\cdot': '·',
                r'\\circ': '∘',
                r'\\oplus': '⊕',
                r'\\otimes': '⊗',
                r'\\wedge': '∧',
                r'\\vee': '∨',
                r'\\neg': '¬',
                r'\\implies': '⇒',
                r'\\iff': '⇔',
                
                # Calculus
                r'\\partial': '∂',
                r'\\nabla': '∇',
                r'\\Delta': 'Δ',
                r'\\delta': 'δ',
                
                # Sets
                r'\\cup': '∪',
                r'\\cap': '∩',
                r'\\subset': '⊂',
                r'\\supset': '⊃',
                r'\\subseteq': '⊆',
                r'\\supseteq': '⊇',
                r'\\in': '∈',
                r'\\notin': '∉',
                r'\\ni': '∋',
                r'\\emptyset': '∅',
                r'\\varnothing': '∅',
                
                # Number sets
                r'\\mathbb{R}': 'ℝ',
                r'\\mathbb{Z}': 'ℤ',
                r'\\mathbb{N}': 'ℕ',
                r'\\mathbb{C}': 'ℂ',
                r'\\mathbb{Q}': 'ℚ',
                r'\\mathbb{H}': 'ℍ',
                
                # Parentheses and brackets
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\\[': '[',
                r'\\right\\]': ']',
                r'\\left\\{': '{',
                r'\\right\\}': '}',
                r'\\langle': '⟨',
                r'\\rangle': '⟩',
                
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
                r'\\mathcal{([^}]+)}': r'𝓬\1',
                
                # Powers and subscripts
                r'\^': '^',
                r'_': '_',
                
                # Clean up any remaining backslashes
                r'\\': '',
            }
            
            # Apply conversions in order of priority
            result = latex_str
            
            # First handle complex patterns
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            # Handle powers and subscripts - CRITICAL FIX for ** to ^
            result = re.sub(r'\*\*', '^', result)  # Convert ** to ^
            result = re.sub(r'([a-zA-Z])\^([0-9]+)', r'\1^\2', result)
            result = re.sub(r'([a-zA-Z])\^({[^}]+})', r'\1^\2', result)
            result = re.sub(r'([a-zA-Z])_([0-9]+)', r'\1_\2', result)
            result = re.sub(r'([a-zA-Z])_({[^}]+})', r'\1_\2', result)
            
            # Clean up extra spaces
            result = re.sub(r'\s+', ' ', result)
            result = result.strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX for professional display: {str(e)}")
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
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering error text: {str(e)}")
            # Create minimal figure
            fig, ax = plt.subplots(figsize=(10, 3))
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


class ProfessionalLaTeXDisplayManager:
    """Professional manager for LaTeX displays with enhanced visual quality"""
    
    def __init__(self):
        self.renderer = ProfessionalLaTeXRenderer()
        self.active_canvases = {}  # Track active canvases for cleanup
    
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
            # CRITICAL FIX: Clear frame completely before rendering
            self._clear_frame_completely(frame)
            
            # Render expression with professional formatting
            fig = self.renderer.render_expression(expression, title, color, fontsize)
            
            # Create canvas
            canvas = self.renderer.get_canvas_widget(fig, frame)
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
            # CRITICAL FIX: Clear frame completely before rendering
            self._clear_frame_completely(frame)
            
            # Render preview with professional formatting
            fig = self.renderer.render_preview(expression)
            
            # Create canvas
            canvas = self.renderer.get_canvas_widget(fig, frame)
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
            
            # Create error label with professional formatting
            import tkinter as tk
            from tkinter import ttk
            
            error_label = ttk.Label(frame, 
                                  text=f"❌ Error: {error_msg}",
                                  font=("Arial", 12), foreground="red")
            error_label.pack(pady=20, padx=20)
            
        except Exception as e:
            logger.error(f"Error showing error in frame: {str(e)}")
    
    def clear_frame(self, frame):
        """Clear all LaTeX displays from a frame"""
        try:
            self._clear_frame_completely(frame)
        except Exception as e:
            logger.error(f"Error clearing frame: {str(e)}")
    
    def clear_all(self):
        """Clear all active displays"""
        try:
            for canvas in self.active_canvases.values():
                if canvas:
                    self.renderer.clear_canvas(canvas)
            self.active_canvases.clear()
        except Exception as e:
            logger.error(f"Error clearing all displays: {str(e)}")


# Use the professional classes
LaTeXRenderer = ProfessionalLaTeXRenderer
LaTeXDisplayManager = ProfessionalLaTeXDisplayManager

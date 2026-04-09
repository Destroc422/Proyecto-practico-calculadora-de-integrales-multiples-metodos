"""
Working LaTeX Renderer - Fixed to work without LaTeX installation
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
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16
})

logger = logging.getLogger(__name__)


class WorkingLaTeXRenderer:
    """Working LaTeX renderer that works without LaTeX installation"""
    
    def __init__(self):
        """Initialize the renderer"""
        try:
            # Color scheme for dark/light themes
            self.colors = {
                'background': '#ffffff',
                'text': '#2c3e50',
                'highlight': '#3498db',
                'success': '#27ae60',
                'warning': '#f39c12',
                'error': '#e74c3c'
            }
            
            logger.info("Working LaTeX renderer initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LaTeX renderer: {str(e)}")
            raise
    
    def render_expression(self, expression, title: str = "", color: str = None, fontsize: int = 14):
        """
        Render a mathematical expression without LaTeX
        
        Args:
            expression: SymPy expression or LaTeX string
            title: Optional title
            color: Optional color
            fontsize: Font size
            
        Returns:
            matplotlib Figure
        """
        try:
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes for clean display
            ax.set_axis_off()
            
            # Convert expression to display format
            display_text = self._convert_to_display_format(expression, title)
            
            # Set color
            text_color = color or self.colors['text']
            
            # Display the expression
            ax.text(0.5, 0.7, title, transform=ax.transAxes,
                   fontsize=fontsize+2, ha='center', va='center', 
                   color=text_color, weight='bold')
            
            ax.text(0.5, 0.3, display_text, transform=ax.transAxes,
                   fontsize=fontsize, ha='center', va='center', 
                   color=text_color, family='monospace')
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering expression: {str(e)}")
            return self._render_error_text(str(e))
    
    def render_preview(self, expression: str):
        """
        Render a preview of an expression without LaTeX
        
        Args:
            expression: Raw expression string
            
        Returns:
            matplotlib Figure
        """
        try:
            # Create small figure for preview
            fig, ax = plt.subplots(figsize=(8, 2))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes
            ax.set_axis_off()
            
            # Convert to display format
            display_text = self._convert_to_display_format(expression)
            
            # Display the expression
            ax.text(0.5, 0.5, display_text, transform=ax.transAxes,
                   fontsize=12, ha='center', va='center', 
                   color=self.colors['text'], family='monospace')
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering preview: {str(e)}")
            return self._render_error_text(str(e))
    
    def _convert_to_display_format(self, expression, title: str = ""):
        """
        Convert expression to readable display format
        
        Args:
            expression: SymPy expression or string
            title: Optional title
            
        Returns:
            Formatted string
        """
        try:
            # Handle different types of expressions
            if hasattr(expression, 'latex'):
                # SymPy expression
                try:
                    latex_str = expression.latex()
                    return self._clean_latex_for_display(latex_str)
                except:
                    return str(expression)
            elif isinstance(expression, str):
                # String expression
                return self._clean_latex_for_display(expression)
            else:
                # Fallback to string representation
                return str(expression)
                
        except Exception as e:
            logger.error(f"Error converting to display format: {str(e)}")
            return str(expression)
    
    def _clean_latex_for_display(self, latex_str: str) -> str:
        """
        Clean LaTeX string for better display
        
        Args:
            latex_str: LaTeX string
            
        Returns:
            Cleaned string
        """
        try:
            # Convert LaTeX to more readable format
            conversions = {
                r'\\frac{([^}]+)}{([^}]+)}': r'\1/\2',
                r'\\sqrt{([^}]+)}': r'√(\1)',
                r'\\int': '∫',
                r'\\sum': '∑',
                r'\\prod': '∏',
                r'\\infty': '∞',
                r'\\pi': 'π',
                r'\\theta': 'θ',
                r'\\alpha': 'α',
                r'\\beta': 'β',
                r'\\gamma': 'γ',
                r'\\delta': 'δ',
                r'\\epsilon': 'ε',
                r'\\lambda': 'λ',
                r'\\mu': 'μ',
                r'\\nu': 'ν',
                r'\\sigma': 'σ',
                r'\\tau': 'τ',
                r'\\phi': 'φ',
                r'\\psi': 'ψ',
                r'\\omega': 'ω',
                r'\\sin': 'sin',
                r'\\cos': 'cos',
                r'\\tan': 'tan',
                r'\\log': 'log',
                r'\\ln': 'ln',
                r'\\exp': 'exp',
                r'\\le': '≤',
                r'\\ge': '≥',
                r'\\ne': '≠',
                r'\\pm': '±',
                r'\\mp': '∓',
                r'\\times': '×',
                r'\\div': '÷',
                r'\\cdot': '·',
                r'\\partial': '∂',
                r'\\nabla': '∇',
                r'\\cup': '∪',
                r'\\cap': '∩',
                r'\\subset': '⊂',
                r'\\supset': '⊃',
                r'\\in': '∈',
                r'\\notin': '∉',
                r'\\emptyset': '∅',
                r'\\mathbb{R}': 'ℝ',
                r'\\mathbb{Z}': 'ℤ',
                r'\\mathbb{N}': 'ℕ',
                r'\\mathbb{C}': 'ℂ',
                r'\\mathbb{Q}': 'ℚ',
                r'\*\*': '^',
                r'\^': '^',
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\\[': '[',
                r'\\right\\]': ']',
                r'\\left\\{': '{',
                r'\\right\\}': '}',
                r'\\,': ' ',
                r'\\;': '  ',
                r'\\!': '',
                r'\\&': '  ',
                r'\\\\': '\n',
                r'\\text{([^}]+)}': r'\1',
                r'\\mathrm{([^}]+)}': r'\1',
                r'\\mathit{([^}]+)}': r'\1',
                r'\\mathbf{([^}]+)}': r'\1',
                r'\\mathsf{([^}]+)}': r'\1',
                r'\\mathtt{([^}]+)}': r'\1',
            }
            
            # Apply conversions
            result = latex_str
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            # Clean up any remaining backslashes
            result = result.replace('\\', '')
            
            return result
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX: {str(e)}")
            return latex_str
    
    def _render_error_text(self, error_msg: str) -> plt.Figure:
        """Render an error message"""
        try:
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes
            ax.set_axis_off()
            
            # Error message
            ax.text(0.5, 0.5, f'Error: {error_msg}', transform=ax.transAxes,
                   fontsize=12, ha='center', va='center', color=self.colors['error'])
            
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


class WorkingLaTeXDisplayManager:
    """Working manager for LaTeX displays that works without LaTeX"""
    
    def __init__(self):
        self.renderer = WorkingLaTeXRenderer()
        self.active_canvases = {}  # Track active canvases for cleanup
    
    def display_expression_in_frame(self, expression, frame, title: str = "", 
                                  color: str = None, fontsize: int = 14):
        """
        Display an expression in a Tkinter frame
        
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
            
            # Render expression
            fig = self.renderer.render_expression(expression, title, color, fontsize)
            
            # Create canvas
            canvas = self.renderer.get_canvas_widget(fig, frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            
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
        Display a preview of an expression
        
        Args:
            expression: Raw expression string
            frame: Tkinter frame
            
        Returns:
            FigureCanvasTkAgg widget
        """
        try:
            # CRITICAL FIX: Clear frame completely before rendering
            self._clear_frame_completely(frame)
            
            # Render preview
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
            
            # Create error label
            import tkinter as tk
            from tkinter import ttk
            
            error_label = ttk.Label(frame, 
                                  text=f"❌ Error: {error_msg}",
                                  font=("Arial", 10), foreground="red")
            error_label.pack(pady=10, padx=10)
            
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


# Use the working classes
LaTeXRenderer = WorkingLaTeXRenderer
LaTeXDisplayManager = WorkingLaTeXDisplayManager

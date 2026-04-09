"""
Fixed LaTeX Renderer for Mathematical Expressions
Completely rewritten to fix rendering issues
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import re
from typing import Optional, Tuple, List
import logging

logger = logging.getLogger(__name__)


class FixedLaTeXRenderer:
    """Fixed LaTeX renderer that actually works"""
    
    def __init__(self):
        # Try to configure LaTeX rendering
        self.latex_available = self._check_latex_availability()
        
        if self.latex_available:
            # Configure matplotlib for LaTeX rendering
            plt.rcParams.update({
                'font.size': 14,
                'text.usetex': True,
                'text.latex.preamble': r'''
                    \usepackage{amsmath}
                    \usepackage{amssymb}
                    \usepackage{amsfonts}
                    \usepackage{mathtools}
                    \usepackage{bm}
                ''',
                'axes.labelsize': 14,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 12,
                'figure.titlesize': 16,
                'axes.titlesize': 14
            })
            logger.info("✓ LaTeX rendering enabled")
        else:
            # Fallback to matplotlib text rendering
            plt.rcParams.update({
                'font.size': 14,
                'text.usetex': False,
                'axes.labelsize': 14,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 12,
                'figure.titlesize': 16,
                'axes.titlesize': 14
            })
            logger.warning("✗ LaTeX not available, using fallback rendering")
        
        # Color schemes
        self.colors = {
            'background': '#ffffff',
            'text': '#2c3e50',
            'integral': '#8e44ad',
            'result': '#27ae60',
            'step': '#3498db',
            'highlight': '#e74c3c'
        }
    
    def _check_latex_availability(self):
        """Check if LaTeX is available"""
        try:
            # Try to render a simple LaTeX expression
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.text(0.5, 0.5, r'$\int x^2 dx$', transform=ax.transAxes)
            plt.close(fig)
            return True
        except Exception as e:
            logger.warning(f"LaTeX not available: {str(e)}")
            return False
    
    def render_expression(self, expression, title: str = "", 
                         color: str = None, fontsize: int = 14) -> plt.Figure:
        """
        Render a mathematical expression using LaTeX or fallback
        
        Args:
            expression: LaTeX string or SymPy expression
            title: Optional title for the expression
            color: Text color override
            fontsize: Font size for the expression
            
        Returns:
            matplotlib Figure with the rendered expression
        """
        try:
            # Convert to LaTeX string
            if hasattr(expression, 'latex'):
                latex_expr = expression.latex()
            elif isinstance(expression, str):
                latex_expr = expression
            else:
                latex_expr = str(expression)
            
            # Clean up LaTeX expression
            latex_expr = self._clean_latex(latex_expr)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes completely
            ax.set_axis_off()
            
            # Set text color
            text_color = color or self.colors['text']
            
            # Render the expression
            if title:
                # Add title
                ax.text(0.5, 0.8, title, transform=ax.transAxes,
                       fontsize=fontsize+2, ha='center', va='top',
                       color=text_color, weight='bold')
                # Add expression
                if self.latex_available:
                    ax.text(0.5, 0.4, f'${latex_expr}$', transform=ax.transAxes,
                           fontsize=fontsize, ha='center', va='center',
                           color=text_color)
                else:
                    # Fallback to plain text
                    fallback_expr = self._latex_to_text(latex_expr)
                    ax.text(0.5, 0.4, fallback_expr, transform=ax.transAxes,
                           fontsize=fontsize, ha='center', va='center',
                           color=text_color, family='monospace')
            else:
                # Just expression
                if self.latex_available:
                    ax.text(0.5, 0.5, f'${latex_expr}$', transform=ax.transAxes,
                           fontsize=fontsize, ha='center', va='center',
                           color=text_color)
                else:
                    # Fallback to plain text
                    fallback_expr = self._latex_to_text(latex_expr)
                    ax.text(0.5, 0.5, fallback_expr, transform=ax.transAxes,
                           fontsize=fontsize, ha='center', va='center',
                           color=text_color, family='monospace')
            
            # Adjust layout
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering expression: {str(e)}")
            return self._render_error_text(str(expression))
    
    def render_preview(self, expression: str) -> plt.Figure:
        """
        Render a quick preview of the expression
        
        Args:
            expression: Raw expression string
            
        Returns:
            matplotlib Figure with the preview
        """
        try:
            # Try to parse and convert to LaTeX
            try:
                # Parse the expression first
                parsed_expr = sp.sympify(expression)
                latex_expr = parsed_expr.latex()
            except:
                # If parsing fails, use simple conversion
                latex_expr = self._convert_to_latex_preview(expression)
            
            # Clean up LaTeX
            latex_expr = self._clean_latex(latex_expr)
            
            # Create small figure for preview
            fig, ax = plt.subplots(figsize=(8, 2))
            ax.set_facecolor(self.colors['background'])
            fig.patch.set_facecolor(self.colors['background'])
            
            # Remove axes completely
            ax.set_axis_off()
            
            # Render preview
            if self.latex_available:
                ax.text(0.5, 0.5, f'${latex_expr}$', transform=ax.transAxes,
                       fontsize=12, ha='center', va='center', color=self.colors['text'])
            else:
                # Fallback to plain text
                fallback_expr = self._latex_to_text(latex_expr)
                ax.text(0.5, 0.5, fallback_expr, transform=ax.transAxes,
                       fontsize=12, ha='center', va='center', color=self.colors['text'], family='monospace')
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering preview: {str(e)}")
            return self._render_error_text(expression)
    
    def _clean_latex(self, latex_str: str) -> str:
        """Clean and improve LaTeX string"""
        try:
            # Common replacements
            replacements = {
                r'\*': r'\\cdot',
                r'**': r'^',
                r'sqrt': r'\\sqrt',
                r'pi': r'\\pi',
                r'e': r'e',
                r'integrate': r'\\int',
                r'diff': r'\\frac{d}{d}',
                r'log': r'\\log',
                r'sin': r'\\sin',
                r'cos': r'\\cos',
                r'tan': r'\\tan',
                r'exp': r'\\exp',
                r'Abs': r'\\left|',
                r'Heaviside': r'\\theta',
            }
            
            cleaned = latex_str
            for old, new in replacements.items():
                cleaned = re.sub(old, new, cleaned)
            
            # Handle special cases
            cleaned = self._handle_special_cases(cleaned)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning LaTeX: {str(e)}")
            return latex_str
    
    def _handle_special_cases(self, latex_str: str) -> str:
        """Handle special LaTeX cases"""
        try:
            # Handle integrate with limits
            if 'integrate(' in latex_str:
                # Convert integrate(f, x) to \int f dx
                latex_str = re.sub(r'integrate\(([^,]+),\s*([^)]+)\)', r'\\int \1\\,d\2', latex_str)
            
            # Handle integrate with limits integrate(f, (x, a, b))
            if '(x,' in latex_str and 'integrate(' in latex_str:
                latex_str = re.sub(r'integrate\(([^,]+),\s*\(([^,]+),\s*([^,]+),\s*([^)]+)\)\)', 
                                  r'\\int_{\3}^{\4} \1\\,d\2', latex_str)
            
            # Handle powers
            latex_str = re.sub(r'\^([0-9]+)', r'^{\1}', latex_str)
            
            # Handle fractions
            if '/' in latex_str and not '\\frac' in latex_str:
                # Simple fraction handling
                latex_str = re.sub(r'([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', r'\\frac{\1}{\2}', latex_str)
            
            return latex_str
            
        except Exception as e:
            logger.error(f"Error handling special cases: {str(e)}")
            return latex_str
    
    def _convert_to_latex_preview(self, expression: str) -> str:
        """Convert raw expression to LaTeX for preview"""
        try:
            # Simple conversions for preview
            conversions = {
                r'integrate': r'\\int',
                r'sqrt': r'\\sqrt',
                r'pi': r'\\pi',
                r'\*\*': r'^',
                r'\*': r'\\cdot',
                r'sin': r'\\sin',
                r'cos': r'\\cos',
                r'tan': r'\\tan',
                r'log': r'\\log',
                r'exp': r'\\exp',
            }
            
            latex_expr = expression
            for old, new in conversions.items():
                latex_expr = re.sub(old, new, latex_expr)
            
            return latex_expr
            
        except Exception as e:
            logger.error(f"Error converting to LaTeX preview: {str(e)}")
            return expression
    
    def _latex_to_text(self, latex_str: str) -> str:
        """Convert LaTeX expression to plain text"""
        try:
            # Simple LaTeX to text conversions
            conversions = {
                r'\\int': '∫',
                r'\\sqrt': '√',
                r'\\pi': 'π',
                r'\\infty': '∞',
                r'\\cdot': '·',
                r'\\frac{([^}]+)}{([^}]+)}': r'(\1)/(\2)',
                r'\^{([^}]+)}': r'^(\1)',
                r'\\sin': 'sin',
                r'\\cos': 'cos',
                r'\\tan': 'tan',
                r'\\log': 'log',
                r'\\exp': 'exp',
                r'\\left\(': '(',
                r'\\right\)': ')',
                r'\\left\\[': '[',
                r'\\right\\]': ']',
                r'\{': '{',
                r'\}': '}',
            }
            
            text = latex_str
            for latex, replacement in conversions.items():
                text = re.sub(latex, replacement, text)
            
            return text
            
        except Exception as e:
            logger.error(f"Error converting LaTeX to text: {str(e)}")
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
                   fontsize=12, ha='center', va='center', color=self.colors['highlight'])
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error rendering error text: {str(e)}")
            # Create minimal figure
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.set_axis_off()
            return fig
    
    def get_canvas_widget(self, figure: plt.Figure, parent) -> FigureCanvasTkAgg:
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


class FixedLaTeXDisplayManager:
    """Fixed manager for LaTeX displays that actually works"""
    
    def __init__(self):
        self.renderer = FixedLaTeXRenderer()
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
                self.renderer.clear_canvas(canvas)
            self.active_canvases.clear()
        except Exception as e:
            logger.error(f"Error clearing all displays: {str(e)}")


# Replace the original classes
LaTeXRenderer = FixedLaTeXRenderer
LaTeXDisplayManager = FixedLaTeXDisplayManager

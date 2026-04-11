"""
Steps Display Panel - Microsoft Math Solver Style
Displays detailed step-by-step solutions with LaTeX rendering
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
from typing import List, Dict, Any, Optional
import re

logger = logging.getLogger(__name__)


class StepsDisplayPanel:
    """Panel for displaying detailed integration steps"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_steps = []
        self.current_result = ""
        self.current_method = ""
        
        # Create the UI
        self.create_ui()
        
        logger.info("Steps Display Panel initialized")
    
    def create_ui(self):
        """Create the steps display interface"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        self.create_content_area(main_frame)
        
        # Footer with verification
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create header with method info"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Method label
        self.method_label = ttk.Label(header_frame, text="Método: Auto-detección", 
                                    font=('Arial', 10, 'bold'))
        self.method_label.pack(side="left")
        
        # Confidence indicator
        self.confidence_label = ttk.Label(header_frame, text="Confianza: --", 
                                         font=('Arial', 9))
        self.confidence_label.pack(side="right")
        
        # Separator
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=2)
    
    def create_content_area(self, parent):
        """Create main content area for steps"""
        # Create notebook for different views
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, pady=5)
        
        # Steps tab
        self.steps_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.steps_frame, text="Pasos Detallados")
        self.create_steps_content(self.steps_frame)
        
        # LaTeX tab
        self.latex_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.latex_frame, text="LaTeX")
        self.create_latex_content(self.latex_frame)
        
        # Analysis tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Análisis")
        self.create_analysis_content(self.analysis_frame)
    
    def create_steps_content(self, parent):
        """Create steps content area"""
        # Scrolled text for steps
        self.steps_text = scrolledtext.ScrolledText(
            parent, 
            height=15, 
            font=('Courier New', 10),
            wrap=tk.WORD,
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.steps_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure tags for different step types
        self.steps_text.tag_configure("title", font=('Arial', 11, 'bold'), foreground='#2c3e50')
        self.steps_text.tag_configure("method", font=('Arial', 10, 'bold'), foreground='#3498db')
        self.steps_text.tag_configure("step", font=('Courier New', 10), foreground='#27ae60')
        self.steps_text.tag_configure("result", font=('Courier New', 10, 'bold'), foreground='#e74c3c')
        self.steps_text.tag_configure("explanation", font=('Arial', 9, 'italic'), foreground='#7f8c8d')
    
    def create_latex_content(self, parent):
        """Create LaTeX content area"""
        # LaTeX display
        self.latex_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            font=('Courier New', 10),
            wrap=tk.WORD,
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.latex_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_frame = ttk.Frame(parent)
        copy_frame.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(copy_frame, text="Copiar LaTeX", 
                  command=self.copy_latex).pack(side="right")
        
        ttk.Button(copy_frame, text="Limpiar", 
                  command=self.clear_latex).pack(side="right", padx=(0, 5))
    
    def create_analysis_content(self, parent):
        """Create analysis content area"""
        # Analysis text
        self.analysis_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            font=('Arial', 10),
            wrap=tk.WORD,
            bg='#ffffff',
            fg='#2c3e50'
        )
        self.analysis_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure tags
        self.analysis_text.tag_configure("info", font=('Arial', 10, 'bold'), foreground='#3498db')
        self.analysis_text.tag_configure("success", font=('Arial', 10), foreground='#27ae60')
        self.analysis_text.tag_configure("warning", font=('Arial', 10), foreground='#f39c12')
        self.analysis_text.tag_configure("error", font=('Arial', 10), foreground='#e74c3c')
    
    def create_footer(self, parent):
        """Create footer with verification info"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill="x", pady=(5, 0))
        
        # Verification status
        self.verification_label = ttk.Label(footer_frame, text="Verificación: --", 
                                          font=('Arial', 9))
        self.verification_label.pack(side="left")
        
        # Export buttons
        button_frame = ttk.Frame(footer_frame)
        button_frame.pack(side="right")
        
        ttk.Button(button_frame, text="Exportar Pasos", 
                  command=self.export_steps).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Imprimir", 
                  command=self.print_steps).pack(side="left", padx=2)
    
    def display_solution(self, solution_data: Dict[str, Any]):
        """Display complete solution with steps"""
        try:
            logger.info("Displaying solution steps")
            
            # Store current data
            self.current_steps = solution_data.get('steps', [])
            self.current_result = solution_data.get('result', '')
            self.current_method = solution_data.get('method', 'auto')
            
            # Update header
            self.update_header(solution_data)
            
            # Display steps
            self.display_steps(self.current_steps)
            
            # Display LaTeX
            self.display_latex(solution_data)
            
            # Display analysis
            self.display_analysis(solution_data)
            
            # Update verification
            self.update_verification(solution_data)
            
            logger.info("Solution displayed successfully")
            
        except Exception as e:
            logger.error(f"Error displaying solution: {str(e)}")
            self.display_error(f"Error al mostrar solución: {str(e)}")
    
    def update_header(self, solution_data: Dict[str, Any]):
        """Update header information"""
        try:
            # Method
            method = solution_data.get('method', 'auto')
            method_names = {
                'polynomial': 'Integración Directa (Polinomios)',
                'parts': 'Integración por Partes',
                'substitution': 'Sustitución',
                'trigonometric': 'Integración Trigonométrica',
                'exponential': 'Integración Exponencial',
                'rational': 'Fracciones Parciales',
                'general': 'Método General'
            }
            
            method_display = method_names.get(method, method.title())
            self.method_label.config(text=f"Método: {method_display}")
            
            # Confidence
            confidence = solution_data.get('confidence', 0.0)
            confidence_text = f"Confianza: {confidence:.1%}"
            self.confidence_label.config(text=confidence_text)
            
            # Color code confidence
            if confidence >= 0.95:
                self.confidence_label.config(foreground='#27ae60')
            elif confidence >= 0.80:
                self.confidence_label.config(foreground='#f39c12')
            else:
                self.confidence_label.config(foreground='#e74c3c')
                
        except Exception as e:
            logger.error(f"Error updating header: {str(e)}")
    
    def display_steps(self, steps: List[Dict[str, Any]]):
        """Display step-by-step solution"""
        try:
            # Clear existing content
            self.steps_text.delete('1.0', tk.END)
            
            # Add title
            self.steps_text.insert(tk.END, "SOLUCIÓN PASO A PASO\n\n", "title")
            
            # Add each step
            for i, step in enumerate(steps, 1):
                step_type = step.get('type', 'step')
                title = step.get('title', f'Paso {i}')
                expression = step.get('expression', '')
                explanation = step.get('explanation', '')
                
                # Step number and title
                self.steps_text.insert(tk.END, f"{i}. {title}\n", "method")
                
                # Expression if available
                if expression:
                    # Clean LaTeX for display
                    clean_expr = self.clean_latex_for_display(expression)
                    self.steps_text.insert(tk.END, f"   {clean_expr}\n", "step")
                
                # Explanation if available
                if explanation:
                    self.steps_text.insert(tk.END, f"   Explicación: {explanation}\n", "explanation")
                
                # Add separator
                self.steps_text.insert(tk.END, "\n")
            
            # Add final result
            if self.current_result:
                self.steps_text.insert(tk.END, "RESULTADO FINAL\n", "result")
                self.steps_text.insert(tk.END, f"   {self.current_result} + C\n", "result")
            
        except Exception as e:
            logger.error(f"Error displaying steps: {str(e)}")
            self.steps_text.insert(tk.END, f"Error al mostrar pasos: {str(e)}")
    
    def display_latex(self, solution_data: Dict[str, Any]):
        """Display LaTeX code"""
        try:
            # Clear existing content
            self.latex_text.delete('1.0', tk.END)
            
            # Add header
            self.latex_text.insert(tk.END, "% CÓDIGO LATEX\n\n")
            self.latex_text.insert(tk.END, "\\documentclass{article}\n")
            self.latex_text.insert(tk.END, "\\usepackage{amsmath}\n")
            self.latex_text.insert(tk.END, "\\usepackage{amssymb}\n")
            self.latex_text.insert(tk.END, "\\begin{document}\n\n")
            
            # Add title
            self.latex_text.insert(tk.END, "\\section*{Solución de Integral}\n\n")
            
            # Add problem
            expression = solution_data.get('expression', '')
            if expression:
                self.latex_text.insert(tk.END, "\\textbf{Problema:}\n")
                self.latex_text.insert(tk.END, "\\[\n")
                self.latex_text.insert(tk.END, f"\\int {expression} \\, dx\n")
                self.latex_text.insert(tk.END, "\\]\n\n")
            
            # Add steps
            steps = solution_data.get('steps', [])
            for i, step in enumerate(steps, 1):
                title = step.get('title', f'Paso {i}')
                expression = step.get('expression', '')
                
                self.latex_text.insert(tk.END, f"\\textbf{{{title}:}}\n")
                if expression:
                    self.latex_text.insert(tk.END, "\\[\n")
                    self.latex_text.insert(tk.END, f"{expression}\n")
                    self.latex_text.insert(tk.END, "\\]\n")
                self.latex_text.insert(tk.END, "\n")
            
            # Add result
            result = solution_data.get('result', '')
            if result:
                self.latex_text.insert(tk.END, "\\textbf{Resultado:}\n")
                self.latex_text.insert(tk.END, "\\[\n")
                self.latex_text.insert(tk.END, f"\\int {expression} \\, dx = {result} + C\n")
                self.latex_text.insert(tk.END, "\\]\n\n")
            
            # Close document
            self.latex_text.insert(tk.END, "\\end{document}")
            
        except Exception as e:
            logger.error(f"Error displaying LaTeX: {str(e)}")
            self.latex_text.insert(tk.END, f"Error al generar LaTeX: {str(e)}")
    
    def display_analysis(self, solution_data: Dict[str, Any]):
        """Display analysis information"""
        try:
            # Clear existing content
            self.analysis_text.delete('1.0', tk.END)
            
            # Add header
            self.analysis_text.insert(tk.END, "ANÁLISIS DE LA SOLUCIÓN\n\n", "info")
            
            # Method analysis
            method = solution_data.get('method', 'auto')
            self.analysis_text.insert(tk.END, f"Método utilizado: {method}\n\n")
            
            # Confidence analysis
            confidence = solution_data.get('confidence', 0.0)
            self.analysis_text.insert(tk.END, f"Nivel de confianza: {confidence:.1%}\n")
            
            if confidence >= 0.95:
                self.analysis_text.insert(tk.END, "Estado: Alta confianza\n\n", "success")
            elif confidence >= 0.80:
                self.analysis_text.insert(tk.END, "Estado: Confianza moderada\n\n", "warning")
            else:
                self.analysis_text.insert(tk.END, "Estado: Requiere verificación manual\n\n", "error")
            
            # Verification info
            verification = solution_data.get('verification', {})
            if verification:
                self.analysis_text.insert(tk.END, "VERIFICACIÓN AUTOMÁTICA\n\n", "info")
                
                are_equal = verification.get('are_equal', False)
                if are_equal:
                    self.analysis_text.insert(tk.END, "Estado: Verificación exitosa\n", "success")
                    self.analysis_text.insert(tk.END, "La derivada del resultado coincide con la función original.\n")
                else:
                    self.analysis_text.insert(tk.END, "Estado: Verificación fallida\n", "error")
                    self.analysis_text.insert(tk.END, "Se recomienda revisar manualmente.\n")
                
                # Add derivative comparison
                original = verification.get('original', '')
                derivative = verification.get('derivative', '')
                if original and derivative:
                    self.analysis_text.insert(tk.END, f"\nFunción original: {original}\n")
                    self.analysis_text.insert(tk.END, f"Derivada del resultado: {derivative}\n")
            
            # Performance info
            timestamp = solution_data.get('timestamp', '')
            if timestamp:
                self.analysis_text.insert(tk.END, f"\nTimestamp: {timestamp}\n")
            
        except Exception as e:
            logger.error(f"Error displaying analysis: {str(e)}")
            self.analysis_text.insert(tk.END, f"Error en análisis: {str(e)}")
    
    def update_verification(self, solution_data: Dict[str, Any]):
        """Update verification status in footer"""
        try:
            verification = solution_data.get('verification', {})
            
            if verification:
                are_equal = verification.get('are_equal', False)
                confidence = verification.get('confidence', 0.0)
                
                if are_equal:
                    self.verification_label.config(
                        text=f"Verificación: Exitosa ({confidence:.1%})",
                        foreground='#27ae60'
                    )
                else:
                    self.verification_label.config(
                        text=f"Verificación: Requiere revisión ({confidence:.1%})",
                        foreground='#e74c3c'
                    )
            else:
                self.verification_label.config(
                    text="Verificación: No disponible",
                    foreground='#7f8c8d'
                )
                
        except Exception as e:
            logger.error(f"Error updating verification: {str(e)}")
            self.verification_label.config(
                text="Verificación: Error",
                foreground='#e74c3c'
            )
    
    def clean_latex_for_display(self, latex_text: str) -> str:
        """Clean LaTeX text for plain text display"""
        # Remove LaTeX commands for display
        cleaned = latex_text
        
        # Common LaTeX patterns to clean
        patterns = [
            (r'\\int', 'Integral'),
            (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2'),
            (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
            (r'\\sin', 'sin'),
            (r'\\cos', 'cos'),
            (r'\\tan', 'tan'),
            (r'\\log', 'log'),
            (r'\\exp', 'exp'),
            (r'\\infty', 'infinito'),
            (r'\\pi', 'pi'),
            (r'\\left\(', '('),
            (r'\\right\)', ')'),
            (r'\\left\[', '['),
            (r'\\right\]', ']'),
            (r'\^\{([^}]+)\}', r'^\1'),
            (r'\\d([a-zA-Z])', r'd\1'),
            (r'\$\s*', ''),
            (r'\s*\$', ''),
        ]
        
        for pattern, replacement in patterns:
            cleaned = re.sub(pattern, replacement, cleaned)
        
        return cleaned
    
    def display_error(self, error_message: str):
        """Display error message"""
        try:
            # Clear all displays
            self.steps_text.delete('1.0', tk.END)
            self.latex_text.delete('1.0', tk.END)
            self.analysis_text.delete('1.0', tk.END)
            
            # Show error in all tabs
            error_text = f"ERROR: {error_message}"
            
            self.steps_text.insert(tk.END, error_text, "error")
            self.latex_text.insert(tk.END, f"% {error_text}")
            self.analysis_text.insert(tk.END, error_text, "error")
            
            # Update header
            self.method_label.config(text="Método: Error")
            self.confidence_label.config(text="Confianza: --")
            self.verification_label.config(text="Verificación: Error", foreground='#e74c3c')
            
        except Exception as e:
            logger.error(f"Error displaying error: {str(e)}")
    
    def clear_all(self):
        """Clear all displays"""
        try:
            self.steps_text.delete('1.0', tk.END)
            self.latex_text.delete('1.0', tk.END)
            self.analysis_text.delete('1.0', tk.END)
            
            self.method_label.config(text="Método: --")
            self.confidence_label.config(text="Confianza: --")
            self.verification_label.config(text="Verificación: --", foreground='#7f8c8d')
            
            self.current_steps = []
            self.current_result = ""
            self.current_method = ""
            
        except Exception as e:
            logger.error(f"Error clearing displays: {str(e)}")
    
    def copy_latex(self):
        """Copy LaTeX code to clipboard"""
        try:
            import tkinter as tk
            self.latex_text.clipboard_clear()
            self.latex_text.clipboard_append(self.latex_text.get('1.0', tk.END))
            logger.info("LaTeX code copied to clipboard")
        except Exception as e:
            logger.error(f"Error copying LaTeX: {str(e)}")
    
    def clear_latex(self):
        """Clear LaTeX display"""
        self.latex_text.delete('1.0', tk.END)
    
    def export_steps(self):
        """Export steps to text file"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"integral_steps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("SOLUCIÓN DE INTEGRAL - PASOS DETALLADOS\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Write steps
                    for i, step in enumerate(self.current_steps, 1):
                        f.write(f"{i}. {step.get('title', f'Paso {i}')}\n")
                        if step.get('expression'):
                            f.write(f"   {step.get('expression')}\n")
                        if step.get('explanation'):
                            f.write(f"   Explicación: {step.get('explanation')}\n")
                        f.write("\n")
                    
                    # Write result
                    if self.current_result:
                        f.write(f"RESULTADO: {self.current_result} + C\n")
                
                logger.info(f"Steps exported to {filename}")
                
        except Exception as e:
            logger.error(f"Error exporting steps: {str(e)}")
    
    def print_steps(self):
        """Print steps"""
        try:
            import tkinter as tk
            self.steps_text.event_generate("<<Print>>")
            logger.info("Steps sent to printer")
        except Exception as e:
            logger.error(f"Error printing steps: {str(e)}")
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get current solution data"""
        return {
            'steps': self.current_steps,
            'result': self.current_result,
            'method': self.current_method
        }

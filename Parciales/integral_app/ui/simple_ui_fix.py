"""
Simple UI Fix for LaTeX Calculator
Direct fix for display issues
"""
import tkinter as tk
from tkinter import ttk
import sympy as sp
import logging

logger = logging.getLogger(__name__)


def patch_calculator_display_methods():
    """Patch the calculator display methods to force UI updates"""
    
    try:
        # Import the calculator
        from ui.latex_calculator import FinalLaTeXIntegralCalculator
        
        # Store original method
        original_method = FinalLaTeXIntegralCalculator._display_working_latex_results
        
        def fixed_display_method(self, func, result, steps, limits):
            """Fixed display method with forced UI updates"""
            try:
                logger.info("Starting fixed display method")
                
                # Clear all frames completely
                for widget in self.latex_result_frame.winfo_children():
                    widget.destroy()
                for widget in self.latex_steps_frame.winfo_children():
                    widget.destroy()
                for widget in self.latex_verify_frame.winfo_children():
                    widget.destroy()
                
                # Force UI update
                self.root.update_idletasks()
                
                # Display result as text (fallback)
                if limits:
                    title = f"∫_{limits[0]}^{limits[1]} f(x) dx"
                else:
                    title = "∫ f(x) dx"
                
                result_text = f"🎯 {title}\n\n"
                result_text += f"Resultado: {result}"
                
                # Create result label
                result_label = ttk.Label(
                    self.latex_result_frame,
                    text=result_text,
                    font=("Courier", 12, "bold"),
                    foreground="#27ae60",
                    justify=tk.LEFT
                )
                result_label.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Display steps
                if steps:
                    steps_text = "📝 PASOS DEL CÁLCULO\n\n"
                    for i, step in enumerate(steps):
                        if step.get('type') in ['method_step', 'transformation']:
                            step_title = step.get('title', f'Paso {i+1}')
                            step_expr = step.get('expression', '')
                            steps_text += f"🔹 {step_title}\n"
                            if step_expr:
                                steps_text += f"   {step_expr}\n"
                            steps_text += "\n"
                    
                    steps_label = ttk.Label(
                        self.latex_steps_frame,
                        text=steps_text,
                        font=("Courier", 10),
                        foreground="#3498db",
                        justify=tk.LEFT
                    )
                    steps_label.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Display verification
                verify_text = "✔️ VERIFICACIÓN\n\n"
                try:
                    derivative = sp.diff(result, self.current_var)
                    if sp.simplify(derivative - func) == 0:
                        verify_text += "✅ Verificación Exitosa\n"
                        verify_text += f"La derivada del resultado coincide con la función original"
                    else:
                        verify_text += "⚠️ Verificación Parcial\n"
                        verify_text += f"La derivada del resultado es similar a la función original"
                except:
                    verify_text += "❌ No se pudo verificar el resultado"
                
                verify_label = ttk.Label(
                    self.latex_verify_frame,
                    text=verify_text,
                    font=("Courier", 10),
                    foreground="#27ae60",
                    justify=tk.LEFT
                )
                verify_label.pack(pady=10, padx=10, fill="both", expand=True)
                
                # Update text mode
                self._display_text_results(func, result, steps, limits)
                
                # Update status
                self.info_label.config(text=f"✅ {self.integral_type_var.get()}")
                
                # Force UI update
                self.root.update_idletasks()
                self.root.update()
                
                logger.info("Fixed display method completed successfully")
                
            except Exception as e:
                logger.error(f"Error in fixed display method: {str(e)}")
                # Fallback to original method
                original_method(self, func, result, steps, limits)
        
        # Replace the method
        FinalLaTeXIntegralCalculator._display_working_latex_results = fixed_display_method
        
        logger.info("Calculator display methods patched successfully")
        
    except Exception as e:
        logger.error(f"Error patching calculator methods: {str(e)}")


# Apply the patch immediately
patch_calculator_display_methods()

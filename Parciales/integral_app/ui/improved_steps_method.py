#!/usr/bin/env python3
"""
Improved Steps Method for Professional Main Window
Complete replacement for the steps section with enhanced Unicode and LaTeX visualization
"""
import sys
import os
import logging
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

def create_improved_steps_method():
    """Create the improved _display_result_steps method"""
    
    method_code = '''
    def _display_result_steps(self, result):
        """Display calculation steps with enhanced Unicode and LaTeX visualization"""
        try:
            logger.info("Starting enhanced steps display")
            
            # Update steps tab with enhanced rendering
            if hasattr(result, 'steps') and result.steps:
                # Clear existing content
                self.steps_text.config(state='normal')
                self.steps_text.delete("1.0", tk.END)
                
                # Initialize enhanced step renderer if not available
                if not hasattr(self, 'enhanced_step_renderer'):
                    try:
                        from enhanced_step_renderer import EnhancedStepRenderer
                        self.enhanced_step_renderer = EnhancedStepRenderer(self)
                        logger.info("Enhanced step renderer initialized")
                    except ImportError as e:
                        logger.warning(f"Could not import enhanced renderer: {e}")
                        self.enhanced_step_renderer = None
                
                # Use enhanced renderer if available
                if self.enhanced_step_renderer:
                    self._render_enhanced_steps(result)
                else:
                    # Fallback to improved manual rendering
                    self._render_improved_manual_steps(result)
                
                logger.info("Steps display completed")
            
        except Exception as e:
            logger.error(f"Error displaying steps: {str(e)}")
            # Ultimate fallback
            self._render_basic_steps(result)
    
    def _render_enhanced_steps(self, result):
        """Render steps using the enhanced step renderer"""
        try:
            # Create enhanced steps container
            steps_container = ttk.Frame(self.steps_text.master, style='Card.TFrame')
            
            # Use the enhanced renderer
            self.enhanced_step_renderer.render_enhanced_steps(steps_container, result)
            
            # Add the container to the steps text area
            self.steps_text.window_create("1.0", window=steps_container)
            
        except Exception as e:
            logger.error(f"Error in enhanced rendering: {e}")
            self._render_improved_manual_steps(result)
    
    def _render_improved_manual_steps(self, result):
        """Render steps with improved manual Unicode and LaTeX handling"""
        try:
            # Create professional header
            steps_text = "Pasos del Cálculo - Visualización Mejorada\\n"
            steps_text += "=" * 60 + "\\n\\n"
            
            # Process each step with enhanced Unicode support
            for i, step in enumerate(result.steps, 1):
                try:
                    logger.info(f"Processing enhanced step {i}: {type(step)}")
                    
                    # Extract step content
                    if isinstance(step, dict):
                        latex_content = step.get('latex', step.get('content', ''))
                        step_type = step.get('type', self._determine_step_type(latex_content))
                        description = step.get('description', '')
                    else:
                        latex_content = str(step)
                        step_type = self._determine_step_type(latex_content)
                        description = ''
                    
                    # Create step title with Unicode typography
                    step_title = self._format_enhanced_step_title(i, step_type)
                    steps_text += step_title + "\\n"
                    
                    # Process content with Unicode enhancement
                    if latex_content:
                        unicode_content = self._enhance_latex_with_unicode(latex_content)
                        steps_text += f"Expresión: {unicode_content}\\n"
                        
                        # Add LaTeX rendering placeholder
                        steps_text += f"[LaTeX Rendering - Paso {i}]\\n"
                        
                        # Store for visual rendering
                        if not hasattr(self, 'enhanced_latex_steps'):
                            self.enhanced_latex_steps = {}
                        self.enhanced_latex_steps[f"step_{i}"] = {
                            'latex': latex_content,
                            'unicode': unicode_content,
                            'type': step_type
                        }
                        
                        # Trigger enhanced visual rendering
                        self.root.after(100 + (i * 50), lambda step_idx=i: self._render_enhanced_visual_step(step_idx))
                    
                    # Add description if available
                    if description:
                        steps_text += f"Descripción: {description}\\n"
                    
                    steps_text += "\\n" + "-" * 50 + "\\n\\n"
                    
                except Exception as e:
                    logger.error(f"Error processing enhanced step {i}: {e}")
                    steps_text += f"Paso {i}: Error en procesamiento\\n\\n"
            
            # Insert the enhanced text
            self.steps_text.insert("1.0", steps_text)
            self.steps_text.config(state='disabled')
            
        except Exception as e:
            logger.error(f"Error in improved manual rendering: {e}")
            self._render_basic_steps(result)
    
    def _render_enhanced_visual_step(self, step_idx):
        """Render enhanced visual step with Unicode and LaTeX"""
        try:
            if not hasattr(self, 'enhanced_latex_steps'):
                return
            
            step_key = f"step_{step_idx}"
            if step_key not in self.enhanced_latex_steps:
                return
            
            step_data = self.enhanced_latex_steps[step_key]
            
            # Create enhanced visualization
            fig = self._create_enhanced_step_figure(step_idx, step_data)
            
            if fig:
                # Create canvas for the figure
                canvas_frame = ttk.Frame(self.steps_text.master)
                canvas = FigureCanvasTkAgg(fig, canvas_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='x', padx=10, pady=5)
                
                # Insert canvas at the appropriate position
                placeholder_tag = f"latex_step_{step_idx}"
                self.steps_text.tag_configure(placeholder_tag, lmargin1=20)
                
                # Find and replace placeholder
                content = self.steps_text.get("1.0", tk.END)
                placeholder = f"[LaTeX Rendering - Paso {step_idx}]"
                
                if placeholder in content:
                    # Get position of placeholder
                    start_pos = content.find(placeholder)
                    if start_pos != -1:
                        line_start = content[:start_pos].count('\\n') + 1
                        line_end = line_start
                        
                        # Replace placeholder with canvas
                        self.steps_text.delete(f"{line_start}.0", f"{line_end}.0")
                        self.steps_text.window_create(f"{line_start}.0", window=canvas_frame)
                
                logger.info(f"Enhanced visual step {step_idx} rendered successfully")
            
        except Exception as e:
            logger.error(f"Error rendering enhanced visual step {step_idx}: {e}")
    
    def _create_enhanced_step_figure(self, step_idx, step_data):
        """Create enhanced figure for step visualization"""
        try:
            # Create figure with professional styling
            fig, ax = plt.subplots(1, 1, figsize=(14, 3))
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')
            
            # Remove axes for clean display
            ax.set_axis_off()
            
            # Prepare LaTeX content with Unicode enhancement
            latex_content = step_data['latex']
            unicode_content = step_data['unicode']
            step_type = step_data['type']
            
            # Clean LaTeX for rendering
            cleaned_latex = self._clean_latex_for_visual_rendering(latex_content)
            
            # Create step title
            step_title = self._format_enhanced_step_title(step_idx, step_type)
            
            # Render title with Unicode typography
            ax.text(0.02, 0.85, step_title,
                   transform=ax.transAxes,
                   fontsize=14, fontweight='bold',
                   color='#2c3e50',
                   ha='left', va='top')
            
            # Render mathematical content
            if cleaned_latex:
                try:
                    ax.text(0.02, 0.5, cleaned_latex,
                           transform=ax.transAxes,
                           fontsize=16,
                           color='#34495e',
                           ha='left', va='center')
                except Exception as latex_error:
                    logger.warning(f"LaTeX rendering failed for step {step_idx}: {latex_error}")
                    # Fallback to Unicode
                    ax.text(0.02, 0.5, unicode_content,
                           transform=ax.transAxes,
                           fontsize=14,
                           color='#34495e',
                           ha='left', va='center')
            else:
                # Use Unicode directly
                ax.text(0.02, 0.5, unicode_content,
                       transform=ax.transAxes,
                       fontsize=14,
                       color='#34495e',
                       ha='left', va='center')
            
            # Add enhanced decorations
            self._add_enhanced_step_decorations(ax, step_idx, step_type)
            
            # Set boundaries and layout
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating enhanced step figure {step_idx}: {e}")
            return None
    
    def _clean_latex_for_visual_rendering(self, latex_text):
        """Clean LaTeX text for visual rendering"""
        if not latex_text:
            return ""
        
        # Basic cleaning
        cleaned = latex_text.replace('\\\\', '\\')
        cleaned = cleaned.replace('\\right', 'right')
        cleaned = cleaned.replace('ight', 'right')
        cleaned = cleaned.replace('\\r', '')
        cleaned = cleaned.replace('\\n', ' ')
        cleaned = cleaned.strip()
        
        # Apply Unicode enhancement
        cleaned = self._enhance_latex_with_unicode(cleaned)
        
        # Ensure proper $ symbol usage
        if cleaned.startswith('$') and cleaned.endswith('$') and len(cleaned) > 2:
            final_latex = cleaned
        elif '$' in cleaned:
            clean_text = cleaned.replace('$', '').strip()
            if clean_text and not clean_text.isspace():
                final_latex = f'${clean_text}$'
            else:
                return ""
        else:
            if cleaned and not cleaned.isspace():
                final_latex = f'${cleaned}$'
            else:
                return ""
        
        # Validate
        if not final_latex.strip() or final_latex.strip() == '$$' or len(final_latex) < 3:
            return ""
        
        return final_latex
    
    def _add_enhanced_step_decorations(self, ax, step_idx, step_type):
        """Add enhanced decorations to step visualization"""
        # Step number badge with color based on type
        color_map = {
            'integral': '#27ae60',      # Green
            'substitution': '#3498db',  # Blue
            'integration': '#9b59b6',    # Purple
            'back_substitution': '#e67e22', # Orange
            'simplification': '#f39c12',  # Yellow
            'evaluation': '#e74c3c',     # Red
            'verification': '#16a085',   # Teal
            'result': '#2c3e50'          # Dark blue
        }
        
        badge_color = color_map.get(step_type, '#3498db')
        
        # Create step number circle
        import matplotlib.patches as patches
        circle = patches.Circle((0.95, 0.85), 0.06,
                               transform=ax.transAxes,
                               facecolor=badge_color,
                               edgecolor='#2c3e50',
                               linewidth=2)
        ax.add_patch(circle)
        
        # Add step number
        ax.text(0.95, 0.85, str(step_idx),
               transform=ax.transAxes,
               fontsize=11, fontweight='bold',
               color='white',
               ha='center', va='center')
        
        # Add type indicator
        type_labels = {
            'integral': 'Integral',
            'substitution': 'Sustitución',
            'integration': 'Integración',
            'back_substitution': 'Retro-sustitución',
            'simplification': 'Simplificación',
            'evaluation': 'Evaluación',
            'verification': 'Verificación',
            'result': 'Resultado'
        }
        
        type_label = type_labels.get(step_type, 'Operación')
        ax.text(0.85, 0.85, type_label,
               transform=ax.transAxes,
               fontsize=9,
               color=badge_color,
               ha='center', va='center',
               fontweight='bold')
        
        # Add subtle separator
        ax.axhline(y=0.15, color='#bdc3c7', linestyle='--', alpha=0.3)
    
    def _format_enhanced_step_title(self, step_idx, step_type):
        """Format enhanced step title with Unicode typography"""
        titles = {
            'integral': f'Paso {step_idx}: Configuración de la Integral',
            'substitution': f'Paso {step_idx}: Sustitución de Variables',
            'integration': f'Paso {step_idx}: Integración Directa',
            'back_substitution': f'Paso {step_idx}: Retro-sustitución',
            'simplification': f'Paso {step_idx}: Simplificación Algebraica',
            'evaluation': f'Paso {step_idx}: Evaluación de Límites',
            'verification': f'Paso {step_idx}: Verificación por Derivación',
            'result': f'Paso {step_idx}: Resultado Final',
            'default': f'Paso {step_idx}: Operación Matemática'
        }
        
        return titles.get(step_type, titles['default'])
    
    def _determine_step_type(self, content):
        """Determine step type from content"""
        if not content:
            return 'default'
        
        content_lower = content.lower()
        
        if '\\\\int' in content or 'integral' in content_lower:
            return 'integral'
        elif 'substitute' in content_lower or 'u=' in content_lower:
            return 'substitution'
        elif 'integrate' in content_lower:
            return 'integration'
        elif 'back' in content_lower or 'original' in content_lower:
            return 'back_substitution'
        elif 'simplify' in content_lower or 'simplif' in content_lower:
            return 'simplification'
        elif 'evaluat' in content_lower:
            return 'evaluation'
        elif 'verif' in content_lower or 'deriv' in content_lower:
            return 'verification'
        elif 'result' in content_lower or 'final' in content_lower:
            return 'result'
        else:
            return 'default'
    
    def _render_basic_steps(self, result):
        """Render basic steps as ultimate fallback"""
        try:
            self.steps_text.config(state='normal')
            self.steps_text.delete("1.0", tk.END)
            
            steps_text = "Pasos del Cálculo (Modo Básico)\\n"
            steps_text += "=" * 40 + "\\n\\n"
            
            if hasattr(result, 'steps') and result.steps:
                for i, step in enumerate(result.steps, 1):
                    if isinstance(step, dict):
                        content = step.get('content', step.get('latex', str(step)))
                    else:
                        content = str(step)
                    
                    steps_text += f"Paso {i}:\\n{content}\\n\\n"
            
            self.steps_text.insert("1.0", steps_text)
            self.steps_text.config(state='disabled')
            
        except Exception as e:
            logger.error(f"Error in basic steps rendering: {e}")
    '''
    
    return method_code

def test_improved_steps():
    """Test the improved steps method"""
    print("=== Test de Método de Pasos Mejorado ===")
    
    # Generate the method code
    method_code = create_improved_steps_method()
    
    print("Método mejorado generado exitosamente")
    print(f"Longitud del código: {len(method_code)} caracteres")
    print()
    
    # Show key features
    features = [
        "Visualización Unicode mejorada",
        "Renderizado LaTeX paso a paso",
        "Tipografía profesional",
        "Colores por tipo de paso",
        "Decoraciones visuales",
        "Fallback robusto",
        "Integración con EnhancedStepRenderer"
    ]
    
    print("Características principales:")
    for feature in features:
        print(f"  × {feature}")
    
    print()
    print("El método está listo para ser integrado en professional_main_window.py")

if __name__ == "__main__":
    test_improved_steps()

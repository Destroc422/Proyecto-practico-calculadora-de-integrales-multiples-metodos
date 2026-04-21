#!/usr/bin/env python3
"""
Enhanced Step Visualization with Unicode and LaTeX Integration
Provides professional step-by-step display with Unicode typography and LaTeX rendering
"""
import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class EnhancedStepVisualizer:
    """Enhanced visualizer for mathematical steps with Unicode and LaTeX"""
    
    def __init__(self):
        self.unicode_mappings = {
            # Mathematical symbols
            r'\int': 'integral',
            r'\int_': 'integral desde ',
            r'\int^': 'integral hasta ',
            r'\sum': 'suma',
            r'\prod': 'producto',
            r'\lim': 'límite',
            r'\infty': 'infinito',
            r'\partial': 'derivada parcial',
            
            # Greek letters
            r'\alpha': 'alpha',
            r'\beta': 'beta',
            r'\gamma': 'gamma',
            r'\delta': 'delta',
            r'\epsilon': 'epsilon',
            r'\theta': 'theta',
            r'\lambda': 'lambda',
            r'\mu': 'mu',
            r'\pi': 'pi',
            r'\sigma': 'sigma',
            r'\phi': 'phi',
            r'\omega': 'omega',
            
            # Functions
            r'\sin': 'sen',
            r'\cos': 'cos',
            r'\tan': 'tan',
            r'\cot': 'cot',
            r'\sec': 'sec',
            r'\csc': 'csc',
            r'\arcsin': 'arcsen',
            r'\arccos': 'arccos',
            r'\arctan': 'arctan',
            r'\sinh': 'senh',
            r'\cosh': 'cosh',
            r'\tanh': 'tanh',
            r'\log': 'log',
            r'\ln': 'ln',
            r'\exp': 'exp',
            r'\sqrt': 'raíz',
            r'\abs': 'valor absoluto',
            
            # Operations
            r'\times': '×',
            r'\div': '÷',
            r'\pm': '±',
            r'\mp': '±',
            r'\cdot': '·',
            r'\circ': '°',
            r'\degree': '°',
            
            # Relations
            r'\leq': 'menor o igual que',
            r'\geq': 'mayor o igual que',
            r'\neq': 'diferente de',
            r'\approx': 'aproximadamente',
            r'\equiv': 'equivalente a',
            r'\sim': 'similar a',
            
            # Fractions
            r'\frac': 'fracción',
            r'\dfrac': 'fracción grande',
            
            # Powers and roots
            r'^2': '²',
            r'^3': '³',
            r'^4': 'sup4',
            r'^5': 'sup5',
            r'^6': 'sup6',
            r'^7': 'sup7',
            r'^8': 'sup8',
            r'^9': 'sup9',
            
            # Brackets and delimiters
            r'\left': '',
            r'\right': '',
            r'\{': '{',
            r'\}': '}',
            r'\[': '[',
            r'\]': ']',
            r'\(': '(',
            r'\)': ')',
            
            # Special characters
            r'\n': ' ',
            r'\r': '',
            r'\t': ' ',
        }
    
    def clean_latex_for_unicode(self, latex_text):
        """Clean LaTeX text and convert to Unicode format"""
        if not latex_text:
            return ""
        
        # Remove problematic LaTeX commands
        cleaned = latex_text.replace('\\\\', '\\')
        cleaned = cleaned.replace('\right', 'right')
        cleaned = cleaned.replace('ight', 'right')
        cleaned = cleaned.replace('\r', '')
        cleaned = cleaned.replace('\n', ' ')
        cleaned = cleaned.replace('\t', ' ')
        cleaned = cleaned.strip()
        
        # Apply Unicode mappings
        unicode_text = cleaned
        for latex_symbol, unicode_symbol in self.unicode_mappings.items():
            unicode_text = unicode_text.replace(latex_symbol, unicode_symbol)
        
        # Clean up remaining LaTeX commands
        unicode_text = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', unicode_text)
        unicode_text = re.sub(r'\\[a-zA-Z]+', '', unicode_text)
        unicode_text = re.sub(r'[{}]', '', unicode_text)
        
        # Handle superscripts and subscripts
        unicode_text = re.sub(r'\^(\{([^}]+)\}|([a-zA-Z0-9]))', 
                              lambda m: f'^{m.group(2) or m.group(3)}', unicode_text)
        unicode_text = re.sub(r'_(\{([^}]+)\}|([a-zA-Z0-9]))', 
                              lambda m: f'_{m.group(2) or m.group(3)}', unicode_text)
        
        return unicode_text.strip()
    
    def enhance_latex_with_unicode(self, latex_text):
        """Enhance LaTeX text with Unicode symbols"""
        if not latex_text:
            return ""
        
        enhanced = latex_text
        
        # Apply comprehensive Unicode mappings
        for latex_symbol, unicode_symbol in self.unicode_mappings.items():
            enhanced = enhanced.replace(latex_symbol, unicode_symbol)
        
        # Special handling for mathematical expressions
        enhanced = enhanced.replace('**2', '²')
        enhanced = enhanced.replace('**3', '³')
        enhanced = enhanced.replace('**4', 'sup4')
        enhanced = enhanced.replace('**5', 'sup5')
        
        # Handle common mathematical patterns
        enhanced = enhanced.replace('integral', 'integral')
        enhanced = enhanced.replace('fraccion', 'fracción')
        enhanced = enhanced.replace('raiz', 'raíz')
        
        return enhanced
    
    def format_step_title(self, step_number, step_type):
        """Format step title with Unicode typography"""
        titles = {
            'integral': f'Paso {step_number}: Configuración de la Integral',
            'substitution': f'Paso {step_number}: Sustitución',
            'integration': f'Paso {step_number}: Integración',
            'back_substitution': f'Paso {step_number}: Retro-sustitución',
            'simplification': f'Paso {step_number}: Simplificación',
            'evaluation': f'Paso {step_number}: Evaluación',
            'verification': f'Paso {step_number}: Verificación',
            'result': f'Paso {step_number}: Resultado Final',
            'default': f'Paso {step_number}: Operación Matemática'
        }
        
        return titles.get(step_type.lower(), titles['default'])
    
    def create_step_visualization(self, step_number, step_content, step_type='default'):
        """Create enhanced visualization for a mathematical step"""
        try:
            # Create figure with professional styling
            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')
            
            # Remove axes for clean display
            ax.set_axis_off()
            
            # Clean and enhance the content
            if isinstance(step_content, dict):
                latex_content = step_content.get('latex', step_content.get('content', str(step_content)))
            else:
                latex_content = str(step_content)
            
            # Clean LaTeX and convert to Unicode
            cleaned_latex = self.clean_latex_for_unicode(latex_content)
            unicode_content = self.enhance_latex_with_unicode(cleaned_latex)
            
            # Prepare LaTeX for rendering
            final_latex = self._prepare_latex_for_rendering(latex_content)
            
            # Create step title
            step_title = self.format_step_title(step_number, step_type)
            
            # Render title
            ax.text(0.05, 0.85, step_title, 
                   transform=ax.transAxes,
                   fontsize=14, fontweight='bold',
                   color='#2c3e50',
                   ha='left', va='top')
            
            # Render mathematical content
            if final_latex:
                try:
                    ax.text(0.05, 0.5, final_latex,
                           transform=ax.transAxes,
                           fontsize=16,
                           color='#34495e',
                           ha='left', va='center')
                except Exception as latex_error:
                    # Fallback to Unicode text if LaTeX fails
                    ax.text(0.05, 0.5, unicode_content,
                           transform=ax.transAxes,
                           fontsize=14,
                           color='#34495e',
                           ha='left', va='center')
            else:
                # Use Unicode text directly
                ax.text(0.05, 0.5, unicode_content,
                       transform=ax.transAxes,
                       fontsize=14,
                       color='#34495e',
                       ha='left', va='center')
            
            # Add decorative elements
            self._add_step_decorations(ax, step_number)
            
            # Set figure boundaries
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            print(f"Error creating step visualization: {e}")
            # Create fallback figure
            fig, ax = plt.subplots(1, 1, figsize=(12, 2))
            ax.set_axis_off()
            ax.text(0.5, 0.5, f"Paso {step_number}: Error en visualización",
                   transform=ax.transAxes,
                   fontsize=12, ha='center', va='center')
            return fig
    
    def _prepare_latex_for_rendering(self, latex_text):
        """Prepare LaTeX text for matplotlib rendering"""
        if not latex_text:
            return ""
        
        # Clean problematic characters
        cleaned = latex_text.replace('\\\\', '\\')
        cleaned = cleaned.replace('\right', 'right')
        cleaned = cleaned.replace('ight', 'right')
        cleaned = cleaned.replace('\r', '')
        cleaned = cleaned.replace('\n', ' ')
        cleaned = cleaned.strip()
        
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
        
        # Validate LaTeX
        if not final_latex.strip() or final_latex.strip() == '$$' or len(final_latex) < 3:
            return ""
        
        return final_latex
    
    def _add_step_decorations(self, ax, step_number):
        """Add decorative elements to step visualization"""
        # Add step number badge
        badge_color = '#3498db'
        if step_number == 1:
            badge_color = '#27ae60'  # Green for first step
        elif step_number % 5 == 0:
            badge_color = '#e74c3c'  # Red for every 5th step
        
        # Create step number circle
        circle = patches.Circle((0.95, 0.85), 0.08, 
                               transform=ax.transAxes,
                               facecolor=badge_color,
                               edgecolor='#2c3e50',
                               linewidth=2)
        ax.add_patch(circle)
        
        # Add step number text
        ax.text(0.95, 0.85, str(step_number),
               transform=ax.transAxes,
               fontsize=12, fontweight='bold',
               color='white',
               ha='center', va='center')
        
        # Add subtle separator line
        ax.axhline(y=0.25, color='#bdc3c7', linestyle='--', alpha=0.3)
    
    def create_complete_step_sequence(self, steps_list):
        """Create visualization for complete step sequence"""
        try:
            # Calculate figure size based on number of steps
            n_steps = len(steps_list)
            fig_height = max(3, n_steps * 1.5)
            
            fig, axes = plt.subplots(n_steps, 1, figsize=(12, fig_height))
            if n_steps == 1:
                axes = [axes]
            
            fig.patch.set_facecolor('#ffffff')
            
            for i, (step_number, step_content, step_type) in enumerate(steps_list):
                ax = axes[i]
                ax.set_facecolor('#ffffff')
                ax.set_axis_off()
                
                # Process step content
                if isinstance(step_content, dict):
                    latex_content = step_content.get('latex', step_content.get('content', str(step_content)))
                else:
                    latex_content = str(step_content)
                
                # Clean and enhance
                cleaned_latex = self.clean_latex_for_unicode(latex_content)
                unicode_content = self.enhance_latex_with_unicode(cleaned_latex)
                final_latex = self._prepare_latex_for_rendering(latex_content)
                
                # Create step title
                step_title = self.format_step_title(step_number, step_type)
                
                # Render title
                ax.text(0.05, 0.85, step_title,
                       transform=ax.transAxes,
                       fontsize=12, fontweight='bold',
                       color='#2c3e50',
                       ha='left', va='top')
                
                # Render content
                if final_latex:
                    try:
                        ax.text(0.05, 0.5, final_latex,
                               transform=ax.transAxes,
                               fontsize=14,
                               color='#34495e',
                               ha='left', va='center')
                    except:
                        ax.text(0.05, 0.5, unicode_content,
                               transform=ax.transAxes,
                               fontsize=12,
                               color='#34495e',
                               ha='left', va='center')
                else:
                    ax.text(0.05, 0.5, unicode_content,
                           transform=ax.transAxes,
                           fontsize=12,
                           color='#34495e',
                           ha='left', va='center')
                
                # Add decorations
                self._add_step_decorations(ax, step_number)
                
                # Add separator between steps (except last)
                if i < n_steps - 1:
                    ax.axhline(y=0.05, color='#95a5a6', linestyle='-', alpha=0.5)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"Error creating complete step sequence: {e}")
            # Create fallback
            fig, ax = plt.subplots(1, 1, figsize=(12, 4))
            ax.set_axis_off()
            ax.text(0.5, 0.5, "Error en visualización de secuencia completa",
                   transform=ax.transAxes,
                   fontsize=14, ha='center', va='center')
            return fig

def test_enhanced_visualization():
    """Test the enhanced step visualization system"""
    print("=== Test de Visualización Mejorada de Pasos ===")
    
    visualizer = EnhancedStepVisualizer()
    
    # Test Unicode conversion
    test_cases = [
        r'\int x^2 dx',
        r'\frac{x^2}{x+1}',
        r'\sin(x) + \cos(x)',
        r'\sqrt{x^2 + 1}',
        r'\sum_{i=1}^{n} i^2'
    ]
    
    print("\nTest 1: Conversión Unicode")
    print("=" * 40)
    
    for test_case in test_cases:
        unicode_result = visualizer.clean_latex_for_unicode(test_case)
        enhanced_result = visualizer.enhance_latex_with_unicode(test_case)
        print(f"LaTeX: {test_case}")
        print(f"Unicode: {unicode_result}")
        print(f"Enhanced: {enhanced_result}")
        print()
    
    print("Test 2: Creación de Visualización Individual")
    print("=" * 45)
    
    # Test individual step visualization
    try:
        fig = visualizer.create_step_visualization(1, r'\int x^2 dx', 'integral')
        print("Visualización individual creada exitosamente")
        plt.close(fig)
    except Exception as e:
        print(f"Error en visualización individual: {e}")
    
    print("\nTest 3: Creación de Secuencia Completa")
    print("=" * 40)
    
    # Test complete sequence
    steps = [
        (1, r'\int (2x + 3) dx', 'integral'),
        (2, r'x^2 + 3x + C', 'integration'),
        (3, r'\text{Resultado final}', 'result')
    ]
    
    try:
        fig = visualizer.create_complete_step_sequence(steps)
        print("Secuencia completa creada exitosamente")
        plt.close(fig)
    except Exception as e:
        print(f"Error en secuencia completa: {e}")
    
    print("\n=== Test Completado ===")

if __name__ == "__main__":
    test_enhanced_visualization()

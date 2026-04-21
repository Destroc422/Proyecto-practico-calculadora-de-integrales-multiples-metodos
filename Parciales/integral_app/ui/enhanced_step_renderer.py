#!/usr/bin/env python3
"""
Enhanced Step Renderer for Professional Main Window
Integrates Unicode typography and LaTeX rendering for step-by-step visualization
"""
import sys
import os
import logging
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced visualizer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
try:
    from enhanced_step_visualization import EnhancedStepVisualizer
except ImportError:
    EnhancedStepVisualizer = None

logger = logging.getLogger(__name__)

class EnhancedStepRenderer:
    """Enhanced step renderer with Unicode and LaTeX integration"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        if EnhancedStepVisualizer:
            self.visualizer = EnhancedStepVisualizer()
        else:
            self.visualizer = None
            logger.warning("EnhancedStepVisualizer not available, using fallback")
        
        self.step_canvases = {}
        self.step_figures = {}
    
    def render_enhanced_steps(self, steps_container, result):
        """Render steps with enhanced Unicode and LaTeX visualization"""
        try:
            logger.info("Starting enhanced step rendering")
            
            # Clear existing steps
            for widget in steps_container.winfo_children():
                widget.destroy()
            
            # Clear stored canvases and figures
            self.step_canvases.clear()
            self.step_figures.clear()
            
            if not hasattr(result, 'steps') or not result.steps:
                logger.info("No steps to render")
                return
            
            # Create header
            self._create_steps_header(steps_container)
            
            # Process each step
            steps_data = []
            for i, step in enumerate(result.steps, 1):
                step_data = self._process_step_data(i, step)
                if step_data:
                    steps_data.append(step_data)
            
            # Render steps
            if steps_data:
                self._render_individual_steps(steps_container, steps_data)
                self._create_complete_sequence_view(steps_container, steps_data)
            
            logger.info(f"Enhanced step rendering completed for {len(steps_data)} steps")
            
        except Exception as e:
            logger.error(f"Error in enhanced step rendering: {e}")
            self._render_fallback_steps(steps_container, result)
    
    def _create_steps_header(self, container):
        """Create professional header for steps section"""
        header_frame = ttk.Frame(container, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="Pasos del Cálculo - Visualización Profesional",
                               style='Header.TLabel')
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Cada paso se muestra con tipología Unicode y renderizado LaTeX",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=(0, 10))
    
    def _process_step_data(self, step_number, step):
        """Process step data and extract content"""
        try:
            logger.info(f"Processing step {step_number}: {type(step)}")
            
            # Extract content from step
            if isinstance(step, dict):
                latex_content = step.get('latex', step.get('content', ''))
                step_type = step.get('type', 'default')
                description = step.get('description', '')
            else:
                latex_content = str(step)
                step_type = 'default'
                description = ''
            
            # Determine step type based on content
            if not step_type or step_type == 'default':
                step_type = self._determine_step_type(latex_content, step_number)
            
            # Clean and enhance content
            if self.visualizer:
                unicode_content = self.visualizer.clean_latex_for_unicode(latex_content)
                enhanced_content = self.visualizer.enhance_latex_with_unicode(latex_content)
            else:
                unicode_content = latex_content
                enhanced_content = latex_content
            
            return {
                'number': step_number,
                'latex': latex_content,
                'unicode': unicode_content,
                'enhanced': enhanced_content,
                'type': step_type,
                'description': description
            }
            
        except Exception as e:
            logger.error(f"Error processing step {step_number}: {e}")
            return None
    
    def _determine_step_type(self, content, step_number):
        """Determine step type based on content"""
        content_lower = content.lower()
        
        if '\\int' in content or 'integral' in content_lower:
            return 'integral'
        elif 'substitute' in content_lower or 'u=' in content:
            return 'substitution'
        elif 'integrate' in content_lower:
            return 'integration'
        elif 'back' in content_lower or 'original' in content_lower:
            return 'back_substitution'
        elif 'simplify' in content_lower or 'simplif' in content_lower:
            return 'simplification'
        elif 'evaluat' in content_lower or step_number == len(getattr(self.parent, 'current_result', {}).get('steps', [])):
            return 'evaluation'
        elif 'verif' in content_lower or 'deriv' in content_lower:
            return 'verification'
        elif 'result' in content_lower or step_number == len(getattr(self.parent, 'current_result', {}).get('steps', [])):
            return 'result'
        else:
            return 'default'
    
    def _render_individual_steps(self, container, steps_data):
        """Render individual steps with enhanced visualization"""
        # Create section for individual steps
        individual_frame = ttk.LabelFrame(container, text="Pasos Individuales", style='Card.TFrame')
        individual_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create scrollable frame
        canvas = tk.Canvas(individual_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(individual_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Render each step
        for step_data in steps_data:
            self._render_single_step(scrollable_frame, step_data)
    
    def _render_single_step(self, container, step_data):
        """Render a single step with enhanced visualization"""
        # Create step frame
        step_frame = ttk.Frame(container, style='Step.TFrame')
        step_frame.pack(fill='x', padx=10, pady=5)
        
        # Step header
        header_frame = ttk.Frame(step_frame)
        header_frame.pack(fill='x', pady=(5, 0))
        
        # Step number badge
        step_number = step_data['number']
        badge_color = self._get_step_color(step_number)
        
        badge_label = ttk.Label(header_frame, text=f"  {step_number}  ",
                               style=f'Step{badge_color}Badge.TLabel')
        badge_label.pack(side='left', padx=(0, 10))
        
        # Step title
        step_title = self._get_step_title(step_data)
        title_label = ttk.Label(header_frame, text=step_title,
                                style='StepTitle.TLabel')
        title_label.pack(side='left', fill='x', expand=True)
        
        # Step content area
        content_frame = ttk.Frame(step_frame)
        content_frame.pack(fill='x', padx=10, pady=5)
        
        # Render mathematical content
        if self.visualizer and step_data['latex']:
            self._render_step_latex(content_frame, step_data)
        else:
            self._render_step_unicode(content_frame, step_data)
        
        # Step description (if available)
        if step_data['description']:
            desc_label = ttk.Label(content_frame, text=step_data['description'],
                                   style='StepDescription.TLabel')
            desc_label.pack(fill='x', pady=(5, 0))
        
        # Separator
        separator = ttk.Separator(step_frame, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=(5, 0))
    
    def _render_step_latex(self, container, step_data):
        """Render step with LaTeX visualization"""
        try:
            # Create matplotlib figure
            fig = self.visualizer.create_step_visualization(
                step_data['number'],
                step_data['latex'],
                step_data['type']
            )
            
            # Create canvas for matplotlib figure
            canvas_frame = ttk.Frame(container)
            canvas_frame.pack(fill='x', pady=5)
            
            canvas = FigureCanvasTkAgg(fig, canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='x')
            
            # Store for cleanup
            self.step_canvases[f"step_{step_data['number']}"] = canvas
            self.step_figures[f"step_{step_data['number']}"] = fig
            
        except Exception as e:
            logger.error(f"Error rendering LaTeX for step {step_data['number']}: {e}")
            # Fallback to Unicode
            self._render_step_unicode(container, step_data)
    
    def _render_step_unicode(self, container, step_data):
        """Render step with Unicode text"""
        # Create text frame
        text_frame = ttk.Frame(container, style='UnicodeText.TFrame')
        text_frame.pack(fill='x', pady=5)
        
        # Unicode content
        unicode_text = step_data['enhanced']
        
        # Create text widget for Unicode display
        text_widget = tk.Text(text_frame, height=3, wrap='word',
                             bg='#f8f9fa', fg='#2c3e50',
                             font=('Consolas', 12, 'normal'),
                             relief='flat', bd=1)
        text_widget.pack(fill='x', padx=5, pady=5)
        
        # Insert content
        text_widget.insert('1.0', unicode_text)
        text_widget.config(state='disabled')
    
    def _create_complete_sequence_view(self, container, steps_data):
        """Create complete step sequence visualization"""
        if not self.visualizer or len(steps_data) < 2:
            return
        
        # Create section for complete sequence
        sequence_frame = ttk.LabelFrame(container, text="Secuencia Completa", style='Card.TFrame')
        sequence_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create matplotlib figure for complete sequence
        try:
            steps_list = [(step['number'], step['latex'], step['type']) for step in steps_data]
            fig = self.visualizer.create_complete_step_sequence(steps_list)
            
            # Create canvas for figure
            canvas_frame = ttk.Frame(sequence_frame)
            canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            canvas = FigureCanvasTkAgg(fig, canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            # Store for cleanup
            self.step_canvases['complete_sequence'] = canvas
            self.step_figures['complete_sequence'] = fig
            
        except Exception as e:
            logger.error(f"Error creating complete sequence: {e}")
            # Create fallback text view
            self._create_sequence_fallback(sequence_frame, steps_data)
    
    def _create_sequence_fallback(self, container, steps_data):
        """Create fallback text view for complete sequence"""
        text_frame = ttk.Frame(container, style='UnicodeText.TFrame')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create text widget
        text_widget = tk.Text(text_frame, height=10, wrap='word',
                             bg='#f8f9fa', fg='#2c3e50',
                             font=('Consolas', 11, 'normal'),
                             relief='flat', bd=1)
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Build sequence text
        sequence_text = "Secuencia Completa de Pasos\n"
        sequence_text += "=" * 50 + "\n\n"
        
        for step_data in steps_data:
            sequence_text += f"Paso {step_data['number']}: {step_data['title']}\n"
            sequence_text += f"Contenido: {step_data['enhanced']}\n"
            sequence_text += "-" * 30 + "\n\n"
        
        # Insert content
        text_widget.insert('1.0', sequence_text)
        text_widget.config(state='disabled')
    
    def _get_step_color(self, step_number):
        """Get color for step based on number"""
        if step_number == 1:
            return 'Green'
        elif step_number % 5 == 0:
            return 'Red'
        else:
            return 'Blue'
    
    def _get_step_title(self, step_data):
        """Get formatted title for step"""
        step_number = step_data['number']
        step_type = step_data['type']
        
        titles = {
            'integral': f'Configuración de la Integral',
            'substitution': f'Sustitución',
            'integration': f'Integración',
            'back_substitution': f'Retro-sustitución',
            'simplification': f'Simplificación',
            'evaluation': f'Evaluación',
            'verification': f'Verificación',
            'result': f'Resultado Final',
            'default': f'Operación Matemática'
        }
        
        base_title = titles.get(step_type, titles['default'])
        return f"Paso {step_number}: {base_title}"
    
    def _render_fallback_steps(self, container, result):
        """Render fallback steps if enhanced rendering fails"""
        logger.info("Using fallback step rendering")
        
        # Clear container
        for widget in container.winfo_children():
            widget.destroy()
        
        # Create simple text display
        text_frame = ttk.Frame(container, style='Card.TFrame')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, height=15, wrap='word',
                             bg='#ffffff', fg='#2c3e50',
                             font=('Arial', 10, 'normal'))
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Build fallback text
        steps_text = "Pasos del Cálculo (Modo Simplificado)\n"
        steps_text += "=" * 50 + "\n\n"
        
        if hasattr(result, 'steps') and result.steps:
            for i, step in enumerate(result.steps, 1):
                steps_text += f"Paso {i}:\n"
                if isinstance(step, dict):
                    content = step.get('content', step.get('latex', str(step)))
                else:
                    content = str(step)
                steps_text += f"{content}\n\n"
        
        # Insert content
        text_widget.insert('1.0', steps_text)
        text_widget.config(state='disabled')
    
    def cleanup(self):
        """Clean up matplotlib figures and canvases"""
        try:
            # Close all figures
            for fig in self.step_figures.values():
                if fig:
                    plt.close(fig)
            
            # Clear dictionaries
            self.step_figures.clear()
            self.step_canvases.clear()
            
            logger.info("Enhanced step renderer cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def test_enhanced_renderer():
    """Test the enhanced step renderer"""
    print("=== Test de Enhanced Step Renderer ===")
    
    # Mock result for testing
    class MockResult:
        def __init__(self):
            self.steps = [
                {'latex': r'\int (2x + 3) dx', 'type': 'integral'},
                {'latex': r'x^2 + 3x + C', 'type': 'integration'},
                {'latex': r'\text{Resultado final}', 'type': 'result'}
            ]
    
    # Test renderer initialization
    try:
        # Mock parent window
        class MockParent:
            def __init__(self):
                pass
        
        renderer = EnhancedStepRenderer(MockParent())
        print("Enhanced step renderer initialized successfully")
        
        # Test step processing
        result = MockResult()
        for i, step in enumerate(result.steps, 1):
            step_data = renderer._process_step_data(i, step)
            if step_data:
                print(f"Step {i}: {step_data['type']} - {step_data['enhanced']}")
        
        print("Test completed successfully")
        
    except Exception as e:
        print(f"Error in test: {e}")

if __name__ == "__main__":
    test_enhanced_renderer()

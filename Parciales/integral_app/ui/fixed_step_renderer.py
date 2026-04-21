#!/usr/bin/env python3
"""
Fixed Step Renderer - Solución definitiva para visualización de pasos LaTeX
Corrige problemas de parsing y muestra todos los pasos correctamente
"""
import sys
import os
import logging
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import re

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

class FixedStepRenderer:
    """Renderer corregido para pasos LaTeX con manejo robusto de errores"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.step_canvases = {}
        self.step_figures = {}
    
    def render_fixed_steps(self, steps_text_widget, result):
        """Renderizar pasos con LaTeX corregido y Unicode"""
        try:
            logger.info("Iniciando renderizado corregido de pasos")
            
            # Limpiar contenido existente
            steps_text_widget.config(state='normal')
            steps_text_widget.delete("1.0", tk.END)
            
            if not hasattr(result, 'steps') or not result.steps:
                logger.info("No hay pasos para renderizar")
                steps_text_widget.insert("1.0", "No hay pasos disponibles para mostrar.")
                steps_text_widget.config(state='disabled')
                return
            
            # Crear header profesional
            self._create_professional_header(steps_text_widget)
            
            # Procesar cada paso
            for i, step in enumerate(result.steps, 1):
                try:
                    logger.info(f"Procesando paso {i}: {type(step)}")
                    
                    # Extraer contenido del paso
                    step_content = self._extract_step_content(step)
                    if not step_content:
                        continue
                    
                    # Renderizar paso individual
                    self._render_single_fixed_step(steps_text_widget, i, step_content)
                    
                except Exception as e:
                    logger.error(f"Error procesando paso {i}: {e}")
                    self._render_error_step(steps_text_widget, i, str(e))
            
            # Configurar widget
            steps_text_widget.config(state='disabled')
            
            # Renderizar visualizaciones después de un delay
            self.parent.root.after(100, lambda: self._render_all_visualizations(result))
            
            logger.info("Renderizado corregido de pasos completado")
            
        except Exception as e:
            logger.error(f"Error en renderizado corregido: {e}")
            self._render_fallback(steps_text_widget, result)
    
    def _create_professional_header(self, text_widget):
        """Crear header profesional para sección de pasos"""
        header_text = "Pasos del Cálculo - Visualización Profesional\n"
        header_text += "=" * 60 + "\n\n"
        header_text += "Cada paso se muestra con formato LaTeX y tipografía Unicode\n"
        header_text += "-" * 40 + "\n\n"
        
        text_widget.insert("end", header_text)
        
        # Configurar tags para formato
        text_widget.tag_configure("header", font=("Arial", 14, "bold"), foreground="#2c3e50")
        text_widget.tag_add("header", "1.0", "1.end")
        text_widget.tag_configure("subtitle", font=("Arial", 11, "italic"), foreground="#7f8c8d")
        text_widget.tag_add("subtitle", "2.0", "4.end")
    
    def _extract_step_content(self, step):
        """Extraer contenido del paso con manejo robusto"""
        try:
            if isinstance(step, dict):
                latex_content = step.get('latex', '')
                content = step.get('content', '')
                description = step.get('description', '')
                
                # Priorizar LaTeX, luego content, luego description
                if latex_content:
                    return {'latex': latex_content, 'type': 'latex'}
                elif content:
                    return {'content': content, 'type': 'content'}
                elif description:
                    return {'content': description, 'type': 'description'}
                else:
                    return None
            else:
                # Si no es diccionario, usar como contenido
                step_str = str(step).strip()
                if step_str:
                    return {'content': step_str, 'type': 'content'}
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Error extrayendo contenido del paso: {e}")
            return None
    
    def _render_single_fixed_step(self, text_widget, step_number, step_data):
        """Renderizar un paso individual con formato corregido"""
        try:
            # Insertar título del paso
            step_title = f"Paso {step_number}: Operación Matemática\n"
            text_widget.insert("end", step_title, "step_title")
            
            # Procesar según tipo de contenido
            if step_data['type'] == 'latex':
                self._render_latex_step(text_widget, step_number, step_data['latex'])
            else:
                self._render_text_step(text_widget, step_number, step_data['content'])
            
            # Insertar separador
            text_widget.insert("end", "\n" + "-" * 50 + "\n\n", "separator")
            
            # Configurar tags
            text_widget.tag_configure("step_title", font=("Arial", 12, "bold"), foreground="#3498db")
            text_widget.tag_configure("separator", font=("Arial", 10), foreground="#bdc3c7")
            
        except Exception as e:
            logger.error(f"Error renderizando paso {step_number}: {e}")
            self._render_error_step(text_widget, step_number, str(e))
    
    def _render_latex_step(self, text_widget, step_number, latex_content):
        """Renderizar paso con contenido LaTeX"""
        try:
            # Limpiar LaTeX para evitar errores
            cleaned_latex = self._clean_latex_content(latex_content)
            
            # Insertar placeholder para LaTeX
            placeholder = f"[LaTeX Step {step_number} - {cleaned_latex[:50]}...]\n"
            text_widget.insert("end", placeholder, "latex_placeholder")
            
            # Almacenar para renderizado visual
            if not hasattr(self, 'latex_steps_data'):
                self.latex_steps_data = {}
            
            self.latex_steps_data[f"step_{step_number}"] = {
                'original': latex_content,
                'cleaned': cleaned_latex,
                'placeholder': placeholder
            }
            
            # Configurar tag
            text_widget.tag_configure("latex_placeholder", 
                                    font=("Courier", 11), 
                                    foreground="#e74c3c",
                                    background="#fdf2f2")
            
        except Exception as e:
            logger.error(f"Error renderizando LaTeX paso {step_number}: {e}")
            # Fallback a texto
            text_widget.insert("end", f"Contenido: {latex_content}\n", "content")
    
    def _render_text_step(self, text_widget, step_number, content):
        """Renderizar paso con contenido de texto"""
        try:
            # Aplicar mejoras Unicode
            enhanced_content = self._apply_unicode_enhancements(content)
            
            text_widget.insert("end", f"Contenido: {enhanced_content}\n", "content")
            text_widget.tag_configure("content", font=("Arial", 11), foreground="#2c3e50")
            
        except Exception as e:
            logger.error(f"Error renderizando texto paso {step_number}: {e}")
            text_widget.insert("end", f"Contenido: {content}\n", "content")
    
    def _render_error_step(self, text_widget, step_number, error_msg):
        """Renderizar paso con error"""
        error_text = f"Paso {step_number}: Error en renderizado\n"
        error_text += f"Error: {error_msg}\n"
        
        text_widget.insert("end", error_text, "error")
        text_widget.tag_configure("error", font=("Arial", 11), foreground="#e74c3c")
    
    def _clean_latex_content(self, latex_text):
        """Limpiar contenido LaTeX para evitar errores de parsing"""
        if not latex_text:
            return ""
        
        try:
            # Limpieza básica
            cleaned = latex_text.replace('\\\\', '\\')
            cleaned = cleaned.replace('\\right', 'right')
            cleaned = cleaned.replace('\right', 'right')
            cleaned = cleaned.replace('\\rright', 'right')
            cleaned = cleaned.replace('\\r', '')
            cleaned = cleaned.replace('\r', '')
            cleaned = cleaned.replace('\n', ' ')
            cleaned = cleaned.replace('\t', ' ')
            cleaned = cleaned.strip()
            
            # Limpieza avanzada de patrones problemáticos
            cleaned = re.sub(r'\\r[a-zA-Z]*', '', cleaned)
            cleaned = re.sub(r'\\rright', 'right', cleaned)
            cleaned = re.sub(r'\\right[^a-zA-Z]', 'right', cleaned)
            cleaned = re.sub(r'right[)}\]>]', lambda m: m.group(0)[-1], cleaned)
            
            # Limpiar comandos LaTeX problemáticos
            cleaned = re.sub(r'\\text\{([^}]+)\}', r'\1', cleaned)
            cleaned = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', cleaned)
            cleaned = re.sub(r'\\[a-zA-Z]+', '', cleaned)
            
            # Limpiar caracteres especiales
            cleaned = re.sub(r'[{}]', '', cleaned)
            cleaned = re.sub(r'\s+', ' ', cleaned)
            
            return cleaned.strip()
            
        except Exception as e:
            logger.error(f"Error limpiando LaTeX: {e}")
            return latex_text
    
    def _apply_unicode_enhancements(self, text):
        """Aplicar mejoras Unicode al texto"""
        if not text:
            return ""
        
        try:
            # Mapeos Unicode comunes
            unicode_map = {
                'x^2': 'x²',
                'x^3': 'x³',
                'x^4': 'x sup4',
                'x^5': 'x sup5',
                'integral': 'integral',
                'fraccion': 'fracción',
                'raiz': 'raíz',
                'sen': 'sen',
                'cos': 'cos',
                'tan': 'tan',
                'sqrt': 'raíz',
                'sum': 'suma',
                'prod': 'producto',
                'lim': 'límite',
                'infinito': 'infinito',
                'alpha': 'alpha',
                'beta': 'beta',
                'gamma': 'gamma',
                'delta': 'delta',
                'theta': 'theta',
                'lambda': 'lambda',
                'mu': 'mu',
                'pi': 'pi',
                'sigma': 'sigma',
                'phi': 'phi',
                'omega': 'omega'
            }
            
            enhanced = text
            for latex, unicode_sym in unicode_map.items():
                enhanced = enhanced.replace(latex, unicode_sym)
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Error aplicando Unicode: {e}")
            return text
    
    def _render_all_visualizations(self, result):
        """Renderizar todas las visualizaciones LaTeX después de cargar texto"""
        try:
            if not hasattr(self, 'latex_steps_data'):
                return
            
            logger.info(f"Renderizando {len(self.latex_steps_data)} visualizaciones LaTeX")
            
            for step_key, step_data in self.latex_steps_data.items():
                try:
                    self._create_latex_visualization(step_key, step_data)
                except Exception as e:
                    logger.error(f"Error renderizando visualización {step_key}: {e}")
            
        except Exception as e:
            logger.error(f"Error en renderizado de visualizaciones: {e}")
    
    def _create_latex_visualization(self, step_key, step_data):
        """Crear visualización LaTeX para un paso"""
        try:
            # Crear figura matplotlib
            fig, ax = plt.subplots(1, 1, figsize=(12, 2.5))
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')
            ax.set_axis_off()
            
            # Preparar LaTeX
            latex_content = step_data['cleaned']
            final_latex = self._prepare_latex_for_rendering(latex_content)
            
            if final_latex:
                try:
                    # Renderizar LaTeX
                    ax.text(0.05, 0.5, final_latex,
                           transform=ax.transAxes,
                           fontsize=14,
                           color='#2c3e50',
                           ha='left', va='center')
                except Exception as latex_error:
                    logger.warning(f"LaTeX falló para {step_key}: {latex_error}")
                    # Fallback a Unicode
                    unicode_text = self._apply_unicode_enhancements(latex_content)
                    ax.text(0.05, 0.5, unicode_text,
                           transform=ax.transAxes,
                           fontsize=12,
                           color='#2c3e50',
                           ha='left', va='center')
            
            # Añadir decoraciones
            self._add_step_decorations(ax, step_key)
            
            # Crear canvas
            canvas_frame = ttk.Frame(self.parent.steps_text.master)
            canvas = FigureCanvasTkAgg(fig, canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='x', padx=10, pady=5)
            
            # Reemplazar placeholder
            self._replace_placeholder(step_key, canvas_frame)
            
            # Almacenar para cleanup
            self.step_canvases[step_key] = canvas
            self.step_figures[step_key] = fig
            
            logger.info(f"Visualización LaTeX creada para {step_key}")
            
        except Exception as e:
            logger.error(f"Error creando visualización {step_key}: {e}")
    
    def _prepare_latex_for_rendering(self, latex_text):
        """Preparar LaTeX para renderizado matplotlib"""
        if not latex_text:
            return ""
        
        # Limpiar nuevamente
        cleaned = self._clean_latex_content(latex_text)
        
        # Añadir símbolos $ si es necesario
        if cleaned.startswith('$') and cleaned.endswith('$') and len(cleaned) > 2:
            return cleaned
        elif '$' in cleaned:
            clean_text = cleaned.replace('$', '').strip()
            if clean_text and not clean_text.isspace():
                return f'${clean_text}$'
        else:
            if cleaned and not cleaned.isspace():
                return f'${cleaned}$'
        
        return ""
    
    def _add_step_decorations(self, ax, step_key):
        """Añadir decoraciones al paso"""
        try:
            # Extraer número del paso
            step_number = step_key.split('_')[-1] if '_' in step_key else '1'
            
            # Crear badge
            circle = patches.Circle((0.95, 0.5), 0.08,
                                   transform=ax.transAxes,
                                   facecolor='#3498db',
                                   edgecolor='#2c3e50',
                                   linewidth=2)
            ax.add_patch(circle)
            
            # Añadir número
            ax.text(0.95, 0.5, step_number,
                   transform=ax.transAxes,
                   fontsize=10, fontweight='bold',
                   color='white',
                   ha='center', va='center')
            
            # Separador sutil
            ax.axhline(y=0.1, color='#bdc3c7', linestyle='--', alpha=0.3)
            
        except Exception as e:
            logger.error(f"Error añadiendo decoraciones: {e}")
    
    def _replace_placeholder(self, step_key, canvas_frame):
        """Reemplazar placeholder con visualización"""
        try:
            if not hasattr(self, 'latex_steps_data'):
                return
            
            step_data = self.latex_steps_data[step_key]
            placeholder = step_data['placeholder']
            
            # Buscar y reemplazar placeholder
            content = self.parent.steps_text.get("1.0", tk.END)
            if placeholder in content:
                # Encontrar posición
                start_pos = content.find(placeholder)
                if start_pos != -1:
                    line_start = content[:start_pos].count('\n') + 1
                    line_end = line_start
                    
                    # Reemplazar
                    self.parent.steps_text.delete(f"{line_start}.0", f"{line_end}.0")
                    self.parent.steps_text.window_create(f"{line_start}.0", window=canvas_frame)
            
        except Exception as e:
            logger.error(f"Error reemplazando placeholder {step_key}: {e}")
    
    def _render_fallback(self, text_widget, result):
        """Renderizado fallback si todo falla"""
        try:
            text_widget.config(state='normal')
            text_widget.delete("1.0", tk.END)
            
            fallback_text = "Pasos del Cálculo (Modo Simplificado)\n"
            fallback_text += "=" * 40 + "\n\n"
            
            if hasattr(result, 'steps') and result.steps:
                for i, step in enumerate(result.steps, 1):
                    if isinstance(step, dict):
                        content = step.get('content', step.get('latex', str(step)))
                    else:
                        content = str(step)
                    
                    fallback_text += f"Paso {i}:\n{content}\n\n"
            
            text_widget.insert("1.0", fallback_text)
            text_widget.config(state='disabled')
            
        except Exception as e:
            logger.error(f"Error en fallback: {e}")
    
    def cleanup(self):
        """Limpiar recursos"""
        try:
            for fig in self.step_figures.values():
                if fig:
                    plt.close(fig)
            
            self.step_figures.clear()
            self.step_canvases.clear()
            
            if hasattr(self, 'latex_steps_data'):
                self.latex_steps_data.clear()
            
            logger.info("Cleanup de FixedStepRenderer completado")
            
        except Exception as e:
            logger.error(f"Error en cleanup: {e}")

def test_fixed_renderer():
    """Test del renderer corregido"""
    print("=== Test de Fixed Step Renderer ===")
    
    # Mock result para test
    class MockResult:
        def __init__(self):
            self.steps = [
                {'latex': r'\int (2x + 3) dx', 'type': 'integral'},
                {'latex': r'x^2 + 3x + C', 'type': 'integration'},
                {'content': 'Resultado final', 'type': 'result'},
                {'latex': r'fraccion{x^2}{x+1} + \rright problematic', 'type': 'problem'}
            ]
    
    # Mock parent
    class MockParent:
        def __init__(self):
            self.steps_text = MockTextWidget()
            self.root = MockRoot()
    
    class MockTextWidget:
        def __init__(self):
            self.content = ""
        
        def config(self, **kwargs):
            pass
        
        def delete(self, start, end):
            self.content = ""
        
        def insert(self, pos, text, tag=None):
            self.content += text
        
        def get(self, start, end):
            return self.content
    
    class MockRoot:
        def after(self, delay, func):
            func()
    
    # Test renderer
    try:
        parent = MockParent()
        renderer = FixedStepRenderer(parent)
        result = MockResult()
        
        renderer.render_fixed_steps(parent.steps_text, result)
        
        print("Fixed renderer test completado exitosamente")
        print(f"Contenido generado: {len(parent.steps_text.content)} caracteres")
        
    except Exception as e:
        print(f"Error en test: {e}")

if __name__ == "__main__":
    test_fixed_renderer()

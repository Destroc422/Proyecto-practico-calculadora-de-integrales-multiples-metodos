"""
Enhanced UI Controls for Professional Calculator
Advanced plotting controls with interactive features
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
import threading
import time

logger = logging.getLogger(__name__)


class EnhancedPlotControls:
    """Enhanced plotting controls with professional features"""
    
    def __init__(self, parent, plotter_callback: Callable):
        """Initialize enhanced plot controls"""
        self.parent = parent
        self.plotter_callback = plotter_callback
        self.current_figure = None
        self.current_canvas = None
        self.toolbar = None
        
        # Control variables
        self.zoom_level = tk.DoubleVar(value=1.0)
        self.pan_offset_x = tk.DoubleVar(value=0.0)
        self.pan_offset_y = tk.DoubleVar(value=0.0)
        self.grid_enabled = tk.BooleanVar(value=True)
        self.legend_enabled = tk.BooleanVar(value=True)
        self.quality_level = tk.StringVar(value="auto")
        self.animation_enabled = tk.BooleanVar(value=False)
        
        # Plot history for undo/redo
        self.plot_history = []
        self.history_index = -1
        
        # Animation state
        self.animation_thread = None
        self.animation_running = False
        
        self._create_enhanced_controls()
    
    def _create_enhanced_controls(self):
        """Create enhanced control panel"""
        # Main control frame
        self.control_frame = ttk.LabelFrame(self.parent, text="Control de Gráficos", padding="10")
        self.control_frame.pack(fill="x", padx=5, pady=5)
        
        # Row 1: Basic controls
        basic_frame = ttk.Frame(self.control_frame)
        basic_frame.pack(fill="x", pady=2)
        
        ttk.Button(basic_frame, text="Actualizar Gráfico", 
                  command=self._refresh_plot).pack(side="left", padx=2)
        ttk.Button(basic_frame, text="Limpiar", 
                  command=self._clear_plot).pack(side="left", padx=2)
        ttk.Button(basic_frame, text="Pantalla Completa", 
                  command=self._fullscreen_plot).pack(side="left", padx=2)
        
        # Row 2: Zoom controls
        zoom_frame = ttk.Frame(self.control_frame)
        zoom_frame.pack(fill="x", pady=2)
        
        ttk.Label(zoom_frame, text="Zoom:").pack(side="left", padx=2)
        ttk.Scale(zoom_frame, from_=0.1, to=5.0, variable=self.zoom_level, 
                 orient="horizontal", length=200).pack(side="left", padx=2)
        ttk.Label(zoom_frame, textvariable=self.zoom_level).pack(side="left", padx=2)
        
        ttk.Button(zoom_frame, text="Restablecer Zoom", 
                  command=self._reset_zoom).pack(side="left", padx=5)
        
        # Row 3: Pan controls
        pan_frame = ttk.Frame(self.control_frame)
        pan_frame.pack(fill="x", pady=2)
        
        ttk.Label(pan_frame, text="Pan:").pack(side="left", padx=2)
        
        # Pan buttons
        ttk.Button(pan_frame, text="^", command=lambda: self._pan(0, 0.1), 
                  width=3).pack(side="left", padx=1)
        pan_lr_frame = ttk.Frame(pan_frame)
        pan_lr_frame.pack(side="left")
        ttk.Button(pan_lr_frame, text="<", command=lambda: self._pan(-0.1, 0), 
                  width=3).pack(side="left", padx=1)
        ttk.Button(pan_lr_frame, text=">", command=lambda: self._pan(0.1, 0), 
                  width=3).pack(side="left", padx=1)
        ttk.Button(pan_frame, text="v", command=lambda: self._pan(0, -0.1), 
                  width=3).pack(side="left", padx=1)
        
        ttk.Button(pan_frame, text="Centrar", 
                  command=self._center_plot).pack(side="left", padx=5)
        
        # Row 4: Display options
        display_frame = ttk.Frame(self.control_frame)
        display_frame.pack(fill="x", pady=2)
        
        ttk.Checkbutton(display_frame, text="Grid", 
                       variable=self.grid_enabled, 
                       command=self._toggle_grid).pack(side="left", padx=2)
        ttk.Checkbutton(display_frame, text="Leyenda", 
                       variable=self.legend_enabled, 
                       command=self._toggle_legend).pack(side="left", padx=2)
        ttk.Checkbutton(display_frame, text="Animación", 
                       variable=self.animation_enabled, 
                       command=self._toggle_animation).pack(side="left", padx=2)
        
        # Row 5: Quality controls
        quality_frame = ttk.Frame(self.control_frame)
        quality_frame.pack(fill="x", pady=2)
        
        ttk.Label(quality_frame, text="Calidad:").pack(side="left", padx=2)
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_level, 
                                     values=["baja", "media", "alta", "auto"], 
                                     state="readonly", width=10)
        quality_combo.pack(side="left", padx=2)
        quality_combo.bind("<<ComboboxSelected>>", self._quality_changed)
        
        # Row 6: Export controls
        export_frame = ttk.Frame(self.control_frame)
        export_frame.pack(fill="x", pady=2)
        
        ttk.Label(export_frame, text="Exportar:").pack(side="left", padx=2)
        ttk.Button(export_frame, text="PNG", 
                  command=lambda: self._export_plot("png")).pack(side="left", padx=1)
        ttk.Button(export_frame, text="SVG", 
                  command=lambda: self._export_plot("svg")).pack(side="left", padx=1)
        ttk.Button(export_frame, text="PDF", 
                  command=lambda: self._export_plot("pdf")).pack(side="left", padx=1)
        
        # Row 7: History controls
        history_frame = ttk.Frame(self.control_frame)
        history_frame.pack(fill="x", pady=2)
        
        ttk.Button(history_frame, text="Deshacer", 
                  command=self._undo_plot).pack(side="left", padx=2)
        ttk.Button(history_frame, text="Rehacer", 
                  command=self._redo_plot).pack(side="left", padx=2)
        ttk.Button(history_frame, text="Guardar en Historial", 
                  command=self._save_to_history).pack(side="left", padx=2)
    
    def update_plot(self, figure):
        """Update the current plot with enhanced controls"""
        try:
            # Clear previous plot
            self._clear_current_plot()
            
            # Store current figure
            self.current_figure = figure
            
            # Create canvas with enhanced toolbar
            self.current_canvas = FigureCanvasTkAgg(figure, self.parent)
            self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add enhanced toolbar
            self.toolbar = EnhancedNavigationToolbar(self.current_canvas, self.parent)
            self.toolbar.update()
            
            # Apply current settings
            self._apply_current_settings()
            
            logger.info("Enhanced plot controls updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating enhanced plot: {str(e)}")
            messagebox.showerror("Error", f"No se pudo actualizar el gráfico: {str(e)}")
    
    def _apply_current_settings(self):
        """Apply current control settings to the plot"""
        if not self.current_figure:
            return
        
        try:
            # Apply grid setting
            for ax in self.current_figure.get_axes():
                if self.grid_enabled.get():
                    ax.grid(True, alpha=0.3)
                else:
                    ax.grid(False)
                
                # Apply legend setting
                if self.legend_enabled.get() and ax.get_legend():
                    ax.legend(loc='best')
                elif not self.legend_enabled.get() and ax.get_legend():
                    ax.get_legend().set_visible(False)
            
            # Apply zoom
            if self.zoom_level.get() != 1.0:
                self._apply_zoom()
            
            # Apply pan
            if self.pan_offset_x.get() != 0.0 or self.pan_offset_y.get() != 0.0:
                self._apply_pan()
            
            self.current_canvas.draw()
            
        except Exception as e:
            logger.error(f"Error applying plot settings: {str(e)}")
    
    def _refresh_plot(self):
        """Refresh the current plot"""
        try:
            if self.plotter_callback:
                # Get current quality setting
                quality_map = {
                    "baja": "low",
                    "media": "medium", 
                    "alta": "high",
                    "auto": "auto"
                }
                quality = quality_map.get(self.quality_level.get(), "auto")
                
                # Call plotter callback with current settings
                self.plotter_callback(quality=quality)
                
        except Exception as e:
            logger.error(f"Error refreshing plot: {str(e)}")
            messagebox.showerror("Error", f"No se pudo actualizar el gráfico: {str(e)}")
    
    def _clear_plot(self):
        """Clear the current plot"""
        try:
            self._clear_current_plot()
            
            # Create empty plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "Gráfico limpio - Listo para nueva función", 
                   transform=ax.transAxes, ha='center', va='center', 
                   fontsize=14, color='gray')
            ax.set_title("Gráfico Vacío")
            
            self.update_plot(fig)
            
        except Exception as e:
            logger.error(f"Error clearing plot: {str(e)}")
    
    def _clear_current_plot(self):
        """Clear current canvas and toolbar"""
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        
        if self.toolbar:
            self.toolbar.destroy()
            self.toolbar = None
        
        self.current_figure = None
    
    def _fullscreen_plot(self):
        """Open plot in fullscreen window"""
        if not self.current_figure:
            messagebox.showwarning("Advertencia", "No hay gráfico actual para mostrar")
            return
        
        try:
            # Create fullscreen window
            fullscreen_window = tk.Toplevel(self.parent)
            fullscreen_window.title("Gráfico en Pantalla Completa")
            fullscreen_window.state('zoomed')  # Maximize window
            
            # Create new canvas for fullscreen
            canvas = FigureCanvasTkAgg(self.current_figure, fullscreen_window)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add toolbar
            toolbar = NavigationToolbar2Tk(canvas, fullscreen_window)
            toolbar.update()
            
            # Close button
            close_frame = ttk.Frame(fullscreen_window)
            close_frame.pack(side="bottom", pady=5)
            ttk.Button(close_frame, text="Cerrar", 
                      command=fullscreen_window.destroy).pack()
            
        except Exception as e:
            logger.error(f"Error creating fullscreen plot: {str(e)}")
            messagebox.showerror("Error", f"No se pudo crear vista de pantalla completa: {str(e)}")
    
    def _reset_zoom(self):
        """Reset zoom to default"""
        self.zoom_level.set(1.0)
        self.pan_offset_x.set(0.0)
        self.pan_offset_y.set(0.0)
        self._apply_current_settings()
    
    def _pan(self, dx, dy):
        """Pan the plot"""
        current_x = self.pan_offset_x.get()
        current_y = self.pan_offset_y.get()
        
        self.pan_offset_x.set(current_x + dx)
        self.pan_offset_y.set(current_y + dy)
        
        self._apply_current_settings()
    
    def _center_plot(self):
        """Center the plot"""
        self.pan_offset_x.set(0.0)
        self.pan_offset_y.set(0.0)
        self._apply_current_settings()
    
    def _apply_zoom(self):
        """Apply zoom to the plot"""
        if not self.current_figure:
            return
        
        zoom = self.zoom_level.get()
        
        for ax in self.current_figure.get_axes():
            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            # Calculate new limits
            x_center = (xlim[0] + xlim[1]) / 2
            y_center = (ylim[0] + ylim[1]) / 2
            
            x_range = (xlim[1] - xlim[0]) / (2 * zoom)
            y_range = (ylim[1] - ylim[0]) / (2 * zoom)
            
            ax.set_xlim(x_center - x_range, x_center + x_range)
            ax.set_ylim(y_center - y_range, y_center + y_range)
    
    def _apply_pan(self):
        """Apply pan to the plot"""
        if not self.current_figure:
            return
        
        pan_x = self.pan_offset_x.get()
        pan_y = self.pan_offset_y.get()
        
        for ax in self.current_figure.get_axes():
            # Get current limits
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            
            # Apply pan
            x_range = xlim[1] - xlim[0]
            y_range = ylim[1] - ylim[0]
            
            ax.set_xlim(xlim[0] + pan_x * x_range, xlim[1] + pan_x * x_range)
            ax.set_ylim(ylim[0] + pan_y * y_range, ylim[1] + pan_y * y_range)
    
    def _toggle_grid(self):
        """Toggle grid display"""
        self._apply_current_settings()
    
    def _toggle_legend(self):
        """Toggle legend display"""
        self._apply_current_settings()
    
    def _toggle_animation(self):
        """Toggle animation mode"""
        if self.animation_enabled.get():
            self._start_animation()
        else:
            self._stop_animation()
    
    def _start_animation(self):
        """Start plot animation"""
        if self.animation_running:
            return
        
        try:
            self.animation_running = True
            self.animation_thread = threading.Thread(target=self._animate_plot)
            self.animation_thread.daemon = True
            self.animation_thread.start()
            
            logger.info("Plot animation started")
            
        except Exception as e:
            logger.error(f"Error starting animation: {str(e)}")
            self.animation_running = False
    
    def _stop_animation(self):
        """Stop plot animation"""
        self.animation_running = False
        
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
        
        logger.info("Plot animation stopped")
    
    def _animate_plot(self):
        """Animate the plot (simple rotation/zoom effect)"""
        if not self.current_figure:
            self.animation_running = False
            return
        
        try:
            frame = 0
            while self.animation_running:
                # Simple animation: oscillate zoom
                zoom = 1.0 + 0.1 * np.sin(frame * 0.1)
                self.zoom_level.set(zoom)
                
                # Update plot
                self.parent.after(0, self._apply_current_settings)
                
                frame += 1
                time.sleep(0.05)  # 20 FPS
                
        except Exception as e:
            logger.error(f"Error in animation: {str(e)}")
        finally:
            self.animation_running = False
    
    def _quality_changed(self, event=None):
        """Handle quality change"""
        self._refresh_plot()
    
    def _export_plot(self, format_type):
        """Export plot to file"""
        if not self.current_figure:
            messagebox.showwarning("Advertencia", "No hay gráfico para exportar")
            return
        
        try:
            from tkinter import filedialog
            
            # Get file path
            file_types = {
                "png": [("PNG files", "*.png")],
                "svg": [("SVG files", "*.svg")],
                "pdf": [("PDF files", "*.pdf")]
            }
            
            file_path = filedialog.asksaveasfilename(
                title=f"Exportar gráfico como {format_type.upper()}",
                filetypes=file_types.get(format_type, [("All files", "*.*")]),
                defaultextension=f".{format_type}"
            )
            
            if file_path:
                # Save with high resolution
                dpi = 300 if format_type == "png" else None
                self.current_figure.savefig(file_path, dpi=dpi, bbox_inches='tight')
                
                messagebox.showinfo("Éxito", f"Gráfico exportado a:\n{file_path}")
                logger.info(f"Plot exported to {file_path}")
                
        except Exception as e:
            logger.error(f"Error exporting plot: {str(e)}")
            messagebox.showerror("Error", f"No se pudo exportar el gráfico: {str(e)}")
    
    def _save_to_history(self):
        """Save current plot to history"""
        if not self.current_figure:
            messagebox.showwarning("Advertencia", "No hay gráfico para guardar")
            return
        
        try:
            # Add to history
            self.plot_history.append(self.current_figure)
            self.history_index = len(self.plot_history) - 1
            
            # Limit history size
            if len(self.plot_history) > 10:
                self.plot_history.pop(0)
                self.history_index -= 1
            
            messagebox.showinfo("Éxito", "Gráfico guardado en el historial")
            logger.info("Plot saved to history")
            
        except Exception as e:
            logger.error(f"Error saving to history: {str(e)}")
            messagebox.showerror("Error", f"No se pudo guardar en el historial: {str(e)}")
    
    def _undo_plot(self):
        """Undo to previous plot"""
        if self.history_index > 0:
            self.history_index -= 1
            previous_figure = self.plot_history[self.history_index]
            self.update_plot(previous_figure)
            logger.info("Plot undone")
        else:
            messagebox.showinfo("Información", "No hay gráficos anteriores para deshacer")
    
    def _redo_plot(self):
        """Redo to next plot"""
        if self.history_index < len(self.plot_history) - 1:
            self.history_index += 1
            next_figure = self.plot_history[self.history_index]
            self.update_plot(next_figure)
            logger.info("Plot redone")
        else:
            messagebox.showinfo("Información", "No hay gráficos siguientes para rehacer")
    
    def get_current_settings(self) -> Dict:
        """Get current control settings"""
        return {
            'zoom': self.zoom_level.get(),
            'pan_x': self.pan_offset_x.get(),
            'pan_y': self.pan_offset_y.get(),
            'grid_enabled': self.grid_enabled.get(),
            'legend_enabled': self.legend_enabled.get(),
            'quality': self.quality_level.get(),
            'animation_enabled': self.animation_enabled.get()
        }
    
    def apply_settings(self, settings: Dict):
        """Apply control settings"""
        if 'zoom' in settings:
            self.zoom_level.set(settings['zoom'])
        if 'pan_x' in settings:
            self.pan_offset_x.set(settings['pan_x'])
        if 'pan_y' in settings:
            self.pan_offset_y.set(settings['pan_y'])
        if 'grid_enabled' in settings:
            self.grid_enabled.set(settings['grid_enabled'])
        if 'legend_enabled' in settings:
            self.legend_enabled.set(settings['legend_enabled'])
        if 'quality' in settings:
            self.quality_level.set(settings['quality'])
        if 'animation_enabled' in settings:
            self.animation_enabled.set(settings['animation_enabled'])
        
        self._apply_current_settings()


class EnhancedNavigationToolbar(NavigationToolbar2Tk):
    """Enhanced navigation toolbar with additional features"""
    
    def __init__(self, canvas, parent):
        """Initialize enhanced toolbar"""
        super().__init__(canvas, parent)
        
        # Add custom buttons
        self._add_enhanced_buttons()
    
    def _add_enhanced_buttons(self):
        """Add enhanced buttons to toolbar"""
        # Add separator
        ttk.Separator(self, orient="vertical").pack(side="left", padx=5, fill="y")
        
        # Add custom buttons
        ttk.Button(self, text="Centrar", command=self._center_view).pack(side="left", padx=2)
        ttk.Button(self, text="Ajustar", command=self._fit_view).pack(side="left", padx=2)
        ttk.Button(self, text="Exportar", command=self._quick_export).pack(side="left", padx=2)
    
    def _center_view(self):
        """Center the view"""
        try:
            if self.canvas.figure:
                for ax in self.canvas.figure.get_axes():
                    ax.relim()
                    ax.autoscale()
                self.canvas.draw()
        except Exception as e:
            logger.error(f"Error centering view: {str(e)}")
    
    def _fit_view(self):
        """Fit the view to data"""
        try:
            if self.canvas.figure:
                for ax in self.canvas.figure.get_axes():
                    ax.relim()
                    ax.autoscale_view()
                self.canvas.draw()
        except Exception as e:
            logger.error(f"Error fitting view: {str(e)}")
    
    def _quick_export(self):
        """Quick export to PNG"""
        try:
            from tkinter import filedialog
            import datetime
            
            # Generate default filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"plot_{timestamp}.png"
            
            file_path = filedialog.asksaveasfilename(
                title="Exportar gráfico",
                initialfile=default_filename,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                defaultextension=".png"
            )
            
            if file_path and self.canvas.figure:
                self.canvas.figure.savefig(file_path, dpi=300, bbox_inches='tight')
                logger.info(f"Quick export saved to {file_path}")
                
        except Exception as e:
            logger.error(f"Error in quick export: {str(e)}")


class FloatingControlPanel:
    """Floating control panel for plot manipulation"""
    
    def __init__(self, parent, plot_controls: EnhancedPlotControls):
        """Initialize floating panel"""
        self.plot_controls = plot_controls
        self.parent = parent
        self.floating_window = None
        
        self._create_floating_button()
    
    def _create_floating_button(self):
        """Create floating control button"""
        self.floating_button = tk.Button(
            self.parent, 
            text="Controles", 
            command=self._toggle_floating_panel,
            bg="#2196F3", 
            fg="white",
            relief="raised",
            bd=2
        )
        
        # Position button in top-right corner
        self.floating_button.place(relx=0.98, rely=0.02, anchor="ne")
    
    def _toggle_floating_panel(self):
        """Toggle floating control panel"""
        if self.floating_window and self.floating_window.winfo_exists():
            self.floating_window.destroy()
            self.floating_window = None
        else:
            self._show_floating_panel()
    
    def _show_floating_panel(self):
        """Show floating control panel"""
        self.floating_window = tk.Toplevel(self.parent)
        self.floating_window.title("Controles Flotantes")
        self.floating_window.geometry("300x400")
        self.floating_window.transient(self.parent)
        
        # Make it stay on top
        self.floating_window.attributes('-topmost', True)
        
        # Add plot controls to floating window
        controls_frame = ttk.Frame(self.floating_window)
        controls_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quick controls
        ttk.Label(controls_frame, text="Controles Rápidos", 
                 font=("Arial", 12, "bold")).pack(pady=5)
        
        ttk.Button(controls_frame, text="Actualizar", 
                  command=self._quick_refresh).pack(fill="x", pady=2)
        ttk.Button(controls_frame, text="Centrar", 
                  command=self._quick_center).pack(fill="x", pady=2)
        ttk.Button(controls_frame, text="Restablecer", 
                  command=self._quick_reset).pack(fill="x", pady=2)
        
        ttk.Separator(controls_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Zoom controls
        ttk.Label(controls_frame, text="Zoom", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        zoom_frame = ttk.Frame(controls_frame)
        zoom_frame.pack(fill="x", pady=2)
        
        ttk.Button(zoom_frame, text="-", width=3,
                  command=lambda: self._adjust_zoom(-0.1)).pack(side="left", padx=2)
        ttk.Label(zoom_frame, textvariable=self.plot_controls.zoom_level).pack(side="left", padx=5)
        ttk.Button(zoom_frame, text="+", width=3,
                  command=lambda: self._adjust_zoom(0.1)).pack(side="left", padx=2)
        
        ttk.Separator(controls_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Display options
        ttk.Label(controls_frame, text="Opciones de Visualización", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        ttk.Checkbutton(controls_frame, text="Grid", 
                       variable=self.plot_controls.grid_enabled).pack(anchor="w", pady=2)
        ttk.Checkbutton(controls_frame, text="Leyenda", 
                       variable=self.plot_controls.legend_enabled).pack(anchor="w", pady=2)
        
        ttk.Separator(controls_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Quick export
        ttk.Button(controls_frame, text="Exportar PNG", 
                  command=lambda: self.plot_controls._export_plot("png")).pack(fill="x", pady=2)
        
        # Close button
        ttk.Button(controls_frame, text="Cerrar", 
                  command=self.floating_window.destroy).pack(fill="x", pady=10)
    
    def _quick_refresh(self):
        """Quick refresh from floating panel"""
        self.plot_controls._refresh_plot()
    
    def _quick_center(self):
        """Quick center from floating panel"""
        self.plot_controls._center_plot()
    
    def _quick_reset(self):
        """Quick reset from floating panel"""
        self.plot_controls._reset_zoom()
    
    def _adjust_zoom(self, delta):
        """Adjust zoom from floating panel"""
        current_zoom = self.plot_controls.zoom_level.get()
        new_zoom = max(0.1, min(5.0, current_zoom + delta))
        self.plot_controls.zoom_level.set(new_zoom)
        self.plot_controls._apply_current_settings()

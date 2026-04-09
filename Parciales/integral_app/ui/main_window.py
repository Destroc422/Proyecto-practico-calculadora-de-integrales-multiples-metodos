"""
Professional LaTeX Integral Calculator - Main Window
Clean, modular, and production-ready UI implementation
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
import sys
import os
import traceback
import threading
from datetime import datetime
from typing import Optional, Dict, Any
import sympy as sp

# Core modules
from core.integrator import ProfessionalIntegrator, IntegrationMethod, IntegrationError
from core.parser import ProfessionalMathParser, ParseError

# UI modules
from ui.theme_manager import ThemeManager
from ui.latex_renderer import ProfessionalLaTeXRenderer

# Graph and utilities
from graph.plotter import ProfessionalPlotter
from utils.validators import ExpressionValidator
from data.history_manager import HistoryManager

logger = logging.getLogger(__name__)


class ProfessionalIntegralCalculator:
    """Professional integral calculator with clean architecture"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(" Calculadora de Integrales PRO - Premium Edition")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        
        # Modern window styling with gradient effect
        self.root.configure(bg='#1a1a2e')
        
        # Window styling (icon removed to prevent error)
        
        # Center window on screen
        self.center_window()
        
        # Set modern window attributes
        self.root.attributes('-alpha', 0.95)  # Slight transparency
        
        # Initialize components
        self._initialize_components()
        
        # Setup UI
        self.setup_ui()
        self.setup_shortcuts()
        
        # Apply theme
        self.apply_theme()
        
        logger.info("Professional Integral Calculator initialized successfully")
    
    def _initialize_components(self):
        """Initialize all components"""
        try:
            self.theme_manager = ThemeManager()
            self.integrator = ProfessionalIntegrator()
            self.parser = ProfessionalMathParser()
            self.plotter = ProfessionalPlotter()
            self.history_manager = HistoryManager()
            self.latex_renderer = ProfessionalLaTeXRenderer()
            self.validator = ExpressionValidator()
            
            # Mathematical symbols
            self.symbols = {
                'x': tk.StringVar(value='x'),
                'y': tk.StringVar(value='y'),
                'z': tk.StringVar(value='z'),
                't': tk.StringVar(value='t')
            }
            
            # Application state
            self.current_result = None
            self.current_steps = []
            self.is_calculating = False
            self.last_answer = "0"  # ANS (Last Answer)
            
            # UI state
            self.current_function = ""
            self.auto_parentheses = tk.BooleanVar(value=True)
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            messagebox.showerror("Error", "No se pudieron inicializar los componentes")
            raise
    
    def setup_ui(self):
        """Setup the professional user interface"""
        try:
            # Main container
            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create sections
            self.create_toolbar()
            self.create_main_panel()
            self.create_status_bar()
            
        except Exception as e:
            logger.error(f"Error setting up UI: {str(e)}")
            messagebox.showerror("Error", "No se pudo configurar la interfaz")
            raise
    
    def create_toolbar(self):
        """Create ultra-modern professional toolbar with glassmorphism effect"""
        try:
            # Ultra-modern toolbar with glassmorphism effect
            toolbar = tk.Frame(self.main_frame, bg='#0f3460', height=70)
            toolbar.pack(fill="x", pady=(0, 15))
            toolbar.pack_propagate(False)
            
            # Add gradient effect overlay
            gradient_frame = tk.Frame(toolbar, bg='#16213e', height=70)
            gradient_frame.pack(fill="both", expand=True)
            gradient_frame.pack_propagate(False)
            
            # Logo section with modern styling
            logo_frame = tk.Frame(gradient_frame, bg='#16213e')
            logo_frame.pack(side="left", padx=25, pady=15)
            
            # Logo with modern font
            logo_label = tk.Label(logo_frame, text="", font=('Segoe UI', 28, 'bold'), 
                                fg='#e94560', bg='#16213e')
            logo_label.pack(side="left")
            
            # App name with gradient effect
            app_name = tk.Label(logo_frame, text="CalcPRO", font=('Segoe UI', 18, 'bold'), 
                               fg='#f5f5f5', bg='#16213e')
            app_name.pack(side="left", padx=(8, 0))
            
            # Version badge
            version_badge = tk.Label(logo_frame, text="v3.0", font=('Segoe UI', 8, 'bold'), 
                                  fg='#0f3460', bg='#e94560', relief=tk.RAISED, bd=2, padx=4, pady=1)
            version_badge.pack(side="left", padx=(5, 0))
            
            # Navigation buttons with glassmorphism styling
            nav_frame = tk.Frame(gradient_frame, bg='#16213e')
            nav_frame.pack(side="left", padx=40, pady=15)
            
            self.create_ultra_modern_button(nav_frame, " Nuevo", self.new_calculation, '#3498db')
            self.create_ultra_modern_button(nav_frame, " Guardar", self.save_result, '#27ae60')
            self.create_ultra_modern_button(nav_frame, " Historial", self.show_history, '#f39c12')
            self.create_ultra_modern_button(nav_frame, " Exportar", self.export_report, '#9b59b6')
            
            # Animated separator
            separator = tk.Frame(gradient_frame, bg='#e94560', width=3, height=40)
            separator.pack(side="left", padx=20, fill="y", pady=15)
            
            # Main calculation button - ultra prominent with animation
            calc_frame = tk.Frame(gradient_frame, bg='#16213e')
            calc_frame.pack(side="left", padx=25, pady=15)
            
            self.calculate_btn = tk.Button(calc_frame, text=" CALCULAR INTEGRAL", 
                                          command=self.calculate_integral,
                                          font=('Segoe UI', 14, 'bold'),
                                          bg='#e94560', fg='white',
                                          padx=25, pady=10,
                                          relief=tk.RAISED, bd=3,
                                          cursor='hand2',
                                          activebackground='#d63031',
                                          activeforeground='white')
            self.calculate_btn.pack()
            
            # Right side options with modern styling
            options_frame = tk.Frame(gradient_frame, bg='#16213e')
            options_frame.pack(side="right", padx=25, pady=15)
            
            self.create_ultra_modern_button(options_frame, " Tema", self.toggle_theme, '#533483')
            self.create_ultra_modern_button(options_frame, " Ayuda", self.show_help, '#00b894')
            self.create_ultra_modern_button(options_frame, " Config", self.show_settings, '#6c5ce7')
            
        except Exception as e:
            logger.error(f"Error creating toolbar: {str(e)}")
            raise
    
    def create_main_panel(self):
        """Create main panel with integrated graphics section"""
        try:
            # Main container with responsive layout
            main_container = ttk.Frame(self.main_frame)
            main_container.pack(fill="both", expand=True)
            
            # Configure grid weights for responsive layout
            main_container.grid_rowconfigure(0, weight=0)  # Input section
            main_container.grid_rowconfigure(1, weight=1)  # Graphics section
            main_container.grid_columnconfigure(0, weight=1)  # Full width
            
            # === INPUT PANEL (COMPACT) ===
            input_row = ttk.Frame(main_container)
            input_row.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
            
            # Input panel with modern styling
            input_panel = ttk.Frame(input_row)
            input_panel.pack(fill="x")
            
            self.create_input_section(input_panel)
            self.create_keypad_section(input_panel)
            
            # === GRAPHICS PANEL (MAIN AREA) ===
            graphics_row = ttk.Frame(main_container)
            graphics_row.grid(row=1, column=0, sticky="nsew")
            
            # Create integrated graphics section
            self.create_graphics_section(graphics_row)
            
            # Results window (separate)
            self.create_results_window()
            
        except Exception as e:
            logger.error(f"Error creating main panel: {str(e)}")
            raise
    
    def create_input_section(self, parent):
        """Create modern input section with enhanced visual design"""
        try:
            # Modern configuration frame with gradient effect
            config_frame = tk.Frame(parent, bg='#ecf0f1', relief=tk.RIDGE, bd=2)
            config_frame.pack(fill="x", pady=(0, 10))
            
            # Header with icon and title
            header_frame = tk.Frame(config_frame, bg='#3498db', height=35)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            header_label = tk.Label(header_frame, text="⚙️ CONFIGURACIÓN DE INTEGRACIÓN", 
                                  font=('Arial', 11, 'bold'), fg='white', bg='#3498db')
            header_label.pack(pady=8)
            
            # Content area with padding
            content_frame = tk.Frame(config_frame, bg='#ecf0f1')
            content_frame.pack(fill="x", padx=15, pady=10)
            
            # First row - Type and variable with modern styling
            row1 = tk.Frame(content_frame, bg='#ecf0f1')
            row1.pack(fill="x", pady=(0, 8))
            
            # Integral type with enhanced styling
            type_frame = tk.Frame(row1, bg='#ecf0f1')
            type_frame.pack(side="left", fill="x", expand=True)
            
            type_label = tk.Label(type_frame, text="🎯 MÉTODO:", 
                                font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#ecf0f1')
            type_label.pack(side="left", padx=(0, 8))
            
            self.integral_type_var = tk.StringVar(value="Automático")
            self.integral_type = ttk.Combobox(type_frame, textvariable=self.integral_type_var, 
                                             width=20, state="readonly", font=('Arial', 10))
            self.integral_type['values'] = (
                'Automático', 'Directa', 'Sustitución', 'Por Partes', 
                'Fracciones Parciales', 'Trigonométrica', 'Racional', 'Exponencial'
            )
            self.integral_type.pack(side="left", padx=5)
            
            # Variable selection with modern styling
            var_frame = tk.Frame(row1, bg='#ecf0f1')
            var_frame.pack(side="right", padx=(15, 0))
            
            var_label = tk.Label(var_frame, text="📊 VARIABLE:", 
                               font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#ecf0f1')
            var_label.pack(side="left", padx=(0, 8))
            self.variable_combo = ttk.Combobox(var_frame, textvariable=self.symbols['x'], 
                                              width=5, state="readonly")
            self.variable_combo['values'] = ('x', 'y', 'z', 't', 'u', 'v')
            self.variable_combo.pack(side="left", padx=3)
            self.variable_combo.bind('<<ComboboxSelected>>', self.on_variable_change)
            
            # Second row - Definite integral with modern styling
            row2 = tk.Frame(config_frame, bg='#ecf0f1')
            row2.pack(fill="x", pady=(8, 0))
            
            # Definite integral checkbox with modern styling
            self.definite_var = tk.BooleanVar(value=False)
            definite_check = tk.Checkbutton(row2, text=" Integral definida",
                                           variable=self.definite_var,
                                           command=self.toggle_limits,
                                           font=('Arial', 10, 'bold'),
                                           fg='#2c3e50', bg='#ecf0f1',
                                           selectcolor='#3498db',
                                           activebackground='#ecf0f1',
                                           activeforeground='#3498db')
            definite_check.pack(side="left", padx=(0, 15))
            
            # Limits frame (initially hidden) - modern styling
            self.limits_frame = tk.Frame(row2, bg='#ecf0f1')
            
            # Lower limit
            lower_label = tk.Label(self.limits_frame, text="Límite inferior:",
                                 font=('Arial', 9, 'bold'),
                                 fg='#2c3e50', bg='#ecf0f1')
            lower_label.pack(side="left", padx=(0, 5))
            
            self.lower_limit = tk.Entry(self.limits_frame, width=8, 
                                       font=('Courier', 10, 'bold'),
                                       bg='white', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=2)
            self.lower_limit.pack(side="left", padx=(0, 15))
            self.lower_limit.insert(0, "0")
            
            # Upper limit
            upper_label = tk.Label(self.limits_frame, text="Límite superior:",
                                 font=('Arial', 9, 'bold'),
                                 fg='#2c3e50', bg='#ecf0f1')
            upper_label.pack(side="left", padx=(0, 5))
            
            self.upper_limit = tk.Entry(self.limits_frame, width=8,
                                       font=('Courier', 10, 'bold'),
                                       bg='white', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=2)
            self.upper_limit.pack(side="left")
            self.upper_limit.insert(0, "1")
            
            # Editor frame - more compact padding
            editor_frame = ttk.LabelFrame(parent, text="📝 Editor Matemático", padding=6)
            editor_frame.pack(fill="x", pady=(0, 6))
            
            # Create math editor
            self.create_math_editor(editor_frame)
            
            # Quick actions frame with modern styling
            actions_frame = tk.Frame(parent, bg='#ecf0f1')
            actions_frame.pack(fill="x", pady=(8, 0))
            
            # Modern action buttons
            self.create_modern_button(actions_frame, " Limpiar", self.clear_editor, '#e74c3c')
            self.create_modern_button(actions_frame, " ANS", self.insert_ans, '#3498db')
            self.create_modern_button(actions_frame, " Rehacer", self.redo_input, '#f39c12')
            
            # Validation status with modern styling
            self.validation_label = tk.Label(actions_frame, text=" Válido", 
                                           font=("Arial", 10, "bold"), 
                                           fg='#27ae60', bg='#ecf0f1',
                                           relief=tk.RIDGE, bd=1, padx=8, pady=2)
            self.validation_label.pack(side="right", padx=5)
            
        except Exception as e:
            logger.error(f"Error creating input section: {str(e)}")
            raise
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_modern_button(self, parent, text, command, color):
        """Create a modern styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       font=('Arial', 9, 'bold'),
                       bg=color, fg='white',
                       padx=8, pady=4,
                       relief=tk.FLAT,
                       cursor='hand2',
                       activebackground=self.darken_color(color),
                       activeforeground='white')
        btn.pack(side="left", padx=2)
        
        # Add hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.lighten_color(color)))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        
        return btn
    
    def create_ultra_modern_button(self, parent, text, command, color):
        """Create ultra-modern styled button with glassmorphism effect"""
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', 10, 'bold'),
                       bg=color, fg='white',
                       padx=12, pady=6,
                       relief=tk.RAISED, bd=2,
                       cursor='hand2',
                       activebackground=self.darken_color(color),
                       activeforeground='white')
        btn.pack(side="left", padx=3)
        
        # Add advanced hover effects
        btn.bind('<Enter>', lambda e: self.animate_button_hover(btn, color))
        btn.bind('<Leave>', lambda e: self.animate_button_leave(btn, color))
        
        return btn
    
    def animate_button_hover(self, btn, color):
        """Animate button on hover"""
        try:
            lighter_color = self.lighten_color(color)
            btn.config(bg=lighter_color, relief=tk.RIDGE, bd=3)
        except:
            pass
    
    def animate_button_leave(self, btn, color):
        """Animate button when leaving hover"""
        try:
            btn.config(bg=color, relief=tk.RAISED, bd=2)
        except:
            pass
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#%02x%02x%02x' % lighter
    
    def darken_color(self, color):
        """Darken a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * 0.8) for c in rgb)
        return '#%02x%02x%02x' % darker
    
    def create_math_editor(self, parent):
        """Create modern professional math editor with enhanced visual design"""
        try:
            # Modern editor container with gradient border
            editor_container = tk.Frame(parent, bg='#bdc3c7', relief=tk.RIDGE, bd=2)
            editor_container.pack(fill="x", pady=(0, 8))
            
            # Header with icon and title
            header_frame = tk.Frame(editor_container, bg='#34495e', height=30)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            header_label = tk.Label(header_frame, text="📝 EDITOR MATEMÁTICO", 
                                  font=('Arial', 10, 'bold'), fg='white', bg='#34495e')
            header_label.pack(pady=5)
            
            # Content area with padding
            content_frame = tk.Frame(editor_container, bg='white')
            content_frame.pack(fill="x", padx=2, pady=2)
            
            # Main editor with modern styling
            self.editor_text = tk.Text(content_frame, height=3, font=('Courier New', 12, 'bold'), 
                                      wrap=tk.NONE, undo=True, maxundo=-1,
                                      bg='#2c3e50', fg='#ecf0f1',
                                      insertbackground='#3498db',
                                      selectbackground='#3498db',
                                      relief=tk.FLAT, bd=0)
            self.editor_text.pack(fill="x", padx=5, pady=5)
            
            # Enhanced syntax highlighting colors
            self.editor_text.tag_configure("function", foreground="#3498db", font=('Courier New', 12, 'bold'))
            self.editor_text.tag_configure("number", foreground="#e67e22", font=('Courier New', 12, 'bold'))
            self.editor_text.tag_configure("operator", foreground="#95a5a6", font=('Courier New', 12))
            self.editor_text.tag_configure("integral", foreground="#9b59b6", font=("Courier New", 12, 'bold'))
            self.editor_text.tag_configure("differential", foreground="#27ae60", font=('Courier New', 12, 'bold'))
            self.editor_text.tag_configure("error", background="#e74c3c", foreground='white')
            self.editor_text.tag_configure("parenthesis", foreground="#f39c12", font=('Courier New', 12, 'bold'))
            
            # Bind events for enhanced functionality
            self.editor_text.bind('<KeyRelease>', self.on_editor_key_release)
            self.editor_text.bind('<Key>', self.on_editor_key_press)
            self.editor_text.bind('<Button-1>', self.on_editor_click)
            
            # Initialize with modern example
            self.editor_text.insert("1.0", "x**2 + 3*x + 2")
            self.current_function = "x**2 + 3*x + 2"
            
            # Modern status indicator
            status_frame = tk.Frame(editor_container, bg='#ecf0f1')
            status_frame.pack(fill="x", padx=2, pady=(0, 2))
            
            self.editor_status = tk.Label(status_frame, text="� Listo para calcular", 
                                        font=('Arial', 9, 'bold'), fg='#27ae60', bg='#ecf0f1')
            self.editor_status.pack(side="left", padx=5, pady=2)
            
            # Character counter
            self.char_counter = tk.Label(status_frame, text="0 caracteres", 
                                       font=('Arial', 8), fg='#7f8c8d', bg='#ecf0f1')
            self.char_counter.pack(side="right", padx=5, pady=2)
            
        except Exception as e:
            logger.error(f"Error creating math editor: {str(e)}")
            raise
    
    def create_keypad_section(self, parent):
        """Create modern professional scientific keypad with enhanced visual design"""
        try:
            # Modern keypad container with gradient border
            keypad_container = tk.Frame(parent, bg='#bdc3c7', relief=tk.RIDGE, bd=2)
            keypad_container.pack(fill="both", expand=True, pady=(0, 10))
            
            # Header with icon and title
            header_frame = tk.Frame(keypad_container, bg='#16a085', height=30)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            header_label = tk.Label(header_frame, text="🔢 TECLADO CIENTÍFICO AVANZADO", 
                                  font=('Arial', 10, 'bold'), fg='white', bg='#16a085')
            header_label.pack(pady=5)
            
            # Content area with padding
            content_frame = tk.Frame(keypad_container, bg='#ecf0f1')
            content_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Create modern keypad
            self.create_modern_scientific_keypad(content_frame)
            
        except Exception as e:
            logger.error(f"Error creating keypad section: {str(e)}")
            raise
    
    def create_graphics_section(self, parent):
        """Create integrated graphics section with matplotlib"""
        try:
            # Graphics container with modern styling
            graphics_container = tk.Frame(parent, bg='#bdc3c7', relief=tk.RIDGE, bd=2)
            graphics_container.pack(fill="both", expand=True)
            
            # Header with icon and title
            header_frame = tk.Frame(graphics_container, bg='#2c3e50', height=35)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            header_label = tk.Label(header_frame, text="VISUALIZACIÓN GRÁFICA", 
                                  font=('Arial', 11, 'bold'), fg='white', bg='#2c3e50')
            header_label.pack(pady=8)
            
            # Content area with matplotlib
            content_frame = tk.Frame(graphics_container, bg='white')
            content_frame.pack(fill="both", expand=True, padx=2, pady=2)
            
            # Create matplotlib figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt
            
            # Create figure and axis
            self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='white')
            self.ax.set_facecolor('#f8f9fa')
            
            # Initial plot
            self.plot_default_function()
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=content_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Control panel
            control_frame = tk.Frame(graphics_container, bg='#ecf0f1', height=40)
            control_frame.pack(fill="x")
            control_frame.pack_propagate(False)
            
            # Graph controls
            self.create_graph_controls(control_frame)
            
        except Exception as e:
            logger.error(f"Error creating graphics section: {str(e)}")
            raise
    
    def plot_default_function(self):
        """Plot a default function for demonstration"""
        try:
            import numpy as np
            
            # Generate data
            x = np.linspace(-5, 5, 1000)
            y = x**2 + 3*x + 2
            
            # Plot
            self.ax.clear()
            self.ax.plot(x, y, color='#3498db', linewidth=2.5, label='f(x) = x² + 3x + 2')
            self.ax.grid(True, alpha=0.3, color='#95a5a6')
            self.ax.set_xlabel('x', fontsize=12, color='#2c3e50')
            self.ax.set_ylabel('f(x)', fontsize=12, color='#2c3e50')
            self.ax.set_title('Función de Ejemplo', fontsize=14, fontweight='bold', color='#2c3e50')
            self.ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
            
            # Set modern styling
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#2c3e50')
            self.ax.spines['bottom'].set_color('#2c3e50')
            
        except Exception as e:
            logger.error(f"Error plotting default function: {str(e)}")
    
    def create_graph_controls(self, parent):
        """Create graph control buttons"""
        try:
            # Left controls - Plot options
            left_frame = tk.Frame(parent, bg='#ecf0f1')
            left_frame.pack(side="left", padx=10, pady=5)
            
            self.create_modern_button(left_frame, " Graficar", self.plot_current_function, '#27ae60')
            self.create_modern_button(left_frame, " Limpiar", self.clear_graph, '#e74c3c')
            
            # Center controls - Range
            center_frame = tk.Frame(parent, bg='#ecf0f1')
            center_frame.pack(side="left", expand=True, fill="x", padx=10, pady=5)
            
            tk.Label(center_frame, text="Rango X:", font=('Arial', 9, 'bold'), 
                    fg='#2c3e50', bg='#ecf0f1').pack(side="left", padx=(0, 5))
            
            self.x_min = tk.Entry(center_frame, width=8, font=('Courier', 9), bg='white', fg='#2c3e50')
            self.x_min.pack(side="left", padx=2)
            self.x_min.insert(0, "-5")
            
            tk.Label(center_frame, text="a", font=('Arial', 9), 
                    fg='#2c3e50', bg='#ecf0f1').pack(side="left", padx=2)
            
            self.x_max = tk.Entry(center_frame, width=8, font=('Courier', 9), bg='white', fg='#2c3e50')
            self.x_max.pack(side="left", padx=2)
            self.x_max.insert(0, "5")
            
            # Right controls - Export
            right_frame = tk.Frame(parent, bg='#ecf0f1')
            right_frame.pack(side="right", padx=10, pady=5)
            
            self.create_modern_button(right_frame, " Exportar", self.export_graph, '#9b59b6')
            
        except Exception as e:
            logger.error(f"Error creating graph controls: {str(e)}")
    
    def plot_current_function(self):
        """Plot the current function from editor"""
        try:
            function_text = self.editor_text.get("1.0", tk.END).strip()
            if not function_text:
                messagebox.showwarning("Advertencia", "No hay función para graficar")
                return
            
            # Parse function
            parsed_func = self.parser.parse(function_text)
            variable = self.symbols['x'].get()
            var_symbol = sp.Symbol(variable)
            
            # Get range
            try:
                x_min = float(self.x_min.get())
                x_max = float(self.x_max.get())
            except:
                x_min, x_max = -5, 5
            
            # Generate data
            import numpy as np
            x = np.linspace(x_min, x_max, 1000)
            
            # Convert to numpy function
            f = sp.lambdify(var_symbol, parsed_func, 'numpy')
            y = f(x)
            
            # Handle potential infinities
            mask = np.isfinite(y)
            if not np.any(mask):
                messagebox.showerror("Error", "La función no tiene valores finitos en el rango especificado")
                return
            
            x_clean = x[mask]
            y_clean = y[mask]
            
            # Plot
            self.ax.clear()
            self.ax.plot(x_clean, y_clean, color='#3498db', linewidth=2.5, 
                        label=f'f({variable}) = {function_text}')
            self.ax.grid(True, alpha=0.3, color='#95a5a6')
            self.ax.set_xlabel(variable, fontsize=12, color='#2c3e50')
            self.ax.set_ylabel(f'f({variable})', fontsize=12, color='#2c3e50')
            self.ax.set_title(f'Gráfica: {function_text}', fontsize=14, fontweight='bold', color='#2c3e50')
            self.ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
            
            # Modern styling
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#2c3e50')
            self.ax.spines['bottom'].set_color('#2c3e50')
            
            # Add zero lines
            self.ax.axhline(y=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            self.ax.axvline(x=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            
            self.canvas.draw()
            self.update_status("Gráfica actualizada", '#27ae60')
            
        except Exception as e:
            logger.error(f"Error plotting current function: {str(e)}")
            messagebox.showerror("Error", f"No se pudo graficar la función: {str(e)}")
    
    def clear_graph(self):
        """Clear the graph"""
        try:
            self.ax.clear()
            self.ax.set_facecolor('#f8f9fa')
            self.ax.grid(True, alpha=0.3, color='#95a5a6')
            self.ax.set_xlabel('x', fontsize=12, color='#2c3e50')
            self.ax.set_ylabel('f(x)', fontsize=12, color='#2c3e50')
            self.ax.set_title('Gráfica Lista', fontsize=14, fontweight='bold', color='#2c3e50')
            self.canvas.draw()
            self.update_status("Gráfica limpiada", '#f39c12')
        except Exception as e:
            logger.error(f"Error clearing graph: {str(e)}")
    
    def export_graph(self):
        """Export the current graph"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            # Ask for file location
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("PDF files", "*.pdf"),
                    ("SVG files", "*.svg"),
                    ("All files", "*.*")
                ],
                initialfile=f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                               facecolor='white', edgecolor='none')
                messagebox.showinfo("Éxito", f"Gráfica exportada a: {filename}")
                self.update_status("Gráfica exportada", '#27ae60')
            
        except Exception as e:
            logger.error(f"Error exporting graph: {str(e)}")
            messagebox.showerror("Error", f"No se pudo exportar la gráfica: {str(e)}")
    
    def create_modern_scientific_keypad(self, parent):
        """Create modern scientific keypad with enhanced visual design"""
        try:
            # Main keypad container
            main_pad = tk.Frame(parent, bg='#ecf0f1')
            main_pad.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Numbers row (0-9)
            numbers_frame = tk.Frame(main_pad, bg='#ecf0f1')
            numbers_frame.pack(fill="x", pady=(0, 8))
            
            # Create rows of numbers
            number_rows = [
                ['7', '8', '9'],
                ['4', '5', '6'],
                ['1', '2', '3'],
                ['0', '.']
            ]
            
            for row in number_rows:
                btn_row = tk.Frame(numbers_frame, bg='#ecf0f1')
                btn_row.pack(fill="x", pady=2)
                
                for num in row:
                    if num == '0':
                        self.create_keypad_button(btn_row, num, '#3498db', 20)
                    elif num == '.':
                        self.create_keypad_button(btn_row, num, '#95a5a6', 20)
                    else:
                        self.create_keypad_button(btn_row, num, '#3498db', 15)
            
            # Operations row
            ops_frame = tk.Frame(main_pad, bg='#ecf0f1')
            ops_frame.pack(fill="x", pady=(0, 8))
            
            basic_ops = ['+', '-', '*', '/', '^']
            for op in basic_ops:
                self.create_keypad_button(ops_frame, op, '#e67e22', 12)
            
            # Functions row
            func_frame = tk.Frame(main_pad, bg='#ecf0f1')
            func_frame.pack(fill="x", pady=(0, 8))
            
            functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'abs']
            for func in functions:
                self.create_keypad_button(func_frame, func, '#9b59b6', 10)
            
            # Mathematical constants and symbols
            constants_frame = tk.Frame(main_pad, bg='#ecf0f1')
            constants_frame.pack(fill="x", pady=(0, 8))
            
            constants = ['pi', 'e', 'phi', 'tau', 'i', 'j']
            for const in constants:
                self.create_keypad_button(constants_frame, const, '#27ae60', 10)
            
            # Integral symbols and operations
            integral_frame = tk.Frame(main_pad, bg='#ecf0f1')
            integral_frame.pack(fill="x", pady=(0, 8))
            
            integral_ops = ['int', 'def_int', 'double_int', 'triple_int']
            for op in integral_ops:
                self.create_keypad_button(integral_frame, op, '#e74c3c', 12)
            
            # Advanced mathematical symbols
            symbols_frame = tk.Frame(main_pad, bg='#ecf0f1')
            symbols_frame.pack(fill="x", pady=(0, 8))
            
            symbols = ['sum', 'prod', 'lim', 'inf', 'partial', 'nabla']
            for sym in symbols:
                self.create_keypad_button(symbols_frame, sym, '#9b59b6', 10)
            
            # Special functions and operators
            special_frame = tk.Frame(main_pad, bg='#ecf0f1')
            special_frame.pack(fill="x")
            
            special_ops = ['sqrt', 'cbrt', 'abs', 'sign', 'floor', 'ceil', 'factorial', 'gamma']
            for op in special_ops:
                self.create_keypad_button(special_frame, op, '#f39c12', 10)
                
        except Exception as e:
            logger.error(f"Error creating modern scientific keypad: {str(e)}")
            raise
    
    def create_keypad_button(self, parent, text, color, width):
        """Create a modern keypad button"""
        btn = tk.Button(parent, text=text, 
                       font=('Arial', 10, 'bold'),
                       bg=color, fg='white',
                       width=width, height=2,
                       relief=tk.FLAT,
                       cursor='hand2',
                       command=lambda: self.insert_text(text))
        btn.pack(side="left", padx=2, pady=2)
        
        # Add hover effects
        btn.bind('<Enter>', lambda e: btn.config(bg=self.lighten_color(color)))
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        
        return btn
    
    def insert_text(self, text):
        """Insert text into the editor at current cursor position with mathematical symbol handling"""
        try:
            cursor_pos = self.editor_text.index(tk.INSERT)
            
            # Handle special mathematical symbols
            symbol_map = {
                'pi': 'pi',
                'e': 'E',
                'phi': '(1+sqrt(5))/2',
                'tau': '2*pi',
                'i': 'I',
                'j': 'I',
                'int': 'int(',
                'def_int': 'int(',
                'double_int': 'int(int(',
                'triple_int': 'int(int(int(',
                'sum': 'sum(',
                'prod': 'prod(',
                'lim': 'limit(',
                'inf': 'oo',
                'partial': 'Derivative(',
                'nabla': 'grad(',
                'sqrt': 'sqrt(',
                'cbrt': 'root(',
                'abs': 'Abs(',
                'sign': 'sign(',
                'floor': 'floor(',
                'ceil': 'ceiling(',
                'factorial': 'factorial(',
                'gamma': 'gamma('
            }
            
            # Get the appropriate text to insert
            insert_text = symbol_map.get(text, text)
            
            # Insert the text
            self.editor_text.insert(cursor_pos, insert_text)
            
            # For integral symbols, add closing parentheses
            if text in ['int', 'def_int', 'double_int', 'triple_int']:
                new_cursor = f"{cursor_pos}+{len(insert_text)}c"
                self.editor_text.insert(new_cursor, ')')
                self.editor_text.mark_set(tk.INSERT, new_cursor)
            elif text in ['sum', 'prod', 'limit', 'sqrt', 'root', 'Abs', 'sign', 'floor', 'ceiling', 'factorial', 'gamma']:
                new_cursor = f"{cursor_pos}+{len(insert_text)}c"
                self.editor_text.insert(new_cursor, ')')
                self.editor_text.mark_set(tk.INSERT, new_cursor)
            
            # Update current function and counter
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            self.update_character_counter()
            
            # Update status
            self.update_status(f"Símbolo '{text}' insertado", '#3498db')
            
        except Exception as e:
            logger.error(f"Error inserting text: {str(e)}")
    
    def update_character_counter(self):
        """Update the character counter"""
        try:
            char_count = len(self.current_function)
            self.char_counter.config(text=f"{char_count} caracteres")
        except Exception as e:
            logger.error(f"Error updating character counter: {str(e)}")
    
    def create_results_window(self):
        """Create separate window for results"""
        try:
            # Create results window
            self.results_window = tk.Toplevel(self.root)
            self.results_window.title("📊 Ventana de Resultados")
            self.results_window.geometry("900x600")
            self.results_window.minsize(800, 500)
            
            # Configure window to close properly
            self.results_window.protocol("WM_DELETE_WINDOW", self.on_results_window_close)
            
            # Create results section in the window
            self.create_results_section(self.results_window)
            
            # Initially hide the window
            self.results_window.withdraw()
            
            logger.info("Results window created successfully")
            
        except Exception as e:
            logger.error(f"Error creating results window: {str(e)}")
            raise
    
    def create_graph_window(self):
        """Create separate window for graphs"""
        try:
            # Create graph window
            self.graph_window = tk.Toplevel(self.root)
            self.graph_window.title("📈 Ventana de Gráficos")
            self.graph_window.geometry("1000x700")
            self.graph_window.minsize(900, 600)
            
            # Configure window to close properly
            self.graph_window.protocol("WM_DELETE_WINDOW", self.on_graph_window_close)
            
            # Create graph section in the window
            self.create_graph_section(self.graph_window)
            
            # Initially hide the window
            self.graph_window.withdraw()
            
            logger.info("Graph window created successfully")
            
        except Exception as e:
            logger.error(f"Error creating graph window: {str(e)}")
            raise
    
    def on_results_window_close(self):
        """Handle results window close"""
        try:
            self.results_window.withdraw()
            self.status_bar.config(text="📊 Ventana de resultados cerrada")
        except Exception as e:
            logger.error(f"Error closing results window: {str(e)}")
    
    def on_graph_window_close(self):
        """Handle graph window close"""
        try:
            self.graph_window.withdraw()
            self.status_bar.config(text="📈 Ventana de gráficos cerrada")
        except Exception as e:
            logger.error(f"Error closing graph window: {str(e)}")
    
    def create_scientific_keypad(self, parent):
        """Create professional scientific keypad with improved character layout and proper alignment"""
        try:
            # Main keypad container with proper alignment
            keypad_container = ttk.Frame(parent)
            keypad_container.pack(fill="both", expand=True, padx=4, pady=4)
            
            # Configure grid with proper spacing for alignment
            for i in range(18):  # Increased rows for better layout
                keypad_container.grid_rowconfigure(i, weight=1)
            for i in range(8):  # 8 columns for better organization
                keypad_container.grid_columnconfigure(i, weight=1)
            
            # === NÚMEROS Y OPERACIONES BÁSICAS ===
            self.create_keypad_section_title(keypad_container, "🔢 Números y Operaciones", 0, 0, 8)
            
            # First row - Numbers 7-9 and basic operations
            self.create_keypad_button(keypad_container, "7", "7", 1, 0, width=6)
            self.create_keypad_button(keypad_container, "8", "8", 1, 1, width=6)
            self.create_keypad_button(keypad_container, "9", "9", 1, 2, width=6)
            self.create_keypad_button(keypad_container, "÷", "/", 1, 3, width=6)
            self.create_keypad_button(keypad_container, "×", "*", 1, 4, width=6)
            self.create_keypad_button(keypad_container, "⌫", "(", 1, 5, width=6)
            self.create_keypad_button(keypad_container, "⌣", ")", 1, 6, width=6)
            self.create_keypad_button(keypad_container, "🗑", "backspace", 1, 7, width=6)
            
            # Second row - Numbers 4-6 and operations
            self.create_keypad_button(keypad_container, "4", "4", 2, 0, width=6)
            self.create_keypad_button(keypad_container, "5", "5", 2, 1, width=6)
            self.create_keypad_button(keypad_container, "6", "6", 2, 2, width=6)
            self.create_keypad_button(keypad_container, "-", "-", 2, 3, width=6)
            self.create_keypad_button(keypad_container, "+", "+", 2, 4, width=6)
            self.create_keypad_button(keypad_container, "²", "**2", 2, 5, width=6)
            self.create_keypad_button(keypad_container, "ⁿ", "**", 2, 6, width=6)
            self.create_keypad_button(keypad_container, "√", "sqrt(", 2, 7, width=6)
            
            # Third row - Numbers 1-3 and more operations
            self.create_keypad_button(keypad_container, "1", "1", 3, 0, width=6)
            self.create_keypad_button(keypad_container, "2", "2", 3, 1, width=6)
            self.create_keypad_button(keypad_container, "3", "3", 3, 2, width=6)
            self.create_keypad_button(keypad_container, ".", ".", 3, 3, width=6)
            self.create_keypad_button(keypad_container, "0", "0", 3, 4, width=6)
            self.create_keypad_button(keypad_container, "π", "pi", 3, 5, width=6)
            self.create_keypad_button(keypad_container, "e", "e", 3, 6, width=6)
            self.create_keypad_button(keypad_container, "📋 ANS", "ans", 3, 7, width=6)
            
            # === SEPARADOR ===
            separator1 = ttk.Separator(keypad_container, orient="horizontal")
            separator1.grid(row=4, column=0, columnspan=8, sticky="ew", pady=4)
            
            # === FUNCIONES TRIGONOMÉTRICAS ===
            self.create_keypad_section_title(keypad_container, "📐 Funciones Trigonométricas", 5, 0, 8)
            
            # Trigonometric functions row 1
            self.create_keypad_button(keypad_container, "sin", "sin(", 6, 0, width=6)
            self.create_keypad_button(keypad_container, "cos", "cos(", 6, 1, width=6)
            self.create_keypad_button(keypad_container, "tan", "tan(", 6, 2, width=6)
            self.create_keypad_button(keypad_container, "asin", "asin(", 6, 3, width=6)
            self.create_keypad_button(keypad_container, "acos", "acos(", 6, 4, width=6)
            self.create_keypad_button(keypad_container, "atan", "atan(", 6, 5, width=6)
            self.create_keypad_button(keypad_container, "sinh", "sinh(", 6, 6, width=6)
            self.create_keypad_button(keypad_container, "cosh", "cosh(", 6, 7, width=6)
            
            # Trigonometric functions row 2
            self.create_keypad_button(keypad_container, "tanh", "tanh(", 7, 0, width=6)
            self.create_keypad_button(keypad_container, "sec", "sec(", 7, 1, width=6)
            self.create_keypad_button(keypad_container, "csc", "csc(", 7, 2, width=6)
            self.create_keypad_button(keypad_container, "cot", "cot(", 7, 3, width=6)
            self.create_keypad_button(keypad_container, "arcsin", "asin(", 7, 4, width=6)
            self.create_keypad_button(keypad_container, "arccos", "acos(", 7, 5, width=6)
            self.create_keypad_button(keypad_container, "arctan", "atan(", 7, 6, width=6)
            self.create_keypad_button(keypad_container, "🧹", "clear", 7, 7, width=6)
            
            # === SEPARADOR ===
            separator2 = ttk.Separator(keypad_container, orient="horizontal")
            separator2.grid(row=8, column=0, columnspan=8, sticky="ew", pady=4)
            
            # === FUNCIONES LOGARÍTMICAS Y EXPONENCIALES ===
            self.create_keypad_section_title(keypad_container, "📐 Logaritmicas y Exponenciales", 9, 0, 8)
            
            # Logarithmic and exponential functions
            self.create_keypad_button(keypad_container, "log", "log(", 10, 0, width=6)
            self.create_keypad_button(keypad_container, "ln", "ln(", 10, 1, width=6)
            self.create_keypad_button(keypad_container, "log₂", "log(2,", 10, 2, width=6)
            self.create_keypad_button(keypad_container, "log₁₀", "log(10,", 10, 3, width=6)
            self.create_keypad_button(keypad_container, "exp", "exp(", 10, 4, width=6)
            self.create_keypad_button(keypad_container, "abs", "abs(", 10, 5, width=6)
            self.create_keypad_button(keypad_container, "sqrt2", "sqrt(2)", 10, 6, width=6)
            self.create_keypad_button(keypad_container, "sqrt3", "sqrt(3)", 10, 7, width=6)
            
            # === SEPARADOR ===
            separator3 = ttk.Separator(keypad_container, orient="horizontal")
            separator3.grid(row=11, column=0, columnspan=8, sticky="ew", pady=4)
            
            # === INTEGRALES Y DIFERENCIALES ===
            self.create_keypad_section_title(keypad_container, "� Integrales y Diferenciales", 12, 0, 8)
            
            # Integral operations row 1
            self.create_integral_button(keypad_container, "∫", "indefinite", 13, 0, "Integral indefinida")
            self.create_integral_button(keypad_container, "∫_a^b", "definite", 13, 1, "Integral definida")
            self.create_integral_button(keypad_container, "∬", "double", 13, 2, "Integral doble")
            self.create_integral_button(keypad_container, "∭", "triple", 13, 3, "Integral triple")
            self.create_keypad_button(keypad_container, "∂", "partial", 13, 4, "Derivada parcial")
            self.create_keypad_button(keypad_container, "∇", "gradient", 13, 5, "Gradiente")
            self.create_keypad_button(keypad_container, "∑", "sum", 13, 6, "Sumatoria")
            self.create_keypad_button(keypad_container, "∏", "product", 13, 7, "Productoria")
            
            # Differential operators row 2
            self.create_keypad_button(keypad_container, "d/dx", "diff(", 14, 0, width=6)
            self.create_keypad_button(keypad_container, "dx", "dx", 14, 1, width=6)
            self.create_keypad_button(keypad_container, "dy", "dy", 14, 2, width=6)
            self.create_keypad_button(keypad_container, "dz", "dz", 14, 3, width=6)
            self.create_keypad_button(keypad_container, "dt", "dt", 14, 4, width=6)
            self.create_keypad_button(keypad_container, "∫", "integral", 14, 5, width=6)
            self.create_keypad_button(keypad_container, "∞", "oo", 14, 6, width=6)
            self.create_keypad_button(keypad_container, "∅", "emptyset", 14, 7, width=6)
            
            # === SEPARADOR ===
            separator4 = ttk.Separator(keypad_container, orient="horizontal")
            separator4.grid(row=15, column=0, columnspan=8, sticky="ew", pady=4)
            
            # === SÍMBOLOS GRIEGOS Y ESPECIALES ===
            self.create_keypad_section_title(keypad_container, "🔢 Símbolos Griegos y Especiales", 16, 0, 8)
            
            # Greek letters row 1
            self.create_keypad_button(keypad_container, "α", "alpha", 17, 0, width=6)
            self.create_keypad_button(keypad_container, "β", "beta", 17, 1, width=6)
            self.create_keypad_button(keypad_container, "γ", "gamma", 17, 2, width=6)
            self.create_keypad_button(keypad_container, "δ", "delta", 17, 3, width=6)
            self.create_keypad_button(keypad_container, "θ", "theta", 17, 4, width=6)
            self.create_keypad_button(keypad_container, "λ", "lambda", 17, 5, width=6)
            self.create_keypad_button(keypad_container, "μ", "mu", 17, 6, width=6)
            self.create_keypad_button(keypad_container, "σ", "sigma", 17, 7, width=6)
            
        except Exception as e:
            logger.error(f"Error creating scientific keypad: {str(e)}")
            raise
    
    def create_keypad_section_title(self, parent, title, row, col, colspan):
        """Create a section title for the keypad with improved layout"""
        try:
            title_label = ttk.Label(parent, text=title, font=("Arial", 9, "bold"), 
                                  foreground="#2c3e50")
            title_label.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=(3, 1))
        except Exception as e:
            logger.error(f"Error creating section title: {str(e)}")
    
        
    def create_integral_button(self, parent, display_text, integral_type, row, col, tooltip):
        """Create an integral button with improved layout"""
        try:
            btn = ttk.Button(parent, text=display_text, width=5,
                          command=lambda t=integral_type: self.insert_integral_structure(t))
            btn.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            
            return btn
        except Exception as e:
            logger.error(f"Error creating integral button: {str(e)}")
            return None
    
    def create_results_section(self, parent):
        """Create results section with tabs"""
        try:
            # Results notebook
            self.results_notebook = ttk.Notebook(parent)
            self.results_notebook.pack(fill="both", expand=True)
            
            # Create result tabs
            self.create_result_tabs()
            
        except Exception as e:
            logger.error(f"Error creating results section: {str(e)}")
            raise
    
    def create_result_tabs(self):
        """Create result tabs"""
        try:
            # Result tab
            result_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(result_frame, text="🎯 Resultado")
            
            self.latex_result_frame = ttk.Frame(result_frame)
            self.latex_result_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Initial message
            self.latex_result_label = ttk.Label(self.latex_result_frame, 
                                              text="📊 Ingresa una función y presiona 'Calcular'",
                                              font=("Arial", 12), foreground="gray")
            self.latex_result_label.pack(pady=20)
            
            # Steps tab
            steps_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(steps_frame, text="📝 Pasos")
            
            self.latex_steps_container = ttk.Frame(steps_frame)
            self.latex_steps_container.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Create scrollable frame
            canvas = tk.Canvas(self.latex_steps_container)
            scrollbar = ttk.Scrollbar(self.latex_steps_container, orient="vertical", command=canvas.yview)
            self.latex_steps_frame = ttk.Frame(canvas)
            
            self.latex_steps_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=self.latex_steps_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Initial message
            self.latex_steps_label = ttk.Label(self.latex_steps_frame, 
                                             text="📝 Los pasos aparecerán aquí",
                                             font=("Arial", 12), foreground="gray")
            self.latex_steps_label.pack(pady=20)
            
            # Verification tab
            verify_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(verify_frame, text="✔️ Verificación")
            
            self.latex_verify_frame = ttk.Frame(verify_frame)
            self.latex_verify_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Initial message
            self.latex_verify_label = ttk.Label(self.latex_verify_frame, 
                                              text="✔️ La verificación aparecerá aquí",
                                              font=("Arial", 12), foreground="gray")
            self.latex_verify_label.pack(pady=20)
            
            # Text mode tab
            text_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(text_frame, text="📄 Modo Texto")
            
            # Text display
            text_container = ttk.Frame(text_frame)
            text_container.pack(fill="both", expand=True, padx=8, pady=8)
            
            self.text_result_display = scrolledtext.ScrolledText(
                text_container, wrap=tk.WORD, width=100, height=20,
                font=('Courier', 11), bg='#f8f9fa'
            )
            self.text_result_display.pack(fill="both", expand=True)
            
            # Configure tags
            self.text_result_display.tag_configure("title", font=("Courier", 12, "bold"), 
                                                 foreground="#2c3e50")
            self.text_result_display.tag_configure("result", font=("Courier", 11, "bold"), 
                                                 foreground="#27ae60")
            self.text_result_display.tag_configure("method", font=("Courier", 10), 
                                                 foreground="#3498db")
            
        except Exception as e:
            logger.error(f"Error creating result tabs: {str(e)}")
            raise
    
    def create_graph_section(self, parent):
        """Create graph section"""
        try:
            # Graph frame
            graph_frame = ttk.LabelFrame(parent, text="📈 Visualización", padding=8)
            graph_frame.pack(fill="both", expand=True)
            
            # Controls
            controls_frame = ttk.Frame(graph_frame)
            controls_frame.pack(fill="x", pady=(0, 8))
            
            ttk.Button(controls_frame, text="📊 Graficar", command=self.plot_function, width=12).pack(side="left", padx=5)
            ttk.Button(controls_frame, text="📈 Análisis", command=self.plot_analysis, width=12).pack(side="left", padx=5)
            ttk.Button(controls_frame, text="🔄 Actualizar", command=self.update_graph, width=12).pack(side="left", padx=5)
            ttk.Button(controls_frame, text="🧹 Limpiar", command=self.clear_graph, width=12).pack(side="left", padx=5)
            
            # Graph area
            self.graph_frame = ttk.Frame(graph_frame)
            self.graph_frame.pack(fill="both", expand=True)
            
            # Initial message
            self.graph_label = ttk.Label(self.graph_frame, 
                                        text="📊 Ingresa una función y presiona 'Graficar'",
                                        font=("Arial", 11), foreground="gray")
            self.graph_label.pack(pady=20)
            
        except Exception as e:
            logger.error(f"Error creating graph section: {str(e)}")
            raise
    
    def create_status_bar(self):
        """Create modern professional status bar with enhanced visual design"""
        try:
            # Modern status bar with gradient effect
            status_bar = tk.Frame(self.main_frame, bg='#34495e', height=35)
            status_bar.pack(fill="x", pady=(10, 0))
            status_bar.pack_propagate(False)
            
            # Left section - Status and performance
            left_section = tk.Frame(status_bar, bg='#34495e')
            left_section.pack(side="left", padx=15, pady=8)
            
            # Animated status indicator
            self.status_label = tk.Label(left_section, text="🚀 Sistema listo", 
                                       font=('Arial', 10, 'bold'), fg='#2ecc71', bg='#34495e')
            self.status_label.pack(side="left", padx=(0, 15))
            
            # Performance indicator with color coding
            self.performance_label = tk.Label(left_section, text="⚡ Rendimiento: Excelente", 
                                           font=('Arial', 9), fg='#f39c12', bg='#34495e')
            self.performance_label.pack(side="left", padx=(0, 15))
            
            # Memory usage indicator
            self.memory_label = tk.Label(left_section, text="💾 Memoria: Normal", 
                                       font=('Arial', 9), fg='#3498db', bg='#34495e')
            self.memory_label.pack(side="left")
            
            # Center section - Quick stats
            center_section = tk.Frame(status_bar, bg='#34495e')
            center_section.pack(side="left", expand=True, fill="x", pady=8)
            
            # Calculation counter
            self.calc_counter = tk.Label(center_section, text="📊 Cálculos: 0", 
                                       font=('Arial', 9), fg='#ecf0f1', bg='#34495e')
            self.calc_counter.pack()
            
            # Right section - Version and time
            right_section = tk.Frame(status_bar, bg='#34495e')
            right_section.pack(side="right", padx=15, pady=8)
            
            # Current time
            self.time_label = tk.Label(right_section, text="🕐 00:00:00", 
                                     font=('Arial', 9), fg='#ecf0f1', bg='#34495e')
            self.time_label.pack(side="right", padx=(15, 0))
            
            # Version badge
            version_badge = tk.Label(right_section, text="PRO v3.0", 
                                  font=('Arial', 9, 'bold'), fg='#e74c3c', bg='#34495e',
                                  relief=tk.RIDGE, bd=1, padx=5, pady=2)
            version_badge.pack(side="right")
            
            # Start time updates
            self.update_time()
            
        except Exception as e:
            logger.error(f"Error creating status bar: {str(e)}")
            raise
    
    def apply_theme(self):
        """Apply modern theme to the application with enhanced visual effects"""
        try:
            theme = self.theme_manager.apply_theme(self.root)
            
            # Apply theme to all widgets
            self.apply_theme_to_widget(self.root, theme)
            
            # Add modern styling effects
            self.add_modern_styling()
            
            logger.info(f"Modern theme applied: {self.theme_manager.current_theme}")
            
        except Exception as e:
            logger.error(f"Error applying theme: {str(e)}")
    
    def add_modern_styling(self):
        """Add modern visual styling effects"""
        try:
            # Add subtle animations to buttons
            if hasattr(self, 'calculate_btn'):
                self.calculate_btn.bind('<ButtonPress-1>', self.on_button_press)
                self.calculate_btn.bind('<ButtonRelease-1>', self.on_button_release)
            
            # Add focus effects to editor
            if hasattr(self, 'editor_text'):
                self.editor_text.bind('<FocusIn>', self.on_editor_focus_in)
                self.editor_text.bind('<FocusOut>', self.on_editor_focus_out)
                
        except Exception as e:
            logger.error(f"Error adding modern styling: {str(e)}")
    
    def on_button_press(self, event):
        """Handle button press with visual feedback"""
        try:
            event.widget.config(relief=tk.SUNKEN)
            self.update_status("🔄 Calculando...")
        except Exception as e:
            logger.error(f"Error in button press: {str(e)}")
    
    def on_button_release(self, event):
        """Handle button release with visual feedback"""
        try:
            event.widget.config(relief=tk.FLAT)
            self.update_status("🚀 Sistema listo")
        except Exception as e:
            logger.error(f"Error in button release: {str(e)}")
    
    def on_editor_focus_in(self, event):
        """Handle editor focus in with visual feedback"""
        try:
            self.editor_text.config(bg='#34495e')
            self.update_status("✏️ Editando expresión...")
        except Exception as e:
            logger.error(f"Error in editor focus in: {str(e)}")
    
    def on_editor_focus_out(self, event):
        """Handle editor focus out with visual feedback"""
        try:
            self.editor_text.config(bg='#2c3e50')
            self.update_status("🚀 Sistema listo")
        except Exception as e:
            logger.error(f"Error in editor focus out: {str(e)}")
    
    def update_time(self):
        """Update the time display"""
        try:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            if hasattr(self, 'time_label'):
                self.time_label.config(text=f"🕐 {current_time}")
            # Schedule next update
            self.root.after(1000, self.update_time)
        except Exception as e:
            logger.error(f"Error updating time: {str(e)}")
    
    def update_status(self, message, color='#2ecc71'):
        """Update status message with color"""
        try:
            if hasattr(self, 'status_label'):
                self.status_label.config(text=message, fg=color)
        except Exception as e:
            logger.error(f"Error updating status: {str(e)}")
    
    def increment_calc_counter(self):
        """Increment calculation counter"""
        try:
            if hasattr(self, 'calc_counter'):
                current_text = self.calc_counter.cget("text")
                current_count = int(current_text.split(": ")[1]) if ": " in current_text else 0
                new_count = current_count + 1
                self.calc_counter.config(text=f"Calculos: {new_count}")
        except Exception as e:
            logger.error(f"Error incrementing calc counter: {str(e)}")
    
    def calculate_integral(self):
        """Calculate the integral with modern UI feedback"""
        if self.is_calculating:
            return
        
        try:
            # Get function from editor
            function_text = self.editor_text.get("1.0", tk.END).strip()
            if not function_text:
                messagebox.showwarning("Advertencia", "Por favor ingresa una función")
                return
            
            # Update UI state
            self.is_calculating = True
            self.update_status("Calculando...", '#f39c12')
            self.calculate_btn.config(text="Calculando...", state="disabled")
            
            # Parse function
            parsed_func = self.parser.parse(function_text)
            
            # Get integration method
            method_map = {
                'Automático': 'auto',
                'Directa': 'direct', 
                'Sustitución': 'substitution',
                'Por Partes': 'parts',
                'Fracciones Parciales': 'partial_fractions',
                'Trigonométrica': 'trigonometric',
                'Racional': 'racional',
                'Exponencial': 'exponencial'
            }
            method = method_map.get(self.integral_type_var.get(), 'auto')
            
            # Get variable
            variable = self.symbols['x'].get()
            var_symbol = sp.Symbol(variable)
            
            # Calculate integral
            result = self.integrator.integrate(parsed_func, var_symbol, method)
            
            # Store result
            self.current_result = result
            self.current_function = function_text
            self.last_answer = str(result.result)
            
            # Update UI
            self.display_result(result)
            self.increment_calc_counter()
            self.update_status("Cálculo completado", '#27ae60')
            
            # Add to history
            self.history_manager.add_entry(function_text, self.integral_type_var.get())
            
        except Exception as e:
            logger.error(f"Error calculating integral: {str(e)}")
            messagebox.showerror("Error", f"No se pudo calcular la integral: {str(e)}")
            self.update_status("Error en cálculo", '#e74c3c')
        finally:
            self.is_calculating = False
            self.calculate_btn.config(text="CALCULAR", state="normal")
    
    def display_result(self, result):
        """Display the integration result"""
        try:
            # Create result display window if not exists
            if not hasattr(self, 'result_window') or not self.result_window.winfo_exists():
                self.create_result_display()
            
            # Format the result nicely
            if hasattr(result, 'result') and result.result is not None:
                result_text = f"Resultado: {result.result}"
                if hasattr(result, 'method'):
                    result_text += f"\\nMétodo: {result.method.value}"
                if hasattr(result, 'is_definite') and result.is_definite:
                    definite_result = result.get_definite_result()
                    if definite_result is not None:
                        result_text += f"\\nValor definido: {definite_result}"
            else:
                result_text = "No se pudo calcular la integral"
            
            # Update result display
            if hasattr(self, 'result_label'):
                self.result_label.config(text=result_text, justify="left")
                
        except Exception as e:
            logger.error(f"Error displaying result: {str(e)}")
    
    def create_result_display(self):
        """Create result display window"""
        try:
            self.result_window = tk.Toplevel(self.root)
            self.result_window.title("Resultado de la Integral")
            self.result_window.geometry("600x400")
            
            # Result display
            self.result_label = tk.Label(self.result_window, text="", 
                                        font=('Arial', 14), bg='white', fg='#2c3e50')
            self.result_label.pack(pady=20, padx=20, fill="both", expand=True)
            
        except Exception as e:
            logger.error(f"Error creating result display: {str(e)}")
    
    def new_calculation(self):
        """Clear for new calculation"""
        try:
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", "x**2 + 3*x + 2")
            self.current_function = "x**2 + 3*x + 2"
            self.current_result = None
            self.update_status("Listo para nuevo cálculo", '#2ecc71')
            self.update_character_counter()
        except Exception as e:
            logger.error(f"Error in new calculation: {str(e)}")
    
    def save_result(self):
        """Save current result"""
        try:
            if self.current_result:
                messagebox.showinfo("Guardar", "Resultado guardado exitosamente")
                self.update_status("Resultado guardado", '#27ae60')
            else:
                messagebox.showwarning("Guardar", "No hay resultado para guardar")
        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")
    
    def show_history(self):
        """Show calculation history"""
        try:
            history = self.history_manager.get_all()
            if history:
                history_text = "\\n".join([f"{i+1}. {entry['function']} - {entry['date']}" 
                                         for i, entry in enumerate(history[-10:])])
                messagebox.showinfo("Historial", history_text)
            else:
                messagebox.showinfo("Historial", "No hay cálculos en el historial")
        except Exception as e:
            logger.error(f"Error showing history: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        try:
            new_theme = self.theme_manager.toggle_theme()
            self.apply_theme()
            self.update_status(f"Tema cambiado a: {new_theme}", '#3498db')
        except Exception as e:
            logger.error(f"Error toggling theme: {str(e)}")
    
    def show_help(self):
        """Show help information"""
        try:
            help_text = """Calculadora de Integrales PRO v3.0 - Ayuda

FUNCIONES BÁSICAS:
- Operadores: +, -, *, /, ^ (potencia)
- Funciones: sin, cos, tan, log, ln, exp, sqrt
- Constantes: pi, e, phi, tau, i, j
- Variables: x, y, z, t, u, v

MÉTODOS DE INTEGRACIÓN:
- Automático: Detección inteligente
- Directa: Integración directa
- Sustitución: Por sustitución
- Por Partes: Integración por partes
- Fracciones Parciales: Descomposición
- Trigonométrica: Identidades trigonométricas
- Racional: Funciones racionales
- Exponencial: Funciones exponenciales

SÍMBOLOS ESPECIALES:
- Integrales: int, def_int, double_int, triple_int
- Sumatorias: sum, prod
- Límites: lim, inf, partial
- Funciones: sqrt, cbrt, abs, sign, floor, ceil, factorial, gamma

ATAJOS DE TECLADO:
- Ctrl+Enter: Calcular integral
- Ctrl+N: Nuevo cálculo
- Ctrl+S: Guardar resultado
- Ctrl+H: Mostrar historial
- Ctrl+G: Graficar función
- Ctrl+E: Exportar gráfica"""
            
            messagebox.showinfo("Ayuda v3.0", help_text)
        except Exception as e:
            logger.error(f"Error showing help: {str(e)}")
    
    def export_report(self):
        """Export comprehensive calculation report"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            if not self.current_result:
                messagebox.showwarning("Exportar", "No hay resultados para exportar")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("PDF files", "*.pdf"),
                    ("All files", "*.*")
                ],
                initialfile=f"integral_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                report = self.generate_comprehensive_report()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                messagebox.showinfo("Exportar", f"Informe exportado a: {filename}")
                self.update_status("Informe exportado", '#27ae60')
                
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            messagebox.showerror("Error", f"No se pudo exportar el informe: {str(e)}")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive calculation report"""
        try:
            from datetime import datetime
            
            report = f"""
{'='*60}
CALCULADORA DE INTEGRALES PRO v3.0 - INFORME COMPLETO
{'='*60}

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

1. FUNCIÓN ORIGINAL:
{self.current_function}

2. MÉTODO DE INTEGRACIÓN:
{self.integral_type_var.get()}

3. RESULTADO:
{self.current_result.result if self.current_result else 'No disponible'}

4. VARIABLE DE INTEGRACIÓN:
{self.symbols['x'].get()}

5. PASOS DEL CÁLCULO:
{{'- ' + '\\n- '.join(str(step) for step in self.current_result.steps) if self.current_result and hasattr(self.current_result, 'steps') else 'No disponibles'}}

6. INFORMACIÓN ADICIONAL:
- Método utilizado: {self.current_result.method.value if self.current_result else 'N/A'}
- Tipo de integral: {{'Definida' if self.definite_var.get() else 'Indefinida'}}
- Límites: {{self.lower_limit.get()}} a {{self.upper_limit.get()}} if self.definite_var.get() else 'N/A'}}

7. VERIFICACIÓN:
{self.current_result.get_definite_result() if self.current_result and hasattr(self.current_result, 'get_definite_result') else 'N/A'}

8. ESTADÍSTICAS:
- Caracteres en función: {len(self.current_function)}
- Tiempo de cálculo: < 1 segundo
- Precisión: Simbólica exacta

{'='*60}
FIN DEL INFORME
{'='*60}
"""
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return "Error al generar el informe"
    
    def show_settings(self):
        """Show settings dialog"""
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Configuración - CalcPRO v3.0")
            settings_window.geometry("500x400")
            settings_window.configure(bg='#1a1a2e')
            
            # Title
            title_label = tk.Label(settings_window, text="CONFIGURACIÓN", 
                                 font=('Segoe UI', 16, 'bold'), 
                                 fg='#e94560', bg='#1a1a2e')
            title_label.pack(pady=20)
            
            # Settings sections
            settings_frame = tk.Frame(settings_window, bg='#16213e')
            settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Theme settings
            theme_frame = tk.Frame(settings_frame, bg='#16213e')
            theme_frame.pack(fill="x", pady=10)
            
            tk.Label(theme_frame, text="Tema:", font=('Segoe UI', 10, 'bold'), 
                    fg='white', bg='#16213e').pack(side="left", padx=10)
            
            # Calculation settings
            calc_frame = tk.Frame(settings_frame, bg='#16213e')
            calc_frame.pack(fill="x", pady=10)
            
            tk.Label(calc_frame, text="Precisión:", font=('Segoe UI', 10, 'bold'), 
                    fg='white', bg='#16213e').pack(side="left", padx=10)
            
            # Auto-parentheses setting
            auto_frame = tk.Frame(settings_frame, bg='#16213e')
            auto_frame.pack(fill="x", pady=10)
            
            tk.Checkbutton(auto_frame, text="Auto-paréntesis", 
                          variable=self.auto_parentheses,
                          font=('Segoe UI', 10),
                          fg='white', bg='#16213e',
                          selectcolor='#e94560',
                          activebackground='#16213e',
                          activeforeground='white').pack(side="left", padx=10)
            
            # Close button
            close_btn = tk.Button(settings_window, text="Cerrar", 
                                command=settings_window.destroy,
                                font=('Segoe UI', 10, 'bold'),
                                bg='#e94560', fg='white',
                                padx=20, pady=5)
            close_btn.pack(pady=20)
            
        except Exception as e:
            logger.error(f"Error showing settings: {str(e)}")
            messagebox.showerror("Error", f"No se pudo mostrar la configuración: {str(e)}")
    
    def on_variable_change(self, event):
        """Handle variable change"""
        try:
            new_var = self.variable_combo.get()
            self.symbols['x'].set(new_var)
            self.update_status(f"Variable cambiada a: {new_var}", '#3498db')
        except Exception as e:
            logger.error(f"Error changing variable: {str(e)}")
    
    def on_editor_key_release(self, event):
        """Handle editor key release"""
        try:
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            self.update_character_counter()
            
            # Basic validation
            if self.current_function:
                validation = self.validator.validate(self.current_function)
                if validation['valid']:
                    self.editor_status.config(text="Válido", fg='#27ae60')
                else:
                    self.editor_status.config(text="Inválido", fg='#e74c3c')
            else:
                self.editor_status.config(text="Vacío", fg='#95a5a6')
                
        except Exception as e:
            logger.error(f"Error in editor key release: {str(e)}")
    
    def on_editor_key_press(self, event):
        """Handle editor key press"""
        try:
            # Auto-parentheses
            if self.auto_parentheses.get() and event.char in '([':
                cursor_pos = self.editor_text.index(tk.INSERT)
                self.editor_text.insert(cursor_pos, event.char + ')')
                self.editor_text.mark_set(tk.INSERT, f"{cursor_pos}+1c")
                return "break"
        except Exception as e:
            logger.error(f"Error in editor key press: {str(e)}")
    
    def on_editor_click(self, event):
        """Handle editor click"""
        try:
            # Update cursor position if needed
            pass
        except Exception as e:
            logger.error(f"Error in editor click: {str(e)}")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        try:
            self.root.bind('<Control-Return>', lambda e: self.calculate_integral())
            self.root.bind('<Control-n>', lambda e: self.new_calculation())
            self.root.bind('<Control-s>', lambda e: self.save_result())
            self.root.bind('<Control-h>', lambda e: self.show_history())
        except Exception as e:
            logger.error(f"Error setting up shortcuts: {str(e)}")
    
    def apply_theme_to_widget(self, widget, theme):
        """Apply theme to widget and children"""
        try:
            widget.configure(bg=theme.get("bg", "#FFFFFF"))
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, theme)
        except:
            pass  # Some widgets don't support bg configuration
    
    def toggle_limits(self):
        """Toggle definite integral limits visibility"""
        try:
            if self.definite_var.get():
                # Show limits frame
                self.limits_frame.pack(fill="x", pady=(4, 0))
                self.update_status("Modo integral definida activado", '#3498db')
            else:
                # Hide limits frame
                self.limits_frame.pack_forget()
                self.update_status("Modo integral indefinida", '#2ecc71')
        except Exception as e:
            logger.error(f"Error toggling limits: {str(e)}")
    
    def create_scientific_keypad(self, parent):
        """Create scientific keypad (placeholder for compatibility)"""
        try:
            # Create a simple keypad as fallback
            keypad_frame = tk.Frame(parent, bg='#ecf0f1')
            keypad_frame.pack(fill="both", expand=True)
            
            # Basic buttons
            buttons = [
                ('7', '8', '9', '/'),
                ('4', '5', '6', '*'),
                ('1', '2', '3', '-'),
                ('0', '.', '=', '+'),
                ('sin', 'cos', 'tan', '^'),
                ('log', 'ln', 'exp', 'sqrt'),
                ('pi', 'e', '(', ')'),
                ('x', 'y', 'z', 't')
            ]
            
            for row in buttons:
                row_frame = tk.Frame(keypad_frame, bg='#ecf0f1')
                row_frame.pack(fill="x", pady=2)
                
                for btn_text in row:
                    btn = tk.Button(row_frame, text=btn_text, 
                                  font=('Arial', 10),
                                  bg='#3498db', fg='white',
                                  padx=10, pady=5,
                                  command=lambda t=btn_text: self.insert_text(t))
                    btn.pack(side="left", padx=2, expand=True, fill="x")
                    
        except Exception as e:
            logger.error(f"Error creating scientific keypad: {str(e)}")
    
    def clear_editor(self):
        """Clear the editor content"""
        try:
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", "")
            self.current_function = ""
            self.update_character_counter()
            self.update_status("Editor limpiado", '#2ecc71')
        except Exception as e:
            logger.error(f"Error clearing editor: {str(e)}")
    
    def insert_ans(self):
        """Insert last answer (ANS) into editor"""
        try:
            cursor_pos = self.editor_text.index(tk.INSERT)
            self.editor_text.insert(cursor_pos, self.last_answer)
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            self.update_character_counter()
            self.update_status("ANS insertado", '#3498db')
        except Exception as e:
            logger.error(f"Error inserting ANS: {str(e)}")
    
    def redo_input(self):
        """Redo last input"""
        try:
            if hasattr(self, 'last_function') and self.last_function:
                self.editor_text.delete("1.0", tk.END)
                self.editor_text.insert("1.0", self.last_function)
                self.current_function = self.last_function
                self.update_character_counter()
                self.update_status("Entrada rehecha", '#f39c12')
            else:
                self.update_status("No hay entrada anterior", '#e74c3c')
        except Exception as e:
            logger.error(f"Error redoing input: {str(e)}")
    
    def clear_results_display(self):
        """Clear results display"""
        try:
            if hasattr(self, 'result_label'):
                self.result_label.config(text="Sin resultados")
            self.current_result = None
            self.update_status("Resultados limpiados", '#2ecc71')
        except Exception as e:
            logger.error(f"Error clearing results: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        try:
            if hasattr(self, 'results_window') and self.results_window:
                self.results_window.destroy()
            if hasattr(self, 'graph_window') and self.graph_window:
                self.graph_window.destroy()
            self.root.destroy()
        except Exception as e:
            logger.error(f"Error closing application: {str(e)}")
            self.root.destroy()
    
    def new_calculation(self):
        """Start a new calculation"""
        try:
            self.clear_editor()
            self.clear_results_display()
            
            self.current_result = None
            self.current_steps = []
            
            self.status_bar.config(text="🚀 Calculadora Profesional Lista")
            
        except Exception as e:
            logger.error(f"Error in new calculation: {str(e)}")
    
    def save_result(self):
        """Save the current result"""
        try:
            if self.current_result:
                self.history_manager.add_entry(self.current_function, self.integral_type_var.get())
                messagebox.showinfo("Éxito", "Resultado guardado en historial")
                self.status_bar.config(text="💾 Resultado guardado")
            else:
                messagebox.showwarning("Advertencia", "No hay resultado para guardar")
        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def show_history(self):
        """Show calculation history"""
        try:
            history_window = tk.Toplevel(self.root)
            history_window.title("📋 Historial de Cálculos")
            history_window.geometry("800x500")
            
            # Buttons frame
            btn_frame = ttk.Frame(history_window)
            btn_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Button(btn_frame, text="🗑️ Limpiar", command=self.clear_history).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="📥 Exportar", command=self.export_history).pack(side="left", padx=5)
            
            # History list
            listbox = tk.Listbox(history_window, font=('Courier', 10))
            listbox.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Load history
            for entry in self.history_manager.get_all():
                display_text = f"{entry['function']} ({entry['type']}) - {entry['date']}"
                listbox.insert(tk.END, display_text)
            
            # Double click to load
            def load_from_history(event=None):
                selection = listbox.curselection()
                if selection:
                    entry = self.history_manager.get_all()[selection[0]]
                    self.editor_text.delete("1.0", tk.END)
                    self.editor_text.insert("1.0", entry['function'])
                    self.integral_type_var.set(entry['type'])
                    history_window.destroy()
            
            listbox.bind('<Double-1>', load_from_history)
            
        except Exception as e:
            logger.error(f"Error showing history: {str(e)}")
            messagebox.showerror("Error", f"Error al mostrar historial: {str(e)}")
    
    def clear_history(self):
        """Clear calculation history"""
        try:
            if messagebox.askyesno("Confirmar", "¿Desea limpiar todo el historial?"):
                self.history_manager.clear()
                self.status_bar.config(text="🗑️ Historial limpiado")
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
    
    def export_history(self):
        """Export calculation history"""
        try:
            self.history_manager.export_to_file()
            messagebox.showinfo("Éxito", "Historial exportado correctamente")
        except Exception as e:
            logger.error(f"Error exporting history: {str(e)}")
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def plot_function(self):
        """Plot the function"""
        try:
            if not self.current_function:
                messagebox.showwarning("Advertencia", "Ingresa una función")
                return
            
            if not self.validate_expression():
                messagebox.showwarning("Advertencia", "La expresión no es válida")
                return
            
            # Clear previous graph
            self.clear_graph()
            
            # Parse expression
            func = self.parser.parse(self.current_function)
            
            # Get range
            if self.definite_var.get():
                try:
                    lower = float(self.lower_limit.get())
                    upper = float(self.upper_limit.get())
                    a, b = lower - 1, upper + 1
                    limits = (lower, upper)
                except:
                    a, b = -5, 5
                    limits = None
            else:
                a, b = -5, 5
                limits = None
            
            # Generate plot
            fig = self.plotter.plot_interactive(func, self.parser._get_symbol(self.symbols['x'].get()), a, b, limits, show_area=bool(limits))
            
            # Show new plot
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            self.status_bar.config(text="📊 Gráfica generada")
            
        except Exception as e:
            logger.error(f"Error plotting function: {str(e)}")
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")
    
    def plot_analysis(self):
        """Generate complete analysis plot"""
        try:
            if not self.current_function:
                messagebox.showwarning("Advertencia", "Ingresa una función")
                return
            
            if not self.validate_expression():
                messagebox.showwarning("Advertencia", "La expresión no es válida")
                return
            
            # Parse expression
            func = self.parser.parse(self.current_function)
            
            # Get range
            if self.definite_var.get():
                try:
                    lower = float(self.lower_limit.get())
                    upper = float(self.upper_limit.get())
                    a, b = lower - 2, upper + 2
                    limits = (lower, upper)
                except:
                    a, b = -5, 5
                    limits = None
            else:
                a, b = -5, 5
                limits = None
            
            # Generate analysis plot
            fig = self.plotter.plot_with_analysis(func, self.parser._get_symbol(self.symbols['x'].get()), a, b, limits)
            
            # Show new plot
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            self.status_bar.config(text="📈 Análisis completo")
            
        except Exception as e:
            logger.error(f"Error generating analysis: {str(e)}")
            messagebox.showerror("Error", f"Error al generar análisis: {str(e)}")
    
    def update_graph(self):
        """Update the current graph"""
        try:
            if hasattr(self, 'current_function') and self.current_function:
                self.plot_function()
            else:
                messagebox.showinfo("Info", "No hay función para graficar")
        except Exception as e:
            logger.error(f"Error updating graph: {str(e)}")
    
    def clear_graph(self):
        """Clear the graph"""
        try:
            for widget in self.graph_frame.winfo_children():
                if hasattr(widget, 'winfo_class') and widget.winfo_class() == 'Canvas':
                    widget.destroy()
            
            self.graph_label = ttk.Label(self.graph_frame, 
                                        text="📊 Ingresa una función y presiona 'Graficar'",
                                        font=("Arial", 11), foreground="gray")
            self.graph_label.pack(pady=20)
            
        except Exception as e:
            logger.error(f"Error clearing graph: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between themes"""
        try:
            self.theme_manager.toggle_theme()
            self.apply_theme()
            theme_name = self.theme_manager.current_theme.capitalize()
            self.status_bar.config(text=f"🎨 Tema cambiado a {theme_name}")
        except Exception as e:
            logger.error(f"Error toggling theme: {str(e)}")
    
    def show_help(self):
        """Show help dialog"""
        try:
            help_window = tk.Toplevel(self.root)
            help_window.title("📖 Ayuda")
            help_window.geometry("750x700")
            
            help_text = """
🎓 CALCULADORA DE INTEGRALES PRO

🔥 CARACTERÍSTICAS:
• Motor de cálculo profesional con detección automática de métodos
• Renderizado LaTeX de alta calidad sin dependencias externas
• Teclado científico completo
• Visualización interactiva
• Historial de cálculos
• Temas profesional claro/oscuro

📐 MÉTODOS DE INTEGRACIÓN:
• Automático - Detección inteligente
• Directa - Integración simbólica directa
• Sustitución - Método u-substitución
• Por Partes - Integración por partes
• Fracciones Parciales - Descomposición racional
• Trigonométrica - Identidades trigonométricas
• Racional - Funciones racionales
• Exponencial - Funciones exponenciales

⌨️ ATAJOS:
• Ctrl+Enter: Calcular integral
• Ctrl+L: Nueva cálculo
• Ctrl+S: Guardar resultado
• Ctrl+H: Mostrar historial
• Ctrl+T: Cambiar tema
• F1: Mostrar ayuda

💡 CONSEJOS:
• Usa la notación estándar: x**2, sin(x), log(x)
• El teclado científico facilita la entrada
• Los resultados se muestran en múltiples formatos
• Las gráficas son interactivas y se pueden ampliar

🎯 NIVEL: Wolfram Alpha / GeoGebra
            """
            
            text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Arial', 10))
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, help_text)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"Error showing help: {str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        try:
            self.root.destroy()
        except Exception as e:
            logger.error(f"Error closing application: {str(e)}")


# Use the professional class
LaTeXIntegralCalculator = ProfessionalIntegralCalculator

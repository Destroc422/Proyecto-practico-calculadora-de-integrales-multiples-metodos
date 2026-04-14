"""
Professional Integral Calculator - Ultra-Modern Main Window
Redesigned for professional mathematical software experience
Compatible with Wolfram/GeoGebra/Maple level applications
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
import sys
import os
import traceback
import threading
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import sympy as sp
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Core modules
from core.integrator import ProfessionalIntegrator, IntegrationMethod, IntegrationError
from core.parser import ProfessionalMathParser, ParseError
from core.microsoft_math_engine import MicrosoftMathEngine

# UI modules
from ui.theme_manager import ThemeManager
from ui.latex_renderer import ProfessionalLaTeXRenderer
from ui.template_browser import TemplateBrowser, QuickTemplateSelector
from data.template_manager import TemplateRepository

# Graph and utilities
from graph.plotter import ProfessionalPlotter
from utils.validators import ExpressionValidator
from data.history_manager import HistoryManager

logger = logging.getLogger(__name__)


class ProfessionalIntegralCalculator:
    """Ultra-modern professional integral calculator with Wolfram-grade interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Integrales PRO v4.0 - Professional Edition")
        
        # Initialize screen management
        self.setup_screen_management()
        
        # Professional window styling
        self.root.configure(bg='#f8f9fa')
        
        # Center window
        self.center_window()
        
        # Initialize professional components
        self._initialize_components()
        
        # Setup professional UI
        self.setup_professional_ui()
        self.setup_shortcuts()
        
        # Apply professional theme
        self.apply_professional_theme()
        
        logger.info("Professional Integral Calculator v4.0 initialized successfully")
    
    def _initialize_components(self):
        """Initialize all professional components"""
        try:
            self.theme_manager = ThemeManager()
            self.integrator = ProfessionalIntegrator()
            self.parser = ProfessionalMathParser()
            self.plotter = ProfessionalPlotter()
            self.history_manager = HistoryManager()
            self.latex_renderer = ProfessionalLaTeXRenderer()
            self.validator = ExpressionValidator()
            self.math_engine = MicrosoftMathEngine()  # Microsoft Mathematics Engine
            self.template_manager = TemplateRepository()  # Template repository
            
            # Enhanced mathematical symbols
            self.symbols = {
                'x': tk.StringVar(value='x'),
                'y': tk.StringVar(value='y'),
                'z': tk.StringVar(value='z'),
                't': tk.StringVar(value='t'),
                'u': tk.StringVar(value='u'),
                'v': tk.StringVar(value='v')
            }
            
            # Enhanced application state
            self.current_result = None
            self.current_steps = []
            self.is_calculating = False
            self.last_answer = "0"
            self.favorite_expressions = []
            self.calculation_history = []
            
            # Professional UI state
            self.current_function = ""
            self.auto_parentheses = tk.BooleanVar(value=True)
            self.dark_mode = tk.BooleanVar(value=False)
            self.show_grid = tk.BooleanVar(value=True)
            self.show_legend = tk.BooleanVar(value=True)
            
            # Graph state
            self.graph_functions = []
            self.graph_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
            self.current_zoom_level = 1.0
            self.pan_start = None
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            messagebox.showerror("Error", "No se pudieron inicializar los componentes")
            raise
    
    def setup_professional_ui(self):
        """Setup ultra-modern professional user interface"""
        try:
            # Create main container with professional styling
            self.main_container = tk.Frame(self.root, bg='#f8f9fa')
            self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Create professional toolbar
            self.create_professional_toolbar()
            
            # Create main splitter layout
            self.create_professional_layout()
            
            # Create status bar
            self.create_professional_status_bar()
            
        except Exception as e:
            logger.error(f"Error setting up professional UI: {str(e)}")
            messagebox.showerror("Error", "No se pudo configurar la interfaz profesional")
            raise
    
    def create_professional_toolbar(self):
        """Create Wolfram-grade professional toolbar"""
        try:
            # Modern toolbar with rounded corners and shadows
            toolbar = tk.Frame(self.main_container, bg='#ffffff', height=65, relief=tk.RAISED, bd=1)
            toolbar.pack(fill="x", pady=(0, 5))
            toolbar.pack_propagate(False)
            
            # Logo and branding section
            logo_frame = tk.Frame(toolbar, bg='#ffffff')
            logo_frame.pack(side="left", padx=20, pady=15)
            
            # Professional logo with scaled font
            logo_label = tk.Label(logo_frame, text=" CalcPRO", 
                                font=('Segoe UI', self.font_sizes.get('title', 20), 'bold'), 
                                fg='#2c3e50', bg='#ffffff')
            logo_label.pack(side="left")
            
            # Version badge with scaled font
            version_badge = tk.Label(logo_frame, text="v4.0", 
                                  font=('Segoe UI', self.font_sizes.get('small', 9), 'bold'), 
                                  fg='#ffffff', bg='#3498db', 
                                  relief=tk.RAISED, bd=1, padx=6, pady=2)
            version_badge.pack(side="left", padx=(8, 0))
            
            # Professional navigation buttons
            nav_frame = tk.Frame(toolbar, bg='#ffffff')
            nav_frame.pack(side="left", padx=30, pady=15)
            
            self.create_professional_button(nav_frame, "Nuevo", self.new_calculation, '#3498db')
            self.create_professional_button(nav_frame, "Guardar", self.save_result, '#27ae60')
            self.create_professional_button(nav_frame, "Exportar", self.export_report, '#9b59b6')
            self.create_professional_button(nav_frame, "Historial", self.show_history, '#f39c12')
            
            # Separator
            separator = tk.Frame(toolbar, bg='#ecf0f1', width=2, height=45)
            separator.pack(side="left", padx=15, fill="y", pady=10)
            
            # Main calculation button - prominent
            calc_frame = tk.Frame(toolbar, bg='#ffffff')
            calc_frame.pack(side="left", padx=20, pady=15)
            
            self.calculate_btn = tk.Button(calc_frame, text="CALCULAR INTEGRAL", 
                                          command=self.calculate_integral,
                                          font=('Segoe UI', self.font_sizes.get('subtitle', 12), 'bold'),
                                          bg='#e74c3c', fg='white',
                                          padx=20, pady=8,
                                          relief=tk.RAISED, bd=2,
                                          cursor='hand2',
                                          activebackground='#c0392b',
                                          activeforeground='white')
            self.calculate_btn.pack()
            
            # Window controls
            window_frame = tk.Frame(toolbar, bg='#ffffff')
            window_frame.pack(side="right", padx=25, pady=15)
            
            # Zoom controls
            self.create_professional_button(window_frame, "Zoom In", lambda: self.adjust_window_size(1.1), '#3498db')
            self.create_professional_button(window_frame, "Zoom Out", lambda: self.adjust_window_size(0.9), '#3498db')
            self.create_professional_button(window_frame, "Maximizar", self.maximize_window, '#27ae60')
            self.create_professional_button(window_frame, "Pantalla Completa", self.toggle_fullscreen, '#9b59b6')
            
            # Separator
            separator2 = tk.Frame(window_frame, bg='#ecf0f1', width=2, height=30)
            separator2.pack(side="left", padx=10, fill="y", pady=15)
            
            # Theme toggle
            self.theme_btn = tk.Button(window_frame, text=" Tema", 
                                       command=self.toggle_professional_theme,
                                       font=('Segoe UI', 10, 'bold'),
                                       bg='#95a5a6', fg='white',
                                       padx=12, pady=6,
                                       relief=tk.RAISED, bd=1,
                                       cursor='hand2')
            self.theme_btn.pack(side="left", padx=3)
            
            # Settings
            self.settings_btn = tk.Button(window_frame, text=" Config", 
                                         command=self.show_professional_settings,
                                         font=('Segoe UI', 10, 'bold'),
                                         bg='#7f8c8d', fg='white',
                                         padx=12, pady=6,
                                         relief=tk.RAISED, bd=1,
                                         cursor='hand2')
            self.settings_btn.pack(side="left", padx=3)
            
            # Help
            self.help_btn = tk.Button(window_frame, text=" Ayuda", 
                                     command=self.show_professional_help,
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='#34495e', fg='white',
                                     padx=12, pady=6,
                                     relief=tk.RAISED, bd=1,
                                     cursor='hand2')
            self.help_btn.pack(side="left", padx=3)
            
        except Exception as e:
            logger.error(f"Error creating professional toolbar: {str(e)}")
            raise
    
    def create_professional_layout(self):
        """Create professional resizable layout with splitters"""
        try:
            # Setup main horizontal splitter with balanced proportions
            self.main_horizontal_paned = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
            self.main_horizontal_paned.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Left panel (input + keypad) - Balanced weight
            self.left_panel = tk.Frame(self.main_horizontal_paned, bg='#ecf0f1', relief=tk.RAISED, bd=1)
            self.main_horizontal_paned.add(self.left_panel, weight=2)  # Balanced from 3 to 2
            
            # Right panel (results + graph) - Balanced weight
            self.right_panel = tk.Frame(self.main_horizontal_paned, bg='#ecf0f1', relief=tk.RAISED, bd=1)
            self.main_horizontal_paned.add(self.right_panel, weight=3)  # Balanced from 4 to 3
            
            # Setup left panel
            self.setup_left_panel()
            
            # Setup right panel
            self.setup_right_panel()
            
        except Exception as e:
            logger.error(f"Error creating professional layout: {str(e)}")
            raise
    
    def setup_left_panel(self):
        """Setup left panel with input and ENHANCED keypad"""
        try:
            # Vertical splitter for left panel with enhanced keypad size
            self.left_vertical_paned = ttk.PanedWindow(self.left_panel, orient=tk.VERTICAL)
            self.left_vertical_paned.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Input section - Optimized weight for better balance
            self.input_frame = tk.Frame(self.left_vertical_paned, bg='#ffffff', relief=tk.RAISED, bd=1)
            self.left_vertical_paned.add(self.input_frame, weight=1)  # Optimized from 2 to 1
            
            # Keypad section - Optimized weight for symbol visibility
            self.keypad_frame = tk.Frame(self.left_vertical_paned, bg='#ffffff', relief=tk.RAISED, bd=1)
            self.left_vertical_paned.add(self.keypad_frame, weight=2)  # Optimized from 4 to 2
            
            # Setup input section
            self.setup_professional_input_section()
            
            # Setup ENHANCED keypad section
            self.setup_professional_keypad()
            
        except Exception as e:
            logger.error(f"Error setting up left panel: {str(e)}")
            raise
    
    def setup_right_panel(self):
        """Setup right panel with results and graph"""
        try:
            # Vertical splitter for right panel
            self.right_vertical_paned = ttk.PanedWindow(self.right_panel, orient=tk.VERTICAL)
            self.right_vertical_paned.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Results section
            self.results_frame = tk.Frame(self.right_vertical_paned, bg='#ffffff', relief=tk.RAISED, bd=1)
            self.right_vertical_paned.add(self.results_frame, weight=1)
            
            # Graph section
            self.graph_frame = tk.Frame(self.right_vertical_paned, bg='#ffffff', relief=tk.RAISED, bd=1)
            self.right_vertical_paned.add(self.graph_frame, weight=2)
            
            # Setup results section
            self.setup_professional_results_section()
            
            # Setup graph section
            self.setup_professional_graph_section()
            
        except Exception as e:
            logger.error(f"Error setting up right panel: {str(e)}")
            raise
    
    def setup_professional_input_section(self):
        """Setup professional input section"""
        try:
            # Header
            header = tk.Frame(self.input_frame, bg='#3498db', height=40)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="ENTRADA MATEMÁTICA", 
                    font=('Segoe UI', 12, 'bold'), 
                    fg='white', bg='#3498db').pack(pady=10)
            
            # Configuration section
            config_frame = tk.Frame(self.input_frame, bg='#ffffff')
            config_frame.pack(fill="x", padx=10, pady=10)
            
            # Method selection
            method_frame = tk.Frame(config_frame, bg='#ffffff')
            method_frame.pack(fill="x", pady=5)
            
            tk.Label(method_frame, text="Método:", 
                    font=('Segoe UI', 10, 'bold'), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=(0, 10))
            
            self.integral_type_var = tk.StringVar(value="Automático")
            self.method_combo = ttk.Combobox(method_frame, textvariable=self.integral_type_var,
                                           values=["Automático", "Directa", "Sustitución", "Por Partes", 
                                                   "Fracciones Parciales", "Trigonométrica", "Racional", "Exponencial"],
                                           state="readonly", width=20)
            self.method_combo.pack(side="left", padx=5)
            
            # Variable selection
            var_frame = tk.Frame(config_frame, bg='#ffffff')
            var_frame.pack(fill="x", pady=5)
            
            tk.Label(var_frame, text="Variable:", 
                    font=('Segoe UI', 10, 'bold'), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=(0, 10))
            
            self.variable_combo = ttk.Combobox(var_frame, textvariable=self.symbols['x'],
                                             values=['x', 'y', 'z', 't', 'u', 'v'],
                                             state="readonly", width=10)
            self.variable_combo.pack(side="left", padx=5)
            
            # Definite integral checkbox
            self.definite_var = tk.BooleanVar(value=False)
            definite_check = tk.Checkbutton(var_frame, text="Integral definida",
                                          variable=self.definite_var,
                                          command=self.toggle_limits,
                                          font=('Segoe UI', 10),
                                          fg='#2c3e50', bg='#ffffff',
                                          selectcolor='#3498db')
            definite_check.pack(side="left", padx=20)
            
            # Limits frame (initially hidden)
            self.limits_frame = tk.Frame(config_frame, bg='#ffffff')
            
            tk.Label(self.limits_frame, text="De:", 
                    font=('Segoe UI', 9), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=(0, 5))
            
            self.lower_limit = tk.Entry(self.limits_frame, width=8, 
                                       font=('Courier', 10), 
                                       bg='#f8f9fa', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=1)
            self.lower_limit.pack(side="left", padx=2)
            self.lower_limit.insert(0, "0")
            
            tk.Label(self.limits_frame, text="a:", 
                    font=('Segoe UI', 9), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=(10, 5))
            
            self.upper_limit = tk.Entry(self.limits_frame, width=8, 
                                       font=('Courier', 10), 
                                       bg='#f8f9fa', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=1)
            self.upper_limit.pack(side="left", padx=2)
            self.upper_limit.insert(0, "1")
            
            # Professional math editor
            editor_container = tk.Frame(self.input_frame, bg='#ffffff')
            editor_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Editor header
            editor_header = tk.Frame(editor_container, bg='#ecf0f1', height=30)
            editor_header.pack(fill="x")
            editor_header.pack_propagate(False)
            
            tk.Label(editor_header, text="Editor de Expresiones", 
                    font=('Segoe UI', 10, 'bold'), 
                    fg='#2c3e50', bg='#ecf0f1').pack(side="left", padx=10, pady=5)
            
            # Editor text widget with scaled font
            self.editor_text = tk.Text(editor_container, 
                                      font=('Courier', self.font_sizes.get('editor', 12)), 
                                      bg='#2c3e50', fg='#ecf0f1',
                                      relief=tk.RIDGE, bd=2,
                                      padx=10, pady=10,
                                      wrap=tk.WORD,
                                      undo=True)
            self.editor_text.pack(fill="both", expand=True)
            
            # Editor status
            editor_status = tk.Frame(editor_container, bg='#ecf0f1', height=25)
            editor_status.pack(fill="x", pady=(5, 0))
            editor_status.pack_propagate(False)
            
            self.editor_status_label = tk.Label(editor_status, text=" Listo", 
                                              font=('Segoe UI', 9), 
                                              fg='#27ae60', bg='#ecf0f1')
            self.editor_status_label.pack(side="left", padx=10, pady=2)
            
            self.char_counter = tk.Label(editor_status, text="0 caracteres", 
                                       font=('Segoe UI', 8), 
                                       fg='#7f8c8d', bg='#ecf0f1')
            self.char_counter.pack(side="right", padx=10, pady=2)
            
            # Bind events
            self.editor_text.bind('<KeyRelease>', self.on_editor_key_release)
            self.editor_text.bind('<Key>', self.on_editor_key_press)
            
            # Initialize with example
            self.editor_text.insert("1.0", "x**2 + 3*x + 2")
            self.current_function = "x**2 + 3*x + 2"
            
        except Exception as e:
            logger.error(f"Error setting up professional input section: {str(e)}")
            raise
    
    def setup_professional_keypad(self):
        """Setup ultra-modern professional scientific keypad with enhanced tabs"""
        try:
            # Enhanced header with gradient effect - Optimized height
            header = tk.Frame(self.keypad_frame, bg='#16a085', height=50)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            # Title with modern styling - Optimized font
            title_frame = tk.Frame(header, bg='#16a085')
            title_frame.pack(pady=12)
            
            tk.Label(title_frame, text=" TECLADO CIENTÍFICO AVANZADO", 
                    font=('Segoe UI', self.font_sizes.get('subtitle', 12), 'bold'), 
                    fg='white', bg='#16a085').pack()
            
            # Modern tab container with styling - Optimized for symbol visibility
            style = ttk.Style()
            style.theme_use('default')
            style.configure('Keypad.TNotebook', background='#f8f9fa')
            style.configure('Keypad.TNotebook.Tab', 
                          padding=[20, 12],  # Optimized padding for better space utilization
                          font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'))  # Optimized font
            
            self.tab_notebook = ttk.Notebook(self.keypad_frame, style='Keypad.TNotebook')
            self.tab_notebook.pack(fill="both", expand=True, padx=8, pady=8)  # Optimized padding
            
            # Create enhanced tabs with better organization
            self.create_enhanced_algebra_tab()
            self.create_enhanced_trigonometry_tab()
            self.create_enhanced_calculus_tab()
            self.create_enhanced_constants_tab()
            self.create_enhanced_special_tab()
            self.create_enhanced_matrix_tab()
            self.create_templates_tab()
            
        except Exception as e:
            logger.error(f"Error setting up professional keypad: {str(e)}")
            raise
    
    def create_enhanced_algebra_tab(self):
        """Create enhanced algebra tab with perfectly organized layout and clear symbol visibility"""
        try:
            algebra_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(algebra_frame, text="Álgebra")
            
            # Create scrollable frame with better styling
            canvas = tk.Canvas(algebra_frame, bg='#ffffff', highlightthickness=0)
            scrollbar = ttk.Scrollbar(algebra_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ffffff')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
            scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
            
            # === SECCIÓN 1: OPERACIONES FUNDAMENTALES ===
            section_frame = tk.LabelFrame(scrollable_frame, text="Operaciones Fundamentales", 
                                        font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame.pack(fill="x", padx=10, pady=(10, 8))
            
            ops_frame = tk.Frame(section_frame, bg='#ffffff')
            ops_frame.pack(fill="x", padx=8, pady=8)
            
            # Operaciones básicas (4 columnas para mejor visibilidad)
            basic_ops = [
                ('+', '-', '*', '/'),
                ('^', '%', '(', ')'),
                ('[', ']', '{', '}'),
                ('=', '<', '>', '!=')
            ]
            
            for i, row in enumerate(basic_ops):
                row_frame = tk.Frame(ops_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#3498db', 10)
            
            # Operadores de comparación y lógicos (separados)
            comp_ops = [
                ('<=', '>=', '!=', '==')
            ]
            
            for row in comp_ops:
                row_frame = tk.Frame(ops_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#95a5a6', 10)
            
            # === SECCIÓN 2: TECLADO NUMÉRICO CLÁSICO ===
            section_frame2 = tk.LabelFrame(scrollable_frame, text="Teclado Numérico", 
                                         font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame2.pack(fill="x", padx=10, pady=8)
            
            numbers_frame = tk.Frame(section_frame2, bg='#ffffff')
            numbers_frame.pack(fill="x", padx=8, pady=8)
            
            # Layout clásico de calculadora (4x4)
            numbers = [
                ('7', '8', '9', '÷'),
                ('4', '5', '6', '×'),
                ('1', '2', '3', 'minus'),
                ('0', '.', '=', '+')
            ]
            
            for i, row in enumerate(numbers):
                row_frame = tk.Frame(numbers_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for num in row:
                    if num == '=':
                        self.create_enhanced_keypad_button(row_frame, num, '#e74c3c', 10)
                    elif num in ['÷', '×', 'minus']:
                        self.create_enhanced_keypad_button(row_frame, num, '#3498db', 10)
                    elif num == '.':
                        self.create_enhanced_keypad_button(row_frame, num, '#95a5a6', 10)
                    else:
                        self.create_enhanced_keypad_button(row_frame, num, '#34495e', 10)
            
            # Botones especiales
            special_frame = tk.Frame(numbers_frame, bg='#ffffff')
            special_frame.pack(fill="x", pady=(8, 0))
            
            special_buttons = [
                ('ANS', 'DEL', 'CLEAR', 'CE')
            ]
            
            for row in special_buttons:
                row_frame = tk.Frame(special_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for btn in row:
                    if btn == 'ANS':
                        self.create_enhanced_keypad_button(row_frame, btn, '#9b59b6', 10)
                    elif btn in ['DEL', 'CLEAR', 'CE']:
                        self.create_enhanced_keypad_button(row_frame, btn, '#e74c3c', 10)
            
            # === SECCIÓN 3: FUNCIONES ALGEBRAICAS ===
            section_frame3 = tk.LabelFrame(scrollable_frame, text="Funciones Algebraicas", 
                                         font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame3.pack(fill="x", padx=10, pady=8)
            
            algebra_frame = tk.Frame(section_frame3, bg='#ffffff')
            algebra_frame.pack(fill="x", padx=8, pady=8)
            
            # Funciones básicas (3 columnas para mejor espacio)
            basic_funcs = [
                ('sqrt', 'cbrt', 'abs'),
                ('factorial', 'gcd', 'lcm'),
                ('mod', 'divmod', 'floor'),
                ('ceil', 'round', 'sign')
            ]
            
            for row in basic_funcs:
                row_frame = tk.Frame(algebra_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#e67e22', 12)
            
            # === SECCIÓN 4: POTENCIAS Y LOGARITMOS ===
            section_frame4 = tk.LabelFrame(scrollable_frame, text="Potencias y Logaritmos", 
                                         font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame4.pack(fill="x", padx=10, pady=8)
            
            power_frame = tk.Frame(section_frame4, bg='#ffffff')
            power_frame.pack(fill="x", padx=8, pady=8)
            
            # Potencias
            power_ops = [
                ('x²', 'x³', 'x^n'),
                ('x^(-1)', 'x^(1/2)', 'x^(1/3)')
            ]
            
            for row in power_ops:
                row_frame = tk.Frame(power_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#9b59b6', 12)
            
            # Logaritmos
            log_ops = [
                ('log(x)', 'ln(x)', 'log10(x)'),
                ('log2(x)', 'log_b(x)', 'exp(x)')
            ]
            
            for row in log_ops:
                row_frame = tk.Frame(power_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#27ae60', 12)
            
            # === SECCIÓN 5: SÍMBOLOS MATEMÁTICOS ESENCIALES ===
            section_frame5 = tk.LabelFrame(scrollable_frame, text="Símbolos Matemáticos Esenciales", 
                                         font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame5.pack(fill="x", padx=10, pady=8)
            
            symbols_frame = tk.Frame(section_frame5, bg='#ffffff')
            symbols_frame.pack(fill="x", padx=8, pady=8)
            
            # Símbolos de cálculo
            calc_symbols = [
                ('integral', 'd/dx', 'lim', 'sum', 'prod', 'infinity')
            ]
            
            for row in calc_symbols:
                row_frame = tk.Frame(symbols_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for symbol in row:
                    self.create_enhanced_keypad_button(row_frame, symbol, '#e74c3c', 10)
            
            # Símbolos lógicos y de conjuntos
            logic_symbols = [
                ('partial', 'nabla', 'Delta', 'exists', 'forall', 'in'),
                ('subset', 'superset', 'union', 'intersection', 'empty', 'element')
            ]
            
            for row in logic_symbols:
                row_frame = tk.Frame(symbols_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for symbol in row:
                    self.create_enhanced_keypad_button(row_frame, symbol, '#8e44ad', 10)
            
            # === SECCIÓN 6: CONSTANTES MATEMÁTICAS ===
            section_frame6 = tk.LabelFrame(scrollable_frame, text="Constantes Matemáticas", 
                                         font=('Segoe UI', self.font_sizes.get('subtitle', 11), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff', relief=tk.RIDGE, bd=2)
            section_frame6.pack(fill="x", padx=10, pady=(8, 10))
            
            constants_frame = tk.Frame(section_frame6, bg='#ffffff')
            constants_frame.pack(fill="x", padx=8, pady=8)
            
            constants = [
                ('pi', 'e', 'phi', 'tau'),
                ('i', 'j', 'oo', 'nan')
            ]
            
            for row in constants:
                row_frame = tk.Frame(constants_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for const in row:
                    self.create_enhanced_keypad_button(row_frame, const, '#16a085', 10)
            
            # Bind mouse wheel to canvas for smooth scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind("<MouseWheel>", _on_mousewheel)
            
        except Exception as e:
            logger.error(f"Error creating enhanced algebra tab: {str(e)}")
            raise
    
    def create_enhanced_trigonometry_tab(self):
        """Create enhanced trigonometry tab with comprehensive functions"""
        try:
            trig_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(trig_frame, text="Trigonometría")
            
            # Section: Basic Trigonometric Functions
            section_frame = tk.LabelFrame(trig_frame, text="Funciones Básicas", 
                                        font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            section_frame.pack(fill="x", padx=12, pady=8)
            
            basic_frame = tk.Frame(section_frame, bg='#ffffff')
            basic_frame.pack(fill="x", padx=8, pady=8)
            
            basic_trig = [
                ('sin', 'cos', 'tan', 'cot', 'sec', 'csc'),
                ('sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch')
            ]
            
            for row in basic_trig:
                row_frame = tk.Frame(basic_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#9b59b6', 6)
            
            # Section: Inverse Functions
            section_frame2 = tk.LabelFrame(trig_frame, text="Funciones Inversas", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame2.pack(fill="x", padx=12, pady=8)
            
            inverse_frame = tk.Frame(section_frame2, bg='#ffffff')
            inverse_frame.pack(fill="x", padx=8, pady=8)
            
            inverse_trig = [
                ('asin', 'acos', 'atan', 'acot', 'asec', 'acsc'),
                ('asinh', 'acosh', 'atanh', 'acoth', 'asech', 'acsch')
            ]
            
            for row in inverse_trig:
                row_frame = tk.Frame(inverse_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#8e44ad', 6)
            
            # Section: Advanced Trigonometric Functions
            section_frame3 = tk.LabelFrame(trig_frame, text="Funciones Avanzadas", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame3.pack(fill="x", padx=12, pady=8)
            
            advanced_frame = tk.Frame(section_frame3, bg='#ffffff')
            advanced_frame.pack(fill="x", padx=8, pady=8)
            
            advanced_trig = [
                ('sinc', 'cosc', 'tanc', 'sinhc', 'coshc', 'tanhc'),
                ('atan2', 'hypot', 'degrees', 'radians', 'phase', 'unwrap')
            ]
            
            for row in advanced_trig:
                row_frame = tk.Frame(advanced_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#e67e22', 6)
            
        except Exception as e:
            logger.error(f"Error creating enhanced trigonometry tab: {str(e)}")
            raise
    
    def create_enhanced_calculus_tab(self):
        """Create enhanced calculus tab with comprehensive mathematical functions"""
        try:
            calc_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(calc_frame, text="Cálculo")
            
            # Section: Derivatives
            section_frame = tk.LabelFrame(calc_frame, text="Derivadas", 
                                        font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            section_frame.pack(fill="x", padx=12, pady=8)
            
            deriv_frame = tk.Frame(section_frame, bg='#ffffff')
            deriv_frame.pack(fill="x", padx=8, pady=8)
            
            deriv_ops = [
                ('diff', 'D', 'Derivative', 'TotalDiff', 'jacobian', 'hessian'),
                ('grad', 'div', 'curl', 'laplacian', 'rot', 'dAlembertian')
            ]
            
            for row in deriv_ops:
                row_frame = tk.Frame(deriv_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#e67e22', 7)
            
            # Section: Integrals
            section_frame2 = tk.LabelFrame(calc_frame, text="Integrales", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame2.pack(fill="x", padx=12, pady=8)
            
            integral_frame = tk.Frame(section_frame2, bg='#ffffff')
            integral_frame.pack(fill="x", padx=8, pady=8)
            
            integral_ops = [
                ('∫', 'def_int', 'double_int', 'triple_int', 'line_int', 'surface_int'),
                ('contour_int', 'volume_int', 'path_int', 'area_int', 'arc_length', 'surface_area')
            ]
            
            for row in integral_ops:
                row_frame = tk.Frame(integral_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#e74c3c', 7)
            
            # Section: Limits and Series
            section_frame3 = tk.LabelFrame(calc_frame, text="Límites y Series", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame3.pack(fill="x", padx=12, pady=8)
            
            limit_frame = tk.Frame(section_frame3, bg='#ffffff')
            limit_frame.pack(fill="x", padx=8, pady=8)
            
            limit_ops = [
                ('limit', 'lim_inf', 'lim_sup', 'series', 'taylor', 'maclaurin'),
                ('fourier_series', 'laplace_transform', 'fourier_transform', 'zeta', 'dirichlet', 'riemann_zeta')
            ]
            
            for row in limit_ops:
                row_frame = tk.Frame(limit_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#f39c12', 7)
            
        except Exception as e:
            logger.error(f"Error creating enhanced calculus tab: {str(e)}")
            raise
    
    def create_enhanced_constants_tab(self):
        """Create enhanced constants tab with comprehensive mathematical and physical constants"""
        try:
            const_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(const_frame, text="Constantes")
            
            # Section: Mathematical Constants
            section_frame = tk.LabelFrame(const_frame, text="Constantes Matemáticas", 
                                        font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            section_frame.pack(fill="x", padx=12, pady=8)
            
            math_frame = tk.Frame(section_frame, bg='#ffffff')
            math_frame.pack(fill="x", padx=8, pady=8)
            
            math_consts = [
                ('pi', 'e', 'phi', 'tau', 'gamma', 'zeta(2)'),
                ('EulerGamma', 'Catalan', 'Glaisher', 'Khinchin', 'TwinPrime', 'ME')
            ]
            
            for row in math_consts:
                row_frame = tk.Frame(math_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for const in row:
                    self.create_enhanced_keypad_button(row_frame, const, '#27ae60', 6)
            
            # Section: Physical Constants
            section_frame2 = tk.LabelFrame(const_frame, text="Constantes Físicas", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame2.pack(fill="x", padx=12, pady=8)
            
            physics_frame = tk.Frame(section_frame2, bg='#ffffff')
            physics_frame.pack(fill="x", padx=8, pady=8)
            
            physics_consts = [
                ('c', 'h', 'G', 'k', 'NA', 'R'),
                ('mu0', 'eps0', 'alpha', 're', 'me', 'mp')
            ]
            
            for row in physics_consts:
                row_frame = tk.Frame(physics_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for const in row:
                    self.create_enhanced_keypad_button(row_frame, const, '#16a085', 6)
            
            # Section: Special Numbers and Units
            section_frame3 = tk.LabelFrame(const_frame, text="Números Especiales y Unidades", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame3.pack(fill="x", padx=12, pady=8)
            
            special_frame = tk.Frame(section_frame3, bg='#ffffff')
            special_frame.pack(fill="x", padx=8, pady=8)
            
            special_nums = [
                ('i', 'j', 'oo', 'nan', 'inf', 'E'),
                ('I', 'J', 'Infinity', 'NaN', 'Exp1', 'GoldenRatio')
            ]
            
            for row in special_nums:
                row_frame = tk.Frame(special_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for num in row:
                    self.create_enhanced_keypad_button(row_frame, num, '#34495e', 6)
            
        except Exception as e:
            logger.error(f"Error creating enhanced constants tab: {str(e)}")
            raise
    
    def create_enhanced_special_tab(self):
        """Create enhanced special functions tab with comprehensive mathematical functions"""
        try:
            special_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(special_frame, text="Especiales")
            
            # Section: Basic Functions
            section_frame = tk.LabelFrame(special_frame, text="Funciones Básicas", 
                                        font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            section_frame.pack(fill="x", padx=12, pady=8)
            
            basic_frame = tk.Frame(section_frame, bg='#ffffff')
            basic_frame.pack(fill="x", padx=8, pady=8)
            
            basic_funcs = [
                ('sqrt', 'cbrt', 'abs', 'sign', 'floor', 'ceil'),
                ('round', 'trunc', 'frac', 'real', 'imag', 'conj')
            ]
            
            for row in basic_funcs:
                row_frame = tk.Frame(basic_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#e74c3c', 6)
            
            # Section: Advanced Functions
            section_frame2 = tk.LabelFrame(special_frame, text="Funciones Avanzadas", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame2.pack(fill="x", padx=12, pady=8)
            
            adv_frame = tk.Frame(section_frame2, bg='#ffffff')
            adv_frame.pack(fill="x", padx=8, pady=8)
            
            adv_funcs = [
                ('factorial', 'gamma', 'beta', 'erf', 'erfc', 'gamma_inc'),
                ('digamma', 'polygamma', 'loggamma', 'beta_inc', 'uppergamma', 'lowergamma')
            ]
            
            for row in adv_funcs:
                row_frame = tk.Frame(adv_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#9b59b6', 6)
            
            # Section: Series and Sums
            section_frame3 = tk.LabelFrame(special_frame, text="Series y Sumatorias", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame3.pack(fill="x", padx=12, pady=8)
            
            series_frame = tk.Frame(section_frame3, bg='#ffffff')
            series_frame.pack(fill="x", padx=8, pady=8)
            
            series_funcs = [
                ('sum', 'prod', 'summation', 'product', 'zeta', 'dirichlet'),
                ('binomial', 'bernoulli', 'euler', 'fibonacci', 'lucas', 'catalan')
            ]
            
            for row in series_funcs:
                row_frame = tk.Frame(series_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#f39c12', 6)
            
        except Exception as e:
            logger.error(f"Error creating enhanced special tab: {str(e)}")
            raise
    
    def create_enhanced_matrix_tab(self):
        """Create enhanced matrix tab with comprehensive matrix operations"""
        try:
            matrix_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(matrix_frame, text="Matrices")
            
            # Section: Basic Matrix Operations
            section_frame = tk.LabelFrame(matrix_frame, text="Operaciones Básicas", 
                                        font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            section_frame.pack(fill="x", padx=12, pady=8)
            
            basic_frame = tk.Frame(section_frame, bg='#ffffff')
            basic_frame.pack(fill="x", padx=8, pady=8)
            
            basic_ops = [
                ('det', 'trace', 'rank', 'inv', 'transpose', 'adjugate'),
                ('Matrix', 'eye', 'zeros', 'ones', 'diag', 'block_diag')
            ]
            
            for row in basic_ops:
                row_frame = tk.Frame(basic_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#3498db', 6)
            
            # Section: Advanced Matrix Operations
            section_frame2 = tk.LabelFrame(matrix_frame, text="Operaciones Avanzadas", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame2.pack(fill="x", padx=12, pady=8)
            
            advanced_frame = tk.Frame(section_frame2, bg='#ffffff')
            advanced_frame.pack(fill="x", padx=8, pady=8)
            
            advanced_ops = [
                ('eigenvals', 'eigenvects', 'svd', 'qr', 'lu', 'cholesky'),
                ('norm', 'cond', 'rcond', 'pinv', 'hilbert', 'vandermonde')
            ]
            
            for row in advanced_ops:
                row_frame = tk.Frame(advanced_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for op in row:
                    self.create_enhanced_keypad_button(row_frame, op, '#9b59b6', 6)
            
            # Section: Matrix Functions
            section_frame3 = tk.LabelFrame(matrix_frame, text="Funciones Matriciales", 
                                         font=('Segoe UI', self.font_sizes.get('normal', 10), 'bold'), 
                                         fg='#2c3e50', bg='#ffffff')
            section_frame3.pack(fill="x", padx=12, pady=8)
            
            func_frame = tk.Frame(section_frame3, bg='#ffffff')
            func_frame.pack(fill="x", padx=8, pady=8)
            
            matrix_funcs = [
                ('expm', 'logm', 'sqrtm', 'sinm', 'cosm', 'tanm'),
                ('sinhm', 'coshm', 'tanhm', 'funm', 'expm_multiply', 'matrix_power')
            ]
            
            for row in matrix_funcs:
                row_frame = tk.Frame(func_frame, bg='#ffffff')
                row_frame.pack(fill="x", pady=2)
                
                for func in row:
                    self.create_enhanced_keypad_button(row_frame, func, '#e67e22', 6)
            
        except Exception as e:
            logger.error(f"Error creating enhanced matrix tab: {str(e)}")
            raise
    
    def create_templates_tab(self):
        """Create templates tab with mathematical function repository"""
        try:
            templates_frame = tk.Frame(self.tab_notebook, bg='#ffffff')
            self.tab_notebook.add(templates_frame, text="Plantillas")
            
            # Initialize template browser
            self.template_browser = TemplateBrowser(templates_frame, self.insert_template_expression, self.template_manager)
            self.template_browser.pack(fill="both", expand=True, padx=5, pady=5)
            
        except Exception as e:
            logger.error(f"Error creating templates tab: {str(e)}")
            raise
    
    def insert_template_expression(self, template_expression: str):
        """Insert template expression into the input field"""
        try:
            # Get current cursor position
            current_text = self.input_text.get()
            cursor_pos = self.input_text.index(tk.INSERT)
            
            # Insert template at cursor position
            self.input_text.insert(cursor_pos, template_expression)
            
            # Set focus back to input
            self.input_text.focus_set()
            
            # Update cursor position after insertion
            new_cursor_pos = cursor_pos + len(template_expression)
            self.input_text.mark_set(tk.INSERT, new_cursor_pos)
            
            logger.info(f"Template expression inserted: {template_expression}")
            
        except Exception as e:
            logger.error(f"Error inserting template expression: {str(e)}")
            messagebox.showerror("Error", f"No se pudo insertar la plantilla: {str(e)}")
    
    def create_enhanced_keypad_button(self, parent, text, color, width):
        """Create enhanced keypad button optimized for symbol visibility"""
        try:
            # Optimized button styling for better symbol visibility
            btn = tk.Button(parent, text=text, 
                          font=('Segoe UI', self.font_sizes.get('subtitle', 10), 'bold'),  # Optimized font size
                          bg=color, fg='white',
                          width=max(width, 7), height=2,  # Balanced dimensions
                          relief=tk.RAISED, bd=2,  # Professional border depth
                          cursor='hand2',
                          command=lambda: self.insert_symbol(text))
            btn.pack(side="left", padx=1, pady=1)  # Optimized padding
            
            # Enhanced hover effects with color transitions
            btn.bind('<Enter>', lambda e: self.animate_enhanced_button_hover(btn, color))
            btn.bind('<Leave>', lambda e: self.animate_enhanced_button_leave(btn, color))
            
            # Press effect
            btn.bind('<ButtonPress-1>', lambda e: self.animate_button_press(btn, color))
            btn.bind('<ButtonRelease-1>', lambda e: self.animate_button_release(btn, color))
            
            # Enhanced tooltip with better styling
            self.add_enhanced_tooltip(btn, self.get_symbol_description(text))
            
            return btn
            
        except Exception as e:
            logger.error(f"Error creating enhanced keypad button: {str(e)}")
            return None
    
    def animate_enhanced_button_hover(self, btn, color):
        """Enhanced hover animation with smooth color transition"""
        try:
            lighter_color = self.lighten_color(color)
            btn.config(bg=lighter_color, relief=tk.RIDGE, bd=3, cursor='hand2')
            # Add subtle scale effect
            btn.config(font=('Segoe UI', self.font_sizes.get('button', 9) + 1, 'bold'))
        except:
            pass
    
    def animate_enhanced_button_leave(self, btn, color):
        """Enhanced leave animation"""
        try:
            btn.config(bg=color, relief=tk.RAISED, bd=2, cursor='hand2')
            # Reset font size
            btn.config(font=('Segoe UI', self.font_sizes.get('button', 9), 'bold'))
        except:
            pass
    
    def animate_button_press(self, btn, color):
        """Button press animation"""
        try:
            darker_color = self.darken_color(color)
            btn.config(bg=darker_color, relief=tk.SUNKEN, bd=1)
        except:
            pass
    
    def animate_button_release(self, btn, color):
        """Button release animation"""
        try:
            btn.config(bg=color, relief=tk.RAISED, bd=2)
        except:
            pass
    
    def add_enhanced_tooltip(self, widget, text):
        """Add enhanced tooltip with better styling"""
        try:
            def on_enter(event):
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                
                # Enhanced tooltip styling
                label = tk.Label(tooltip, text=text, 
                                font=('Segoe UI', self.font_sizes.get('small', 9)),
                                bg='#2c3e50', fg='white',
                                relief=tk.RAISED, bd=1,
                                padx=8, pady=4)
                label.pack()
                
                widget.tooltip = tooltip
            
            def on_leave(event):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
                    del widget.tooltip
            
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            
        except Exception as e:
            logger.error(f"Error adding enhanced tooltip: {str(e)}")
    
    def create_button_grid(self, parent, buttons, color, columns):
        """Create a grid of buttons (legacy method for compatibility)"""
        try:
            for i, button_text in enumerate(buttons):
                row = i // columns
                col = i % columns
                
                if col == 0:
                    row_frame = tk.Frame(parent, bg='#ffffff')
                    row_frame.pack(fill="x", pady=2)
                
                self.create_keypad_button(row_frame, button_text, color, 10)
                
        except Exception as e:
            logger.error(f"Error creating button grid: {str(e)}")
            raise
    
    def setup_professional_results_section(self):
        """Setup professional results section"""
        try:
            # Header
            header = tk.Frame(self.results_frame, bg='#27ae60', height=40)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="RESULTADOS", 
                    font=('Segoe UI', 12, 'bold'), 
                    fg='white', bg='#27ae60').pack(pady=10)
            
            # Results display
            self.results_display = tk.Frame(self.results_frame, bg='#ffffff')
            self.results_display.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create notebook for tabs
            self.results_notebook = ttk.Notebook(self.results_display)
            self.results_notebook.pack(fill="both", expand=True)
            
            # Result tab
            result_tab = tk.Frame(self.results_notebook, bg='#ffffff')
            self.results_notebook.add(result_tab, text="Resultado")
            
            self.result_text = tk.Text(result_tab, 
                                     font=('Courier', 11), 
                                     bg='#f8f9fa', fg='#2c3e50',
                                     relief=tk.RIDGE, bd=1,
                                     padx=10, pady=10,
                                     wrap=tk.WORD,
                                     state='disabled')
            self.result_text.pack(fill="both", expand=True)
            
            # Steps tab
            steps_tab = tk.Frame(self.results_notebook, bg='#ffffff')
            self.results_notebook.add(steps_tab, text="Pasos")
            
            self.steps_text = tk.Text(steps_tab, 
                                    font=('Courier', 10), 
                                    bg='#f8f9fa', fg='#2c3e50',
                                    relief=tk.RIDGE, bd=1,
                                    padx=10, pady=10,
                                    wrap=tk.WORD,
                                    state='disabled')
            self.steps_text.pack(fill="both", expand=True)
            
            # Verification tab
            verify_tab = tk.Frame(self.results_notebook, bg='#ffffff')
            self.results_notebook.add(verify_tab, text="Verificación")
            
            self.verify_text = tk.Text(verify_tab, 
                                     font=('Courier', 10), 
                                     bg='#f8f9fa', fg='#2c3e50',
                                     relief=tk.RIDGE, bd=1,
                                     padx=10, pady=10,
                                     wrap=tk.WORD,
                                     state='disabled')
            self.verify_text.pack(fill="both", expand=True)
            
        except Exception as e:
            logger.error(f"Error setting up professional results section: {str(e)}")
            raise
    
    def setup_professional_graph_section(self):
        """Setup professional graph section with interactive features"""
        try:
            # Header
            header = tk.Frame(self.graph_frame, bg='#3498db', height=40)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="VISUALIZACIÓN GRÁFICA", 
                    font=('Segoe UI', 12, 'bold'), 
                    fg='white', bg='#3498db').pack(pady=10)
            
            # Graph controls
            controls_frame = tk.Frame(self.graph_frame, bg='#ffffff')
            controls_frame.pack(fill="x", padx=10, pady=5)
            
            # Left controls
            left_controls = tk.Frame(controls_frame, bg='#ffffff')
            left_controls.pack(side="left")
            
            self.create_professional_button(left_controls, "Graficar", self.plot_function, '#27ae60')
            self.create_professional_button(left_controls, "Limpiar", self.clear_graph, '#e74c3c')
            self.create_professional_button(left_controls, "Zoom In", self.zoom_in, '#3498db')
            self.create_professional_button(left_controls, "Zoom Out", self.zoom_out, '#3498db')
            self.create_professional_button(left_controls, "Reset", self.reset_graph, '#95a5a6')
            
            # Center controls
            center_controls = tk.Frame(controls_frame, bg='#ffffff')
            center_controls.pack(side="left", expand=True, fill="x", padx=20)
            
            tk.Label(center_controls, text="Rango X:", 
                    font=('Segoe UI', 9, 'bold'), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=(0, 5))
            
            self.x_min_entry = tk.Entry(center_controls, width=8, 
                                       font=('Courier', 9), 
                                       bg='#f8f9fa', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=1)
            self.x_min_entry.pack(side="left", padx=2)
            self.x_min_entry.insert(0, "-10")
            
            tk.Label(center_controls, text="a", 
                    font=('Segoe UI', 9), 
                    fg='#2c3e50', bg='#ffffff').pack(side="left", padx=2)
            
            self.x_max_entry = tk.Entry(center_controls, width=8, 
                                       font=('Courier', 9), 
                                       bg='#f8f9fa', fg='#2c3e50',
                                       relief=tk.RIDGE, bd=1)
            self.x_max_entry.pack(side="left", padx=2)
            self.x_max_entry.insert(0, "10")
            
            # Options
            self.show_grid_var = tk.BooleanVar(value=True)
            grid_check = tk.Checkbutton(center_controls, text="Grid", 
                                       variable=self.show_grid_var,
                                       command=self.update_graph_display,
                                       font=('Segoe UI', 9),
                                       fg='#2c3e50', bg='#ffffff',
                                       selectcolor='#3498db')
            grid_check.pack(side="left", padx=10)
            
            self.show_legend_var = tk.BooleanVar(value=True)
            legend_check = tk.Checkbutton(center_controls, text="Leyenda", 
                                         variable=self.show_legend_var,
                                         command=self.update_graph_display,
                                         font=('Segoe UI', 9),
                                         fg='#2c3e50', bg='#ffffff',
                                         selectcolor='#3498db')
            legend_check.pack(side="left", padx=5)
            
            # Right controls
            right_controls = tk.Frame(controls_frame, bg='#ffffff')
            right_controls.pack(side="right")
            
            self.create_professional_button(right_controls, "Exportar", self.export_graph, '#9b59b6')
            self.create_professional_button(right_controls, "Pantalla Completa", self.fullscreen_graph, '#e67e22')
            
            # Graph display
            self.graph_display = tk.Frame(self.graph_frame, bg='#ffffff')
            self.graph_display.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Create matplotlib figure
            self.setup_matplotlib_graph()
            
        except Exception as e:
            logger.error(f"Error setting up professional graph section: {str(e)}")
            raise
    
    def setup_matplotlib_graph(self):
        """Setup matplotlib graph with interactive features"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            from matplotlib.figure import Figure
            
            # Create figure
            self.fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
            self.ax = self.fig.add_subplot(111)
            
            # Setup initial plot
            self.setup_initial_plot()
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_display)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Add navigation toolbar
            toolbar_frame = tk.Frame(self.graph_display, bg='#ffffff')
            toolbar_frame.pack(fill="x")
            
            self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            self.toolbar.update()
            
            # Bind mouse events
            self.canvas.mpl_connect('scroll_event', self.on_scroll)
            self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
            self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
            self.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)
            
        except Exception as e:
            logger.error(f"Error setting up matplotlib graph: {str(e)}")
            raise
    
    def setup_initial_plot(self):
        """Setup initial plot"""
        try:
            self.ax.clear()
            self.ax.set_facecolor('#f8f9fa')
            self.ax.grid(True, alpha=0.3, color='#bdc3c7')
            self.ax.set_xlabel('x', fontsize=12, color='#2c3e50')
            self.ax.set_ylabel('f(x)', fontsize=12, color='#2c3e50')
            self.ax.set_title('Gráfica Lista', fontsize=14, fontweight='bold', color='#2c3e50')
            
            # Modern styling
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#2c3e50')
            self.ax.spines['bottom'].set_color('#2c3e50')
            
        except Exception as e:
            logger.error(f"Error setting up initial plot: {str(e)}")
    
    def create_professional_status_bar(self):
        """Create professional status bar"""
        try:
            status_bar = tk.Frame(self.main_container, bg='#34495e', height=25)
            status_bar.pack(fill="x", side="bottom")
            status_bar.pack_propagate(False)
            
            # Status message
            self.status_label = tk.Label(status_bar, text=" Listo para calcular", 
                                      font=('Segoe UI', 9), 
                                      fg='#ecf0f1', bg='#34495e')
            self.status_label.pack(side="left", padx=10, pady=2)
            
            # Separator
            separator = tk.Frame(status_bar, bg='#2c3e50', width=1, height=20)
            separator.pack(side="left", padx=5, fill="y", pady=2)
            
            # Calculation counter
            self.calc_counter = tk.Label(status_bar, text="Cálculos: 0", 
                                      font=('Segoe UI', 9), 
                                      fg='#ecf0f1', bg='#34495e')
            self.calc_counter.pack(side="left", padx=10, pady=2)
            
            # Memory usage
            self.memory_label = tk.Label(status_bar, text="Memoria: 0MB", 
                                       font=('Segoe UI', 9), 
                                       fg='#ecf0f1', bg='#34495e')
            self.memory_label.pack(side="left", padx=10, pady=2)
            
            # Clock
            self.clock_label = tk.Label(status_bar, text="", 
                                     font=('Segoe UI', 9), 
                                     fg='#ecf0f1', bg='#34495e')
            self.clock_label.pack(side="right", padx=10, pady=2)
            
            # Update clock
            self.update_clock()
            
        except Exception as e:
            logger.error(f"Error creating professional status bar: {str(e)}")
            raise
    
    def create_professional_button(self, parent, text, command, color):
        """Create professional styled button with scaled fonts"""
        try:
            btn = tk.Button(parent, text=text, command=command,
                          font=('Segoe UI', self.font_sizes.get('button', 9), 'bold'),
                          bg=color, fg='white',
                          padx=10, pady=4,
                          relief=tk.RAISED, bd=1,
                          cursor='hand2',
                          activebackground=self.darken_color(color),
                          activeforeground='white')
            btn.pack(side="left", padx=2)
            
            # Add hover effects
            btn.bind('<Enter>', lambda e: self.animate_button_hover(btn, color))
            btn.bind('<Leave>', lambda e: self.animate_button_leave(btn, color))
            
            return btn
            
        except Exception as e:
            logger.error(f"Error creating professional button: {str(e)}")
            return None
    
    def create_keypad_button(self, parent, text, color, width):
        """Create professional keypad button with scaled fonts"""
        try:
            btn = tk.Button(parent, text=text, 
                          font=('Segoe UI', self.font_sizes.get('button', 9), 'bold'),
                          bg=color, fg='white',
                          width=width, height=2,
                          relief=tk.RAISED, bd=1,
                          cursor='hand2',
                          command=lambda: self.insert_symbol(text))
            btn.pack(side="left", padx=1, pady=1)
            
            # Add hover effects
            btn.bind('<Enter>', lambda e: self.animate_button_hover(btn, color))
            btn.bind('<Leave>', lambda e: self.animate_button_leave(btn, color))
            
            # Add tooltip
            self.add_tooltip(btn, self.get_symbol_description(text))
            
            return btn
            
        except Exception as e:
            logger.error(f"Error creating keypad button: {str(e)}")
            return None
    
    def get_symbol_description(self, symbol):
        """Get description for symbol tooltip"""
        descriptions = {
            'sin': 'Seno',
            'cos': 'Coseno', 
            'tan': 'Tangente',
            'pi': 'Número pi (3.14159...)',
            'e': 'Número de Euler (2.71828...)',
            'int': 'Integral indefinida',
            'def_int': 'Integral definida',
            'sqrt': 'Raíz cuadrada',
            'sum': 'Sumatoria',
            'diff': 'Derivada',
            'limit': 'Límite',
            'oo': 'Infinito',
            'i': 'Unidad imaginaria'
        }
        return descriptions.get(symbol, symbol)
    
    def add_tooltip(self, widget, text):
        """Add tooltip to widget"""
        try:
            def on_enter(event):
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                
                label = tk.Label(tooltip, text=text, 
                                font=('Segoe UI', 9),
                                bg='#2c3e50', fg='white',
                                relief=tk.RAISED, bd=1,
                                padx=5, pady=2)
                label.pack()
                
                widget.tooltip = tooltip
            
            def on_leave(event):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
                    del widget.tooltip
            
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            
        except Exception as e:
            logger.error(f"Error adding tooltip: {str(e)}")
    
    def animate_button_hover(self, btn, color):
        """Animate button on hover"""
        try:
            lighter_color = self.lighten_color(color)
            btn.config(bg=lighter_color, relief=tk.RIDGE, bd=2)
        except:
            pass
    
    def animate_button_leave(self, btn, color):
        """Animate button when leaving hover"""
        try:
            btn.config(bg=color, relief=tk.RAISED, bd=1)
        except:
            pass
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
            return '#%02x%02x%02x' % lighter
        except:
            return color
    
    def darken_color(self, color):
        """Darken a hex color"""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darker = tuple(max(0, int(c * 0.8)) for c in rgb)
            return '#%02x%02x%02x' % darker
        except:
            return color
    
    def setup_screen_management(self):
        """Setup automatic screen adjustment based on display resolution"""
        try:
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Calculate optimal window size based on screen resolution
            optimal_width, optimal_height = self.calculate_optimal_size(screen_width, screen_height)
            
            # Set window geometry
            self.root.geometry(f"{optimal_width}x{optimal_height}")
            
            # Set minimum size based on screen resolution
            min_width = max(1200, int(screen_width * 0.6))
            min_height = max(800, int(screen_height * 0.7))
            self.root.minsize(min_width, min_height)
            
            # Store screen info for responsive adjustments
            self.screen_info = {
                'width': screen_width,
                'height': screen_height,
                'window_width': optimal_width,
                'window_height': optimal_height,
                'scale_factor': min(optimal_width / 1920, optimal_height / 1080)
            }
            
            # Setup DPI scaling if available
            self.setup_dpi_scaling()
            
            # Setup responsive font scaling
            self.setup_font_scaling()
            
            logger.info(f"Screen setup: {screen_width}x{screen_height} -> Window: {optimal_width}x{optimal_height}")
            
        except Exception as e:
            logger.error(f"Error setting up screen management: {str(e)}")
            # Fallback to default size
            self.root.geometry("1600x900")
            self.root.minsize(1200, 800)
    
    def calculate_optimal_size(self, screen_width, screen_height):
        """Calculate optimal window size based on screen resolution"""
        try:
            # Define screen categories and optimal sizes
            if screen_width >= 3840:  # 4K displays
                return (3200, 1800)  # 16:9 aspect ratio
            elif screen_width >= 2560:  # QHD/WQHD displays
                return (2400, 1350)  # 16:9 aspect ratio
            elif screen_width >= 1920:  # Full HD displays
                return (1800, 1012)  # 16:9 aspect ratio
            elif screen_width >= 1600:  # HD+ displays
                return (1500, 844)   # 16:9 aspect ratio
            elif screen_width >= 1366:  # Standard HD displays
                return (1280, 720)   # 16:9 aspect ratio
            else:  # Smaller displays
                return (int(screen_width * 0.9), int(screen_height * 0.9))
                
        except Exception as e:
            logger.error(f"Error calculating optimal size: {str(e)}")
            return (1600, 900)  # Fallback
    
    def setup_dpi_scaling(self):
        """Setup DPI scaling for high-DPI displays"""
        try:
            # Check if DPI scaling is available
            if hasattr(self.root, 'tk') and hasattr(self.root.tk, 'call'):
                try:
                    # Get DPI scaling factor
                    dpi = self.root.tk.call('tk', 'scaling')
                    if dpi and dpi != '1.0':
                        # Apply DPI scaling to fonts
                        self.dpi_scale = float(dpi)
                        logger.info(f"DPI scaling factor: {self.dpi_scale}")
                    else:
                        self.dpi_scale = 1.0
                except:
                    self.dpi_scale = 1.0
            else:
                self.dpi_scale = 1.0
                
        except Exception as e:
            logger.error(f"Error setting up DPI scaling: {str(e)}")
            self.dpi_scale = 1.0
    
    def setup_font_scaling(self):
        """Setup font scaling based on screen size"""
        try:
            # Calculate font scale based on screen resolution
            base_resolution = 1920  # Base resolution for font scaling
            font_scale = self.screen_info['width'] / base_resolution
            
            # Limit font scale to reasonable range
            self.font_scale = max(0.8, min(1.5, font_scale))
            
            # Define font sizes based on scale
            self.font_sizes = {
                'title': int(14 * self.font_scale * self.dpi_scale),
                'subtitle': int(12 * self.font_scale * self.dpi_scale),
                'normal': int(10 * self.font_scale * self.dpi_scale),
                'small': int(9 * self.font_scale * self.dpi_scale),
                'editor': int(12 * self.font_scale * self.dpi_scale),
                'button': int(10 * self.font_scale * self.dpi_scale)
            }
            
            logger.info(f"Font scaling: {self.font_scale:.2f}x, DPI: {self.dpi_scale:.2f}x")
            
        except Exception as e:
            logger.error(f"Error setting up font scaling: {str(e)}")
            # Fallback font sizes
            self.font_sizes = {
                'title': 14, 'subtitle': 12, 'normal': 10, 
                'small': 9, 'editor': 12, 'button': 10
            }
    
    def center_window(self):
        """Center window on screen"""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
        except Exception as e:
            logger.error(f"Error centering window: {str(e)}")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        try:
            current_state = self.root.attributes('-fullscreen')
            self.root.attributes('-fullscreen', not current_state)
            
            if not current_state:
                self.update_status("Modo pantalla completa", '#9b59b6')
            else:
                self.update_status("Modo ventana normal", '#3498db')
                
        except Exception as e:
            logger.error(f"Error toggling fullscreen: {str(e)}")
    
    def adjust_window_size(self, scale_factor):
        """Adjust window size by scale factor"""
        try:
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            new_width = int(current_width * scale_factor)
            new_height = int(current_height * scale_factor)
            
            # Ensure minimum size
            new_width = max(self.root.winfo_minsize()[0], new_width)
            new_height = max(self.root.winfo_minsize()[1], new_height)
            
            # Ensure maximum size (fit screen)
            max_width = self.root.winfo_screenwidth() - 50
            max_height = self.root.winfo_screenheight() - 50
            new_width = min(max_width, new_width)
            new_height = min(max_height, new_height)
            
            self.root.geometry(f"{new_width}x{new_height}")
            self.update_status(f"Tamaño ajustado: {new_width}x{new_height}", '#3498db')
            
        except Exception as e:
            logger.error(f"Error adjusting window size: {str(e)}")
    
    def maximize_window(self):
        """Maximize window to fit screen"""
        try:
            self.root.state('zoomed')
            self.update_status("Ventana maximizada", '#27ae60')
        except Exception as e:
            logger.error(f"Error maximizing window: {str(e)}")
    
    def restore_window(self):
        """Restore window to normal size"""
        try:
            self.root.state('normal')
            self.update_status("Ventana restaurada", '#f39c12')
        except Exception as e:
            logger.error(f"Error restoring window: {str(e)}")
    
    def update_clock(self):
        """Update clock display"""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.clock_label.config(text=current_time)
            self.root.after(1000, self.update_clock)
        except:
            pass
    
    def calculate_integral(self):
        """Calculate integral with professional feedback"""
        try:
            if self.is_calculating:
                return
            
            # Get function from editor
            function_text = self.editor_text.get("1.0", tk.END).strip()
            if not function_text:
                messagebox.showwarning("Advertencia", "Por favor ingresa una función")
                return
            
            # Update UI state
            self.is_calculating = True
            self.update_status("Calculando integral...", '#e74c3c')
            self.calculate_btn.config(text="Calculando...", state="disabled")
            
            # Parse function using Microsoft Math Engine first
            try:
                parsed_func = self.math_engine.parse_natural_math(function_text)
                self.update_status("Función parseada con Microsoft Math Engine", '#27ae60')
            except Exception as e:
                logger.info(f"Microsoft Math Engine parsing failed: {str(e)}, falling back to regular parser")
                try:
                    parsed_func = self.parser.parse(function_text)
                    self.update_status("Función parseada con parser estándar", '#f39c12')
                except Exception as e2:
                    messagebox.showerror("Error de Parseo", 
                                       f"No se pudo parsear la función '{function_text}':\n\n"
                                       f"Microsoft Math Engine: {str(e)}\n"
                                       f"Parser estándar: {str(e2)}")
                    self.update_status("Error de parseo", '#e74c3c')
                    self.is_calculating = False
                    self.calculate_btn.config(text="CALCULAR INTEGRAL", state="normal")
                    return
            
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
            
            # Get limits for definite integral
            limits = None
            if self.definite_var.get():
                try:
                    lower = sp.sympify(self.lower_limit.get())
                    upper = sp.sympify(self.upper_limit.get())
                    limits = (lower, upper)
                except Exception as e:
                    messagebox.showwarning("Advertencia", "Límites inválidos")
                    return
            
            # Calculate integral in thread
            thread = threading.Thread(target=self._calculate_integral_thread, 
                                    args=(parsed_func, var_symbol, method, limits))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            logger.error(f"Error calculating integral: {str(e)}")
            messagebox.showerror("Error", f"No se pudo calcular la integral: {str(e)}")
            self.update_status("Error en cálculo", '#e74c3c')
            self.is_calculating = False
            self.calculate_btn.config(text="CALCULAR INTEGRAL", state="normal")
    
    def _calculate_integral_thread(self, parsed_func, var_symbol, method, limits):
        """Thread for integral calculation"""
        try:
            # Calculate integral
            result = self.integrator.integrate(parsed_func, var_symbol, method, limits)
            
            # Update UI in main thread
            self.root.after(0, lambda: self._display_calculation_result(result, parsed_func, limits))
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in calculation thread: {error_msg}")
            self.root.after(0, lambda: self._display_calculation_error(error_msg))
        finally:
            self.root.after(0, self._finish_calculation)
    
    def _display_calculation_result(self, result, parsed_func, limits):
        """Display calculation result with LaTeX rendering"""
        try:
            self.current_result = result
            
            # Clear previous LaTeX data
            self._clear_latex_data()
            
            # Update result tab with LaTeX rendering
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            
            # Create LaTeX-formatted result
            result_text = "Resultado de la Integral\n"
            result_text += "=" * 50 + "\n\n"
            
            # Render the mathematical result using visual LaTeX format
            if hasattr(result, 'result') and result.result is not None:
                try:
                    # Create visual LaTeX rendering with matplotlib
                    academic_result = self.latex_renderer.convert_to_academic_format(
                        result.original_func, result.result, result.variable
                    )
                    
                    # Add placeholder for visual LaTeX (will be rendered as image)
                    result_text += "[LaTeX Mathematical Expression]\n"
                    result_text += f"Expression: {academic_result}\n\n"
                    
                    # Store for visual rendering
                    self.current_latex_expression = academic_result
                    
                    # Trigger visual rendering after text is set
                    self.root.after(100, lambda: self._render_visual_latex_result())
                    
                except Exception as e:
                    logger.error(f"Visual LaTeX rendering failed: {str(e)}")
                    # Fallback to text format if visual rendering fails
                    try:
                        latex_result = self.latex_renderer.convert_to_text_format(result.result)
                        result_text += f"{latex_result}\n\n"
                    except:
                        result_text += f"{result.result}\n\n"
            
            # Add method and variable information
            result_text += "Información del Cálculo:\n"
            result_text += "-" * 30 + "\n"
            result_text += f"Método: {result.method.value}\n"
            result_text += f"Variable: {result.variable}\n"
            
            if limits:
                result_text += f"Límites: {limits[0]} a {limits[1]}\n"
                definite_result = result.get_definite_result()
                if definite_result is not None:
                    result_text += f"Valor definido: {definite_result}\n"
            
            result_text += f"Función original: {result.original_func}\n"
            
            self.result_text.insert("1.0", result_text)
            self.result_text.config(state='disabled')
            
            # Update steps tab with LaTeX rendering if available
            if hasattr(result, 'steps') and result.steps:
                self.steps_text.config(state='normal')
                self.steps_text.delete("1.0", tk.END)
                
                steps_text = "Pasos del Cálculo\n"
                steps_text += "=" * 50 + "\n\n"
                
                for i, step in enumerate(result.steps, 1):
                    try:
                        # Debug: mostrar información del paso
                        logger.info(f"Processing step {i}: {type(step)} - {step}")
                        
                        # Acceder al contenido del paso (step es un diccionario)
                        if isinstance(step, dict):
                            # Obtener contenido LaTeX del paso
                            latex_content = step.get('latex', step.get('content', ''))
                            logger.info(f"Step {i} latex_content: {latex_content}")
                            
                            if latex_content and ('\\int' in latex_content or '\\frac' in latex_content or '\\sqrt' in latex_content or 'x' in latex_content):
                                # Agregar placeholder para el paso
                                steps_text += f"[Paso {i} - Operación Matemática]\n"
                                
                                # Store step for visual rendering
                                if not hasattr(self, 'latex_steps'):
                                    self.latex_steps = {}
                                self.latex_steps[f"step_{i}"] = latex_content
                                
                                # Trigger visual rendering after text is set
                                self.root.after(100 + (i * 50), lambda step_idx=i: self._render_visual_latex_step(step_idx))
                            else:
                                # Si no es LaTeX matemático, mostrar el contenido como texto
                                step_content = step.get('content', latex_content or str(step))
                                if step_content and step_content != '':
                                    steps_text += f"{step_content}\n\n"
                        else:
                            # Si step no es diccionario, mostrar como texto
                            step_str = str(step)
                            if step_str and step_str != '':
                                steps_text += f"{step_str}\n\n"
                        
                    except Exception as e:
                        # Si hay error, mostrar el paso como texto fallback
                        logger.error(f"Error rendering step {i}: {str(e)}")
                        steps_text += f"[Step {i} - Error en renderizado]\n\n"
                
                self.steps_text.insert("1.0", steps_text)
                self.steps_text.config(state='disabled')
            
            # Update verification tab with LaTeX rendering
            self._display_verification_result(result)
            
            # Update status
            self.update_status("Cálculo completado", '#27ae60')
            
            # Increment calculation counter
            self.increment_calc_counter()
            
            # Add to history
            self.history_manager.add_entry(self.current_function, self.integral_type_var.get())
            
            # Auto-plot function
            self.plot_function()
            
        except Exception as e:
            logger.error(f"Error displaying calculation result: {str(e)}")
            messagebox.showerror("Error", f"No se pudo mostrar el resultado: {str(e)}")
            self.update_status("Error al mostrar resultado", '#e74c3c')
    
    def _display_verification_result(self, result):
        """Display verification result with LaTeX rendering"""
        try:
            self.verify_text.config(state='normal')
            self.verify_text.delete("1.0", tk.END)
            
            verify_text = "Verificación del Resultado\n"
            verify_text += "=" * 50 + "\n\n"
            
            # Step 1: Show original function
            verify_text += "Paso 1: Función Original\n"
            verify_text += "-" * 30 + "\n"
            try:
                latex_original = self.latex_renderer.convert_to_text_format(result.original_func)
                verify_text += f"f(x) = {latex_original}\n\n"
            except:
                verify_text += f"f(x) = {result.original_func}\n\n"
            
            # Step 2: Show integral result in academic format
            verify_text += "Paso 2: Resultado de la Integral\n"
            verify_text += "-" * 30 + "\n"
            try:
                # Use academic format for the integral result
                academic_result = self.latex_renderer.convert_to_academic_format(
                    result.original_func, result.result, result.variable
                )
                verify_text += f"{academic_result}\n\n"
            except:
                try:
                    latex_result = self.latex_renderer.convert_to_text_format(result.result)
                    verify_text += f"F(x) = {latex_result}\n\n"
                except:
                    verify_text += f"F(x) = {result.result}\n\n"
            
            # Step 3: Show derivative verification
            verify_text += "Paso 3: Verificación por Derivación\n"
            verify_text += "-" * 30 + "\n"
            try:
                import sympy as sp
                # Calculate derivative of the result
                derivative = sp.diff(result.result, sp.Symbol(result.variable))
                
                # Show derivative with LaTeX in text format
                latex_derivative = self.latex_renderer.convert_to_text_format(derivative)
                verify_text += f"F'(x) = {latex_derivative}\n\n"
                
                # Compare with original function using academic format
                verify_text += "Paso 4: Comparación Académica\n"
                verify_text += "-" * 30 + "\n"
                
                # Show academic format comparison
                try:
                    academic_comparison = f"[{latex_derivative} = {self.latex_renderer.convert_to_text_format(result.original_func)}]"
                    verify_text += f"Verificación: {academic_comparison}\n\n"
                except:
                    verify_text += "Función original: "
                    try:
                        latex_original_comp = self.latex_renderer.convert_to_text_format(result.original_func)
                        verify_text += f"{latex_original_comp}\n"
                    except:
                        verify_text += f"{result.original_func}\n"
                    
                    verify_text += "Derivada del resultado: "
                    try:
                        latex_derivative_comp = self.latex_renderer.convert_to_text_format(derivative)
                        verify_text += f"{latex_derivative_comp}\n\n"
                    except:
                        verify_text += f"{derivative}\n\n"
                
                # Verification result
                verify_text += "Paso 5: Resultado de Verificación\n"
                verify_text += "-" * 30 + "\n"
                
                if sp.simplify(derivative - result.original_func) == 0:
                    verify_text += "¡VERIFICACIÓN EXITOSA! \n"
                    verify_text += "La derivada del resultado coincide exactamente con la función original.\n"
                    verify_text += "El cálculo de la integral es CORRECTO.\n"
                else:
                    simplified_diff = sp.simplify(derivative - result.original_func)
                    if simplified_diff == 0:
                        verify_text += "¡VERIFICACIÓN EXITOSA! \n"
                        verify_text += "La derivada coincide con la función original (después de simplificación).\n"
                        verify_text += "El cálculo de la integral es CORRECTO.\n"
                    else:
                        verify_text += "ADVERTENCIA: \n"
                        verify_text += f"Diferencia detectada: {simplified_diff}\n"
                        verify_text += "La verificación no es exacta (puede ser por constantes de integración o simplificación).\n"
                
            except Exception as e:
                verify_text += f"Error en verificación: {str(e)}\n"
                verify_text += "No se pudo completar la verificación automática.\n"
            
            # Additional verification info
            verify_text += "\n" + "=" * 50 + "\n"
            verify_text += "Información Adicional:\n"
            verify_text += f"Método utilizado: {result.method.value}\n"
            verify_text += f"Variable de integración: {result.variable}\n"
            
            if hasattr(result, 'limits') and result.limits:
                verify_text += f"Tipo: Integral definida\n"
                verify_text += f"Límites: {result.limits[0]} a {result.limits[1]}\n"
            else:
                verify_text += f"Tipo: Integral indefinida\n"
            
            self.verify_text.insert("1.0", verify_text)
            self.verify_text.config(state='disabled')
            
        except Exception as e:
            logger.error(f"Error displaying verification result: {str(e)}")
            # Fallback error message
            self.verify_text.config(state='normal')
            self.verify_text.delete("1.0", tk.END)
            self.verify_text.insert("1.0", f"Error en verificación:\n\n{str(e)}")
            self.verify_text.config(state='disabled')
    
    def _clear_latex_data(self):
        """Clear previous LaTeX data and canvases"""
        try:
            # Clear LaTeX expressions
            if hasattr(self, 'current_latex_expression'):
                delattr(self, 'current_latex_expression')
            
            if hasattr(self, 'latex_steps'):
                delattr(self, 'latex_steps')
            
            # Clear canvases
            if hasattr(self, 'latex_canvas'):
                try:
                    self.latex_canvas.get_tk_widget().destroy()
                except:
                    pass
                delattr(self, 'latex_canvas')
            
            if hasattr(self, 'latex_step_canvases'):
                for canvas_key, canvas in self.latex_step_canvases.items():
                    try:
                        canvas.get_tk_widget().destroy()
                    except:
                        pass
                delattr(self, 'latex_step_canvases')
                
        except Exception as e:
            logger.error(f"Error clearing LaTeX data: {str(e)}")
    
    def _render_visual_latex_result(self):
        """Render LaTeX expression as visual image using matplotlib"""
        try:
            if hasattr(self, 'current_latex_expression'):
                # Create matplotlib figure for LaTeX rendering
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                
                # Create figure with LaTeX rendering - much smaller and centered
                fig, ax = plt.subplots(figsize=(6, 1.5))
                ax.set_facecolor('white')
                fig.patch.set_facecolor('white')
                
                # Remove axes for clean display
                ax.set_axis_off()
                
                # Render LaTeX expression - centered and much smaller
                latex_text = self.current_latex_expression.replace('\\\\', '\\')
                ax.text(0.5, 0.5, f'${latex_text}$', 
                       transform=ax.transAxes,
                       fontsize=10, ha='center', va='center', 
                       color='black', family='serif')
                
                plt.tight_layout()
                
                # Create canvas and embed in result text widget
                canvas = FigureCanvasTkAgg(fig, self.result_text)
                canvas.draw()
                
                # Insert canvas at the beginning of the text widget
                self.result_text.config(state='normal')
                self.result_text.mark_set("latex_start", "1.9")  # After "Resultado de la Integral\n"
                self.result_text.window_create("latex_start", window=canvas.get_tk_widget())
                self.result_text.config(state='disabled')
                
                # Store canvas for cleanup
                self.latex_canvas = canvas
                
                logger.info("Visual LaTeX rendering completed successfully")
                
        except Exception as e:
            logger.error(f"Error rendering visual LaTeX: {str(e)}")
            # Fallback: show LaTeX as text
            try:
                self.result_text.config(state='normal')
                if hasattr(self, 'current_latex_expression'):
                    self.result_text.insert("1.9", f"{self.current_latex_expression}\n\n")
                self.result_text.config(state='disabled')
            except:
                pass
    
    def _render_visual_latex_step(self, step_idx):
        """Render LaTeX step as visual image using matplotlib"""
        try:
            if hasattr(self, 'latex_steps') and f"step_{step_idx}" in self.latex_steps:
                step_expression = self.latex_steps[f"step_{step_idx}"]
                
                # Create matplotlib figure for LaTeX rendering
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                
                # Create figure with LaTeX rendering - much smaller like results
                fig, ax = plt.subplots(figsize=(6, 1.5))
                ax.set_facecolor('white')
                fig.patch.set_facecolor('white')
                
                # Remove axes for clean display
                ax.set_axis_off()
                
                # Render LaTeX expression - much smaller like results
                latex_text = step_expression.replace('\\\\', '\\')
                ax.text(0.5, 0.5, f'${latex_text}$', 
                       transform=ax.transAxes,
                       fontsize=10, ha='center', va='center', 
                       color='black', family='serif')
                
                plt.tight_layout()
                
                # Create canvas and embed in steps text widget
                canvas = FigureCanvasTkAgg(fig, self.steps_text)
                canvas.draw()
                
                # Find the position to insert canvas (after step header)
                self.steps_text.config(state='normal')
                
                # Search for the step position
                step_marker = f"Paso {step_idx}:\n--------------------\n[LaTeX Mathematical Step]\n"
                search_pos = self.steps_text.search(step_marker, "1.0", tk.END)
                
                if search_pos:
                    # Get the position after the marker
                    end_pos = f"{search_pos}+{len(step_marker)}c"
                    self.steps_text.window_create(end_pos, window=canvas.get_tk_widget())
                
                self.steps_text.config(state='disabled')
                
                # Store canvas for cleanup
                if not hasattr(self, 'latex_step_canvases'):
                    self.latex_step_canvases = {}
                self.latex_step_canvases[f"step_{step_idx}"] = canvas
                
                logger.info(f"Visual LaTeX step {step_idx} rendering completed successfully")
                
        except Exception as e:
            logger.error(f"Error rendering visual LaTeX step {step_idx}: {str(e)}")
            # Fallback: show LaTeX as text
            try:
                self.steps_text.config(state='normal')
                if hasattr(self, 'latex_steps') and f"step_{step_idx}" in self.latex_steps:
                    step_text = self.latex_steps[f"step_{step_idx}"]
                    self.steps_text.insert(tk.END, f"{step_text}\n\n")
                self.steps_text.config(state='disabled')
            except:
                pass
    
    def _display_calculation_error(self, error_msg):
        """Display calculation error"""
        try:
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"Error en el cálculo:\n\n{error_msg}")
            self.result_text.config(state='disabled')
            
            self.update_status("Error en cálculo", '#e74c3c')
        except Exception as e:
            logger.error(f"Error displaying calculation error: {str(e)}")
    
    def _finish_calculation(self):
        """Finish calculation and reset UI state"""
        try:
            self.is_calculating = False
            self.calculate_btn.config(text="CALCULAR INTEGRAL", state="normal")
        except Exception as e:
            logger.error(f"Error finishing calculation: {str(e)}")
    
    def new_calculation(self):
        """Start new calculation"""
        try:
            # Clear editor
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", "x**2 + 3*x + 2")
            self.current_function = "x**2 + 3*x + 2"
            
            # Clear results
            self.result_text.config(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.config(state='disabled')
            
            self.steps_text.config(state='normal')
            self.steps_text.delete("1.0", tk.END)
            self.steps_text.config(state='disabled')
            
            self.verify_text.config(state='normal')
            self.verify_text.delete("1.0", tk.END)
            self.verify_text.config(state='disabled')
            
            # Reset state
            self.current_result = None
            self.definite_var.set(False)
            
            # Update status
            self.update_status("Nuevo cálculo iniciado", '#3498db')
            
        except Exception as e:
            logger.error(f"Error in new calculation: {str(e)}")
    
    def save_result(self):
        """Save current result"""
        try:
            if not self.current_result:
                messagebox.showwarning("Guardar", "No hay resultado para guardar")
                return
            
            from tkinter import filedialog
            from datetime import datetime
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"integral_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Calculadora de Integrales PRO v4.0\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(f"Función: {self.current_function}\n")
                    f.write(f"Método: {self.integral_type_var.get()}\n")
                    f.write(f"Resultado: {self.current_result.result}\n")
                    f.write(f"Variable: {self.current_result.variable}\n")
                    
                    if self.definite_var.get():
                        f.write(f"Límites: {self.lower_limit.get()} a {self.upper_limit.get()}\n")
                    
                    if hasattr(self.current_result, 'steps') and self.current_result.steps:
                        f.write(f"\nPasos:\n")
                        for i, step in enumerate(self.current_result.steps, 1):
                            f.write(f"{i}. {step}\n")
                
                messagebox.showinfo("Guardar", f"Resultado guardado en: {filename}")
                self.update_status("Resultado guardado", '#27ae60')
                
        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")
            messagebox.showerror("Error", f"No se pudo guardar el resultado: {str(e)}")
    
    def export_report(self):
        """Export comprehensive report"""
        try:
            if not self.current_result:
                messagebox.showwarning("Exportar", "No hay resultados para exportar")
                return
            
            from tkinter import filedialog
            from datetime import datetime
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"integral_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if filename:
                report = self.generate_comprehensive_report()
                
                if filename.endswith('.pdf'):
                    # For now, save as text (PDF generation would require additional libraries)
                    txt_filename = filename.replace('.pdf', '.txt')
                    with open(txt_filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    messagebox.showinfo("Exportar", f"Informe exportado como texto: {txt_filename}")
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    messagebox.showinfo("Exportar", f"Informe exportado: {filename}")
                
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
CALCULADORA DE INTEGRALES PRO v4.0 - INFORME COMPLETO
{'='*60}

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Versión: 4.0 Professional Edition
{'='*60}

1. FUNCIÓN ORIGINAL:
{self.current_function}

2. CONFIGURACIÓN:
- Método de integración: {self.integral_type_var.get()}
- Variable: {self.symbols['x'].get()}
- Tipo: {'Definida' if self.definite_var.get() else 'Indefinida'}
{'Límites: ' + self.lower_limit.get() + ' a ' + self.upper_limit.get() if self.definite_var.get() else ''}

3. RESULTADO:
{self.current_result.result if self.current_result else 'No disponible'}

4. INFORMACIÓN DEL CÁLCULO:
- Método utilizado: {self.current_result.method.value if self.current_result else 'N/A'}
- Variable de integración: {self.current_result.variable if self.current_result else 'N/A'}
- Función original: {self.current_result.original_func if self.current_result else 'N/A'}

5. PASOS DEL CÁLCULO:
{'Pasos disponibles en la aplicación' if self.current_result and hasattr(self.current_result, 'steps') else 'No disponibles'}

6. VERIFICACIÓN:
{'Verificación disponible en la aplicación' if self.current_result else 'No disponible'}

7. ESTADÍSTICAS:
- Caracteres en función: {len(self.current_function)}
- Precisión: Simbólica exacta
- Motor: SymPy {sp.__version__}

{'='*60}
FIN DEL INFORME - Generado por CalcPRO v4.0
{'='*60}
"""
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return "Error al generar el informe"
    
    def show_history(self):
        """Show calculation history"""
        try:
            history = self.history_manager.get_all()
            
            if not history:
                messagebox.showinfo("Historial", "No hay cálculos en el historial")
                return
            
            # Create history window
            history_window = tk.Toplevel(self.root)
            history_window.title("Historial de Cálculos")
            history_window.geometry("800x600")
            history_window.configure(bg='#ffffff')
            
            # Header
            header = tk.Frame(history_window, bg='#3498db', height=40)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="HISTORIAL DE CÁLCULOS", 
                    font=('Segoe UI', 12, 'bold'), 
                    fg='white', bg='#3498db').pack(pady=10)
            
            # History list
            history_frame = tk.Frame(history_window, bg='#ffffff')
            history_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create treeview for history
            columns = ('Fecha', 'Función', 'Método')
            history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=20)
            
            # Configure columns
            history_tree.heading('Fecha', text='Fecha')
            history_tree.heading('Función', text='Función')
            history_tree.heading('Método', text='Método')
            
            history_tree.column('Fecha', width=150)
            history_tree.column('Función', width=400)
            history_tree.column('Método', width=200)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
            history_tree.configure(yscrollcommand=scrollbar.set)
            
            history_tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Populate history
            for entry in history[-50:]:  # Show last 50 entries
                date = entry.get('date', 'N/A')
                function = entry.get('function', 'N/A')
                method = entry.get('method', 'N/A')
                
                history_tree.insert('', 'end', values=(date, function, method))
            
            # Buttons
            button_frame = tk.Frame(history_window, bg='#ffffff')
            button_frame.pack(fill="x", padx=10, pady=10)
            
            tk.Button(button_frame, text="Cargar", 
                     command=lambda: self.load_from_history(history_tree),
                     font=('Segoe UI', 10, 'bold'),
                     bg='#3498db', fg='white',
                     padx=15, pady=5).pack(side="left", padx=5)
            
            tk.Button(button_frame, text="Limpiar Historial", 
                     command=self.clear_history,
                     font=('Segoe UI', 10, 'bold'),
                     bg='#e74c3c', fg='white',
                     padx=15, pady=5).pack(side="left", padx=5)
            
            tk.Button(button_frame, text="Cerrar", 
                     command=history_window.destroy,
                     font=('Segoe UI', 10, 'bold'),
                     bg='#95a5a6', fg='white',
                     padx=15, pady=5).pack(side="right", padx=5)
            
        except Exception as e:
            logger.error(f"Error showing history: {str(e)}")
            messagebox.showerror("Error", f"No se pudo mostrar el historial: {str(e)}")
    
    def load_from_history(self, history_tree):
        """Load selected entry from history"""
        try:
            selected = history_tree.selection()
            if not selected:
                messagebox.showwarning("Historial", "Selecciona una entrada del historial")
                return
            
            item = history_tree.item(selected[0])
            function = item['values'][1]
            
            # Load function into editor
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", function)
            self.current_function = function
            
            messagebox.showinfo("Historial", f"Función cargada: {function}")
            
        except Exception as e:
            logger.error(f"Error loading from history: {str(e)}")
    
    def clear_history(self):
        """Clear calculation history"""
        try:
            if messagebox.askyesno("Historial", "¿Estás seguro de que quieres limpiar todo el historial?"):
                self.history_manager.clear()
                messagebox.showinfo("Historial", "Historial limpiado exitosamente")
                self.update_status("Historial limpiado", '#f39c12')
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
    
    def toggle_professional_theme(self):
        """Toggle professional theme"""
        try:
            if self.dark_mode.get():
                self.apply_light_theme()
                self.dark_mode.set(False)
                self.theme_btn.config(text=" Tema Oscuro")
            else:
                self.apply_dark_theme()
                self.dark_mode.set(True)
                self.theme_btn.config(text=" Tema Claro")
            
            self.update_status("Tema cambiado", '#3498db')
        except Exception as e:
            logger.error(f"Error toggling theme: {str(e)}")
    
    def apply_light_theme(self):
        """Apply light theme"""
        try:
            # Update main container
            self.main_container.configure(bg='#f8f9fa')
            
            # Update panels
            for panel in [self.left_panel, self.right_panel]:
                panel.configure(bg='#ffffff')
            
            # Update frames
            for widget in self.main_container.winfo_children():
                self.apply_theme_to_widget(widget, '#ffffff', '#2c3e50')
            
            # Update graph
            if hasattr(self, 'ax'):
                self.ax.set_facecolor('#f8f9fa')
                self.canvas.draw()
                
        except Exception as e:
            logger.error(f"Error applying light theme: {str(e)}")
    
    def apply_dark_theme(self):
        """Apply dark theme"""
        try:
            # Update main container
            self.main_container.configure(bg='#2c3e50')
            
            # Update panels
            for panel in [self.left_panel, self.right_panel]:
                panel.configure(bg='#34495e')
            
            # Update frames
            for widget in self.main_container.winfo_children():
                self.apply_theme_to_widget(widget, '#34495e', '#ecf0f1')
            
            # Update graph
            if hasattr(self, 'ax'):
                self.ax.set_facecolor('#2c3e50')
                self.canvas.draw()
                
        except Exception as e:
            logger.error(f"Error applying dark theme: {str(e)}")
    
    def apply_theme_to_widget(self, widget, bg_color, fg_color):
        """Apply theme to widget recursively"""
        try:
            widget.configure(bg=bg_color)
            
            # Update text color if supported
            try:
                widget.configure(fg=fg_color)
            except:
                pass
            
            # Recursively apply to children
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, bg_color, fg_color)
                
        except:
            pass
    
    def show_professional_settings(self):
        """Show professional settings dialog"""
        try:
            settings_window = tk.Toplevel(self.root)
            settings_window.title("Configuración - CalcPRO v4.0")
            settings_window.geometry("600x500")
            settings_window.configure(bg='#ffffff')
            
            # Header
            header = tk.Frame(settings_window, bg='#2c3e50', height=50)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="CONFIGURACIÓN PROFESIONAL", 
                    font=('Segoe UI', 14, 'bold'), 
                    fg='white', bg='#2c3e50').pack(pady=15)
            
            # Settings content
            settings_frame = tk.Frame(settings_window, bg='#ffffff')
            settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # General settings
            general_frame = tk.LabelFrame(settings_frame, text="General", 
                                        font=('Segoe UI', 11, 'bold'), 
                                        fg='#2c3e50', bg='#ffffff')
            general_frame.pack(fill="x", pady=10)
            
            # Auto-parentheses
            auto_check = tk.Checkbutton(general_frame, text="Auto-paréntesis inteligente", 
                                       variable=self.auto_parentheses,
                                       font=('Segoe UI', 10),
                                       fg='#2c3e50', bg='#ffffff',
                                       selectcolor='#3498db')
            auto_check.pack(anchor="w", padx=10, pady=5)
            
            # Theme settings
            theme_frame = tk.LabelFrame(settings_frame, text="Apariencia", 
                                       font=('Segoe UI', 11, 'bold'), 
                                       fg='#2c3e50', bg='#ffffff')
            theme_frame.pack(fill="x", pady=10)
            
            theme_check = tk.Checkbutton(theme_frame, text="Modo oscuro", 
                                       variable=self.dark_mode,
                                       command=self.toggle_professional_theme,
                                       font=('Segoe UI', 10),
                                       fg='#2c3e50', bg='#ffffff',
                                       selectcolor='#3498db')
            theme_check.pack(anchor="w", padx=10, pady=5)
            
            # Graph settings
            graph_frame = tk.LabelFrame(settings_frame, text="Gráficos", 
                                      font=('Segoe UI', 11, 'bold'), 
                                      fg='#2c3e50', bg='#ffffff')
            graph_frame.pack(fill="x", pady=10)
            
            grid_check = tk.Checkbutton(graph_frame, text="Mostrar cuadrícula por defecto", 
                                      variable=self.show_grid,
                                      font=('Segoe UI', 10),
                                      fg='#2c3e50', bg='#ffffff',
                                      selectcolor='#3498db')
            grid_check.pack(anchor="w", padx=10, pady=5)
            
            legend_check = tk.Checkbutton(graph_frame, text="Mostrar leyenda por defecto", 
                                         variable=self.show_legend,
                                         font=('Segoe UI', 10),
                                         fg='#2c3e50', bg='#ffffff',
                                         selectcolor='#3498db')
            legend_check.pack(anchor="w", padx=10, pady=5)
            
            # Calculation settings
            calc_frame = tk.LabelFrame(settings_frame, text="Cálculo", 
                                      font=('Segoe UI', 11, 'bold'), 
                                      fg='#2c3e50', bg='#ffffff')
            calc_frame.pack(fill="x", pady=10)
            
            tk.Label(calc_frame, text="Precisión numérica:", 
                    font=('Segoe UI', 10), 
                    fg='#2c3e50', bg='#ffffff').pack(anchor="w", padx=10, pady=2)
            
            precision_combo = ttk.Combobox(calc_frame, 
                                          values=["Baja", "Media", "Alta", "Máxima"],
                                          state="readonly", width=20)
            precision_combo.set("Alta")
            precision_combo.pack(anchor="w", padx=10, pady=2)
            
            # Buttons
            button_frame = tk.Frame(settings_frame, bg='#ffffff')
            button_frame.pack(fill="x", pady=20)
            
            tk.Button(button_frame, text="Guardar Configuración", 
                     command=lambda: self.save_settings(settings_window),
                     font=('Segoe UI', 10, 'bold'),
                     bg='#27ae60', fg='white',
                     padx=15, pady=8).pack(side="left", padx=5)
            
            tk.Button(button_frame, text="Restablecer", 
                     command=self.reset_settings,
                     font=('Segoe UI', 10, 'bold'),
                     bg='#e74c3c', fg='white',
                     padx=15, pady=8).pack(side="left", padx=5)
            
            tk.Button(button_frame, text="Cerrar", 
                     command=settings_window.destroy,
                     font=('Segoe UI', 10, 'bold'),
                     bg='#95a5a6', fg='white',
                     padx=15, pady=8).pack(side="right", padx=5)
            
        except Exception as e:
            logger.error(f"Error showing professional settings: {str(e)}")
    
    def save_settings(self, settings_window):
        """Save settings"""
        try:
            # Save settings to file or apply immediately
            messagebox.showinfo("Configuración", "Configuración guardada exitosamente")
            settings_window.destroy()
            self.update_status("Configuración guardada", '#27ae60')
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        try:
            if messagebox.askyesno("Configuración", "¿Restablecer configuración a valores predeterminados?"):
                self.auto_parentheses.set(True)
                self.dark_mode.set(False)
                self.show_grid.set(True)
                self.show_legend.set(True)
                messagebox.showinfo("Configuración", "Configuración restablecida")
        except Exception as e:
            logger.error(f"Error resetting settings: {str(e)}")
    
    def show_professional_help(self):
        """Show professional help dialog"""
        try:
            help_window = tk.Toplevel(self.root)
            help_window.title("Ayuda - CalcPRO v4.0")
            help_window.geometry("700x600")
            help_window.configure(bg='#ffffff')
            
            # Header
            header = tk.Frame(help_window, bg='#3498db', height=50)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text="AYUDA PROFESIONAL", 
                    font=('Segoe UI', 14, 'bold'), 
                    fg='white', bg='#3498db').pack(pady=15)
            
            # Help content
            help_frame = tk.Frame(help_window, bg='#ffffff')
            help_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            help_text = tk.Text(help_frame, 
                               font=('Segoe UI', 10), 
                               bg='#f8f9fa', fg='#2c3e50',
                               relief=tk.RIDGE, bd=1,
                               padx=15, pady=15,
                               wrap=tk.WORD)
            help_text.pack(fill="both", expand=True)
            
            help_content = """CALCULADORA DE INTEGRALES PRO v4.0 - GUÍA COMPLETA

FUNCIONES BÁSICAS:
- Operadores aritméticos: +, -, *, /, ^ (potencia)
- Funciones trigonométricas: sin, cos, tan, cot, sec, csc
- Funciones inversas: asin, acos, atan, acot, asec, acsc
- Funciones hiperbólicas: sinh, cosh, tanh, coth, sech, csch
- Logaritmos: log, ln, log10
- Exponenciales: exp, sqrt, cbrt
- Valor absoluto: abs
- Signo: sign

CONSTANTES MATEMÁTICAS:
- pi: Número pi (3.14159...)
- e: Número de Euler (2.71828...)
- phi: Proporción áurea ((1+sqrt(5))/2)
- tau: 2*pi (6.28318...)
- i, j: Unidades imaginarias
- oo: Infinito
- nan: No es un número

CÁLCULO DIFERENCIAL:
- diff: Derivada
- D: Operador derivada
- grad: Gradiente
- div: Divergencia
- curl: Rotacional
- laplacian: Laplaciano

CÁLCULO INTEGRAL:
- int: Integral indefinida
- def_int: Integral definida
- double_int: Integral doble
- triple_int: Integral triple
- line_int: Integral de línea
- surface_int: Integral de superficie

LÍMITES Y SERIES:
- limit: Límite
- lim_inf: Límite inferior
- lim_sup: Límite superior
- series: Serie
- taylor: Serie de Taylor
- maclaurin: Serie de Maclaurin
- sum: Sumatoria
- prod: Productoria
- zeta: Función zeta de Riemann

FUNCIONES ESPECIALES:
- factorial: Factorial
- gamma: Función gamma
- beta: Función beta
- erf: Función error
- erfc: Función error complementaria
- gamma_inc: Gamma incompleta

ATAJOS DE TECLADO:
- Ctrl+Enter: Calcular integral
- Ctrl+N: Nuevo cálculo
- Ctrl+S: Guardar resultado
- Ctrl+H: Mostrar historial
- Ctrl+E: Exportar informe
- Ctrl+G: Graficar función
- F11: Pantalla completa
- Esc: Salir de pantalla completa

MÉTODOS DE INTEGRACIÓN:
1. Automático: Detección inteligente del mejor método
2. Directa: Integración directa simple
3. Sustitución: Método de sustitución u
4. Por Partes: Integración por partes
5. Fracciones Parciales: Descomposición en fracciones parciales
6. Trigonométrica: Identidades trigonométricas
7. Racional: Funciones racionales
8. Exponencial: Funciones exponenciales y logarítmicas

CONSEJOS DE USO:
- Usa paréntesis para agrupar expresiones complejas
- Verifica la sintaxis antes de calcular
- Usa el historial para recuperar cálculos anteriores
- Exporta informes para documentación
- Experimenta con diferentes métodos de integración

SOPORTE TÉCNICO:
- Compatible con Python 3.11+
- Requiere SymPy, Matplotlib, NumPy
- Soporte para Windows, Linux, macOS
- Memoria recomendada: 4GB RAM
- Procesador recomendado: 2GHz+

Para más información, visite la documentación en línea o contacte al soporte técnico."""
            
            help_text.insert("1.0", help_content)
            help_text.config(state='disabled')
            
            # Close button
            close_frame = tk.Frame(help_window, bg='#ffffff')
            close_frame.pack(fill="x", padx=20, pady=10)
            
            tk.Button(close_frame, text="Cerrar", 
                     command=help_window.destroy,
                     font=('Segoe UI', 10, 'bold'),
                     bg='#3498db', fg='white',
                     padx=20, pady=8).pack()
            
        except Exception as e:
            logger.error(f"Error showing professional help: {str(e)}")
    
    def toggle_limits(self):
        """Toggle definite integral limits visibility"""
        try:
            if self.definite_var.get():
                self.limits_frame.pack(fill="x", pady=(5, 0))
                self.update_status("Modo integral definida activado", '#3498db')
            else:
                self.limits_frame.pack_forget()
                self.update_status("Modo integral indefinida", '#2ecc71')
        except Exception as e:
            logger.error(f"Error toggling limits: {str(e)}")
    
    def on_editor_key_release(self, event):
        """Handle editor key release with live validation"""
        try:
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            
            # Update character counter
            char_count = len(self.current_function)
            self.char_counter.config(text=f"{char_count} caracteres")
            
            # Live validation with Microsoft Math Engine
            if self.current_function:
                # First try Microsoft Math Engine validation
                try:
                    is_valid, error = self.math_engine.validate_expression(self.current_function)
                    if is_valid:
                        self.editor_status_label.config(text=" Válido (MS Math)", fg='#27ae60')
                    else:
                        self.editor_status_label.config(text=f" Error MS: {error[:20]}...", fg='#e74c3c')
                except Exception as e:
                    # Fallback to regular validator
                    validation = self.validator.validate(self.current_function)
                    if validation['valid']:
                        self.editor_status_label.config(text=" Válido", fg='#27ae60')
                    else:
                        self.editor_status_label.config(text=" Inválido", fg='#e74c3c')
            else:
                self.editor_status_label.config(text=" Vacío", fg='#95a5a6')
                
        except Exception as e:
            logger.error(f"Error in editor key release: {str(e)}")
    
    def on_editor_key_press(self, event):
        """Handle editor key press with auto-completion"""
        try:
            # Auto-parentheses
            if self.auto_parentheses.get() and event.char in '([':
                cursor_pos = self.editor_text.index(tk.INSERT)
                self.editor_text.insert(cursor_pos, event.char + ')')
                self.editor_text.mark_set(tk.INSERT, f"{cursor_pos}+1c")
                return "break"
                
        except Exception as e:
            logger.error(f"Error in editor key press: {str(e)}")
    
    def insert_symbol(self, symbol):
        """Insert symbol into editor with smart insertion"""
        try:
            # Handle special operations
            if symbol == 'DEL':
                self.delete_last_character()
                return
            elif symbol == 'ANS':
                self.insert_last_answer()
                return
            elif symbol == 'CLEAR':
                self.clear_editor()
                return
            elif symbol == 'CE':
                self.clear_editor()
                return
            
            cursor_pos = self.editor_text.index(tk.INSERT)
            
            # Enhanced symbol mapping for Microsoft Math Engine natural notation
            symbol_map = {
                # Basic operations
                '+': '+', '-': '-', '*': '*', '/': '/', '^': '^', '%': '%',
                '(': '(', ')': ')', '[': '[', ']': ']', '{': '{', '}': '}',
                '=': '=', '<': '<', '>': '>', '!=': '!=', '<=': '<=', '>=': '>=', '==': '==',
                '÷': '/', '×': '*', 'minus': '-',
                
                # Trigonometric functions (natural notation)
                'sin': 'sin(', 'cos': 'cos(', 'tan': 'tan(',
                'asin': 'asin(', 'acos': 'acos(', 'atan': 'atan(',
                'sinh': 'sinh(', 'cosh': 'cosh(', 'tanh': 'tanh(',
                'asinh': 'asinh(', 'acosh': 'acosh(', 'atanh': 'atanh(',
                'cot': 'cot(', 'sec': 'sec(', 'csc': 'csc(',
                'acot': 'acot(', 'asec': 'asec(', 'acsc': 'acsc(',
                'coth': 'coth(', 'sech': 'sech(', 'csch': 'csch(',
                'acoth': 'acoth(', 'asech': 'asech(', 'acsch': 'acsch(',
                
                # Logarithmic and exponential functions (natural notation)
                'log': 'log(', 'ln': 'ln(', 'log10': 'log10(', 'exp': 'exp(',
                'log(x)': 'log(', 'ln(x)': 'ln(', 'log10(x)': 'log10(',
                'log2(x)': 'log2(', 'log_b(x)': 'log(',
                'exp(x)': 'exp(',
                
                # Power and root functions (natural notation)
                'sqrt': 'sqrt(', 'cbrt': '**(1/3)', 'abs': 'abs(', 'sign': 'sign(',
                'sqrt(x)': 'sqrt(', 'cbrt(x)': '**(1/3)', 'root(x,n)': 'root(',
                'x²': 'x²', 'x³': 'x³', 'x^n': 'x^',
                'x^(-1)': 'x^(-1)', 'x^(1/2)': 'x^(1/2)', 'x^(1/3)': 'x^(1/3)',
                
                # Advanced functions (natural notation)
                'floor': 'floor(', 'ceil': 'ceiling(', 'round': 'round(',
                'log2(x)': 'log(2,', 'log_b(x)': 'log(x,', 'exp(x)': 'exp(',
                
                # Power and root functions (SymPy compatible)
                'sqrt': 'sqrt(', 'cbrt': 'root(3,', 'abs': 'Abs(', 'sign': 'sign(',
                'sqrt(x)': 'sqrt(', 'cbrt(x)': 'root(3,', 'root(x,n)': 'root(',
                'x²': '**2', 'x³': '**3', 'x^n': '**',
                'x^(-1)': '**(-1)', 'x^(1/2)': '**(1/2)', 'x^(1/3)': '**(1/3)',
                
                # Advanced functions (SymPy compatible)
                'floor': 'floor(', 'ceil': 'ceiling(', 'round': 'round(',
                'factorial': 'factorial(', 'gcd': 'gcd(', 'lcm': 'lcm(',
                'mod': 'mod(', 'divmod': 'divmod(', 'frac': 'Rational(',
                
                # Calculus functions (natural notation)
                'diff': 'diff(', 'D': 'Derivative(', 'grad': 'grad(', 'div': 'div(',
                'curl': 'curl(', 'laplacian': 'laplacian(',
                'int': 'integrate(', 'def_int': 'integrate(', 'limit': 'limit(',
                'series': 'series(', 'taylor': 'series(', 'maclaurin': 'series(',
                'sum': 'sum(', 'prod': 'product(',
                
                # Special functions (natural notation)
                'gamma': 'gamma(', 'beta': 'beta(', 'erf': 'erf(', 'erfc': 'erfc(',
                'zeta': 'zeta(', 'dirichlet': 'dirichlet(',
                
                # Constants (natural notation)
                'pi': 'pi', 'e': 'e', 'phi': '(1+sqrt(5))/2',
                'tau': '2*pi', 'i': 'i', 'j': 'i', 'oo': 'infinity',
                'nan': 'nan', 'inf': 'infinity', 'E': 'e',
                'Infinity': 'infinity', 'NaN': 'nan', 'Exp1': 'e', 'GoldenRatio': '(1+sqrt(5))/2',
                
                # Essential mathematical symbols (SymPy compatible)
                'integral': 'integrate(', 'd/dx': 'diff(', 'lim': 'limit(', 'sum': 'Sum(', 'prod': 'Product(', 'infinity': 'oo',
                'partial': 'Derivative(', 'nabla': 'grad(', 'Delta': 'laplacian(', 'exists': 'Exists(', 'forall': 'ForAll(', 'in': 'in',
                'subset': 'subset', 'superset': 'superset', 'union': 'Union(', 'intersection': 'Intersection(', 'empty': 'EmptySet', 'element': 'Element('
            }
            
            # Get proper symbol
            insert_text = symbol_map.get(symbol, symbol)
            
            # Insert symbol
            self.editor_text.insert(cursor_pos, insert_text)
            
            # Auto-close parentheses for functions (natural notation)
            functions_with_parens = [
                'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                'asinh', 'acosh', 'atanh', 'cot', 'sec', 'csc', 'acot', 'asec', 'acsc',
                'coth', 'sech', 'csch', 'acoth', 'asech', 'acsch',
                'log', 'ln', 'log10', 'log2', 'exp', 'sqrt', 'cbrt', 'abs', 'sign',
                'floor', 'ceil', 'round', 'factorial', 'gcd', 'lcm', 'mod', 'divmod', 'frac',
                'diff', 'D', 'grad', 'div', 'curl', 'laplacian',
                'int', 'integrate', 'def_int', 'limit', 'series', 'taylor', 'maclaurin',
                'sum', 'prod', 'gamma', 'beta', 'erf', 'erfc', 'zeta', 'dirichlet'
            ]
            
            if symbol in functions_with_parens:
                new_cursor = f"{cursor_pos}+{len(insert_text)}c"
                self.editor_text.insert(new_cursor, ')')
                self.editor_text.mark_set(tk.INSERT, new_cursor)
            
            # Special handling for x^n
            elif symbol == 'x^n':
                new_cursor = f"{cursor_pos}+{len(insert_text)}c"
                self.editor_text.mark_set(tk.INSERT, new_cursor)
            
            # Special handling for integral
            elif symbol == 'integral':
                # Insert integrate(, x, 0, 3) format for definite integral
                self.editor_text.insert(cursor_pos, 'integrate(')
                # Move cursor inside the integrate function
                new_cursor = f"{cursor_pos}+{len('integrate(')}c"
                self.editor_text.mark_set(tk.INSERT, new_cursor)
            
            # Update current function
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            
            # Update status
            self.update_status(f"Símbolo '{symbol}' insertado", '#3498db')
            
        except Exception as e:
            logger.error(f"Error inserting symbol: {str(e)}")
    
    def validate_input_with_math_engine(self):
        """Validate current input using Microsoft Math Engine"""
        try:
            current_text = self.editor_text.get("1.0", tk.END).strip()
            if current_text:
                is_valid, error = self.math_engine.validate_expression(current_text)
                if is_valid:
                    self.update_status("Expresión válida (Microsoft Math Engine)", '#27ae60')
                else:
                    self.update_status(f"Error: {error}", '#e74c3c')
            else:
                self.update_status("Listo para ingresar expresión", '#3498db')
        except Exception as e:
            logger.error(f"Error validating with math engine: {str(e)}")
    
    def get_math_engine_suggestions(self, partial_input):
        """Get suggestions from Microsoft Math Engine"""
        try:
            return self.math_engine.get_suggestions(partial_input)
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return []
    
    def delete_last_character(self):
        """Delete last character from editor"""
        try:
            self.editor_text.delete("end-2c", "end-1c")
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            self.update_status("Carácter eliminado", '#f39c12')
        except Exception as e:
            logger.error(f"Error deleting character: {str(e)}")
    
    def insert_last_answer(self):
        """Insert last answer (ANS) into editor"""
        try:
            if hasattr(self, 'last_answer') and self.last_answer:
                cursor_pos = self.editor_text.index(tk.INSERT)
                self.editor_text.insert(cursor_pos, self.last_answer)
                self.current_function = self.editor_text.get("1.0", tk.END).strip()
                self.update_status("ANS insertado", '#9b59b6')
            else:
                self.update_status("No hay respuesta anterior", '#e74c3c')
        except Exception as e:
            logger.error(f"Error inserting ANS: {str(e)}")
    
    def plot_function(self):
        """Plot current function with professional styling"""
        try:
            function_text = self.editor_text.get("1.0", tk.END).strip()
            if not function_text:
                messagebox.showwarning("Gráfica", "No hay función para graficar")
                return
            
            # Check if expression contains integral notation and process it
            if '∫' in function_text or 'integrate' in function_text.lower() or ('d' in function_text and 'dx' in function_text):
                try:
                    # Parse with Microsoft Math Engine to get clean expression
                    parsed_expr = self.math_engine.parse_natural_math(function_text)
                    
                    # Integrate the expression
                    variable = self.symbols['x'].get()
                    var_symbol = sp.Symbol(variable)
                    expr = sp.sympify(parsed_expr)
                    
                    # Remove integral notation if exists
                    expr_str = str(expr).replace('integrate', '').replace('∫', '').replace('dx', '').strip()
                    expr_clean = sp.sympify(expr_str)
                    
                    # Integrate
                    result = sp.integrate(expr_clean, var_symbol)
                    parsed_func = result
                    display_text = f"∫({expr_clean})dx = {str(result)}"
                    
                except Exception as e:
                    logger.error(f"Error integrating for plot: {e}")
                    messagebox.showerror("Error", f"No se pudo integrar la expresión:\n{str(e)}")
                    return
            else:
                # Regular function parsing
                try:
                    parsed_func = self.parser.parse(function_text)
                    display_text = function_text
                except Exception as parse_err:
                    messagebox.showerror("Error de Parsing", f"No se pudo parsear la función:\n{str(parse_err)}")
                    logger.error(f"Parse error in plot_function: {parse_err}")
                    return
            
            variable = self.symbols['x'].get()
            var_symbol = sp.Symbol(variable)
            
            # Get range
            try:
                x_min = float(self.x_min_entry.get())
                x_max = float(self.x_max_entry.get())
            except:
                x_min, x_max = -10, 10
            
            # Generate data
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
            
            # Clear and plot
            self.ax.clear()
            
            # Get next color for multiple functions
            color_index = len(self.graph_functions) % len(self.graph_colors)
            color = self.graph_colors[color_index]
            
            # Plot function
            self.ax.plot(x_clean, y_clean, color=color, linewidth=2.5, 
                        label=f'f({variable}) = {display_text}')
            
            # Add to graph functions list
            self.graph_functions.append((display_text, color))
            
            # Set styling
            if self.show_grid.get():
                self.ax.grid(True, alpha=0.3, color='#bdc3c7')
            
            self.ax.set_xlabel(variable, fontsize=12, color='#2c3e50')
            self.ax.set_ylabel(f'f({variable})', fontsize=12, color='#2c3e50')
            self.ax.set_title(f'Gráfica: {display_text}', fontsize=14, fontweight='bold', color='#2c3e50')
            
            # Add legend if enabled
            if self.show_legend.get() and len(self.graph_functions) > 0:
                self.ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
            
            # Modern styling
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#2c3e50')
            self.ax.spines['bottom'].set_color('#2c3e50')
            
            # Add zero lines
            self.ax.axhline(y=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            self.ax.axvline(x=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            
            # Highlight area for definite integrals
            if self.definite_var.get():
                try:
                    lower = float(self.lower_limit.get())
                    upper = float(self.upper_limit.get())
                    
                    if lower >= x_min and upper <= x_max:
                        # Shade area under curve
                        x_fill = np.linspace(lower, upper, 100)
                        y_fill = f(x_fill)
                        
                        # Handle infinities in fill area
                        mask_fill = np.isfinite(y_fill)
                        if np.any(mask_fill):
                            self.ax.fill_between(x_fill[mask_fill], 0, y_fill[mask_fill], 
                                              alpha=0.3, color=color)
                        
                except:
                    pass
            
            self.canvas.draw()
            self.update_status("Gráfica actualizada", '#27ae60')
            
        except Exception as e:
            logger.error(f"Error plotting function: {str(e)}")
            messagebox.showerror("Error", f"No se pudo graficar la función: {str(e)}")
                
            variable = self.symbols['x'].get()
            var_symbol = sp.Symbol(variable)
            
            # Get range
            try:
                x_min = float(self.x_min_entry.get())
                x_max = float(self.x_max_entry.get())
            except:
                x_min, x_max = -10, 10
            
            # Generate data
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
            
            # Clear and plot
            self.ax.clear()
            
            # Get next color for multiple functions
            color_index = len(self.graph_functions) % len(self.graph_colors)
            color = self.graph_colors[color_index]
            
            # Plot function
            self.ax.plot(x_clean, y_clean, color=color, linewidth=2.5, 
                        label=f'f({variable}) = {function_text}')
            
            # Add to graph functions list
            self.graph_functions.append((function_text, color))
            
            # Set styling
            if self.show_grid.get():
                self.ax.grid(True, alpha=0.3, color='#bdc3c7')
            
            self.ax.set_xlabel(variable, fontsize=12, color='#2c3e50')
            self.ax.set_ylabel(f'f({variable})', fontsize=12, color='#2c3e50')
            self.ax.set_title(f'Gráfica: {function_text}', fontsize=14, fontweight='bold', color='#2c3e50')
            
            # Add legend if enabled
            if self.show_legend.get() and len(self.graph_functions) > 0:
                self.ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
            
            # Modern styling
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#2c3e50')
            self.ax.spines['bottom'].set_color('#2c3e50')
            
            # Add zero lines
            self.ax.axhline(y=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            self.ax.axvline(x=0, color='#2c3e50', linewidth=0.8, alpha=0.5)
            
            # Highlight area for definite integrals
            if self.definite_var.get():
                try:
                    lower = float(self.lower_limit.get())
                    upper = float(self.upper_limit.get())
                    
                    if lower >= x_min and upper <= x_max:
                        # Shade area under curve
                        x_fill = np.linspace(lower, upper, 100)
                        y_fill = f(x_fill)
                        
                        # Handle infinities in fill area
                        mask_fill = np.isfinite(y_fill)
                        if np.any(mask_fill):
                            self.ax.fill_between(x_fill[mask_fill], 0, y_fill[mask_fill], 
                                              alpha=0.3, color=color)
                        
                except:
                    pass
            
            self.canvas.draw()
            self.update_status("Gráfica actualizada", '#27ae60')
            
        except Exception as e:
            logger.error(f"Error plotting function: {str(e)}")
            messagebox.showerror("Error", f"No se pudo graficar la función: {str(e)}")
    
    def clear_graph(self):
        """Clear graph and reset"""
        try:
            self.ax.clear()
            self.setup_initial_plot()
            self.canvas.draw()
            self.graph_functions = []
            self.update_status("Gráfica limpiada", '#f39c12')
        except Exception as e:
            logger.error(f"Error clearing graph: {str(e)}")
    
    def zoom_in(self):
        """Zoom in the graph"""
        try:
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            
            x_center = (current_xlim[0] + current_xlim[1]) / 2
            y_center = (current_ylim[0] + current_ylim[1]) / 2
            
            x_range = (current_xlim[1] - current_xlim[0]) / 2
            y_range = (current_ylim[1] - current_ylim[0]) / 2
            
            self.ax.set_xlim(x_center - x_range, x_center + x_range)
            self.ax.set_ylim(y_center - y_range, y_center + y_range)
            
            self.canvas.draw()
            self.update_status("Zoom aplicado", '#3498db')
            
        except Exception as e:
            logger.error(f"Error zooming in: {str(e)}")
    
    def zoom_out(self):
        """Zoom out the graph"""
        try:
            current_xlim = self.ax.get_xlim()
            current_ylim = self.ax.get_ylim()
            
            x_center = (current_xlim[0] + current_xlim[1]) / 2
            y_center = (current_ylim[0] + current_ylim[1]) / 2
            
            x_range = (current_xlim[1] - current_xlim[0]) * 1.5
            y_range = (current_ylim[1] - current_ylim[0]) * 1.5
            
            self.ax.set_xlim(x_center - x_range, x_center + x_range)
            self.ax.set_ylim(y_center - y_range, y_center + y_range)
            
            self.canvas.draw()
            self.update_status("Zoom reducido", '#3498db')
            
        except Exception as e:
            logger.error(f"Error zooming out: {str(e)}")
    
    def reset_graph(self):
        """Reset graph to original view"""
        try:
            self.ax.clear()
            self.setup_initial_plot()
            self.canvas.draw()
            self.update_status("Gráfica restablecida", '#95a5a6')
        except Exception as e:
            logger.error(f"Error resetting graph: {str(e)}")
    
    def update_graph_display(self):
        """Update graph display based on settings"""
        try:
            # Replot current function with new settings
            if self.graph_functions:
                self.clear_graph()
                # Replot all functions
                for func_text, color in self.graph_functions:
                    self.editor_text.delete("1.0", tk.END)
                    self.editor_text.insert("1.0", func_text)
                    self.plot_function()
            else:
                self.setup_initial_plot()
                self.canvas.draw()
                
        except Exception as e:
            logger.error(f"Error updating graph display: {str(e)}")
    
    def export_graph(self):
        """Export graph to file"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
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
                messagebox.showinfo("Exportar", f"Gráfica exportada a: {filename}")
                self.update_status("Gráfica exportada", '#27ae60')
            
        except Exception as e:
            logger.error(f"Error exporting graph: {str(e)}")
            messagebox.showerror("Error", f"No se pudo exportar la gráfica: {str(e)}")
    
    def fullscreen_graph(self):
        """Toggle fullscreen for graph"""
        try:
            # Create fullscreen window
            fullscreen_window = tk.Toplevel(self.root)
            fullscreen_window.title("Gráfica - Pantalla Completa")
            fullscreen_window.attributes('-fullscreen', True)
            fullscreen_window.configure(bg='#000000')
            
            # Create new figure for fullscreen
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            fig_fullscreen = self.fig.copy()
            canvas_fullscreen = FigureCanvasTkAgg(fig_fullscreen, fullscreen_window)
            canvas_fullscreen.get_tk_widget().pack(fill="both", expand=True)
            
            # Add toolbar
            toolbar_frame = tk.Frame(fullscreen_window, bg='#000000')
            toolbar_frame.pack(fill="x")
            
            # Close button
            close_btn = tk.Button(toolbar_frame, text="Cerrar (ESC)", 
                                command=fullscreen_window.destroy,
                                font=('Segoe UI', 12, 'bold'),
                                bg='#e74c3c', fg='white',
                                padx=20, pady=5)
            close_btn.pack(side="right", padx=10, pady=5)
            
            # Bind ESC key
            fullscreen_window.bind('<Escape>', lambda e: fullscreen_window.destroy())
            
            self.update_status("Modo pantalla completa", '#9b59b6')
            
        except Exception as e:
            logger.error(f"Error in fullscreen graph: {str(e)}")
    
    def on_scroll(self, event):
        """Handle mouse scroll for zoom"""
        try:
            if event.inaxes == self.ax:
                # Zoom in/out with scroll
                scale_factor = 1.1 if event.button == 'up' else 0.9
                
                xlim = self.ax.get_xlim()
                ylim = self.ax.get_ylim()
                
                x_center = event.xdata
                y_center = event.ydata
                
                new_xlim = [x_center - (x_center - xlim[0]) * scale_factor,
                           x_center + (xlim[1] - x_center) * scale_factor]
                new_ylim = [y_center - (y_center - ylim[0]) * scale_factor,
                           y_center + (ylim[1] - y_center) * scale_factor]
                
                self.ax.set_xlim(new_xlim)
                self.ax.set_ylim(new_ylim)
                
                self.canvas.draw()
                
        except Exception as e:
            logger.error(f"Error handling scroll: {str(e)}")
    
    def on_mouse_press(self, event):
        """Handle mouse press for pan"""
        try:
            if event.inaxes == self.ax and event.button == 1:  # Left click
                self.pan_start = (event.xdata, event.ydata)
                
        except Exception as e:
            logger.error(f"Error handling mouse press: {str(e)}")
    
    def on_mouse_release(self, event):
        """Handle mouse release"""
        try:
            self.pan_start = None
            
        except Exception as e:
            logger.error(f"Error handling mouse release: {str(e)}")
    
    def on_mouse_motion(self, event):
        """Handle mouse motion for pan and tooltips"""
        try:
            if self.pan_start and event.inaxes == self.ax:
                # Pan the graph
                dx = event.xdata - self.pan_start[0]
                dy = event.ydata - self.pan_start[1]
                
                xlim = self.ax.get_xlim()
                ylim = self.ax.get_ylim()
                
                self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
                self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
                
                self.canvas.draw()
                
            elif event.inaxes == self.ax:
                # Show coordinates
                self.update_status(f"Coordenadas: ({event.xdata:.3f}, {event.ydata:.3f})", '#3498db')
                
        except Exception as e:
            logger.error(f"Error handling mouse motion: {str(e)}")
    
    def apply_professional_theme(self):
        """Apply professional theme on startup"""
        try:
            if self.dark_mode.get():
                self.apply_dark_theme()
            else:
                self.apply_light_theme()
        except Exception as e:
            logger.error(f"Error applying professional theme: {str(e)}")
    
    def setup_shortcuts(self):
        """Setup professional keyboard shortcuts"""
        try:
            # Calculation shortcuts
            self.root.bind('<Control-Return>', lambda e: self.calculate_integral())
            self.root.bind('<Control-n>', lambda e: self.new_calculation())
            self.root.bind('<Control-s>', lambda e: self.save_result())
            self.root.bind('<Control-h>', lambda e: self.show_history())
            self.root.bind('<Control-e>', lambda e: self.export_report())
            self.root.bind('<Control-g>', lambda e: self.plot_function())
            
            # Window management shortcuts
            self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
            self.root.bind('<Control-F11>', lambda e: self.maximize_window())
            self.root.bind('<Control-plus>', lambda e: self.adjust_window_size(1.1))
            self.root.bind('<Control-minus>', lambda e: self.adjust_window_size(0.9))
            self.root.bind('<Control-0>', lambda e: self.restore_window())
            self.root.bind('<Escape>', lambda e: self.close_fullscreen())
            
            # Graph shortcuts
            self.root.bind('<Control-Shift-g>', lambda e: self.fullscreen_graph())
            
        except Exception as e:
            logger.error(f"Error setting up shortcuts: {str(e)}")
    
    def close_fullscreen(self):
        """Close fullscreen windows"""
        try:
            for window in self.root.winfo_children():
                if isinstance(window, tk.Toplevel) and window.attributes('-fullscreen'):
                    window.destroy()
        except Exception as e:
            logger.error(f"Error closing fullscreen: {str(e)}")
    
    def update_status(self, message, color='#2c3e50'):
        """Update status bar message"""
        try:
            self.status_label.config(text=f" {message}", fg=color)
        except Exception as e:
            logger.error(f"Error updating status: {str(e)}")
    
    def increment_calc_counter(self):
        """Increment calculation counter"""
        try:
            if hasattr(self, 'calc_counter'):
                current_text = self.calc_counter.cget("text")
                current_count = int(current_text.split(": ")[1]) if ": " in current_text else 0
                new_count = current_count + 1
                self.calc_counter.config(text=f"Cálculos: {new_count}")
        except Exception as e:
            logger.error(f"Error incrementing calc counter: {str(e)}")
    
    def update_memory_usage(self):
        """Update memory usage display"""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.memory_label.config(text=f"Memoria: {memory_mb:.1f}MB")
        except:
            # Fallback if psutil not available
            self.memory_label.config(text="Memoria: N/A")

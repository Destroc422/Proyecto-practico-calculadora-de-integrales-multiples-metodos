"""
Fixed Layout Calculator - Results Panel Repositioned
Maintains original structure but moves results panel to better position
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sympy as sp
import threading
import logging
import re
from typing import Optional, Dict, Any, Tuple

# Core modules
from core.math_engine_optimized import AdvancedMathEngine
from core.parser import MathParser

# UI modules
from ui.theme_manager import ThemeManager

# Graph and utilities
from graph.plotter import Plotter
from utils.validators import validate_input
from utils.latex_renderer import LaTeXDisplayManager
from data.history_manager import HistoryManager

# Matplotlib backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import UI update fix
from ui.simple_ui_fix import patch_calculator_display_methods

# Configure logging without Unicode issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('latex_calculator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FixedLayoutLaTeXCalculator:
    """Fixed Layout LaTeX Calculator with repositioned results panel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculadora de Integrales PRO - Layout Fixed")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 800)
        
        # Initialize components
        self._initialize_components()
        
        # Setup UI
        self.setup_ui()
        self.setup_shortcuts()
        
        # Apply theme
        self.apply_theme()
        
        # Apply UI update fix
        patch_calculator_display_methods()
        
        logger.info("Fixed Layout LaTeX Integral Calculator initialized successfully")
    
    def _initialize_components(self):
        """Initialize all components"""
        try:
            self.theme_manager = ThemeManager()
            self.math_engine = AdvancedMathEngine()
            self.parser = MathParser()
            self.plotter = Plotter()
            self.history_manager = HistoryManager()
            self.latex_manager = LaTeXDisplayManager()
            
            # Mathematical symbols
            self.symbols = {
                'x': sp.Symbol('x'),
                'y': sp.Symbol('y'),
                'z': sp.Symbol('z'),
                't': sp.Symbol('t')
            }
            self.current_var = self.symbols['x']
            
            # Application state
            self.current_result = None
            self.current_steps = []
            self.is_calculating = False
            self.last_result = "0"  # ANS (Last Answer)
            
            # UI state
            self.current_function = ""
            self.auto_parentheses = True
            self.cursor_positions = {}  # Track cursor positions for smart navigation
            
            # LaTeX display state
            self.preview_enabled = True
            self.auto_preview_delay = 200  # milliseconds (reduced for faster updates)
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            messagebox.showerror("Error", "No se pudieron inicializar los componentes")
            raise
    
    def setup_ui(self):
        """Setup the fixed layout user interface"""
        try:
            # Main container
            self.main_frame = ttk.Frame(self.root)
            self.main_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Create sections
            self.create_toolbar()
            self.create_fixed_layout_main_panel()
            self.create_status_bar()
            
        except Exception as e:
            logger.error(f"Error setting up UI: {str(e)}")
            messagebox.showerror("Error", "No se pudo configurar la interfaz")
            raise
    
    def create_toolbar(self):
        """Create the professional toolbar"""
        try:
            toolbar = ttk.Frame(self.main_frame)
            toolbar.pack(fill="x", pady=(0, 8))
            
            # Left section - File operations
            file_frame = ttk.Frame(toolbar)
            file_frame.pack(side="left", padx=5)
            
            self.create_tooltip_button(file_frame, "📁 Nuevo", "Nueva cálculo (Ctrl+L)", 
                                      self.new_calculation, width=8)
            self.create_tooltip_button(file_frame, "💾 Guardar", "Guardar en historial (Ctrl+S)", 
                                      self.save_result, width=8)
            self.create_tooltip_button(file_frame, "📋 Historial", "Ver historial (Ctrl+H)", 
                                      self.show_history, width=8)
            
            # Separator
            ttk.Separator(toolbar, orient="vertical").pack(side="left", padx=8, fill="y")
            
            # Center section - Main operations
            ops_frame = ttk.Frame(toolbar)
            ops_frame.pack(side="left", padx=5)
            
            self.calculate_btn = self.create_tooltip_button(ops_frame, "🧮 Calcular", 
                                                           "Calcular integral (Ctrl+Enter)", 
                                                           self.calculate_integral, 
                                                           style="Accent.TButton", width=10)
            self.create_tooltip_button(ops_frame, "📊 Graficar", "Graficar función (Ctrl+G)", 
                                      self.plot_function, width=10)
            self.create_tooltip_button(ops_frame, "🎨 Tema", "Cambiar tema (Ctrl+T)", 
                                      self.toggle_theme, width=8)
            
            # Separator
            ttk.Separator(toolbar, orient="vertical").pack(side="left", padx=8, fill="y")
            
            # Right section - LaTeX options
            latex_frame = ttk.Frame(toolbar)
            latex_frame.pack(side="right", padx=5)
            
            self.preview_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(latex_frame, text="📝 Preview", variable=self.preview_var,
                           command=self.toggle_preview).pack(side="left", padx=2)
            
            self.create_tooltip_button(latex_frame, "🎨 LaTeX", "Alternar renderizado LaTeX", 
                                      self.toggle_latex_mode, width=8)
            
            # Help
            self.create_tooltip_button(latex_frame, "📖 Ayuda", "Ayuda rápida (F1)", 
                                      self.show_help, width=8)
            
        except Exception as e:
            logger.error(f"Error creating toolbar: {str(e)}")
            raise
    
    def create_tooltip_button(self, parent, text, tooltip, command, width=None, style=None):
        """Create a button with tooltip"""
        btn = ttk.Button(parent, text=text, command=command, style=style, width=width)
        btn.pack(side="left", padx=2)
        
        # Create tooltip
        self.create_tooltip(btn, tooltip)
        
        return btn
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", 
                             relief="solid", borderwidth=1, font=("Arial", 9))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def create_fixed_layout_main_panel(self):
        """Create the fixed layout main panel with repositioned results"""
        try:
            # Main container with 3-column layout
            main_container = ttk.Frame(self.main_frame)
            main_container.pack(fill="both", expand=True)
            
            # Configure grid weights for 3-column layout
            main_container.grid_rowconfigure(0, weight=2)  # Input and preview row
            main_container.grid_rowconfigure(1, weight=3)  # Results row  
            main_container.grid_rowconfigure(2, weight=1)  # Graph row
            main_container.grid_columnconfigure(0, weight=2)  # Input panel
            main_container.grid_columnconfigure(1, weight=3)  # Results panel
            main_container.grid_columnconfigure(2, weight=1)  # Preview panel
            
            # === ROW 1: INPUT AND PREVIEW ===
            input_row = ttk.Frame(main_container)
            input_row.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 8))
            
            input_row.grid_columnconfigure(0, weight=2)  # Input
            input_row.grid_columnconfigure(1, weight=1)  # Preview
            
            # Left: Input controls (2/3 of width)
            input_panel = ttk.Frame(input_row)
            input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
            
            self.create_input_section(input_panel)
            self.create_professional_keypad_section(input_panel)
            
            # Right: Preview panel (1/3 of width)
            preview_panel = ttk.Frame(input_row)
            preview_panel.grid(row=0, column=1, sticky="nsew")
            
            self.create_preview_panel(preview_panel)
            
            # === ROW 2: RESULTS (FULL WIDTH) ===
            results_row = ttk.Frame(main_container)
            results_row.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(8, 0))
            
            self.create_repositioned_results_section(results_row)
            
            # === ROW 3: GRAPH (FULL WIDTH) ===
            graph_row = ttk.Frame(main_container)
            graph_row.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(8, 0))
            
            self.create_graph_section(graph_row)
            
        except Exception as e:
            logger.error(f"Error creating fixed layout main panel: {str(e)}")
            raise
    
    def create_input_section(self, parent):
        """Create the input section"""
        try:
            # Configuration frame
            config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración", padding=8)
            config_frame.pack(fill="x", pady=(0, 8))
            
            # First row - Type and variable
            row1 = ttk.Frame(config_frame)
            row1.pack(fill="x", pady=(0, 5))
            
            # Integral type
            type_frame = ttk.Frame(row1)
            type_frame.pack(side="left", fill="x", expand=True)
            
            ttk.Label(type_frame, text="🎯 Método:").pack(side="left", padx=(0, 5))
            self.integral_type_var = tk.StringVar(value="Automático")
            self.integral_type = ttk.Combobox(type_frame, textvariable=self.integral_type_var, 
                                             width=18, state="readonly")
            self.integral_type['values'] = (
                'Automático', 'Directa', 'Sustitución', 'Por Partes', 
                'Fracciones Parciales', 'Trigonométrica', 'Racional', 'Exponencial'
            )
            self.integral_type.pack(side="left", padx=5)
            
            # Variable
            var_frame = ttk.Frame(row1)
            var_frame.pack(side="right", padx=(10, 0))
            
            ttk.Label(var_frame, text="📊 Variable:").pack(side="left", padx=(0, 5))
            self.variable_var = tk.StringVar(value="x")
            self.variable_combo = ttk.Combobox(var_frame, textvariable=self.variable_var, 
                                              width=6, state="readonly")
            self.variable_combo['values'] = ('x', 'y', 'z', 't', 'u', 'v')
            self.variable_combo.pack(side="left", padx=5)
            self.variable_combo.bind('<<ComboboxSelected>>', self.on_variable_change)
            
            # Second row - Definite integral
            row2 = ttk.Frame(config_frame)
            row2.pack(fill="x")
            
            self.definite_var = tk.BooleanVar(value=False)
            ttk.Checkbutton(row2, text="📏 Integral definida", 
                           variable=self.definite_var,
                           command=self.toggle_limits).pack(side="left")
            
            # Limits frame (initially hidden)
            self.limits_frame = ttk.Frame(row2)
            
            ttk.Label(self.limits_frame, text="De:").pack(side="left", padx=(15, 3))
            self.lower_limit = ttk.Entry(self.limits_frame, width=8, font=('Courier', 10))
            self.lower_limit.pack(side="left", padx=2)
            self.lower_limit.insert(0, "0")
            
            ttk.Label(self.limits_frame, text="a:").pack(side="left", padx=(8, 3))
            self.upper_limit = ttk.Entry(self.limits_frame, width=8, font=('Courier', 10))
            self.upper_limit.pack(side="left", padx=2)
            self.upper_limit.insert(0, "1")
            
            # Editor frame
            editor_frame = ttk.LabelFrame(parent, text="📝 Editor Matemático", padding=8)
            editor_frame.pack(fill="x", pady=(0, 8))
            
            # Create working math editor
            self.create_working_latex_editor(editor_frame)
            
            # Quick actions frame
            actions_frame = ttk.Frame(parent)
            actions_frame.pack(fill="x")
            
            ttk.Button(actions_frame, text="🧹 Limpiar", command=self.clear_editor, width=8).pack(side="left", padx=2)
            ttk.Button(actions_frame, text="📋 ANS", command=self.insert_ans, width=8).pack(side="left", padx=2)
            ttk.Button(actions_frame, text="🔄 Rehacer", command=self.redo_input, width=8).pack(side="left", padx=2)
            
            # Validation status
            self.validation_label = ttk.Label(actions_frame, text="✅ Válido", 
                                           font=("Arial", 9), foreground="green")
            self.validation_label.pack(side="right", padx=5)
            
        except Exception as e:
            logger.error(f"Error creating input section: {str(e)}")
            raise
    
    def create_working_latex_editor(self, parent):
        """Create working editor"""
        try:
            # Main editor
            self.editor_text = tk.Text(parent, height=3, font=('Courier', 12), 
                                      wrap=tk.NONE, undo=True, maxundo=-1)
            self.editor_text.pack(fill="x", pady=(0, 5))
            
            # Configure text tags for syntax highlighting
            self.editor_text.tag_configure("function", foreground="#0066cc")
            self.editor_text.tag_configure("number", foreground="#cc6600")
            self.editor_text.tag_configure("operator", foreground="#666666")
            self.editor_text.tag_configure("integral", foreground="#8e44ad", font=("Courier", 12, "bold"))
            self.editor_text.tag_configure("differential", foreground="#27ae60")
            self.editor_text.tag_configure("error", background="#ffe6e6")
            
            # Bind events for enhanced functionality
            self.editor_text.bind('<KeyRelease>', self.on_editor_key_release)
            self.editor_text.bind('<Key>', self.on_editor_key_press)
            self.editor_text.bind('<Button-1>', self.on_editor_click)
            
            # Initialize with example
            self.editor_text.insert("1.0", "x**2 + 3*x + 2")
            self.current_function = "x**2 + 3*x + 2"
            
            # Status indicator
            self.editor_status = ttk.Label(parent, text="📝 Listo para editar", 
                                         font=("Arial", 9), foreground="gray")
            self.editor_status.pack(fill="x")
            
        except Exception as e:
            logger.error(f"Error creating working LaTeX editor: {str(e)}")
            raise
    
    def create_preview_panel(self, parent):
        """Create the preview panel"""
        try:
            # Preview frame
            preview_frame = ttk.LabelFrame(parent, text="📝 Preview", padding=8)
            preview_frame.pack(fill="both", expand=True)
            
            # Preview display area
            self.preview_display = ttk.Frame(preview_frame)
            self.preview_display.pack(fill="both", expand=True)
            
            # Initial preview
            self.update_preview_immediately()
            
        except Exception as e:
            logger.error(f"Error creating preview panel: {str(e)}")
            raise
    
    def create_professional_keypad_section(self, parent):
        """Create professional scientific keypad"""
        try:
            keypad_frame = ttk.LabelFrame(parent, text="🔢 Teclado Científico", padding=8)
            keypad_frame.pack(fill="both", expand=True)
            
            # Create professional keypad
            self.create_professional_keypad(keypad_frame)
            
        except Exception as e:
            logger.error(f"Error creating keypad section: {str(e)}")
            raise
    
    def create_professional_keypad(self, parent):
        """Create professional scientific keypad"""
        try:
            # Main keypad container
            keypad_container = ttk.Frame(parent)
            keypad_container.pack(fill="both", expand=True)
            
            # Configure grid
            for i in range(10):
                keypad_container.grid_rowconfigure(i, weight=1)
            for i in range(6):
                keypad_container.grid_columnconfigure(i, weight=1)
            
            # === BLOQUE 1: BÁSICO ===
            self.create_keypad_section_title(keypad_container, "🔢 Básico", 0, 0, 6)
            
            # Numbers and operations
            self.create_keypad_button(keypad_container, "7", "7", 1, 0)
            self.create_keypad_button(keypad_container, "8", "8", 1, 1)
            self.create_keypad_button(keypad_container, "9", "9", 1, 2)
            self.create_keypad_button(keypad_container, "÷", "/", 1, 3)
            self.create_keypad_button(keypad_container, "⌫", "(", 1, 4)
            self.create_keypad_button(keypad_container, "⌣", ")", 1, 5)
            
            self.create_keypad_button(keypad_container, "4", "4", 2, 0)
            self.create_keypad_button(keypad_container, "5", "5", 2, 1)
            self.create_keypad_button(keypad_container, "6", "6", 2, 2)
            self.create_keypad_button(keypad_container, "×", "*", 2, 3)
            self.create_keypad_button(keypad_container, "²", "**2", 2, 4)
            self.create_keypad_button(keypad_container, "ⁿ", "**", 2, 5)
            
            self.create_keypad_button(keypad_container, "1", "1", 3, 0)
            self.create_keypad_button(keypad_container, "2", "2", 3, 1)
            self.create_keypad_button(keypad_container, "3", "3", 3, 2)
            self.create_keypad_button(keypad_container, "-", "-", 3, 3)
            self.create_keypad_button(keypad_container, "+", "+", 3, 4)
            self.create_keypad_button(keypad_container, "🗑", "backspace", 3, 5)
            
            self.create_keypad_button(keypad_container, "0", "0", 4, 0)
            self.create_keypad_button(keypad_container, ".", ".", 4, 1)
            self.create_keypad_button(keypad_container, "π", "pi", 4, 2)
            self.create_keypad_button(keypad_container, "e", "e", 4, 3)
            self.create_keypad_button(keypad_container, "📋 ANS", "ans", 4, 4)
            self.create_keypad_button(keypad_container, "🧹", "clear", 4, 5)
            
            # === SEPARADOR ===
            separator1 = ttk.Separator(keypad_container, orient="horizontal")
            separator1.grid(row=5, column=0, columnspan=6, sticky="ew", pady=5)
            
            # === BLOQUE 2: FUNCIONES ===
            self.create_keypad_section_title(keypad_container, "📐 Funciones", 6, 0, 6)
            
            self.create_keypad_button(keypad_container, "sin", "sin(", 7, 0)
            self.create_keypad_button(keypad_container, "cos", "cos(", 7, 1)
            self.create_keypad_button(keypad_container, "tan", "tan(", 7, 2)
            self.create_keypad_button(keypad_container, "√", "sqrt(", 7, 3)
            self.create_keypad_button(keypad_container, "log", "log(", 7, 4)
            self.create_keypad_button(keypad_container, "ln", "ln(", 7, 5)
            
            # === SEPARADOR ===
            separator2 = ttk.Separator(keypad_container, orient="horizontal")
            separator2.grid(row=8, column=0, columnspan=6, sticky="ew", pady=5)
            
            # === BLOQUE 3: INTEGRALES ===
            self.create_keypad_section_title(keypad_container, "📐 Integrales", 9, 0, 6)
            
            self.create_integral_button(keypad_container, "∫", "indefinite", 10, 0, "Integral indefinida")
            self.create_integral_button(keypad_container, "∫_a^b", "definite", 10, 1, "Integral definida")
            self.create_integral_button(keypad_container, "∬", "double", 10, 2, "Integral doble")
            self.create_integral_button(keypad_container, "∭", "triple", 10, 3, "Integral triple")
            self.create_integral_button(keypad_container, "dx", "dx", 10, 4, "Diferencial dx")
            self.create_integral_button(keypad_container, "dy", "dy", 10, 5, "Diferencial dy")
            
        except Exception as e:
            logger.error(f"Error creating professional keypad: {str(e)}")
            raise
    
    def create_keypad_section_title(self, parent, title, row, col, colspan):
        """Create a section title for the keypad"""
        try:
            title_label = ttk.Label(parent, text=title, font=("Arial", 10, "bold"), 
                                  foreground="#2c3e50")
            title_label.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=(5, 2))
        except Exception as e:
            logger.error(f"Error creating section title: {str(e)}")
    
    def create_keypad_button(self, parent, display_text, insert_text, row, col):
        """Create a standard keypad button"""
        try:
            btn = ttk.Button(parent, text=display_text, width=6,
                          command=lambda t=insert_text: self.insert_to_editor(t))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            return btn
        except Exception as e:
            logger.error(f"Error creating keypad button: {str(e)}")
            return None
    
    def create_integral_button(self, parent, display_text, integral_type, row, col, tooltip):
        """Create an integral button"""
        try:
            btn = ttk.Button(parent, text=display_text, width=6,
                          command=lambda t=integral_type: self.insert_integral_structure(t))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            btn.configure(style="Accent.TButton")
            
            return btn
        except Exception as e:
            logger.error(f"Error creating integral button: {str(e)}")
            return None
    
    def create_repositioned_results_section(self, parent):
        """Create repositioned results section - FULL WIDTH"""
        try:
            # Results container with title
            results_container = ttk.Frame(parent)
            results_container.pack(fill="both", expand=True)
            
            # Title with status
            title_frame = ttk.Frame(results_container)
            title_frame.pack(fill="x", pady=(0, 8))
            
            ttk.Label(title_frame, text="📊 Resultados del Cálculo", 
                     font=("Arial", 14, "bold")).pack(side="left")
            
            # Loading indicator (initially hidden)
            self.loading_label = ttk.Label(title_frame, text="⏳ Procesando...", 
                                         font=("Arial", 10), foreground="orange")
            
            # Results notebook - FULL WIDTH
            self.results_notebook = ttk.Notebook(results_container)
            self.results_notebook.pack(fill="both", expand=True)
            
            # Create result tabs
            self.create_isolated_result_tab()
            self.create_isolated_steps_tab()
            self.create_isolated_verification_tab()
            self.create_text_mode_tab()
            
        except Exception as e:
            logger.error(f"Error creating repositioned results section: {str(e)}")
            raise
    
    def create_isolated_result_tab(self):
        """Create the isolated result tab"""
        try:
            result_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(result_frame, text="🎯 Resultado")
            
            # Result display
            self.latex_result_frame = ttk.Frame(result_frame)
            self.latex_result_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Initial message
            self.latex_result_label = ttk.Label(self.latex_result_frame, 
                                              text="📊 Ingresa una función y presiona 'Calcular'",
                                              font=("Arial", 12), foreground="gray")
            self.latex_result_label.pack(pady=20)
            
        except Exception as e:
            logger.error(f"Error creating isolated result tab: {str(e)}")
            raise
    
    def create_isolated_steps_tab(self):
        """Create the isolated steps tab"""
        try:
            steps_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(steps_frame, text="📝 Pasos")
            
            # Steps display with scroll
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
            
        except Exception as e:
            logger.error(f"Error creating isolated steps tab: {str(e)}")
            raise
    
    def create_isolated_verification_tab(self):
        """Create the isolated verification tab"""
        try:
            verify_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(verify_frame, text="✔️ Verificación")
            
            # Verification display
            self.latex_verify_frame = ttk.Frame(verify_frame)
            self.latex_verify_frame.pack(fill="both", expand=True, padx=8, pady=8)
            
            # Initial message
            self.latex_verify_label = ttk.Label(self.latex_verify_frame, 
                                              text="✔️ La verificación aparecerá aquí",
                                              font=("Arial", 12), foreground="gray")
            self.latex_verify_label.pack(pady=20)
            
        except Exception as e:
            logger.error(f"Error creating isolated verification tab: {str(e)}")
            raise
    
    def create_text_mode_tab(self):
        """Create the text mode tab"""
        try:
            text_frame = ttk.Frame(self.results_notebook)
            self.results_notebook.add(text_frame, text="📄 Modo Texto")
            
            # Text display
            text_container = ttk.Frame(text_frame)
            text_container.pack(fill="both", expand=True, padx=8, pady=8)
            
            self.text_result_display = scrolledtext.ScrolledText(
                text_container, wrap=tk.WORD, width=100, height=15,
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
            logger.error(f"Error creating text mode tab: {str(e)}")
            raise
    
    def create_graph_section(self, parent):
        """Create enhanced graph section"""
        try:
            graph_frame = ttk.LabelFrame(parent, text="📈 Visualización", padding=8)
            graph_frame.pack(fill="both", expand=True)
            
            # Graph controls
            controls_frame = ttk.Frame(graph_frame)
            controls_frame.pack(fill="x", pady=(0, 8))
            
            # Create button row
            button_row = ttk.Frame(controls_frame)
            button_row.pack(fill="x")
            
            self.create_tooltip_button(button_row, "📊 Graficar", "Graficar función", 
                                      self.plot_function, width=12)
            self.create_tooltip_button(button_row, "📈 Análisis", "Análisis completo", 
                                      self.plot_analysis, width=12)
            self.create_tooltip_button(button_row, "🔄 Actualizar", "Actualizar gráfica", 
                                      self.update_graph, width=12)
            
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
        """Create enhanced status bar"""
        try:
            status_frame = ttk.Frame(self.main_frame)
            status_frame.pack(fill="x", pady=(8, 0))
            
            # Main status
            self.status_bar = ttk.Label(status_frame, text="🚀 Calculadora con Layout Corregido", 
                                      relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
            self.status_bar.pack(side="left", fill="x", expand=True)
            
            # Info label
            self.info_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN, 
                                     font=("Arial", 9), width=30)
            self.info_label.pack(side="right", padx=(8, 0))
            
        except Exception as e:
            logger.error(f"Error creating status bar: {str(e)}")
            raise
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        try:
            self.root.bind('<Control-Return>', lambda e: self.calculate_integral())
            self.root.bind('<Control-g>', lambda e: self.plot_function())
            self.root.bind('<Control-l>', lambda e: self.new_calculation())
            self.root.bind('<Control-s>', lambda e: self.save_result())
            self.root.bind('<Control-h>', lambda e: self.show_history())
            self.root.bind('<F1>', lambda e: self.show_help())
            self.root.bind('<Control-t>', lambda e: self.toggle_theme())
            
        except Exception as e:
            logger.error(f"Error setting up shortcuts: {str(e)}")
    
    def apply_theme(self):
        """Apply the current theme"""
        try:
            theme = self.theme_manager.apply_theme(self.root)
            
            # Update text widgets with theme colors
            if hasattr(self, 'text_result_display'):
                self.text_result_display.config(bg=theme["entry_bg"], fg=theme["entry_fg"])
            if hasattr(self, 'editor_text'):
                self.editor_text.config(bg=theme["entry_bg"], fg=theme["entry_fg"])
                
        except Exception as e:
            logger.error(f"Error applying theme: {str(e)}")
    
    # Enhanced editor functionality
    def on_editor_key_release(self, event):
        """Handle key release events in editor"""
        try:
            self.current_function = self.editor_text.get("1.0", tk.END).strip()
            self.validate_expression()
            self.highlight_syntax()
            
            # Update preview immediately
            if self.preview_enabled:
                self.update_preview_immediately()
            
        except Exception as e:
            logger.error(f"Error in editor key release: {str(e)}")
    
    def update_preview_immediately(self):
        """Update preview immediately"""
        try:
            if not self.preview_enabled:
                return
            
            # Clear previous preview
            self.latex_manager.clear_frame(self.preview_display)
            
            # Get current expression
            if self.current_function:
                try:
                    self.latex_manager.display_preview(
                        self.current_function, 
                        self.preview_display
                    )
                except Exception as e:
                    logger.error(f"Error updating preview: {str(e)}")
                    # Show error message
                    error_label = ttk.Label(self.preview_display, 
                                          text=f"❌ Error en preview: {str(e)}",
                                          font=("Arial", 9), foreground="red")
                    error_label.pack()
            else:
                # Show empty message
                empty_label = ttk.Label(self.preview_display, 
                                      text="📝 Escribe una función para ver el preview",
                                      font=("Arial", 9), foreground="gray")
                empty_label.pack()
                
        except Exception as e:
            logger.error(f"Error in update preview immediately: {str(e)}")
    
    def on_editor_key_press(self, event):
        """Handle key press events"""
        try:
            char = event.char
            
            # Auto-close parentheses
            if self.auto_parentheses and char in "({[":
                self.editor_text.insert(tk.INSERT, char)
                self.editor_text.insert(tk.INSERT, self.get_matching_bracket(char))
                self.editor_text.mark_set(tk.INSERT, f"{self.editor_text.index(tk.INSERT)}-1c")
                return "break"
            
            # Auto-close functions
            if char.isalpha():
                self.check_function_autocomplete()
            
        except Exception as e:
            logger.error(f"Error in editor key press: {str(e)}")
    
    def on_editor_click(self, event):
        """Handle mouse clicks in editor"""
        try:
            self.update_editor_status()
        except Exception as e:
            logger.error(f"Error in editor click: {str(e)}")
    
    def get_matching_bracket(self, opening):
        """Get matching closing bracket"""
        brackets = {'(': ')', '{': '}', '[': ']'}
        return brackets.get(opening, '')
    
    def check_function_autocomplete(self):
        """Check if we should autocomplete a function"""
        try:
            text = self.editor_text.get("1.0", tk.INSERT)
            
            functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'abs', 'integrate', 'diff']
            
            for func in functions:
                if text.endswith(func):
                    next_char = self.editor_text.get(tk.INSERT, tk.INSERT + "1c")
                    if next_char != '(':
                        self.editor_text.insert(tk.INSERT, '(')
                        return
        except Exception as e:
            logger.error(f"Error in function autocomplete: {str(e)}")
    
    def validate_expression(self):
        """Validate the current expression"""
        try:
            if not self.current_function:
                self.validation_label.config(text="✅ Vacío", foreground="gray")
                return True
            
            try:
                sympy_expr = self.convert_to_sympy_format(self.current_function)
                validate_input(sympy_expr)
                self.parser.parse(sympy_expr)
                
                self.validation_label.config(text="✅ Válido", foreground="green")
                return True
                
            except Exception as e:
                self.validation_label.config(text="❌ Inválido", foreground="red")
                return False
                
        except Exception as e:
            logger.error(f"Error in validation: {str(e)}")
            self.validation_label.config(text="❓ Error", foreground="orange")
            return False
    
    def convert_to_sympy_format(self, expression):
        """Convert visual notation to SymPy format"""
        try:
            conversions = {
                r'√': 'sqrt', r'π': 'pi', r'∫': 'integrate', r'∂': 'diff',
                r'\^': '**', r'×': '*', r'÷': '/', r'≤': '<=', r'≥': '>=',
                r'≠': '!=', r'∞': 'oo', r'∑': 'summation', r'∏': 'product',
                r'∈': 'in', r'∉': 'not in', r'⊂': 'subset', r'⊃': 'superset',
                r'∪': 'union', r'∩': 'intersection', r'∅': 'EmptySet',
                r'ℝ': 'Reals', r'ℤ': 'Integers', r'ℕ': 'Naturals',
                r'ℂ': 'Complexes', r'ℚ': 'Rationals'
            }
            
            result = expression
            for pattern, replacement in conversions.items():
                result = re.sub(pattern, replacement, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error converting to SymPy format: {str(e)}")
            return expression
    
    def highlight_syntax(self):
        """Highlight syntax in the editor"""
        try:
            # Remove all tags
            for tag in ["function", "number", "operator", "integral", "differential", "error"]:
                self.editor_text.tag_remove(tag, "1.0", tk.END)
            
            # Highlight patterns
            functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'abs', 'pi', 'e', 
                        'integrate', 'diff', 'line_integral', 'nabla']
            for func in functions:
                self.highlight_pattern(func, "function")
            
            self.highlight_pattern(r'integrate\([^)]+\)', "integral")
            self.highlight_pattern(r'\b\d+\.?\d*\b', "number")
            self.highlight_pattern(r'[+\-*/^()]', "operator")
            self.highlight_pattern(r'd[xyz]', "differential")
            
        except Exception as e:
            logger.error(f"Error in syntax highlighting: {str(e)}")
    
    def highlight_pattern(self, pattern, tag):
        """Highlight a pattern in the editor"""
        try:
            text = self.editor_text.get("1.0", tk.END)
            
            matches = re.finditer(pattern, text)
            for match in matches:
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                self.editor_text.tag_add(tag, start_idx, end_idx)
                
        except Exception as e:
            logger.error(f"Error highlighting pattern {pattern}: {str(e)}")
    
    def update_editor_status(self):
        """Update the editor status"""
        try:
            cursor_pos = self.editor_text.index(tk.INSERT)
            line_num = cursor_pos.split('.')[0]
            col_num = cursor_pos.split('.')[1]
            
            self.editor_status.config(text=f"📝 Línea {line_num}, Columna {col_num}")
        except Exception as e:
            logger.error(f"Error updating editor status: {str(e)}")
    
    # Enhanced functionality methods
    def insert_to_editor(self, text):
        """Insert text into the editor"""
        try:
            if text == "backspace":
                cursor_pos = self.editor_text.index(tk.INSERT)
                if cursor_pos != "1.0":
                    self.editor_text.delete(f"{cursor_pos}-1c", cursor_pos)
            elif text == "clear":
                self.editor_text.delete("1.0", tk.END)
            elif text == "ans":
                self.insert_to_editor(self.last_result)
            else:
                cursor_pos = self.editor_text.index(tk.INSERT)
                self.editor_text.insert(cursor_pos, text)
            
            self.editor_text.focus_set()
            self.on_editor_key_release(None)
            
        except Exception as e:
            logger.error(f"Error inserting to editor: {str(e)}")
    
    def insert_integral_structure(self, integral_type):
        """Insert integral structure"""
        try:
            current_var = self.variable_var.get()
            cursor_pos = self.editor_text.index(tk.INSERT)
            
            if integral_type == "indefinite":
                structure = f"integrate( , {current_var})"
                self.editor_text.insert(cursor_pos, structure)
                new_pos = f"{cursor_pos}+{len('integrate(')}c"
                self.editor_text.mark_set(tk.INSERT, new_pos)
            elif integral_type == "definite":
                structure = f"integrate( , ({current_var}, , ))"
                self.editor_text.insert(cursor_pos, structure)
                new_pos = f"{cursor_pos}+{len('integrate(')}c"
                self.editor_text.mark_set(tk.INSERT, new_pos)
            elif integral_type == "double":
                structure = f"integrate(integrate( , {current_var}), y)"
                self.editor_text.insert(cursor_pos, structure)
                new_pos = f"{cursor_pos}+{len('integrate(integrate(')}c"
                self.editor_text.mark_set(tk.INSERT, new_pos)
            elif integral_type == "triple":
                structure = f"integrate(integrate(integrate( , {current_var}), y), z)"
                self.editor_text.insert(cursor_pos, structure)
                new_pos = f"{cursor_pos}+{len('integrate(integrate(integrate(')}c"
                self.editor_text.mark_set(tk.INSERT, new_pos)
            elif integral_type == "dx":
                self.editor_text.insert(cursor_pos, f"*{current_var}")
            elif integral_type == "dy":
                self.editor_text.insert(cursor_pos, "*y")
            elif integral_type == "dz":
                self.editor_text.insert(cursor_pos, "*z")
            
            self.editor_text.focus_set()
            self.on_editor_key_release(None)
            
        except Exception as e:
            logger.error(f"Error inserting integral structure: {str(e)}")
    
    def insert_ans(self):
        """Insert last answer"""
        try:
            self.insert_to_editor(self.last_result)
        except Exception as e:
            logger.error(f"Error inserting ANS: {str(e)}")
    
    def clear_editor(self):
        """Clear the editor"""
        try:
            self.editor_text.delete("1.0", tk.END)
            self.current_function = ""
            self.validation_label.config(text="✅ Vacío", foreground="gray")
            self.update_editor_status()
            self.update_preview_immediately()
        except Exception as e:
            logger.error(f"Error clearing editor: {str(e)}")
    
    def redo_input(self):
        """Redo last action"""
        try:
            self.editor_text.edit_redo()
        except Exception as e:
            logger.error(f"Error redoing input: {str(e)}")
    
    def toggle_preview(self):
        """Toggle LaTeX preview"""
        try:
            self.preview_enabled = self.preview_var.get()
            if self.preview_enabled:
                self.update_preview_immediately()
            else:
                self.latex_manager.clear_frame(self.preview_display)
        except Exception as e:
            logger.error(f"Error toggling preview: {str(e)}")
    
    def toggle_latex_mode(self):
        """Toggle between LaTeX and text mode"""
        try:
            self.results_notebook.select(3)  # Text mode tab
            messagebox.showinfo("Modo Cambiado", "Cambiado a modo texto. Usa las pestañas LaTeX para renderizado profesional.")
        except Exception as e:
            logger.error(f"Error toggling LaTeX mode: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between themes"""
        try:
            self.theme_manager.toggle_theme()
            self.apply_theme()
            theme_name = self.theme_manager.current_theme.capitalize()
            self.status_bar.config(text=f"🎨 Tema cambiado a {theme_name}")
        except Exception as e:
            logger.error(f"Error toggling theme: {str(e)}")
    
    def on_variable_change(self, event=None):
        """Handle variable change"""
        try:
            var_str = self.variable_var.get()
            if var_str in self.symbols:
                self.current_var = self.symbols[var_str]
            else:
                self.current_var = sp.Symbol(var_str)
                self.symbols[var_str] = self.current_var
        except Exception as e:
            logger.error(f"Error in variable change: {str(e)}")
    
    def toggle_limits(self):
        """Show/hide limits fields"""
        try:
            if self.definite_var.get():
                self.limits_frame.pack(side="left", padx=10)
            else:
                self.limits_frame.pack_forget()
        except Exception as e:
            logger.error(f"Error toggling limits: {str(e)}")
    
    def get_function_text(self):
        """Get function text in SymPy format"""
        try:
            raw_text = self.editor_text.get("1.0", tk.END).strip()
            return self.convert_to_sympy_format(raw_text)
        except Exception as e:
            logger.error(f"Error getting function text: {str(e)}")
            return ""
    
    def calculate_integral(self):
        """Calculate the integral"""
        if self.is_calculating:
            return
        
        if not self.validate_expression():
            messagebox.showwarning("Advertencia", "La expresión no es válida")
            return
        
        self.is_calculating = True
        self.show_loading(True)
        self.status_bar.config(text="🔄 Calculando...")
        
        # Run calculation in separate thread
        thread = threading.Thread(target=self._calculate_integral_thread)
        thread.daemon = True
        thread.start()
    
    def _calculate_integral_thread(self):
        """Thread for integral calculation"""
        try:
            func_str = self.get_function_text()
            if not func_str:
                self.root.after(0, lambda: messagebox.showwarning("Advertencia", "Ingresa una función"))
                return
            
            validate_input(func_str)
            func = self.parser.parse(func_str)
            
            # Get method
            method = None
            integral_type = self.integral_type_var.get()
            if integral_type != 'Automático':
                method_map = {
                    'Directa': 'direct', 'Sustitución': 'substitution',
                    'Por Partes': 'parts', 'Fracciones Parciales': 'partial_fractions',
                    'Trigonométrica': 'trigonometric', 'Racional': 'rational',
                    'Exponencial': 'exponential'
                }
                method = method_map.get(integral_type, 'direct')
            
            # Get limits if definite
            limits = None
            if self.definite_var.get():
                try:
                    lower = sp.sympify(self.lower_limit.get())
                    upper = sp.sympify(self.upper_limit.get())
                    limits = (lower, upper)
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showwarning("Advertencia", "Límites inválidos"))
                    return
            
            # Calculate with advanced engine
            result, steps = self.math_engine.solve_integral(func, self.current_var, method)
            
            # Save results
            self.current_result = result
            self.current_steps = steps
            self.last_result = str(result)
            
            # Update UI
            self.root.after(0, lambda: self._display_working_latex_results(func, result, steps, limits))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error in calculation: {str(e)}")
            self.root.after(0, lambda: self._display_error(error_msg))
        finally:
            self.is_calculating = False
            self.root.after(0, lambda: self.show_loading(False))
            self.root.after(0, lambda: self.status_bar.config(text="✅ Cálculo completado"))
    
    def show_loading(self, show):
        """Show or hide loading indicator"""
        try:
            if show:
                self.loading_label.pack(side="right", padx=10)
                self.calculate_btn.config(state="disabled")
            else:
                self.loading_label.pack_forget()
                self.calculate_btn.config(state="normal")
        except Exception as e:
            logger.error(f"Error showing loading: {str(e)}")
    
    def _display_working_latex_results(self, func, result, steps, limits):
        """Display results with working LaTeX rendering"""
        try:
            logger.info("Displaying working LaTeX results")
            
            # Clear previous displays
            self.latex_manager.clear_frame(self.latex_result_frame)
            self.latex_manager.clear_frame(self.latex_steps_frame)
            self.latex_manager.clear_frame(self.latex_verify_frame)
            
            # Display result
            if limits:
                title = f"∫_{limits[0]}^{limits[1]} f(x) dx"
            else:
                title = "∫ f(x) dx"
            
            logger.info(f"Displaying result: {result}")
            self.latex_manager.display_expression_in_frame(
                result, self.latex_result_frame, title, 
                color="#27ae60", fontsize=16
            )
            
            # Display steps
            if steps:
                logger.info(f"Displaying {len(steps)} steps")
                for i, step in enumerate(steps):
                    if step.get('type') in ['method_step', 'transformation']:
                        step_frame = ttk.Frame(self.latex_steps_frame)
                        step_frame.pack(fill="x", pady=5)
                        
                        step_title = step.get('title', f'Paso {i+1}')
                        step_expr = step.get('expression', '')
                        
                        if step_expr:
                            logger.info(f"Displaying step {i+1}: {step_expr}")
                            self.latex_manager.display_expression_in_frame(
                                step_expr, step_frame, step_title,
                                color="#3498db", fontsize=14
                            )
            
            # Display verification
            try:
                derivative = sp.diff(result, self.current_var)
                
                if sp.simplify(derivative - func) == 0:
                    verify_title = "✅ Verificación Exitosa"
                    verify_expr = f"d/dx({result}) = {func}"
                    verify_color = "#27ae60"
                else:
                    verify_title = "⚠️ Verificación Parcial"
                    verify_expr = f"d/dx({result}) ≈ {func}"
                    verify_color = "#e74c3c"
                
                logger.info(f"Displaying verification: {verify_expr}")
                self.latex_manager.display_expression_in_frame(
                    verify_expr, self.latex_verify_frame, verify_title,
                    color=verify_color, fontsize=14
                )
                
            except Exception as e:
                logger.error(f"Error in LaTeX verification: {str(e)}")
                error_label = ttk.Label(self.latex_verify_frame, 
                                      text="❌ No se pudo verificar",
                                      font=("Arial", 11), foreground="red")
                error_label.pack(pady=10)
            
            # Update text mode
            self._display_text_results(func, result, steps, limits)
            
            # Update status
            self.info_label.config(text=f"✅ {self.integral_type_var.get()}")
            
            logger.info("Working LaTeX results displayed successfully")
            
        except Exception as e:
            logger.error(f"Error displaying working LaTeX results: {str(e)}")
            messagebox.showerror("Error", "No se pudieron mostrar los resultados LaTeX")
    
    def _display_text_results(self, func, result, steps, limits):
        """Display results in text mode"""
        try:
            self.text_result_display.config(state=tk.NORMAL)
            self.text_result_display.delete("1.0", tk.END)
            
            # Format and display result
            if limits:
                antiderivative = result.subs(sp.Symbol('C'), 0)
                upper_val = antiderivative.subs(self.current_var, limits[1])
                lower_val = antiderivative.subs(self.current_var, limits[0])
                definite_result = sp.simplify(upper_val - lower_val)
                
                result_text = f"🎯 INTEGRAL DEFINIDA\n\n"
                result_text += f"∫{limits[0]}^{limits[1]} {func} d{self.current_var.name}\n\n"
                result_text += f"Resultado: {definite_result}\n\n"
                
                try:
                    numeric = float(definite_result.evalf())
                    result_text += f"Valor numérico: {numeric:.6f}\n\n"
                except:
                    pass
            else:
                result_text = f"🎯 INTEGRAL INDEFINIDA\n\n"
                result_text += f"∫ {func} d{self.current_var.name}\n\n"
                result_text += f"Resultado: {result}\n\n"
            
            result_text += f"Método: {self.integral_type_var.get()}\n"
            result_text += f"Variable: {self.current_var.name}\n"
            
            self.text_result_display.insert(tk.END, result_text, "method")
            self.text_result_display.tag_add("result", "4.0", "4.end")
            self.text_result_display.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"Error displaying text results: {str(e)}")
    
    def _display_error(self, error_msg):
        """Display error message"""
        try:
            self.latex_manager.clear_frame(self.latex_result_frame)
            
            error_label = ttk.Label(self.latex_result_frame, 
                                  text=f"❌ ERROR\n\n{error_msg}",
                                  font=("Arial", 12), foreground="red")
            error_label.pack(pady=20)
            
            self.text_result_display.config(state=tk.NORMAL)
            self.text_result_display.delete("1.0", tk.END)
            self.text_result_display.insert(tk.END, f"❌ ERROR\n\n{error_msg}")
            self.text_result_display.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"Error displaying error: {str(e)}")
    
    def plot_function(self):
        """Plot the function"""
        try:
            func_str = self.get_function_text()
            if not func_str:
                messagebox.showwarning("Advertencia", "Ingresa una función")
                return
            
            if not self.validate_expression():
                messagebox.showwarning("Advertencia", "La expresión no es válida")
                return
            
            validate_input(func_str)
            func = self.parser.parse(func_str)
            
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
            fig = self.plotter.plot_interactive(func, self.current_var, a, b, limits, show_area=bool(limits))
            
            # Clear previous plot
            self._clear_graph()
            
            # Show new plot
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            self.status_bar.config(text="📊 Gráfica generada")
            self.info_label.config(text="📈 Gráfica lista")
            
        except Exception as e:
            logger.error(f"Error plotting function: {str(e)}")
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")
    
    def plot_analysis(self):
        """Generate complete analysis plot"""
        try:
            func_str = self.get_function_text()
            if not func_str:
                messagebox.showwarning("Advertencia", "Ingresa una función")
                return
            
            if not self.validate_expression():
                messagebox.showwarning("Advertencia", "La expresión no es válida")
                return
            
            validate_input(func_str)
            func = self.parser.parse(func_str)
            
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
            fig = self.plotter.plot_with_analysis(func, self.current_var, a, b, limits)
            
            # Clear previous plot
            self._clear_graph()
            
            # Show new plot
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            self.status_bar.config(text="📈 Análisis completo")
            self.info_label.config(text="📊 Análisis listo")
            
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
    
    def _clear_graph(self):
        """Clear the graph area"""
        try:
            for widget in self.graph_frame.winfo_children():
                if hasattr(widget, 'winfo_class') and widget.winfo_class() == 'Canvas':
                    widget.destroy()
            
            if hasattr(self, 'graph_label'):
                self.graph_label.pack(pady=20)
        except Exception as e:
            logger.error(f"Error clearing graph: {str(e)}")
    
    def new_calculation(self):
        """Start a new calculation"""
        try:
            self.clear_editor()
            
            # Clear displays
            self.latex_manager.clear_frame(self.latex_result_frame)
            self.latex_manager.clear_frame(self.latex_steps_frame)
            self.latex_manager.clear_frame(self.latex_verify_frame)
            
            # Clear text display
            self.text_result_display.config(state=tk.NORMAL)
            self.text_result_display.delete("1.0", tk.END)
            self.text_result_display.config(state=tk.DISABLED)
            
            # Restore initial labels
            self.latex_result_label = ttk.Label(self.latex_result_frame, 
                                              text="📊 Ingresa una función y presiona 'Calcular'",
                                              font=("Arial", 12), foreground="gray")
            self.latex_result_label.pack(pady=20)
            
            self.latex_steps_label = ttk.Label(self.latex_steps_frame, 
                                             text="📝 Los pasos aparecerán aquí",
                                             font=("Arial", 12), foreground="gray")
            self.latex_steps_label.pack(pady=20)
            
            self.latex_verify_label = ttk.Label(self.latex_verify_frame, 
                                              text="✔️ La verificación aparecerá aquí",
                                              font=("Arial", 12), foreground="gray")
            self.latex_verify_label.pack(pady=20)
            
            self._clear_graph()
            
            self.current_result = None
            self.current_steps = []
            
            self.status_bar.config(text="🚀 Calculadora con Layout Corregido")
            self.info_label.config(text="")
            
        except Exception as e:
            logger.error(f"Error in new calculation: {str(e)}")
    
    def save_result(self):
        """Save the current result"""
        try:
            if self.current_result:
                func_str = self.get_function_text()
                self.history_manager.add_entry(func_str, self.integral_type_var.get())
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
    
    def show_help(self):
        """Show help dialog"""
        try:
            help_window = tk.Toplevel(self.root)
            help_window.title("📖 Ayuda")
            help_window.geometry("750x700")
            
            help_text = """
🎓 CALCULADORA DE INTEGRALES PRO - Layout Fixed

🔥 CARACTERÍSTICAS:
• Layout optimizado de 3 filas
• Panel de resultados reubicado
• Preview lateral dedicado
• Teclado científico completo
• Resultados con formato profesional

📐 ESTRUCTURA DEL LAYOUT:
• FILA 1: Entrada (2/3) + Preview (1/3)
• FILA 2: Resultados (ancho completo)
• FILA 3: Gráficos (ancho completo)

📝 PANEL DE ENTRADA:
• Editor matemático con validación
• Teclado de funciones e integrales
• Configuración de variables y límites

📝 PANEL DE PREVIEW:
• Preview LaTeX en tiempo real
• Posicionado lateral para no interferir
• Actualización inmediata al escribir

📊 PANEL DE RESULTADOS:
• Resultado principal con formato LaTeX
• Pasos detallados del cálculo
• Verificación automática
• Modo texto como fallback
• Ancho completo para mejor visualización

📈 PANEL DE GRÁFICOS:
• Graficación interactiva
• Análisis completo
• Visualización de áreas

⌨️ ATAJOS:
• Ctrl+Enter: Calcular integral
• Ctrl+G: Graficar función
• Ctrl+L: Nueva cálculo
• Ctrl+S: Guardar resultado
• Ctrl+H: Mostrar historial
• Ctrl+T: Cambiar tema
• F1: Mostrar ayuda

💡 CONSEJOS:
• Usa el panel izquierdo para entrada
• Mira el preview lateral mientras escribes
• Los resultados aparecen abajo con todo el ancho
• Revisa las pestañas para más detalles

🎯 NIVEL: Wolfram Alpha / GeoGebra
            """
            
            text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Arial', 10))
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, help_text)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            logger.error(f"Error showing help: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        try:
            about_text = """
🧮 CALCULADORA DE INTEGRALES PRO
Versión 9.0 - Layout Fixed

🎯 DESARROLLADO CON:
• Python 3.14
• Tkinter (Interfaz Gráfica)
• SymPy (Motor Matemático)
• Matplotlib (LaTeX Rendering)
• NumPy (Cálculos Numéricos)

🏆 CARACTERÍSTICAS:
• Layout optimizado de 3 filas
• Panel de resultados reubicado
• Preview lateral dedicado
• Teclado científico avanzado
• Motor de cálculo profesional
• Visualización interactiva
• Temas profesional claro/oscuro

🎓 IDEAL PARA:
• Estudiantes de cálculo avanzado
• Profesores de matemáticas
• Ingenieros y científicos
• Investigadores matemáticos

🚀 NIVEL: Wolfram Alpha / GeoGebra

Diseñado con ❤️ para la educación matemática profesional
            """
            
            messagebox.showinfo("Acerca de", about_text)
            
        except Exception as e:
            logger.error(f"Error showing about: {str(e)}")


# Use the fixed layout class
LaTeXIntegralCalculator = FixedLayoutLaTeXCalculator

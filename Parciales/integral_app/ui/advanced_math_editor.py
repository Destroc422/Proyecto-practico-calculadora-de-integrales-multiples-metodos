"""
Advanced Math Editor with Microsoft Mathematics-style input
Provides intelligent mathematical input with autocomplete and symbol palette
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import List, Dict, Optional, Callable, Any
import re
from collections import deque

# Core modules
from core.microsoft_math_engine import MicrosoftMathEngine, MathParsingError

logger = logging.getLogger(__name__)


class AdvancedMathEditor:
    """Advanced mathematical editor with Microsoft Mathematics-style features"""
    
    def __init__(self, parent, on_expression_change: Optional[Callable] = None):
        self.parent = parent
        self.on_expression_change = on_expression_change
        
        # Initialize math engine
        self.math_engine = MicrosoftMathEngine()
        
        # Editor state
        self.current_text = ""
        self.cursor_position = 0
        self.suggestions = []
        self.current_suggestion_index = 0
        self.showing_suggestions = False
        
        # History for undo/redo
        self.history = deque(maxlen=50)
        self.redo_stack = deque(maxlen=50)
        
        # Create the editor
        self.create_editor()
        
        logger.info("Advanced Math Editor initialized")
    
    def create_editor(self):
        """Create the advanced math editor interface"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Editor toolbar
        self.create_toolbar(main_frame)
        
        # Editor area
        self.create_editor_area(main_frame)
        
        # Symbol palette
        self.create_symbol_palette(main_frame)
        
        # Suggestions popup
        self.create_suggestions_popup()
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_toolbar(self, parent):
        """Create editor toolbar with formatting options"""
        toolbar = tk.Frame(parent, bg='#ecf0f1', height=35)
        toolbar.pack(fill="x", pady=(0, 5))
        toolbar.pack_propagate(False)
        
        # Undo/Redo buttons
        ttk.Button(toolbar, text="Deshacer", command=self.undo).pack(side="left", padx=2)
        ttk.Button(toolbar, text="Rehacer", command=self.redo).pack(side="left", padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        
        # Common symbols
        symbols = ["×", "÷", "²", "³", "±", "°", "½", "¼", "¾"]
        for symbol in symbols:
            btn = tk.Button(toolbar, text=symbol, font=('Arial', 10, 'bold'),
                          bg='#3498db', fg='white', padx=8, pady=2,
                          command=lambda s=symbol: self.insert_symbol(s))
            btn.pack(side="left", padx=1)
        
        # Separator
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=5)
        
        # Function buttons
        functions = ["sin", "cos", "tan", "log", "ln", "exp", "sqrt", "abs"]
        for func in functions:
            btn = tk.Button(toolbar, text=func, font=('Arial', 9, 'bold'),
                          bg='#27ae60', fg='white', padx=6, pady=2,
                          command=lambda f=func: self.insert_function(f))
            btn.pack(side="left", padx=1)
        
        # Right side options
        ttk.Button(toolbar, text="Limpiar", command=self.clear).pack(side="right", padx=2)
        ttk.Button(toolbar, text="Validar", command=self.validate_expression).pack(side="right", padx=2)
    
    def create_editor_area(self, parent):
        """Create the main text editing area"""
        # Editor frame
        editor_frame = ttk.LabelFrame(parent, text="Editor Matemático Avanzado", padding=5)
        editor_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Text widget with enhanced features
        self.text_widget = tk.Text(editor_frame, height=4, font=('Courier New', 12, 'bold'),
                                   wrap=tk.NONE, undo=True, maxundo=-1,
                                   bg='#2c3e50', fg='#ecf0f1', insertbackground='#3498db',
                                   selectbackground='#3498db', relief=tk.FLAT, bd=0)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(editor_frame, orient="vertical", command=self.text_widget.yview)
        h_scrollbar = ttk.Scrollbar(editor_frame, orient="horizontal", command=self.text_widget.xview)
        
        self.text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)
        
        # Configure tags for syntax highlighting
        self.setup_syntax_highlighting()
        
        # Bind events
        self.bind_editor_events()
        
        # Initialize with example
        self.text_widget.insert("1.0", "x² + 2*x + 1")
        self.current_text = "x² + 2*x + 1"
    
    def setup_syntax_highlighting(self):
        """Setup syntax highlighting tags"""
        # Function highlighting
        self.text_widget.tag_configure("function", foreground="#3498db", font=('Courier New', 12, 'bold'))
        
        # Number highlighting
        self.text_widget.tag_configure("number", foreground="#e67e22", font=('Courier New', 12, 'bold'))
        
        # Operator highlighting
        self.text_widget.tag_configure("operator", foreground="#95a5a6", font=('Courier New', 12))
        
        # Variable highlighting
        self.text_widget.tag_configure("variable", foreground="#f39c12", font=('Courier New', 12, 'bold'))
        
        # Error highlighting
        self.text_widget.tag_configure("error", background="#e74c3c", foreground='white')
        
        # Parentheses highlighting
        self.text_widget.tag_configure("parenthesis", foreground="#9b59b6", font=('Courier New', 12, 'bold'))
    
    def bind_editor_events(self):
        """Bind editor events for intelligent behavior"""
        # Text change events
        self.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.text_widget.bind('<Key>', self.on_key_press)
        
        # Cursor movement
        self.text_widget.bind('<Button-1>', self.on_cursor_move)
        self.text_widget.bind('<Up>', self.on_cursor_up)
        self.text_widget.bind('<Down>', self.on_cursor_down)
        
        # Tab completion
        self.text_widget.bind('<Tab>', self.on_tab_completion)
        self.text_widget.bind('<Return>', self.on_enter_pressed)
        
        # Escape to hide suggestions
        self.text_widget.bind('<Escape>', self.hide_suggestions)
    
    def create_symbol_palette(self, parent):
        """Create comprehensive symbol palette"""
        palette_frame = ttk.LabelFrame(parent, text="Paleta de Símbolos", padding=5)
        palette_frame.pack(fill="x", pady=(0, 5))
        
        # Create notebook for symbol categories
        self.symbol_notebook = ttk.Notebook(palette_frame)
        self.symbol_notebook.pack(fill="both", expand=True)
        
        # Symbol categories
        categories = {
            "Básicos": ["+", "-", "×", "÷", "=", "(", ")", "[", "]", "{", "}", "<", ">"],
            "Potencias": ["²", "³", "¹", "¼", "½", "¾", "^", "sqrt", "nroot"],
            "Griegas": ["alpha", "beta", "gamma", "delta", "epsilon", "theta", "lambda", "mu", "pi", "sigma", "phi", "omega"],
            "Funciones": ["sin", "cos", "tan", "cot", "sec", "csc", "asin", "acos", "atan", "sinh", "cosh", "tanh"],
            "Logaritmos": ["log", "ln", "exp", "log2", "log10"],
            "Cálculo": ["int", "d/dx", "sum", "prod", "limit", "partial"],
            "Constantes": ["pi", "e", "infinity", "i"],
            "Operadores": ["±", "!", "°", "mod", "gcd", "lcm"]
        }
        
        # Create tabs for each category
        for category, symbols in categories.items():
            tab_frame = ttk.Frame(self.symbol_notebook)
            self.symbol_notebook.add(tab_frame, text=category)
            
            # Create buttons for symbols
            self.create_symbol_buttons(tab_frame, symbols)
    
    def create_symbol_buttons(self, parent, symbols):
        """Create symbol buttons for a category"""
        # Calculate grid dimensions
        cols = 6
        rows = (len(symbols) + cols - 1) // cols
        
        for i, symbol in enumerate(symbols):
            row = i // cols
            col = i % cols
            
            # Determine button style based on symbol type
            if symbol in ["+", "-", "×", "÷", "="]:
                bg_color = '#3498db'
            elif symbol in ["sin", "cos", "tan", "log", "ln", "exp"]:
                bg_color = '#27ae60'
            elif symbol in ["pi", "e", "infinity"]:
                bg_color = '#e74c3c'
            else:
                bg_color = '#95a5a6'
            
            btn = tk.Button(parent, text=symbol, font=('Arial', 9, 'bold'),
                          bg=bg_color, fg='white', padx=8, pady=4,
                          command=lambda s=symbol: self.insert_symbol(s))
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def create_suggestions_popup(self):
        """Create suggestions popup window"""
        self.suggestions_popup = tk.Toplevel(self.parent)
        self.suggestions_popup.withdraw()  # Hide initially
        self.suggestions_popup.overrideredirect(True)  # No window decorations
        
        # Suggestions listbox
        self.suggestions_listbox = tk.Listbox(self.suggestions_popup, font=('Arial', 10),
                                              bg='white', selectbackground='#3498db',
                                              activestyle='none', height=6)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.suggestions_popup, orient="vertical", 
                                 command=self.suggestions_listbox.yview)
        self.suggestions_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.suggestions_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind events
        self.suggestions_listbox.bind('<Double-Button-1>', self.apply_suggestion)
        self.suggestions_listbox.bind('<Return>', self.apply_suggestion)
        self.suggestions_listbox.bind('<Up>', self.on_suggestion_up)
        self.suggestions_listbox.bind('<Down>', self.on_suggestion_down)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, bg='#34495e', height=20)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(status_frame, text=" Listo", 
                                   font=('Arial', 8), fg='white', bg='#34495e')
        self.status_label.pack(side="left", padx=5, pady=2)
        
        # Position label
        self.position_label = tk.Label(status_frame, text="Línea: 1, Columna: 1", 
                                     font=('Arial', 8), fg='#95a5a6', bg='#34495e')
        self.position_label.pack(side="right", padx=5, pady=2)
        
        # Validation status
        self.validation_status = tk.Label(status_frame, text="", 
                                        font=('Arial', 8, 'bold'), fg='#27ae60', bg='#34495e')
        self.validation_status.pack(side="right", padx=10, pady=2)
    
    def on_text_change(self, event):
        """Handle text change events"""
        # Get current text
        self.current_text = self.text_widget.get("1.0", tk.END).strip()
        
        # Update cursor position
        self.update_cursor_position()
        
        # Apply syntax highlighting
        self.apply_syntax_highlighting()
        
        # Show suggestions if appropriate
        self.check_for_suggestions()
        
        # Validate expression
        self.validate_current_expression()
        
        # Notify parent
        if self.on_expression_change:
            self.on_expression_change(self.current_text)
        
        # Add to history
        self.add_to_history()
    
    def on_key_press(self, event):
        """Handle key press events"""
        # Handle special keys
        if event.keysym == 'Tab':
            return "break"  # Prevent default tab behavior
        elif event.keysym == 'Return':
            return "break"  # Prevent default return behavior
        
        return None
    
    def on_cursor_move(self, event):
        """Handle cursor movement"""
        self.update_cursor_position()
        self.hide_suggestions()
    
    def on_cursor_up(self, event):
        """Handle up arrow key"""
        if self.showing_suggestions:
            self.move_suggestion_selection(-1)
            return "break"
        return None
    
    def on_cursor_down(self, event):
        """Handle down arrow key"""
        if self.showing_suggestions:
            self.move_suggestion_selection(1)
            return "break"
        return None
    
    def on_tab_completion(self, event):
        """Handle tab completion"""
        if self.showing_suggestions and self.suggestions:
            self.apply_suggestion(None)
            return "break"
        return None
    
    def on_enter_pressed(self, event):
        """Handle enter key"""
        if self.showing_suggestions and self.suggestions:
            self.apply_suggestion(None)
            return "break"
        return None
    
    def update_cursor_position(self):
        """Update cursor position display"""
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.position_label.config(text=f"Línea: {line}, Columna: {int(col) + 1}")
        except:
            pass
    
    def apply_syntax_highlighting(self):
        """Apply syntax highlighting to the text"""
        # Clear all tags
        for tag in self.text_widget.tag_names():
            if tag not in ["sel", "mark"]:
                self.text_widget.tag_remove(tag, "1.0", tk.END)
        
        text = self.current_text
        
        # Highlight functions
        function_pattern = r'\b(sin|cos|tan|cot|sec|csc|asin|acos|atan|sinh|cosh|tanh|log|ln|exp|sqrt|abs|sign|ceil|floor|factorial|gamma|beta|zeta|integrate|diff|limit|sum|product)\b'
        self.highlight_pattern(function_pattern, "function")
        
        # Highlight numbers
        number_pattern = r'\b\d+\.?\d*\b'
        self.highlight_pattern(number_pattern, "number")
        
        # Highlight variables
        variable_pattern = r'\b[a-zA-Z]\b'
        self.highlight_pattern(variable_pattern, "variable")
        
        # Highlight operators
        operator_pattern = r'[+\-×÷=<>^!°]|sqrt|nroot'
        self.highlight_pattern(operator_pattern, "operator")
        
        # Highlight parentheses
        self.highlight_pattern(r'[()\[\]{}]', "parenthesis")
    
    def highlight_pattern(self, pattern, tag):
        """Highlight text matching a pattern"""
        for match in re.finditer(pattern, self.current_text):
            start = match.start()
            end = match.end()
            start_index = f"1.0+{start}c"
            end_index = f"1.0+{end}c"
            self.text_widget.tag_add(tag, start_index, end_index)
    
    def check_for_suggestions(self):
        """Check if suggestions should be shown"""
        # Get current word at cursor
        cursor_pos = self.text_widget.index(tk.INSERT)
        line, col = map(int, cursor_pos.split('.'))
        
        # Get text up to cursor
        text_before_cursor = self.text_widget.get("1.0", cursor_pos)
        
        # Find current word
        word_match = re.search(r'(\w+)$', text_before_cursor)
        if word_match:
            current_word = word_match.group(1)
            if len(current_word) >= 2:  # Only show suggestions for words of 2+ chars
                self.show_suggestions_for_word(current_word, cursor_pos)
            else:
                self.hide_suggestions()
        else:
            self.hide_suggestions()
    
    def show_suggestions_for_word(self, word, cursor_pos):
        """Show suggestions for a specific word"""
        suggestions = self.math_engine.get_suggestions(word)
        
        if suggestions:
            self.suggestions = suggestions
            self.current_suggestion_index = 0
            
            # Update listbox
            self.suggestions_listbox.delete(0, tk.END)
            for suggestion in suggestions:
                self.suggestions_listbox.insert(tk.END, suggestion)
            
            # Select first item
            self.suggestions_listbox.selection_set(0)
            
            # Position popup
            self.position_suggestions_popup(cursor_pos)
            
            # Show popup
            self.suggestions_popup.deiconify()
            self.showing_suggestions = True
        else:
            self.hide_suggestions()
    
    def position_suggestions_popup(self, cursor_pos):
        """Position the suggestions popup near the cursor"""
        try:
            # Get cursor coordinates
            bbox = self.text_widget.bbox(cursor_pos)
            if bbox:
                x, y, width, height = bbox
                x_root = self.text_widget.winfo_rootx() + x
                y_root = self.text_widget.winfo_rooty() + y + height
                
                # Position popup
                self.suggestions_popup.geometry(f"+{x_root}+{y_root}")
        except:
            pass
    
    def hide_suggestions(self, event=None):
        """Hide suggestions popup"""
        self.suggestions_popup.withdraw()
        self.showing_suggestions = False
        self.suggestions = []
    
    def move_suggestion_selection(self, direction):
        """Move suggestion selection up or down"""
        if not self.suggestions:
            return
        
        # Calculate new index
        new_index = self.current_suggestion_index + direction
        new_index = max(0, min(len(self.suggestions) - 1, new_index))
        
        if new_index != self.current_suggestion_index:
            self.current_suggestion_index = new_index
            self.suggestions_listbox.selection_clear(0, tk.END)
            self.suggestions_listbox.selection_set(new_index)
            self.suggestions_listbox.see(new_index)
    
    def apply_suggestion(self, event):
        """Apply selected suggestion"""
        if self.suggestions and self.current_suggestion_index < len(self.suggestions):
            suggestion = self.suggestions[self.current_suggestion_index]
            
            # Get current word and replace it
            cursor_pos = self.text_widget.index(tk.INSERT)
            text_before_cursor = self.text_widget.get("1.0", cursor_pos)
            word_match = re.search(r'(\w+)$', text_before_cursor)
            
            if word_match:
                start_pos = word_match.start()
                start_index = f"1.0+{start_pos}c"
                
                # Replace the word
                self.text_widget.delete(start_index, cursor_pos)
                self.text_widget.insert(start_index, suggestion)
                
                # Add parentheses for functions
                if suggestion in ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'abs']:
                    self.text_widget.insert(tk.INSERT, "()")
                    # Move cursor inside parentheses
                    new_pos = self.text_widget.index(tk.INSERT)
                    new_pos = f"{new_pos}-1c"
                    self.text_widget.mark_set(tk.INSERT, new_pos)
            
            self.hide_suggestions()
    
    def on_suggestion_up(self, event):
        """Handle up arrow in suggestions list"""
        self.move_suggestion_selection(-1)
        return "break"
    
    def on_suggestion_down(self, event):
        """Handle down arrow in suggestions list"""
        self.move_suggestion_selection(1)
        return "break"
    
    def insert_symbol(self, symbol):
        """Insert a symbol at cursor position"""
        self.text_widget.insert(tk.INSERT, symbol)
        self.text_widget.focus_set()
    
    def insert_function(self, function):
        """Insert a function with parentheses"""
        self.text_widget.insert(tk.INSERT, f"{function}()")
        # Move cursor inside parentheses
        new_pos = self.text_widget.index(tk.INSERT)
        new_pos = f"{new_pos}-1c"
        self.text_widget.mark_set(tk.INSERT, new_pos)
        self.text_widget.focus_set()
    
    def validate_current_expression(self):
        """Validate the current expression"""
        try:
            is_valid, error = self.math_engine.validate_expression(self.current_text)
            if is_valid:
                self.validation_status.config(text=" Válido", fg='#27ae60')
                self.status_label.config(text=" Expresión válida")
            else:
                self.validation_status.config(text=" Error", fg='#e74c3c')
                self.status_label.config(text=f" Error: {error}")
        except:
            self.validation_status.config(text="", fg='#95a5a6')
            self.status_label.config(text=" Analizando...")
    
    def validate_expression(self):
        """Validate expression and show detailed info"""
        try:
            info = self.math_engine.get_expression_info(self.current_text)
            
            if info.get('is_valid'):
                messagebox.showinfo("Validación Exitosa", 
                                  f"Expresión válida:\n\n"
                                  f"Variables: {', '.join(info.get('variables', []))}\n"
                                  f"Funciones: {', '.join(info.get('functions', []))}\n"
                                  f"Constantes: {', '.join(info.get('constants', []))}\n"
                                  f"Tipo: {info.get('type', 'Unknown')}")
            else:
                messagebox.showerror("Error de Validación", 
                                   f"Expresión inválida:\n\n{info.get('error', 'Error desconocido')}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar la expresión: {str(e)}")
    
    def clear(self):
        """Clear the editor"""
        self.text_widget.delete("1.0", tk.END)
        self.current_text = ""
        self.hide_suggestions()
    
    def undo(self):
        """Undo last action"""
        try:
            self.text_widget.edit_undo()
        except:
            pass
    
    def redo(self):
        """Redo last action"""
        try:
            self.text_widget.edit_redo()
        except:
            pass
    
    def add_to_history(self):
        """Add current state to history"""
        self.history.append(self.current_text)
        self.redo_stack.clear()
    
    def get_expression(self) -> str:
        """Get the current expression"""
        return self.current_text
    
    def set_expression(self, expression: str):
        """Set the editor content"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", expression)
        self.current_text = expression
    
    def get_parsed_expression(self):
        """Get the parsed SymPy expression"""
        try:
            return self.math_engine.parse_natural_math(self.current_text)
        except MathParsingError:
            return None

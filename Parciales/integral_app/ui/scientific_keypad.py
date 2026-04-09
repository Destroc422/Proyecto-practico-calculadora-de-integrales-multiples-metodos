import tkinter as tk
from tkinter import ttk
from ui.math_editor import MathEditor

class ScientificKeypad:
    """Teclado matemático científico profesional"""
    
    def __init__(self, parent, math_editor):
        self.parent = parent
        self.math_editor = math_editor
        
        # Configuración del teclado
        self.button_size = {'width': 6}
        # ttk.Button no soporta font directamente, usará el estilo del tema
        
        # Crear el teclado
        self.create_keypad()
    
    def create_keypad(self):
        """Crea el teclado científico completo"""
        # Frame principal del teclado
        keypad_frame = ttk.LabelFrame(self.parent, text="🔢 Teclado Científico", padding=10)
        keypad_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear secciones del teclado
        self.create_numbers_section(keypad_frame)
        self.create_operations_section(keypad_frame)
        self.create_functions_section(keypad_frame)
        self.create_advanced_section(keypad_frame)
        self.create_fractions_section(keypad_frame)
    
    def create_numbers_section(self, parent):
        """Sección de números básicos"""
        frame = ttk.LabelFrame(parent, text="Números", padding=5)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Botones numéricos
        numbers = [
            ('7', '7'), ('8', '8'), ('9', '9'),
            ('4', '4'), ('5', '5'), ('6', '6'),
            ('1', '1'), ('2', '2'), ('3', '3'),
            ('0', '0'), ('.', '.'), ('±', '-'),  # ± para negativos
        ]
        
        for i, (text, insert) in enumerate(numbers):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                frame, 
                text=text, 
                **self.button_size,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def create_operations_section(self, parent):
        """Sección de operaciones básicas"""
        frame = ttk.LabelFrame(parent, text="Operaciones", padding=5)
        frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        operations = [
            ('÷', '/'), ('×', '*'), ('-', '-'), ('+', '+'),
            ('x^y', '**'), ('√x', 'sqrt('), ('x!', '!'), ('π', 'pi'),
            ('(', '('), (')', ')'), ('|x|', 'abs('), ('⌊x⌋', 'floor(')
        ]
        
        for i, (text, insert) in enumerate(operations):
            row = i // 2
            col = i % 2
            
            btn = ttk.Button(
                frame, 
                text=text, 
                **self.button_size,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def create_functions_section(self, parent):
        """Sección de funciones matemáticas"""
        frame = ttk.LabelFrame(parent, text="Funciones", padding=5)
        frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        functions = [
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('),
            ('asin', 'asin('), ('acos', 'acos('), ('atan', 'atan('),
            ('log', 'log('), ('ln', 'log('), ('exp', 'exp('),
            ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh(')
        ]
        
        for i, (text, insert) in enumerate(functions):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                frame, 
                text=text, 
                **self.button_size,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def create_advanced_section(self, parent):
        """Sección de funciones avanzadas"""
        frame = ttk.LabelFrame(parent, text="Avanzado", padding=5)
        frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        advanced = [
            ('x²', 'x**2'), ('x³', 'x**3'), ('xⁿ', 'x^'),
            ('e^x', 'exp('), ('10^x', '10**'), ('2^x', '2**'),
            ('∛', '**(1/3)'), ('⁴√', '**(1/4)'), ('ⁿ√', '**(1/'),
            ('lim', 'lim'), ('∑', 'sum'), ('∏', 'product')
        ]
        
        for i, (text, insert) in enumerate(advanced):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                frame, 
                text=text, 
                **self.button_size,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def create_fractions_section(self, parent):
        """Sección especializada en fracciones"""
        frame = ttk.LabelFrame(parent, text="🔢 Fracciones", padding=5)
        frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Botón principal de fracción
        fraction_btn = ttk.Button(
            frame, 
            text="🔢\nFracción\n[ ]/[ ]", 
            width=8,
            command=self.math_editor.insert_fraction,
            style='Accent.TButton'
        )
        fraction_btn.grid(row=0, column=0, padx=10, pady=5, rowspan=3)
        
        # Fracciones comunes
        common_fractions = [
            ('1/2', '1/2'), ('1/3', '1/3'), ('1/4', '1/4'),
            ('2/3', '2/3'), ('3/4', '3/4'), ('1/π', '1/pi'),
        ]
        
        for i, (text, insert) in enumerate(common_fractions):
            row = i // 3
            col = i % 3 + 1
            
            btn = ttk.Button(
                frame, 
                text=text, 
                width=6,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
        
        # Fracciones con funciones
        function_fractions = [
            ('sin/x', 'sin(x)/x'), ('cos/x', 'cos(x)/x'), ('tan/x', 'tan(x)/x'),
            ('e^x/x', 'exp(x)/x'), ('ln/x', 'log(x)/x'), ('x²/x', 'x**2/x'),
        ]
        
        for i, (text, insert) in enumerate(function_fractions):
            row = i // 3
            col = i % 3 + 1
            
            btn = ttk.Button(
                frame, 
                text=text, 
                width=6,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row+1, column=col, padx=2, pady=2)
        
        # Botones de control
        control_frame = ttk.Frame(frame)
        control_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(
            control_frame, 
            text="🧹 Limpiar", 
            command=self.clear_editor
        ).pack(side="left", padx=5)
        
        ttk.Button(
            control_frame, 
            text="↶ Deshacer", 
            command=self.undo
        ).pack(side="left", padx=5)
        
        ttk.Button(
            control_frame, 
            text="↷ Rehacer", 
            command=self.redo
        ).pack(side="left", padx=5)
        
        ttk.Button(
            control_frame, 
            text="📋 Copiar", 
            command=self.copy_expression
        ).pack(side="left", padx=5)
    
    def clear_editor(self):
        """Limpia el editor"""
        self.math_editor.set_text("")
    
    def undo(self):
        """Deshacer última acción"""
        try:
            self.math_editor.text_widget.edit_undo()
        except:
            pass
    
    def redo(self):
        """Rehacer última acción"""
        try:
            self.math_editor.text_widget.edit_redo()
        except:
            pass
    
    def copy_expression(self):
        """Copia la expresión convertida a SymPy"""
        try:
            sympy_expr = self.math_editor.convert_to_sympy()
            self.parent.clipboard_clear()
            self.parent.clipboard_append(sympy_expr)
        except:
            pass

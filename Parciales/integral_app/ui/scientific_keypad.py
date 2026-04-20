import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from ui.math_editor import MathEditor

class ScientificKeypad:
    """Teclado matemático científico profesional con soporte Unicode completo"""
    
    def __init__(self, parent, math_editor):
        self.parent = parent
        self.math_editor = math_editor
        
        # Configuración mejorada del teclado con soporte Unicode
        self.button_size = {'width': 8, 'height': 2}
        
        # Configurar fuentes para soporte Unicode
        self.setup_unicode_fonts()
        
        # Crear el teclado
        self.create_keypad()
    
    def setup_unicode_fonts(self):
        """Configurar fuentes para soporte completo de símbolos Unicode"""
        try:
            # Fuente principal con soporte Unicode
            self.unicode_font = tkfont.Font(
                family='Segoe UI Symbol',
                size=12,
                weight='normal'
            )
            
            # Fuente alternativa si la principal no está disponible
            self.fallback_font = tkfont.Font(
                family='Arial Unicode MS',
                size=12,
                weight='normal'
            )
            
            # Fuente para símbolos matemáticos
            self.math_font = tkfont.Font(
                family='Cambria Math',
                size=12,
                weight='normal'
            )
            
            # Intentar usar la mejor fuente disponible
            try:
                self.unicode_font.actual()
                self.active_font = self.unicode_font
            except:
                try:
                    self.fallback_font.actual()
                    self.active_font = self.fallback_font
                except:
                    self.active_font = 'TkDefaultFont'
                    
        except Exception as e:
            print(f"Error configurando fuentes Unicode: {e}")
            self.active_font = 'TkDefaultFont'
    
    def create_keypad(self):
        """Crea el teclado científico completo con soporte Unicode"""
        # Frame principal del teclado
        keypad_frame = ttk.LabelFrame(self.parent, text="⚛️ Teclado Científico Unicode", padding=10)
        keypad_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear secciones del teclado mejoradas
        self.create_unicode_symbols_section(keypad_frame)
        self.create_numbers_section(keypad_frame)
        self.create_operations_section(keypad_frame)
        self.create_functions_section(keypad_frame)
        self.create_advanced_section(keypad_frame)
        self.create_integrals_section(keypad_frame)
        self.create_greek_section(keypad_frame)
        self.create_fractions_section(keypad_frame)
    
    def create_unicode_symbols_section(self, parent):
        """Sección especializada en símbolos Unicode matemáticos"""
        frame = ttk.LabelFrame(parent, text="🔣 Símbolos Unicode", padding=5)
        frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Símbolos matemáticos Unicode esenciales - CONSISTENTE
        unicode_symbols = [
            ('∫', 'int '), ('∬', 'int '), ('∭', 'int '),
            ('∂', 'partial '), ('∇', 'nabla '), ('∞', 'infinity '),
            ('∑', 'sum '), ('∏', 'product '), ('√', 'sqrt('),
            ('±', '±'), ('≈', '~='), ('≠', '!='),
            ('≤', '<='), ('≥', '>='), ('∈', 'in '),
            ('∉', 'notin '), ('⊂', 'subset '), ('⊃', 'superset '),
            ('∧', 'and '), ('∨', 'or '), ('→', '-> '),
            ('↔', '<-> '), ('⇒', '=> '), ('⇔', '<=> '),
            ('∀', 'forall '), ('∃', 'exists '), ('∅', 'empty_set '),
            ('ℕ', 'Natural '), ('ℤ', 'Integer '), ('ℝ', 'Real '),
            ('ℚ', 'Rational '), ('ℂ', 'Complex '), ('π', 'pi '),
            ('θ', 'theta '), ('α', 'alpha '), ('β', 'beta '),
            ('γ', 'gamma '), ('δ', 'delta '), ('ε', 'epsilon '),
            ('λ', 'lambda '), ('μ', 'mu '), ('σ', 'sigma '),
            ('φ', 'phi '), ('ω', 'omega '), ('Δ', 'Delta '),
            ('Θ', 'Theta '), ('Λ', 'Lambda '), ('Σ', 'Sigma '),
            ('Φ', 'Phi '), ('Ω', 'Omega '), ('Γ', 'Gamma '),
            ('x²', 'x**2'), ('x³', 'x**3'), ('x⁴', 'x**4'), ('x⁵', 'x**5'),
            ('²', '**2'), ('³', '**3'), ('⁴', '**4'), ('⁵', '**5')
        ]
        
        # Crear botones con símbolos Unicode
        for i, (symbol, insert) in enumerate(unicode_symbols):
            row = i // 6
            col = i % 6
            
            btn = tk.Button(
                frame,
                text=symbol,
                width=6,
                height=2,
                font=self.active_font,
                bg='#f0f0f0',
                relief='raised',
                bd=2,
                command=lambda s=insert: self.insert_unicode_symbol(s)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_numbers_section(self, parent):
        """Sección de números básicos con soporte Unicode"""
        frame = ttk.LabelFrame(parent, text="🔢 Números", padding=5)
        frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Botones numéricos mejorados
        numbers = [
            ('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('×', '*'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('-', '-'),
            ('0', '0'), ('.', '.'), ('±', '-'), ('+', '+')
        ]
        
        for i, (text, insert) in enumerate(numbers):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#e8f4f8',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_operations_section(self, parent):
        """Sección de operaciones con símbolos Unicode"""
        frame = ttk.LabelFrame(parent, text="⚡ Operaciones", padding=5)
        frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # Operaciones con símbolos Unicode - CORREGIDO
        operations = [
            ('x²', 'x**2'), ('x³', 'x**3'), ('x⁴', 'x**4'), ('x⁵', 'x**5'),
            ('xⁿ', 'x^'), ('√x', 'sqrt('), ('∛x', '**(1/3)'), ('⁴√x', '**(1/4)'),
            ('x!', 'factorial('), ('|x|', 'abs('), ('⌊x⌋', 'floor('), ('⌈x⌉', 'ceil('),
            ('(', '('), (')', ')'), ('{', '{'), ('}', '}'),
            ('[', '['), (']', ']'), ('⟨', '<'), ('⟩', '>'),
            ('π', 'pi'), ('e', 'e'), ('φ', 'phi'), ('γ', 'gamma '),
            ('%', '/100'), ('‰', '/1000'), ('∠', 'angle '), ('°', '*pi/180'),
            ('²', '**2'), ('³', '**3'), ('⁴', '**4'), ('⁵', '**5')
        ]
        
        for i, (text, insert) in enumerate(operations):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#fff0e8',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_functions_section(self, parent):
        """Sección de funciones matemáticas con notación Unicode"""
        frame = ttk.LabelFrame(parent, text="📈 Funciones", padding=5)
        frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        
        # Funciones trigonométricas y matemáticas - CONSISTENTE
        functions = [
            ('sin', 'sin('), ('cos', 'cos('), ('tan', 'tan('), ('cot', 'cot('),
            ('sec', 'sec('), ('csc', 'csc('), ('arcsin', 'asin('), ('arccos', 'acos('),
            ('arctan', 'atan('), ('sinh', 'sinh('), ('cosh', 'cosh('), ('tanh', 'tanh('),
            ('log', 'log('), ('ln', 'ln('), ('log₂', 'log2('), ('log₁₀', 'log10('),
            ('exp', 'exp('), ('√', 'sqrt('), ('∛', '**(1/3)'), ('⁴√', '**(1/4)'),
            ('⌈x⌉', 'ceil('), ('⌊x⌋', 'floor('), ('|x|', 'abs('), ('sgn', 'sign('),
            ('sin²', 'sin(x)**2'), ('cos²', 'cos(x)**2'), ('tan²', 'tan(x)**2'), ('sec²', 'sec(x)**2'),
            ('x²', 'x**2'), ('x³', 'x**3'), ('x⁴', 'x**4'), ('x⁵', 'x**5')
        ]
        
        for i, (text, insert) in enumerate(functions):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#e8f8e8',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_advanced_section(self, parent):
        """Sección de funciones avanzadas con símbolos Unicode mejorados"""
        frame = ttk.LabelFrame(parent, text="🚀 Avanzado", padding=5)
        frame.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        
        # Funciones avanzadas con símbolos Unicode - CONSISTENTE
        advanced = [
            ('lim', 'limit('), ('lim→', 'limit('), ('lim←', 'limit('), ('lim∞', 'limit('),
            ('d/dx', 'diff('), ('∂/∂x', 'diff('), ('∫', 'int '), ('∬', 'int '),
            ('∑', 'sum('), ('∏', 'product('), ('∪', 'union '), ('∩', 'intersection '),
            ('⊕', 'oplus '), ('⊗', 'otimes '), ('⊖', 'ominus '), ('⊙', 'odot '),
            ('→', '-> '), ('←', '<- '), ('↔', '<-> '), ('⇒', '=> '),
            ('∀', 'forall '), ('∃', 'exists '), ('∄', 'nexists '), ('∴', 'therefore '),
            ('∵', 'because '), ('∈', 'in '), ('∉', 'notin '), ('⊂', 'subset '),
            ('⊆', 'subseteq '), ('⊃', 'superset '), ('⊇', 'superseteq '), ('≡', '=='),
            ('≈', '~='), ('≠', '!='), ('≤', '<='), ('≥', '>='),
            ('≪', '<<'), ('≫', '>>'), ('∝', 'propto '), ('∥', 'parallel '),
            ('∫x²', 'int x**2 dx'), ('∫x³', 'int x**3 dx'), ('∫x⁴', 'int x**4 dx'), ('∫x⁵', 'int x**5 dx'),
            ('∑x²', 'sum x**2'), ('∑x³', 'sum x**3'), ('∏x²', 'product x**2'), ('∏x³', 'product x**3')
        ]
        
        for i, (text, insert) in enumerate(advanced):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#f8e8ff',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_integrals_section(self, parent):
        """Sección especializada en integrales con símbolos Unicode mejorados"""
        frame = ttk.LabelFrame(parent, text="∫ Integrales", padding=5)
        frame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        
        # Integrales básicas con símbolos Unicode - MEJORADO
        basic_integrals = [
            ('∫', 'int '), ('∬', 'integral '), ('∭', 'integral '),
            ('∮', 'int '), ('∯', 'int '), ('∰', 'int '),
            ('dx', ' dx'), ('dy', ' dy'), ('dz', ' dz'),
            ('dt', ' dt'), ('dθ', ' dtheta '), ('dφ', ' dphi '),
            ('0→1', '0 to 1 int '), ('0→2', '0 to 2 int '), ('a→b', 'a to b int '),
            ('-∞→∞', '-infinity to infinity int '), ('0→∞', '0 to infinity int '),
            ('∫₀¹', '0 to 1 int '), ('∫₀²', '0 to 2 int '), ('∫ₐᵇ', 'a to b int '),
            ('∫f(x)', 'int f(x) dx'), ('∫g(x)', 'int g(x) dx'), ('∫h(x)', 'int h(x) dx'),
            ('∫[a,b]', 'int from a to b '), ('∫[0,1]', 'int from 0 to 1 '), ('∫[−∞,∞]', 'int from -infinity to infinity ')
        ]
        
        for i, (text, insert) in enumerate(basic_integrals):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#ffe8e8',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_greek_section(self, parent):
        """Sección especializada en letras griegas con símbolos Unicode"""
        frame = ttk.LabelFrame(parent, text="αβγ Letras Griegas", padding=5)
        frame.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        
        # Letras griegas minúsculas - CONSISTENTE
        greek_lowercase = [
            ('α', 'alpha '), ('β', 'beta '), ('γ', 'gamma '), ('δ', 'delta '),
            ('ε', 'epsilon '), ('ζ', 'zeta '), ('η', 'eta '), ('θ', 'theta '),
            ('ι', 'iota '), ('κ', 'kappa '), ('λ', 'lambda '), ('μ', 'mu '),
            ('ν', 'nu '), ('ξ', 'xi '), ('π', 'pi '), ('ρ', 'rho '),
            ('σ', 'sigma '), ('τ', 'tau '), ('υ', 'upsilon '), ('φ', 'phi '),
            ('χ', 'chi '), ('ψ', 'psi '), ('ω', 'omega '),
            ('α²', 'alpha**2'), ('β²', 'beta**2'), ('γ²', 'gamma**2'), ('δ²', 'delta**2'),
            ('θ²', 'theta**2'), ('λ²', 'lambda**2'), ('μ²', 'mu**2'), ('π²', 'pi**2')
        ]
        
        # Letras griegas mayúsculas - CONSISTENTE
        greek_uppercase = [
            ('Α', 'Alpha '), ('Β', 'Beta '), ('Γ', 'Gamma '), ('Δ', 'Delta '),
            ('Ε', 'Epsilon '), ('Ζ', 'Zeta '), ('Η', 'Eta '), ('Θ', 'Theta '),
            ('Ι', 'Iota '), ('Κ', 'Kappa '), ('Λ', 'Lambda '), ('Μ', 'Mu '),
            ('Ν', 'Nu '), ('Ξ', 'Xi '), ('Π', 'Pi '), ('Ρ', 'Rho '),
            ('Σ', 'Sigma '), ('Τ', 'Tau '), ('Υ', 'Upsilon '), ('Φ', 'Phi '),
            ('Χ', 'Chi '), ('Ψ', 'Psi '), ('Ω', 'Omega '),
            ('Α²', 'Alpha**2'), ('Β²', 'Beta**2'), ('Γ²', 'Gamma**2'), ('Δ²', 'Delta**2'),
            ('Θ²', 'Theta**2'), ('Λ²', 'Lambda**2'), ('Π²', 'Pi**2'), ('Σ²', 'Sigma**2')
        ]
        
        # Crear botones para letras griegas minúsculas
        for i, (symbol, insert) in enumerate(greek_lowercase):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=symbol,
                width=6,
                height=2,
                font=self.active_font,
                bg='#e8ffe8',
                relief='raised',
                bd=2,
                command=lambda s=insert: self.math_editor.insert_symbol(s)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Crear botones para letras griegas mayúsculas
        for i, (symbol, insert) in enumerate(greek_uppercase):
            row = i // 4 + 6
            col = i % 4
            
            btn = tk.Button(
                frame,
                text=symbol,
                width=6,
                height=2,
                font=self.active_font,
                bg='#e8e8ff',
                relief='raised',
                bd=2,
                command=lambda s=insert: self.math_editor.insert_symbol(s)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
    
    def create_fractions_section(self, parent):
        """Sección especializada en fracciones con símbolos Unicode"""
        frame = ttk.LabelFrame(parent, text="🔢 Fracciones Unicode", padding=5)
        frame.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Botón principal de fracción Unicode
        fraction_btn = tk.Button(
            frame,
            text="🔢\nFracción\n[ ]/[ ]",
            width=10,
            height=4,
            font=self.active_font,
            bg='#ffcc00',
            relief='raised',
            bd=3,
            command=self.math_editor.insert_fraction
        )
        fraction_btn.grid(row=0, column=0, padx=5, pady=5, rowspan=4)
        
        # Fracciones comunes con símbolos Unicode
        common_fractions = [
            ('½', '1/2'), ('⅓', '1/3'), ('¼', '1/4'),
            ('⅕', '1/5'), ('⅙', '1/6'), ('⅐', '1/7'),
            ('⅛', '1/8'), ('⅑', '1/9'), ('⅒', '1/10'),
            ('⅔', '2/3'), ('¾', '3/4'), ('⅖', '2/5'),
            ('⅗', '3/5'), ('⅘', '4/5'), ('⅚', '5/6'),
            ('⅛', '1/8'), ('³⁄₈', '3/8'), ('⅝', '5/8'),
            ('⅞', '7/8'), ('⅟', '1/'), ('⅟π', '1/pi'),
            ('⅟e', '1/e'), ('⅟2', '1/2'), ('⅟3', '1/3')
        ]
        
        for i, (text, insert) in enumerate(common_fractions):
            row = i // 4
            col = i % 4 + 1
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#fff8dc',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Fracciones con funciones usando símbolos Unicode - CONSISTENTE
        function_fractions = [
            ('sin/x', 'sin(x)/x'), ('cos/x', 'cos(x)/x'), ('tan/x', 'tan(x)/x'),
            ('sec/x', 'sec(x)/x'), ('csc/x', 'csc(x)/x'), ('cot/x', 'cot(x)/x'),
            ('eˣ/x', 'exp(x)/x'), ('ln/x', 'log(x)/x'), ('x²/x', 'x**2/x'),
            ('x³/x', 'x**3/x'), ('√x/x', 'sqrt(x)/x'), ('|x|/x', 'abs(x)/x'),
            ('sin²/x', 'sin(x)**2/x'), ('cos²/x', 'cos(x)**2/x'), ('tan²/x', 'tan(x)**2/x'),
            ('x²+1/x', '(x**2+1)/x'), ('x³+1/x', '(x**3+1)/x'), ('x⁴+1/x', '(x**4+1)/x'),
            ('∫sin/x', 'int sin(x)/x dx'), ('∫cos/x', 'int cos(x)/x dx'), ('∫tan/x', 'int tan(x)/x dx')
        ]
        
        for i, (text, insert) in enumerate(function_fractions):
            row = i // 4 + 5
            col = i % 4 + 1
            
            btn = tk.Button(
                frame,
                text=text,
                width=6,
                height=2,
                font=self.active_font,
                bg='#f0f8ff',
                relief='raised',
                bd=2,
                command=lambda t=insert: self.math_editor.insert_symbol(t)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
        
        # Botones de control mejorados con símbolos Unicode
        control_frame = tk.Frame(frame, bg='#f0f0f0')
        control_frame.grid(row=9, column=0, columnspan=5, pady=10)
        
        # Botones de control con símbolos Unicode
        controls = [
            ('🧹 Limpiar', self.clear_editor, '#ff6b6b'),
            ('↶ Deshacer', self.undo, '#4ecdc4'),
            ('↷ Rehacer', self.redo, '#4ecdc4'),
            ('📋 Copiar', self.copy_expression, '#45b7d1'),
            ('🔍 Verificar', self.verify_expression, '#96ceb4'),
            ('🎨 Formato', self.format_expression, '#ffeaa7'),
            ('📐 Simplificar', self.simplify_expression, '#dfe6e9'),
            ('⚡ Evaluar', self.evaluate_expression, '#74b9ff')
        ]
        
        for text, command, color in controls:
            btn = tk.Button(
                control_frame,
                text=text,
                width=10,
                height=2,
                font=self.active_font,
                bg=color,
                fg='white',
                relief='raised',
                bd=2,
                command=command
            )
            btn.pack(side="left", padx=3, pady=3)
    
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
    
    def insert_unicode_symbol(self, symbol):
        """Inserta un símbolo Unicode con manejo especial consistente"""
        try:
            # Manejo especial para símbolos de elevado
            if symbol == 'x²':
                self.math_editor.insert_symbol('x**2')
            elif symbol == 'x³':
                self.math_editor.insert_symbol('x**3')
            elif symbol == 'x**4':
                self.math_editor.insert_symbol('x**4')
            elif symbol == 'x**5':
                self.math_editor.insert_symbol('x**5')
            elif symbol == '²':
                self.math_editor.insert_symbol('**2')
            elif symbol == '³':
                self.math_editor.insert_symbol('**3')
            elif symbol == '**4':
                self.math_editor.insert_symbol('**4')
            elif symbol == '**5':
                self.math_editor.insert_symbol('**5')
            # Manejo especial para potencias de letras griegas
            elif symbol == 'alpha**2':
                self.math_editor.insert_symbol('alpha**2')
            elif symbol == 'beta**2':
                self.math_editor.insert_symbol('beta**2')
            elif symbol == 'gamma**2':
                self.math_editor.insert_symbol('gamma**2')
            elif symbol == 'delta**2':
                self.math_editor.insert_symbol('delta**2')
            elif symbol == 'theta**2':
                self.math_editor.insert_symbol('theta**2')
            elif symbol == 'lambda**2':
                self.math_editor.insert_symbol('lambda**2')
            elif symbol == 'mu**2':
                self.math_editor.insert_symbol('mu**2')
            elif symbol == 'pi**2':
                self.math_editor.insert_symbol('pi**2')
            elif symbol == 'Alpha**2':
                self.math_editor.insert_symbol('Alpha**2')
            elif symbol == 'Beta**2':
                self.math_editor.insert_symbol('Beta**2')
            elif symbol == 'Gamma**2':
                self.math_editor.insert_symbol('Gamma**2')
            elif symbol == 'Delta**2':
                self.math_editor.insert_symbol('Delta**2')
            elif symbol == 'Theta**2':
                self.math_editor.insert_symbol('Theta**2')
            elif symbol == 'Lambda**2':
                self.math_editor.insert_symbol('Lambda**2')
            elif symbol == 'Pi**2':
                self.math_editor.insert_symbol('Pi**2')
            elif symbol == 'Sigma**2':
                self.math_editor.insert_symbol('Sigma**2')
            # Manejo especial para funciones con potencias
            elif symbol == 'sin(x)**2':
                self.math_editor.insert_symbol('sin(x)**2')
            elif symbol == 'cos(x)**2':
                self.math_editor.insert_symbol('cos(x)**2')
            elif symbol == 'tan(x)**2':
                self.math_editor.insert_symbol('tan(x)**2')
            elif symbol == 'sec(x)**2':
                self.math_editor.insert_symbol('sec(x)**2')
            # Manejo especial para integrales con potencias
            elif symbol == 'int x**2 dx':
                self.math_editor.insert_symbol('int x**2 dx')
            elif symbol == 'int x**3 dx':
                self.math_editor.insert_symbol('int x**3 dx')
            elif symbol == 'int x**4 dx':
                self.math_editor.insert_symbol('int x**4 dx')
            elif symbol == 'int x**5 dx':
                self.math_editor.insert_symbol('int x**5 dx')
            # Manejo especial para sumatorias y productos con potencias
            elif symbol == 'sum x**2':
                self.math_editor.insert_symbol('sum x**2')
            elif symbol == 'sum x**3':
                self.math_editor.insert_symbol('sum x**3')
            elif symbol == 'product x**2':
                self.math_editor.insert_symbol('product x**2')
            elif symbol == 'product x**3':
                self.math_editor.insert_symbol('product x**3')
            # Manejo especial para integrales Unicode
            elif symbol == 'int ':
                # Insertar integral con formato correcto
                current_text = self.math_editor.get_text()
                if current_text.strip():
                    self.math_editor.insert_symbol(' int ')
                else:
                    self.math_editor.insert_symbol('int ')
            elif symbol in ['integral ', 'triple_integral ', 'contour_integral ', 'surface_integral ', 'volume_integral ']:
                # Todas las integrales usan el mismo formato
                self.math_editor.insert_symbol('int ')
            # Manejo especial para fracciones con potencias
            elif symbol == '(x**2+1)/x':
                self.math_editor.insert_symbol('(x**2+1)/x')
            elif symbol == '(x**3+1)/x':
                self.math_editor.insert_symbol('(x**3+1)/x')
            elif symbol == '(x**4+1)/x':
                self.math_editor.insert_symbol('(x**4+1)/x')
            # Manejo especial para integrales de fracciones
            elif symbol == 'int sin(x)/x dx':
                self.math_editor.insert_symbol('int sin(x)/x dx')
            elif symbol == 'int cos(x)/x dx':
                self.math_editor.insert_symbol('int cos(x)/x dx')
            elif symbol == 'int tan(x)/x dx':
                self.math_editor.insert_symbol('int tan(x)/x dx')
            elif symbol == 'sin(x)**2/x':
                self.math_editor.insert_symbol('sin(x)**2/x')
            elif symbol == 'cos(x)**2/x':
                self.math_editor.insert_symbol('cos(x)**2/x')
            elif symbol == 'tan(x)**2/x':
                self.math_editor.insert_symbol('tan(x)**2/x')
            else:
                # Insertar el símbolo Unicode normal
                self.math_editor.insert_symbol(symbol)
            
            # Actualizar el estado del editor para símbolos Unicode
            self.update_unicode_state()
            
        except Exception as e:
            print(f"Error insertando símbolo Unicode: {e}")
    
    def update_unicode_state(self):
        """Actualiza el estado del editor para símbolos Unicode"""
        try:
            # Obtener el texto actual del editor
            current_text = self.math_editor.get_text()
            
            # Verificar si hay símbolos Unicode
            has_unicode = any(ord(char) > 127 for char in current_text)
            
            # Actualizar la configuración si es necesario
            if has_unicode:
                self.math_editor.text_widget.configure(font=self.active_font)
                
        except Exception as e:
            print(f"Error actualizando estado Unicode: {e}")
    
    def verify_expression(self):
        """Verifica la expresión matemática actual"""
        try:
            from core.microsoft_math_engine import MicrosoftMathEngine
            engine = MicrosoftMathEngine()
            
            current_text = self.math_editor.get_text()
            if current_text.strip():
                result = engine.parse_natural_math(current_text)
                print(f"Expresión verificada: {current_text} -> {result}")
                
                # Mostrar resultado en el editor
                self.math_editor.set_text(str(result))
            else:
                print("No hay expresión para verificar")
                
        except Exception as e:
            print(f"Error verificando expresión: {e}")
    
    def format_expression(self):
        """Formatea la expresión matemática actual con soporte Unicode"""
        try:
            current_text = self.math_editor.get_text()
            if current_text.strip():
                # Aplicar formato matemático con soporte Unicode
                formatted = current_text
                
                # Convertir potencias a formato Unicode si es posible
                formatted = formatted.replace('**2', '²')
                formatted = formatted.replace('**3', '³')
                formatted = formatted.replace('**4', '⁴')
                formatted = formatted.replace('**5', '⁵')
                
                # Convertir multiplicación a símbolo Unicode
                formatted = formatted.replace('*', '×')
                
                # Formatear integrales
                formatted = formatted.replace('int ', '∫ ')
                formatted = formatted.replace('integral ', '∫ ')
                
                self.math_editor.set_text(formatted)
                
        except Exception as e:
            print(f"Error formateando expresión: {e}")
    
    def simplify_expression(self):
        """Simplifica la expresión matemática actual"""
        try:
            import sympy as sp
            
            current_text = self.math_editor.get_text()
            if current_text.strip():
                expr = sp.sympify(current_text)
                simplified = sp.simplify(expr)
                self.math_editor.set_text(str(simplified))
                
        except Exception as e:
            print(f"Error simplificando expresión: {e}")
    
    def evaluate_expression(self):
        """Evalúa la expresión matemática actual"""
        try:
            import sympy as sp
            
            current_text = self.math_editor.get_text()
            if current_text.strip():
                expr = sp.sympify(current_text)
                evaluated = sp.N(expr)  # Evaluación numérica
                self.math_editor.set_text(str(evaluated))
                
        except Exception as e:
            print(f"Error evaluando expresión: {e}")
    
    def copy_expression(self):
        """Copia la expresión convertida a SymPy con soporte Unicode"""
        try:
            sympy_expr = self.math_editor.convert_to_sympy()
            self.parent.clipboard_clear()
            self.parent.clipboard_append(sympy_expr)
            
            # Mostrar confirmación
            print(f"Expresión copiada: {sympy_expr}")
            
        except Exception as e:
            print(f"Error copiando expresión: {e}")

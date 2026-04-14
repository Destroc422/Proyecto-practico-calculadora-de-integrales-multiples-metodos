import tkinter as tk
from tkinter import ttk
import re
from core.microsoft_math_engine import MicrosoftMathEngine

class MathEditor:
    """Editor matemático avanzado con soporte para fracciones visuales y Microsoft Math Engine"""
    
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        
        # Initialize Microsoft Math Engine
        self.math_engine = MicrosoftMathEngine()
        
        # Variables de estado
        self.fraction_mode = False
        self.current_fraction = None
        self.cursor_position = 0
        self.fractions = []  # Lista de fracciones en el texto
        
        # Crear widget Text con soporte matemático
        self.text_widget = tk.Text(
            parent, 
            width=50, 
            height=3,
            font=('Courier', 12),
            wrap=tk.NONE,
            undo=True,
            maxundo=-1
        )
        
        # Configurar tags para resaltado
        self.setup_tags()
        
        # Bindear eventos
        self.bind_events()
        
        # Variables para fracciones
        self.fraction_counter = 0
        self.active_fraction = None
    
    def setup_tags(self):
        """Configurar tags para resaltado de fracciones"""
        self.text_widget.tag_configure('fraction_numerator', 
                                     background='#E3F2FD', 
                                     font=('Courier', 11, 'bold'))
        self.text_widget.tag_configure('fraction_denominator', 
                                     background='#FFEBEE', 
                                     font=('Courier', 11, 'bold'))
        self.text_widget.tag_configure('fraction_line', 
                                     font=('Courier', 8), 
                                     foreground='#666')
        self.text_widget.tag_configure('cursor_highlight', 
                                     background='#FFF59D')
    
    def bind_events(self):
        """Bindear eventos del teclado y mouse"""
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<Button-1>', self.on_click)
        self.text_widget.bind('<Left>', self.on_arrow_left)
        self.text_widget.bind('<Right>', self.on_arrow_right)
        self.text_widget.bind('<Up>', self.on_arrow_up)
        self.text_widget.bind('<Down>', self.on_arrow_down)
        self.text_widget.bind('<Tab>', self.on_tab)
        self.text_widget.bind('<Return>', self.on_return)
    
    def insert_fraction(self):
        """Inserta una fracción visual"""
        # Obtener posición actual del cursor
        cursor_pos = self.text_widget.index(tk.INSERT)
        
        # Crear ID único para esta fracción
        frac_id = f"frac_{self.fraction_counter}"
        self.fraction_counter += 1
        
        # Insertar estructura de fracción
        fraction_text = f"[NUM]/[DEN]"
        
        # Insertar en el widget
        self.text_widget.insert(cursor_pos, fraction_text)
        
        # Guardar información de la fracción
        fraction_info = {
            'id': frac_id,
            'start': cursor_pos,
            'numerator_start': cursor_pos,
            'numerator_end': f"{cursor_pos}+3c",
            'denominator_start': f"{cursor_pos}+5c",
            'denominator_end': f"{cursor_pos}+8c",
            'end': f"{cursor_pos}+9c"
        }
        
        self.fractions.append(fraction_info)
        self.current_fraction = fraction_info
        
        # Posicionar cursor en el numerador
        self.text_widget.mark_set(tk.INSERT, fraction_info['numerator_start'])
        self.text_widget.focus_set()
        
        # Resaltar numerador
        self.highlight_fraction_part(fraction_info, 'numerator')
        
        # Llamar callback si existe
        if self.callback:
            self.callback()
    
    def highlight_fraction_part(self, fraction_info, part):
        """Resalta la parte activa de la fracción"""
        # Limpiar resaltados anteriores
        self.text_widget.tag_remove('cursor_highlight', '1.0', tk.END)
        
        if part == 'numerator':
            start = fraction_info['numerator_start']
            end = fraction_info['numerator_end']
        elif part == 'denominator':
            start = fraction_info['denominator_start']
            end = fraction_info['denominator_end']
        else:
            return
        
        self.text_widget.tag_add('cursor_highlight', start, end)
    
    def on_key_release(self, event):
        """Maneja eventos de teclado"""
        # Actualizar posición del cursor
        self.cursor_position = self.text_widget.index(tk.INSERT)
        
        # Verificar si estamos en una fracción
        self.check_fraction_context()
        
        # Validar expresión
        self.validate_expression()
        
        # Llamar callback
        if self.callback:
            self.callback()
    
    def check_fraction_context(self):
        """Verifica si el cursor está en una fracción y resalta la parte correspondiente"""
        cursor_pos = self.text_widget.index(tk.INSERT)
        
        for fraction in self.fractions:
            # Verificar si estamos en el numerador
            if self.is_in_range(cursor_pos, fraction['numerator_start'], fraction['numerator_end']):
                self.highlight_fraction_part(fraction, 'numerator')
                self.active_fraction = fraction
                return
            
            # Verificar si estamos en el denominador
            elif self.is_in_range(cursor_pos, fraction['denominator_start'], fraction['denominator_end']):
                self.highlight_fraction_part(fraction, 'denominator')
                self.active_fraction = fraction
                return
        
        # No estamos en ninguna fracción
        self.text_widget.tag_remove('cursor_highlight', '1.0', tk.END)
        self.active_fraction = None
    
    def is_in_range(self, pos, start, end):
        """Verifica si una posición está en un rango"""
        try:
            pos_line, pos_col = map(int, pos.split('.'))
            start_line, start_col = map(int, start.split('.'))
            end_line, end_col = map(int, end.split('.'))
            
            if pos_line == start_line == end_line:
                return start_col <= pos_col < end_col
            return False
        except:
            return False
    
    def on_arrow_left(self, event):
        """Maneja flecha izquierda - navegación inteligente"""
        if self.active_fraction:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Si estamos en el denominador y vamos hacia la izquierda, saltar al numerador
            if self.is_in_range(cursor_pos, self.active_fraction['denominator_start'], self.active_fraction['denominator_end']):
                # Verificar si estamos al inicio del denominador
                if cursor_pos == self.active_fraction['denominator_start']:
                    # Saltar al final del numerador
                    self.text_widget.mark_set(tk.INSERT, self.active_fraction['numerator_end'])
                    self.highlight_fraction_part(self.active_fraction, 'numerator')
                    return 'break'
        
        # Navegación normal
        self.check_fraction_context()
    
    def on_arrow_right(self, event):
        """Maneja flecha derecha - navegación inteligente"""
        if self.active_fraction:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Si estamos en el numerador y vamos hacia la derecha, saltar al denominador
            if self.is_in_range(cursor_pos, self.active_fraction['numerator_start'], self.active_fraction['numerator_end']):
                # Verificar si estamos al final del numerador
                if cursor_pos == f"{self.active_fraction['numerator_end']}-1c":
                    # Saltar al inicio del denominador
                    self.text_widget.mark_set(tk.INSERT, self.active_fraction['denominator_start'])
                    self.highlight_fraction_part(self.active_fraction, 'denominator')
                    return 'break'
        
        # Navegación normal
        self.check_fraction_context()
    
    def on_arrow_up(self, event):
        """Flecha arriba - saltar de denominador a numerador"""
        if self.active_fraction:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Si estamos en el denominador, saltar al numerador
            if self.is_in_range(cursor_pos, self.active_fraction['denominator_start'], self.active_fraction['denominator_end']):
                # Calcular posición relativa en el denominador
                rel_pos = self.get_relative_position(cursor_pos, self.active_fraction['denominator_start'])
                # Mover a posición equivalente en el numerador
                new_pos = f"{self.active_fraction['numerator_start']}+{rel_pos}c"
                self.text_widget.mark_set(tk.INSERT, new_pos)
                self.highlight_fraction_part(self.active_fraction, 'numerator')
                return 'break'
    
    def on_arrow_down(self, event):
        """Flecha abajo - saltar de numerador a denominador"""
        if self.active_fraction:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Si estamos en el numerador, saltar al denominador
            if self.is_in_range(cursor_pos, self.active_fraction['numerator_start'], self.active_fraction['numerator_end']):
                # Calcular posición relativa en el numerador
                rel_pos = self.get_relative_position(cursor_pos, self.active_fraction['numerator_start'])
                # Mover a posición equivalente en el denominador
                new_pos = f"{self.active_fraction['denominator_start']}+{rel_pos}c"
                self.text_widget.mark_set(tk.INSERT, new_pos)
                self.highlight_fraction_part(self.active_fraction, 'denominator')
                return 'break'
    
    def on_tab(self, event):
        """Tab - navegar entre partes de la fracción o insertar fracción"""
        if self.active_fraction:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Si estamos en el numerador, saltar al denominador
            if self.is_in_range(cursor_pos, self.active_fraction['numerator_start'], self.active_fraction['numerator_end']):
                self.text_widget.mark_set(tk.INSERT, self.active_fraction['denominator_start'])
                self.highlight_fraction_part(self.active_fraction, 'denominator')
                return 'break'
            
            # Si estamos en el denominador, saltar después de la fracción
            elif self.is_in_range(cursor_pos, self.active_fraction['denominator_start'], self.active_fraction['denominator_end']):
                self.text_widget.mark_set(tk.INSERT, self.active_fraction['end'])
                self.text_widget.tag_remove('cursor_highlight', '1.0', tk.END)
                self.active_fraction = None
                return 'break'
        
        # Si no hay fracción activa, insertar una nueva
        self.insert_fraction()
        return 'break'
    
    def on_return(self, event):
        """Return - finalizar edición de fracción"""
        if self.active_fraction:
            # Mover cursor después de la fracción
            self.text_widget.mark_set(tk.INSERT, self.active_fraction['end'])
            self.text_widget.tag_remove('cursor_highlight', '1.0', tk.END)
            self.active_fraction = None
            return 'break'
    
    def on_click(self, event):
        """Maneja clics del mouse"""
        # Actualizar posición y verificar contexto
        self.cursor_position = self.text_widget.index(tk.INSERT)
        self.check_fraction_context()
    
    def get_relative_position(self, pos, start):
        """Calcula posición relativa dentro de un rango"""
        try:
            pos_line, pos_col = map(int, pos.split('.'))
            start_line, start_col = map(int, start.split('.'))
            
            if pos_line == start_line:
                return pos_col - start_col
            return 0
        except:
            return 0
    
    def get_text(self):
        """Obtiene el texto completo del editor"""
        return self.text_widget.get("1.0", tk.END).strip()
    
    def set_text(self, text):
        """Establece el texto del editor"""
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text)
        self.fractions.clear()
        self.active_fraction = None
    
    def convert_to_sympy(self):
        """Convierte el texto visual a formato compatible con SymPy"""
        text = self.get_text()
        
        # Reemplazar fracciones visuales por formato SymPy
        # Patrón: [contenido]/[contenido]
        pattern = r'\[([^\]]*)\]/\[([^\]]*)\]'
        
        def replace_fraction(match):
            numerator = match.group(1).strip()
            denominator = match.group(2).strip()
            
            # Si numerador o denominador están vacíos, asumir 1
            if not numerator:
                numerator = "1"
            if not denominator:
                denominator = "1"
            
            # Convertir a formato SymPy
            return f"({numerator})/({denominator})"
        
        # Aplicar reemplazo
        sympy_text = re.sub(pattern, replace_fraction, text)
        
        # Limpiar espacios extra
        sympy_text = sympy_text.replace(' ', '')
        
        return sympy_text
    
    def validate_expression(self):
        """Valida la expresión actual"""
        try:
            sympy_text = self.convert_to_sympy()
            # Intentar parsear con SymPy para validar
            import sympy as sp
            sp.sympify(sympy_text)
            return True
        except:
            return False
    
    def insert_symbol(self, symbol):
        """Inserta un símbolo en la posición actual con soporte Microsoft Math Engine"""
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
            
            # Mapeo de símbolos naturales a notación Microsoft Math Engine
            natural_mappings = {
                # Potencias naturales
                'x²': 'x²',
                'x³': 'x³', 
                'x^': 'x^',
                
                # Funciones naturales
                'ln(': 'ln(',
                
                # Operadores naturales
                '^': '^',
                
                # Símbolos especiales que el engine puede parsear
                'pi': 'pi',
                'sqrt(': 'sqrt(',
                'exp(': 'exp(',
                'log(': 'log(',
                'sin(': 'sin(',
                'cos(': 'cos(',
                'tan(': 'tan(',
                'factorial(': 'factorial(',
                'abs(': 'abs(',
                'floor(': 'floor(',
                
                # Fracciones naturales
                '1/2': '1/2',
                '1/3': '1/3',
                '1/4': '1/4',
                '2/3': '2/3',
                '3/4': '3/4',
                '1/pi': '1/pi',
                
                # Funciones avanzadas
                'limit(': 'limit(',
                'sum(': 'sum(',
                'product(': 'product(',
                '**(1/3)': '**(1/3)',
                '**(1/4)': '**(1/4)',
                '**(1/': '**(1/',
                '10^': '10^',
                '2^': '2^'
            }
            
            # Usar mapeo natural si existe, sino usar el símbolo original
            insert_text = natural_mappings.get(symbol, symbol)
            
            # Insertar el texto
            self.text_widget.insert(cursor_pos, insert_text)
            
            # Auto-cerrar paréntesis para funciones
            if symbol in ['sqrt(', 'exp(', 'log(', 'ln(', 'sin(', 'cos(', 'tan(',
                          'asin(', 'acos(', 'atan(', 'sinh(', 'cosh(', 'tanh(',
                          'factorial(', 'abs(', 'floor(', 'limit(', 'sum(', 'product(']:
                self.text_widget.insert(tk.INSERT, ')')
                # Mover cursor dentro de los paréntesis
                new_pos = self.text_widget.index(tk.INSERT)
                new_pos = f"{new_pos}-1c"
                self.text_widget.mark_set(tk.INSERT, new_pos)
            
            # Para x^, posicionar cursor después del ^
            elif symbol == 'x^':
                # El cursor ya está en la posición correcta
                pass
            
            # Para fracciones, no hacer nada especial
            elif symbol in ['1/2', '1/3', '1/4', '2/3', '3/4', '1/pi']:
                pass
            
            # Actualizar contexto
            self.check_fraction_context()
            
            # Llamar callback
            if self.callback:
                self.callback()
                
        except Exception as e:
            # Fallback: insertar símbolo original
            cursor_pos = self.text_widget.index(tk.INSERT)
            self.text_widget.insert(cursor_pos, symbol)
            
            # Actualizar contexto
            self.check_fraction_context()
            
            # Llamar callback
            if self.callback:
                self.callback()
    
    def pack(self, **kwargs):
        """Empaqueta el widget"""
        self.text_widget.pack(**kwargs)
    
    def focus_set(self):
        """Establece el foco"""
        self.text_widget.focus_set()

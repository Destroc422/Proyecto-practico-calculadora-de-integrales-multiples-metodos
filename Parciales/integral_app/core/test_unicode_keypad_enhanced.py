#!/usr/bin/env python3
"""
Test script for the enhanced Unicode scientific keypad
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_unicode_keypad_enhanced():
    """Test the enhanced Unicode scientific keypad"""
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Test - Teclado Científico Unicode Mejorado")
    root.geometry("1200x800")
    
    # Create a simple math editor for testing
    class TestMathEditor:
        def __init__(self, parent):
            self.text_widget = tk.Text(parent, height=8, width=80, font=('Arial', 12))
            self.text_widget.pack(pady=10, padx=10, fill="both", expand=True)
            
            # Add a label to show current content
            self.label = ttk.Label(parent, text="Contenido actual: ", font=('Arial', 10))
            self.label.pack()
        
        def insert_symbol(self, symbol):
            """Insert a symbol into the text widget"""
            self.text_widget.insert(tk.END, symbol)
            self.update_label()
        
        def insert_fraction(self):
            """Insert a fraction template"""
            self.text_widget.insert(tk.END, "(/)")
            self.update_label()
        
        def set_text(self, text):
            """Set the text widget content"""
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(1.0, text)
            self.update_label()
        
        def get_text(self):
            """Get the text widget content"""
            return self.text_widget.get(1.0, tk.END).strip()
        
        def convert_to_sympy(self):
            """Convert to SymPy (simplified version)"""
            return self.get_text()
        
        def update_label(self):
            """Update the label with current content"""
            content = self.text_widget.get(1.0, tk.END).strip()
            self.label.config(text=f"Contenido actual: {content}")
    
    # Create test frame
    test_frame = ttk.Frame(root, padding=20)
    test_frame.pack(fill="both", expand=True)
    
    # Create math editor
    math_editor = TestMathEditor(test_frame)
    
    # Create enhanced scientific keypad
    try:
        from ui.scientific_keypad import ScientificKeypad
        keypad = ScientificKeypad(test_frame, math_editor)
        print("Teclado científico Unicode mejorado creado exitosamente!")
    except Exception as e:
        print(f"Error creando teclado: {e}")
        return
    
    # Add test instructions
    instructions = ttk.Label(test_frame, text=(
        "Instrucciones de prueba del Teclado Unicode Mejorado:\n"
        "1. Prueba los símbolos Unicode en la sección 'Símbolos Unicode'\n"
        "2. Verifica las letras griegas en 'Letras Griegas'\n"
        "3. Prueba las integrales con símbolos Unicode\n"
        "4. Test las fracciones Unicode (½, ¼, ¾, etc.)\n"
        "5. Usa los botones de control mejorados (Verificar, Formato, Simplificar, Evaluar)\n"
        "6. Comprueba que todas las fuentes Unicode se muestran correctamente"
    ), font=('Arial', 10))
    instructions.pack(pady=10)
    
    # Add test buttons for common Unicode expressions
    def test_unicode_expressions():
        """Test common Unicode expressions"""
        test_expressions = [
            "int (3x² + 5x) dx",
            "integral (x³ + 2x² + x) dx",
            "sin(2x) + cos(3x)",
            "x² + 2x + 1",
            "sqrt(x² + y²)",
            "alpha + beta + gamma",
            "sum_{i=1}^{n} i²",
            "product_{i=1}^{n} i",
            "limit_{x->0} sin(x)/x",
            "partial f/partial x"
        ]
        
        for expr in test_expressions:
            math_editor.set_text(expr)
            root.update()
            print(f"Test: {expr}")
            root.after(500)  # Wait 0.5 seconds
    
    def test_unicode_symbols():
        """Test individual Unicode symbols"""
        symbols = [
            "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta",
            "iota", "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma",
            "tau", "upsilon", "phi", "chi", "psi", "omega",
            "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
            "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Pi", "Rho", "Sigma",
            "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega",
            "int", "integral", "sum", "product", "partial", "nabla", "infinity",
            "sqrt", "forall", "exists", "empty", "in", "notin", "subset", "superset",
            "le", "ge", "ne", "approx", "equiv", "implies", "iff",
            "Natural", "Integer", "Real", "Rational", "Complex",
            "½", "¼", "¾", "¹", "²", "³", "¼", "½", "¾"
        ]
        
        for symbol in symbols:
            math_editor.set_text(symbol)
            root.update()
            root.after(200)  # Wait 0.2 seconds
    
    # Test buttons
    test_frame_buttons = ttk.Frame(test_frame)
    test_frame_buttons.pack(pady=10)
    
    ttk.Button(test_frame_buttons, text="Probar Expresiones Unicode", command=test_unicode_expressions).pack(side="left", padx=5)
    ttk.Button(test_frame_buttons, text="Probar Símbolos Unicode", command=test_unicode_symbols).pack(side="left", padx=5)
    ttk.Button(test_frame_buttons, text="Limpiar", command=lambda: math_editor.set_text("")).pack(side="left", padx=5)
    
    # Status label
    status_label = ttk.Label(test_frame, text="Estado: Listo para probar", font=('Arial', 10, 'bold'))
    status_label.pack(pady=5)
    
    # Auto-close after 30 seconds
    def auto_close():
        status_label.config(text="Cerrando automáticamente...")
        root.after(1000, root.destroy)
    
    root.after(30000, auto_close)
    
    print("Iniciando prueba del teclado científico Unicode mejorado...")
    print("La ventana se cerrará automáticamente después de 30 segundos.")
    
    root.mainloop()
    print("Prueba completada!")

if __name__ == "__main__":
    test_unicode_keypad_enhanced()

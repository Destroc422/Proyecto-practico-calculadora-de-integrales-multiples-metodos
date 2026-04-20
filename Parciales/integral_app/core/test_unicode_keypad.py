#!/usr/bin/env python3
"""
Test script for the Unicode scientific keypad
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.scientific_keypad import ScientificKeypad
    from ui.math_editor import MathEditor
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("This test requires the full application environment.")
    sys.exit(1)

def test_unicode_keypad():
    """Test the Unicode scientific keypad"""
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Test - Teclado Científico Unicode")
    root.geometry("800x600")
    
    # Create a simple math editor for testing
    class TestMathEditor:
        def __init__(self, parent):
            self.text_widget = tk.Text(parent, height=5, width=50)
            self.text_widget.pack(pady=10)
            
            # Add a label to show current content
            self.label = ttk.Label(parent, text="Contenido actual: ")
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
        
        def update_label(self):
            """Update the label with current content"""
            content = self.text_widget.get(1.0, tk.END).strip()
            self.label.config(text=f"Contenido actual: {content}")
    
    # Create test frame
    test_frame = ttk.Frame(root, padding=20)
    test_frame.pack(fill="both", expand=True)
    
    # Create math editor
    math_editor = TestMathEditor(test_frame)
    
    # Create scientific keypad
    try:
        keypad = ScientificKeypad(test_frame, math_editor)
        print("Teclado científico Unicode creado exitosamente!")
    except Exception as e:
        print(f"Error creando teclado: {e}")
        return
    
    # Add test instructions
    instructions = ttk.Label(test_frame, text=(
        "Instrucciones de prueba:\n"
        "1. Presiona los botones del teclado científico\n"
        "2. Verifica que los símbolos Unicode (, ², ³) aparecen correctamente\n"
        "3. Prueba los botones de integrales\n"
        "4. Verifica las potencias Unicode (x², x³)\n"
        "5. Prueba las funciones matemáticas"
    ))
    instructions.pack(pady=10)
    
    # Add a test button to verify Unicode symbols
    def test_unicode_symbols():
        """Test specific Unicode symbols"""
        test_symbols = [
            "int (3x + 5) dx",
            "integral x² dx", 
            "x² + 2x + 1",
            "sin(x) + cos(x)",
            "0 to 1 int x² dx"
        ]
        
        for symbol in test_symbols:
            math_editor.set_text(symbol)
            root.update()
            print(f"Test: {symbol}")
            root.after(1000)  # Wait 1 second
    
    test_button = ttk.Button(test_frame, text="Probar Símbolos Unicode", command=test_unicode_symbols)
    test_button.pack(pady=5)
    
    # Start the GUI
    print("Iniciando prueba del teclado científico Unicode...")
    print("La ventana se cerrará automáticamente después de 10 segundos.")
    
    # Auto-close after 10 seconds
    root.after(10000, root.destroy)
    
    root.mainloop()
    print("Prueba completada!")

if __name__ == "__main__":
    test_unicode_keypad()

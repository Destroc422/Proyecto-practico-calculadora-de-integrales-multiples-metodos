#!/usr/bin/env python3
"""
Demo script to show the professional result format for Calculadora de Integrales PRO v4.0
"""

def generate_result_format(func_input, variable="x", method="auto"):
    """
    Generate professional result format for integral calculations
    """
    # Parse and integrate the function
    import sympy as sp
    
    # Parse the function
    try:
        x = sp.symbols(variable)
        func = sp.sympify(func_input)
        
        # Integrate
        result = sp.integrate(func, x)
        
        # Generate LaTeX expressions
        func_latex = sp.latex(func)
        result_latex = sp.latex(result)
        
        # Generate the professional output
        output = f"""
Resultado

[\\int{{{func_latex}}} \\, d{variable} = {result_latex}]

de la Integral
==================================================

[LaTeX Mathematical Expression]
Expression: [\\int {func_latex} \\, d{variable} = {result_latex}]

Información del Cálculo:
------------------------
Método: {method}
Variable: {variable}
Función original: {func_input}
"""
        
        return output.strip()
        
    except Exception as e:
        return f"Error processing function: {e}"

# Demo with a sample function
if __name__ == "__main__":
    # Example function
    sample_func = "x**2 + 3*x + 2"
    
    print("=== Calculadora de Integrales PRO v4.0 - Result Engine Demo ===")
    print()
    print(generate_result_format(sample_func))

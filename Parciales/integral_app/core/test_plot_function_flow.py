#!/usr/bin/env python3
"""
Test script to simulate the exact plot_function flow and identify the issue
"""
import sys
import os
import numpy as np
import sympy as sp

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_plot_function_flow():
    """Test the exact plot_function flow to identify the issue"""
    
    print("=== Test del Flujo Exacto de plot_function ===")
    print()
    
    print("Test 1: Simulación del Flujo Completo de plot_function")
    print("=" * 60)
    
    def simulate_plot_function_flow(function_text):
        """Simulate the exact plot_function flow"""
        try:
            print(f"\n  Simulación con: '{function_text}'")
            
            # Step 1: Check if function_text is empty
            if not function_text.strip():
                print("    [ERROR] Función vacía")
                return False
            
            # Step 2: Check for integral notation
            print(f"    Verificando notación de integral...")
            has_integral = ('integrate' in function_text.lower() or 
                           'd' in function_text and 'dx' in function_text)
            print(f"    ¿Contiene notación de integral? {has_integral}")
            
            if has_integral:
                print("    Procesando como integral...")
                # This would integrate the function - for testing, we'll skip
                print("    [SKIP] Procesamiento de integral omitido para prueba")
                return "INTEGRAL_PROCESSED"
            
            # Step 3: Regular function parsing
            print("    Haciendo parsing de función regular...")
            try:
                # Simulate parser.parse()
                parsed_func = sp.sympify(function_text)
                print(f"    Parse exitoso: {parsed_func}")
                display_text = function_text
            except Exception as parse_err:
                print(f"    [ERROR] Parse fallido: {parse_err}")
                return False
            
            # Step 4: Variable setup
            variable = 'x'  # Default variable
            var_symbol = sp.Symbol(variable)
            print(f"    Variable: {variable}")
            
            # Step 5: Range setup
            try:
                x_min = -10.0
                x_max = 10.0
                print(f"    Rango: [{x_min}, {x_max}]")
            except:
                x_min, x_max = -10, 10
                print(f"    Rango por defecto: [{x_min}, {x_max}]")
            
            # Step 6: Generate data
            x = np.linspace(x_min, x_max, 1000)
            print(f"    Puntos x generados: {len(x)}")
            
            # Step 7: Convert to numpy function
            try:
                f = sp.lambdify(var_symbol, parsed_func, 'numpy')
                y = f(x)
                print(f"    y type: {type(y)}")
                print(f"    y shape: {y.shape if hasattr(y, 'shape') else 'N/A'}")
                
                # Check first few values
                if hasattr(y, '__getitem__'):
                    print(f"    Primeros 5 valores y: {y[:5]}")
                else:
                    print(f"    Valor y: {y}")
                    
            except Exception as lambdify_err:
                print(f"    [ERROR] Lambdify fallido: {lambdify_err}")
                return False
            
            # Step 8: Handle potential infinities with robust validation
            print("    Verificando valores finitos...")
            try:
                mask = np.isfinite(y)
                finite_count = np.sum(mask)
                print(f"    Método estándar: {finite_count}/1000 finitos")
            except (TypeError, ValueError) as e:
                print(f"    Método estándar falló: {e}")
                print("    Usando fallback robusto...")
                
                # Robust fallback
                mask = []
                for i, val in enumerate(y):
                    try:
                        if isinstance(val, (int, float, np.number)) and not isinstance(val, bool):
                            if isinstance(val, np.number):
                                mask.append(np.isfinite(val))
                            else:
                                import math
                                mask.append(math.isfinite(val))
                        else:
                            mask.append(False)
                    except (TypeError, ValueError, AttributeError):
                        mask.append(False)
                
                mask = np.array(mask, dtype=bool)
                finite_count = np.sum(mask)
                print(f"    Fallback robusto: {finite_count}/1000 finitos")
            
            # Step 9: Check if any finite values
            if not np.any(mask):
                print("    [ERROR] 'La función no tiene valores finitos en el rango especificado'")
                return False
            
            print("    [OK] Función tiene valores finitos")
            return True
            
        except Exception as e:
            print(f"    [ERROR] Error general: {e}")
            return False
    
    # Test cases that should work
    test_cases = [
        "x**2 + 3*x + 2",
        "sin(x)",
        "cos(x)",
        "exp(x)",
        "log(x)",
        "sqrt(x)",
        "1/x",
        "x**3 - 2*x**2 + x - 1",
        "abs(x)",
        "tan(x)"
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for test_case in test_cases:
        result = simulate_plot_function_flow(test_case)
        if result is True:
            success_count += 1
        elif result == "INTEGRAL_PROCESSED":
            success_count += 1  # Count as success for this test
    
    print(f"\nResultados flujo completo: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print()
    
    print("Test 2: Diagnóstico de Problemas Específicos")
    print("=" * 45)
    
    # Test problematic cases
    problematic_cases = [
        ("", "Función vacía"),
        ("   ", "Solo espacios"),
        ("x**2 + 3*x + 2 +", "Expresión incompleta"),
        ("x**2 + 3*x + 2)", "Paréntesis desbalanceado"),
        ("(x**2 + 3*x + 2", "Paréntesis desbalanceado"),
        ("x**2 + 3*x + 2dx", "Notación dx ambigua"),
        ("integrate(x**2 + 3*x + 2)", "Notación integrate"),
        ("x**2 + 3*x + 2 dx", "Notación dx"),
        ("sin(x) + cos(x) + tan(x) +", "Expresión incompleta")
    ]
    
    problematic_results = []
    
    for test_case, description in problematic_cases:
        print(f"\n  Probando: {description} ('{test_case}')")
        result = simulate_plot_function_flow(test_case)
        problematic_results.append((test_case, description, result))
    
    print()
    
    print("Test 3: Análisis de Casos que Deberían Fallar")
    print("=" * 50)
    
    # Analyze why some cases might fail
    for test_case, description, result in problematic_results:
        if result is False:
            print(f"  {description}: FALLÓ COMO SE ESPERABA")
        elif result is True:
            print(f"  {description}: FUNCIONÓ (inesperado)")
        else:
            print(f"  {description}: PROCESAMIENTO ESPECIAL ({result})")
    
    print()
    
    print("Test 4: Identificación del Problema Real")
    print("=" * 40)
    
    # The most likely issue is in the parsing step
    print("  Posibles causas del error 'no presenta valores finitos':")
    print("  1. El parser está devolviendo una expresión inválida")
    print("  2. lambdify está generando una función que siempre retorna NaN/inf")
    print("  3. Hay un problema en la conversión de tipos de datos")
    print("  4. El rango de valores está causando problemas numéricos")
    print("  5. Hay un error silencioso en el parsing que no se detecta")
    
    print()
    
    # Test the parser specifically
    print("Test 5: Verificación del Parser")
    print("=" * 30)
    
    try:
        # Try to import the actual parser
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
        from parser import ExpressionParser
        
        parser = ExpressionParser()
        print("  Parser importado exitosamente")
        
        # Test the parser with common expressions
        parser_test_cases = ["x**2 + 3*x + 2", "sin(x)", "cos(x)", "exp(x)"]
        
        for test_case in parser_test_cases:
            try:
                result = parser.parse(test_case)
                print(f"  Parser '{test_case}' -> {result} [OK]")
            except Exception as e:
                print(f"  Parser '{test_case}' -> ERROR: {e}")
                
    except ImportError as e:
        print(f"  No se pudo importar el parser: {e}")
        print("  Usando sympify como fallback")
    
    print()
    
    # Overall assessment
    print("=== CONCLUSIÓN ===")
    if success_count >= total_count * 0.8:
        print("DIAGNÓSTICO: El flujo de plot_function funciona correctamente.")
        print("El problema debe estar en:")
        print("- La comunicación con la interfaz")
        print("- El estado de las variables en tiempo de ejecución")
        print("- Un error específico con la entrada del usuario")
    else:
        print("DIAGNÓSTICO: Hay un problema real en el flujo de plot_function.")
        print("Se necesita revisar la lógica de parsing o evaluación.")
    
    print("\n=== RECOMENDACIONES ===")
    print("1. Agregar logging detallado en plot_function")
    print("2. Verificar el estado de self.parser")
    print("3. Revisar la entrada del usuario antes del parsing")
    print("4. Agregar validación de expresiones antes de lambdify")
    print("5. Mejorar el manejo de errores en cada paso del proceso")
    
    return success_count >= total_count * 0.8

if __name__ == "__main__":
    test_plot_function_flow()

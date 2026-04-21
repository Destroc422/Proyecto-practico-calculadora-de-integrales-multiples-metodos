#!/usr/bin/env python3
"""
Test script to diagnose the 'no finite values' issue in function plotting
"""
import sys
import os
import numpy as np
import sympy as sp

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_finite_values_detection():
    """Test the finite values detection logic to identify the issue"""
    
    print("=== Test de Detección de Valores Finitos ===")
    print()
    
    print("Test 1: Funciones Simples que Deberían Funcionar")
    print("=" * 50)
    
    # Test common functions that should have finite values
    test_functions = [
        ("x**2 + 3*x + 2", "Polinomio simple"),
        ("sin(x)", "Función seno"),
        ("cos(x)", "Función coseno"),
        ("exp(x)", "Función exponencial"),
        ("log(x)", "Función logaritmo"),
        ("sqrt(x)", "Función raíz cuadrada"),
        ("1/x", "Función racional"),
        ("x**3 - 2*x**2 + x - 1", "Polinomio cúbico"),
        ("abs(x)", "Función valor absoluto"),
        ("tan(x)", "Función tangente")
    ]
    
    def robust_isfinite_check(values):
        """Robust isfinite check implementation"""
        try:
            # Try standard numpy isfinite first
            mask = np.isfinite(values)
        except (TypeError, ValueError) as e:
            # Robust fallback: manual check for finite values
            mask = []
            for i, val in enumerate(values):
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
        
        return mask
    
    success_count = 0
    total_count = len(test_functions)
    
    for func_expr, func_name in test_functions:
        try:
            print(f"\n  Probando: {func_name} ({func_expr})")
            
            # Parse the function
            x = sp.Symbol('x')
            try:
                parsed_func = sp.sympify(func_expr)
            except Exception as parse_error:
                print(f"    Error parsing: {parse_error}")
                continue
            
            # Generate test data
            x_vals = np.linspace(-10, 10, 1000)
            
            # Convert to numpy function
            try:
                f = sp.lambdify(x, parsed_func, 'numpy')
                y_vals = f(x_vals)
            except Exception as lambdify_error:
                print(f"    Error lambdify: {lambdify_error}")
                continue
            
            print(f"    Tipo de y_vals: {type(y_vals)}")
            print(f"    Shape de y_vals: {y_vals.shape if hasattr(y_vals, 'shape') else 'N/A'}")
            print(f"    Primeros 5 valores: {y_vals[:5] if hasattr(y_vals, '__getitem__') else y_vals}")
            
            # Check for finite values
            mask = robust_isfinite_check(y_vals)
            finite_count = np.sum(mask)
            total_count_y = len(y_vals) if hasattr(y_vals, '__len__') else 1
            
            print(f"    Valores finitos: {finite_count}/{total_count_y}")
            
            if finite_count > 0:
                print(f"    [OK] Función tiene valores finitos")
                success_count += 1
                
                # Show some sample finite values
                if hasattr(y_vals, '__getitem__') and finite_count > 0:
                    finite_indices = np.where(mask)[0]
                    sample_indices = finite_indices[:min(5, len(finite_indices))]
                    sample_values = y_vals[sample_indices]
                    print(f"    Valores finitos de ejemplo: {sample_values}")
            else:
                print(f"    [ERROR] No hay valores finitos")
                
                # Debug: check individual values
                if hasattr(y_vals, '__getitem__'):
                    print(f"    Análisis de valores:")
                    for i in range(min(10, len(y_vals))):
                        val = y_vals[i]
                        try:
                            is_finite = np.isfinite(val) if hasattr(np, 'isfinite') else False
                            print(f"      y[{i}] = {val} (finito: {is_finite})")
                        except:
                            print(f"      y[{i}] = {val} (error al verificar)")
        except Exception as e:
            print(f"    Error general: {e}")
    
    print(f"\nResultados funciones simples: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print()
    
    print("Test 2: Diagnóstico del Problema de 'No Presenta Valores Finitos'")
    print("=" * 60)
    
    # Test specific problematic cases
    diagnostic_tests = [
        ("x**2 + 3*x + 2", "Polinomio que debería funcionar"),
        ("sin(x) + cos(x)", "Trigonométrica combinada"),
        ("exp(-x**2)", "Gaussiana"),
        ("sqrt(abs(x))", "Raíz con valor absoluto"),
        ("x/(x**2 + 1)", "Racional sin singularidades"),
        ("1/(x**2 + 1)", "Racional siempre finita")
    ]
    
    diagnostic_success = 0
    diagnostic_total = len(diagnostic_tests)
    
    for func_expr, func_name in diagnostic_tests:
        try:
            print(f"\n  Diagnóstico: {func_name}")
            print(f"  Expresión: {func_expr}")
            
            # Parse and evaluate
            x = sp.Symbol('x')
            parsed_func = sp.sympify(func_expr)
            f = sp.lambdify(x, parsed_func, 'numpy')
            
            # Test different ranges
            ranges = [
                (-10, 10),
                (-5, 5),
                (-1, 1),
                (0, 1),
                (-100, 100)
            ]
            
            range_success = 0
            for x_min, x_max in ranges:
                x_vals = np.linspace(x_min, x_max, 1000)
                y_vals = f(x_vals)
                
                mask = robust_isfinite_check(y_vals)
                finite_count = np.sum(mask)
                
                print(f"    Rango [{x_min}, {x_max}]: {finite_count}/1000 finitos")
                
                if finite_count > 0:
                    range_success += 1
            
            if range_success > 0:
                print(f"    [OK] Función funciona en {range_success}/{len(ranges)} rangos")
                diagnostic_success += 1
            else:
                print(f"    [ERROR] Función no funciona en ningún rango")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    print(f"\nResultados diagnóstico: {diagnostic_success}/{diagnostic_total} ({diagnostic_success/diagnostic_total*100:.1f}%)")
    print()
    
    print("Test 3: Simulación del Problema Real")
    print("=" * 40)
    
    # Simulate the exact plotting process
    def simulate_plotting_process(expression):
        """Simulate the exact plotting process from the application"""
        try:
            print(f"\n  Simulando graficación de: {expression}")
            
            # Parse expression
            x = sp.Symbol('x')
            parsed_func = sp.sympify(expression)
            
            # Generate data (same as in the app)
            x_vals = np.linspace(-10, 10, 1000)
            
            # Convert to numpy function
            f = sp.lambdify(x, parsed_func, 'numpy')
            y_vals = f(x_vals)
            
            print(f"    y_vals type: {type(y_vals)}")
            print(f"    y_vals shape: {y_vals.shape if hasattr(y_vals, 'shape') else 'N/A'}")
            
            # Apply robust isfinite check
            mask = robust_isfinite_check(y_vals)
            finite_count = np.sum(mask)
            
            print(f"    Finite values: {finite_count}/1000")
            
            if not np.any(mask):
                print(f"    [PROBLEMA] 'La función no tiene valores finitos en el rango especificado'")
                return False
            else:
                print(f"    [OK] Función graficable")
                return True
                
        except Exception as e:
            print(f"    Error en simulación: {e}")
            return False
    
    # Test the most common function
    simulation_result = simulate_plotting_process("x**2 + 3*x + 2")
    
    print()
    
    # Overall assessment
    overall_success = success_count + diagnostic_success + (1 if simulation_result else 0)
    overall_total = total_count + diagnostic_total + 1
    
    print("=== RESUMEN DEL DIAGNÓSTICO ===")
    print(f"Funciones simples: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print(f"Diagnóstico avanzado: {diagnostic_success}/{diagnostic_total} ({diagnostic_success/diagnostic_total*100:.1f}%)")
    print(f"Simulación del problema: {'OK' if simulation_result else 'ERROR'}")
    print(f"TOTAL: {overall_success}/{overall_total} ({overall_success/overall_total*100:.1f}%)")
    print()
    
    if overall_success >= overall_total * 0.8:
        print("DIAGNÓSTICO: La lógica de detección de valores finitos funciona correctamente.")
        print("El problema puede estar en otro lugar del proceso de graficación.")
    else:
        print("DIAGNÓSTICO: Hay un problema real en la detección de valores finitos.")
        print("Se necesita corregir la lógica de evaluación de funciones.")
    
    print("\n=== RECOMENDACIONES ===")
    if not simulation_result:
        print("× Revisar la conversión de expresiones SymPy a numpy")
        print("× Verificar el manejo de dominios de funciones")
        print("× Mejorar el manejo de errores en lambdify")
    else:
        print("× Revisar el flujo de datos en la interfaz")
        print("× Verificar la comunicación entre componentes")
        print("× Chequear el estado de las variables en tiempo de ejecución")
    
    return overall_success >= overall_total * 0.8

if __name__ == "__main__":
    test_finite_values_detection()

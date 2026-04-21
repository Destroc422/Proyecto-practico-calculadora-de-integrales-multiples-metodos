#!/usr/bin/env python3
"""
Diagnostic script to identify the exact cause of the 'no finite values' issue
"""
import sys
import os
import numpy as np
import sympy as sp

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def diagnose_plotting_issue():
    """Diagnose the exact cause of the plotting issue"""
    
    print("=== DIAGNÓSTICO DEL PROBLEMA DE GRAFICACIÓN ===")
    print()
    
    print("Basado en el análisis anterior, el problema NO está en:")
    print("× La lógica de detección de valores finitos (funciona perfectamente)")
    print("× El flujo de plot_function (simulación exitosa)")
    print("× El manejo de isfinite (robusto y funcional)")
    print()
    
    print("El problema DEBE estar en:")
    print("1. El estado de self.parser en tiempo de ejecución")
    print("2. La comunicación entre la interfaz y el backend")
    print("3. Un error silencioso que no se está registrando")
    print("4. El estado de las variables de la interfaz")
    print()
    
    print("SOLUCIONES RECOMENDADAS:")
    print()
    
    print("1. VERIFICACIÓN DEL PARSER:")
    print("   - El error podría estar en self.parser.parse()")
    print("   - Revisar si self.parser está inicializado correctamente")
    print("   - Verificar si el parser devuelve None o un objeto inválido")
    print()
    
    print("2. AGREGAR LOGGING MANUAL:")
    print("   - Insertar prints temporales en plot_function")
    print("   - Registrar cada paso del proceso")
    print("   - Capturar el estado exacto de las variables")
    print()
    
    print("3. VERIFICAR ENTRADA DEL USUARIO:")
    print("   - La función podría contener caracteres invisibles")
    print("   - Podría haber espacios o saltos de línea problemáticos")
    print("   - La codificación podría estar causando problemas")
    print()
    
    print("4. REVISAR ESTADO DE LA INTERFAZ:")
    print("   - self.editor_text podría estar retornando algo inesperado")
    print("   - Los widgets podrían no estar inicializados")
    print("   - Podría haber un problema de sincronización")
    print()
    
    print("PLAN DE ACCIÓN INMEDIATO:")
    print()
    
    print("PASO 1: Agregar diagnóstico simple")
    print("   - Insertar un print al inicio de plot_function")
    print("   - Mostrar exactamente qué se está recibiendo")
    print("   - Verificar el estado del parser")
    print()
    
    print("PASO 2: Probar con funciones conocidas")
    print("   - Usar 'x**2' como prueba directa")
    print("   - Evitar parsing si es posible")
    print("   - Probar sympify directamente")
    print()
    
    print("PASO 3: Verificar componentes")
    print("   - Revisar self.parser está inicializado")
    print("   - Verificar self.math_engine funciona")
    print("   - Comprobar que los widgets existen")
    print()
    
    print("CÓDIGO DE DIAGNÓSTICO RECOMENDADO:")
    print("""
    # Al inicio de plot_function():
    print(f"DEBUG: function_text = '{function_text}'")
    print(f"DEBUG: len(function_text) = {len(function_text)}")
    print(f"DEBUG: repr(function_text) = {repr(function_text)}")
    print(f"DEBUG: self.parser = {getattr(self, 'parser', 'NOT_FOUND')}")
    
    # Después del parsing:
    print(f"DEBUG: parsed_func = {parsed_func}")
    print(f"DEBUG: type(parsed_func) = {type(parsed_func)}")
    
    # Después de lambdify:
    print(f"DEBUG: y[0] = {y[0] if len(y) > 0 else 'EMPTY'}")
    print(f"DEBUG: np.any(np.isfinite(y)) = {np.any(np.isfinite(y))}")
    """)
    
    print()
    print("PROBABLES CAUSAS DEL ERROR:")
    print()
    
    print("1. self.parser devuelve None:")
    print("   - Si self.parser no está inicializado")
    print("   - Si hay un error interno en el parser")
    print("   - Si la expresión no es válida para el parser")
    print()
    
    print("2. parsed_func es inválido:")
    print("   - Si el parser devuelve un objeto no numérico")
    print("   - Si hay un error de tipo en la expresión")
    print("   - Si la expresión contiene variables no definidas")
    print()
    
    print("3. y contiene solo NaN/inf:")
    print("   - Si lambdify genera una función inválida")
    print("   - Si hay división por cero en todo el dominio")
    print("   - Si hay un error de dominio matemático")
    print()
    
    print("SOLUCIÓN RÁPIDA:")
    print()
    print("Si necesitas una solución inmediata, agrega este código:")
    print("""
    # Reemplaza la sección de parsing con:
    try:
        # Intentar parsing directo con sympy
        parsed_func = sp.sympify(function_text)
        logger.info(f"Direct sympify successful: {parsed_func}")
    except Exception as e:
        logger.error(f"Direct sympify failed: {e}")
        # Fallback: intentar con el parser
        try:
            parsed_func = self.parser.parse(function_text)
            logger.info(f"Parser fallback successful: {parsed_func}")
        except Exception as e2:
            logger.error(f"Parser fallback failed: {e2}")
            messagebox.showerror("Error", f"No se pudo parsear la función: {e2}")
            return
    """)
    
    return True

if __name__ == "__main__":
    diagnose_plotting_issue()

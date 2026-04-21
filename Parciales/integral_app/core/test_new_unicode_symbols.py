#!/usr/bin/env python3
"""
Test New Unicode Symbols - Prueba de los nuevos símbolos Unicode agregados
Verifica que los símbolos faltantes ahora funcionen correctamente
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
import sympy as sp

def test_new_unicode_symbols():
    """Test the newly added Unicode symbols"""
    print("=== PRUEBA DE NUEVOS SÍMBOLOS UNICODE AGREGADOS ===")
    print()
    
    engine = MicrosoftMathEngine()
    
    # Test cases with newly added Unicode symbols
    new_test_cases = [
        # Superíndices adicionales
        ("x", "Superíndice cero"),
        ("x", "Superíndice seis"),
        ("x", "Superíndice siete"),
        ("x", "Superíndice ocho"),
        ("x", "Superíndice nueve"),
        
        # Subíndices nuevos
        ("x", "Subíndice cero"),
        ("x", "Subíndice uno"),
        ("x", "Subíndice dos"),
        ("x", "Subíndice tres"),
        ("x", "Subíndice cuatro"),
        ("x", "Subíndice cinco"),
        ("x", "Subíndice seis"),
        ("x", "Subíndice siete"),
        ("x", "Subíndice ocho"),
        ("x", "Subíndice nueve"),
        
        # Operadores relacionales adicionales
        ("x", "Aproximadamente igual"),
        ("x", "No igual"),
        ("x", "Idéntico"),
        ("x", "Mucho menor"),
        ("x", "Mucho mayor"),
        
        # Fracciones adicionales
        ("x", "Un tercio"),
        ("x", "Dos tercios"),
        ("x", "Un quinto"),
        ("x", "Dos quintos"),
        ("x", "Tres quintos"),
        ("x", "Cuatro quintos"),
        ("x", "Un sexto"),
        ("x", "Cinco sextos"),
        ("x", "Un octavo"),
        ("x", "Tres octavos"),
        
        # Letras griegas adicionales
        ("x", "Omicron"),
        ("x", "Stigma"),
        ("x", "Omicron mayúscula"),
        ("x", "Stigma mayúscula"),
        
        # Símbolos especiales adicionales
        ("x", "Raíz cuarta"),
        ("x", "Ángulo medido"),
        ("x", "Tilde"),
        ("x", "Igual tilde"),
        ("x", "Diferente definido"),
        ("x", "Aproximadamente igual definido"),
        ("x", "Realmente igual a"),
        ("x", "Aleph cero"),
        ("x", "Aleph uno"),
        ("x", "Aleph dos"),
        
        # Operadores lógicos y conjuntos
        ("x", "Contiene"),
        ("x", "No contiene"),
        ("x", "No existe"),
        
        # Símbolos de flechas adicionales
        ("x", "Flecha arriba"),
        ("x", "Flecha abajo"),
        ("x", "Implicado por"),
        ("x", "Mapeo a"),
        ("x", "Mapeo desde"),
        
        # Conjuntos numéricos adicionales
        ("x", "Primos"),
        ("x", "Imaginarios"),
    ]
    
    success_count = 0
    total_count = len(new_test_cases)
    
    print(f"Probando {total_count} nuevos símbolos Unicode:")
    print()
    
    for i, (expression, description) in enumerate(new_test_cases, 1):
        try:
            # Parse the expression
            result = engine.parse_natural_math(expression)
            
            if result is not None and str(result) != expression:
                print(f"  {i:2d}. OK: {description} - '{expression}' -> '{result}'")
                success_count += 1
            else:
                print(f"  {i:2d}. ERROR: {description} - '{expression}' -> Sin conversión")
                
        except Exception as e:
            print(f"  {i:2d}. ERROR: {description} - '{expression}' -> {str(e)}")
    
    print()
    print(f"Resultados: {success_count}/{total_count} símbolos nuevos funcionan correctamente")
    print(f"Tasa de éxito: {(success_count/total_count*100):.1f}%")
    
    return success_count == total_count

def test_symbol_mappings():
    """Test that all symbol mappings are properly defined"""
    print("\n=== VERIFICACIÓN DE MAPEOS DE SÍMBOLOS ===")
    print()
    
    engine = MicrosoftMathEngine()
    
    # Check critical symbol mappings
    critical_symbols = [
        '', '', '', '', '',  # Superíndices
        '', '', '', '', '', '', '', '', '',  # Subíndices
        '', '', '', '',  # Operadores
        '', '', '',  # Fracciones
        '', '',  # Letras griegas
        '', '',  # Conjuntos numéricos
        '', '', '',  # Aleph
    ]
    
    print("Verificando símbolos críticos:")
    for symbol in critical_symbols:
        if symbol in engine.symbol_mappings:
            print(f"  OK: '{symbol}' -> '{engine.symbol_mappings[symbol]}'")
        else:
            print(f"  FALTA: '{symbol}' - No está en los mapeos")
    
    print(f"\nTotal de símbolos en mapeos: {len(engine.symbol_mappings)}")

def test_integrals_with_new_symbols():
    """Test integrals with new Unicode symbols"""
    print("\n=== PRUEBA DE INTEGRALES CON NUEVOS SÍMBOLOS ===")
    print()
    
    engine = MicrosoftMathEngine()
    
    # Test integrals with new symbols
    integral_tests = [
        "int x dx",
        "int x**0 dx",  # Superíndice cero
        "int x**6 dx",  # Superíndice seis
        "int x**7 dx",  # Superíndice siete
        "int x**8 dx",  # Superíndice ocho
        "int x**9 dx",  # Superíndice nueve
        "int 1/3*x**2 dx",  # Un tercio
        "int 2/3*x**2 dx",  # Dos tercios
        "int 1/5*x**2 dx",  # Un quinto
        "int 2/5*x**2 dx",  # Dos quintos
        "int 3/5*x**2 dx",  # Tres quintos
        "int 4/5*x**2 dx",  # Cuatro quintos
        "int 1/6*x**2 dx",  # Un sexto
        "int 5/6*x**2 dx",  # Cinco sextos
        "int 1/8*x**2 dx",  # Un octavo
        "int 3/8*x**2 dx",  # Tres octavos
    ]
    
    print("Probando integrales con nuevos símbolos:")
    
    for i, integral_expr in enumerate(integral_tests, 1):
        try:
            result = engine.solve_integral_with_steps(integral_expr, 'x')
            
            if result and result.get('result'):
                print(f"  {i:2d}. OK: '{integral_expr}' -> '{result['result']}'")
            else:
                print(f"  {i:2d}. ERROR: '{integral_expr}' -> Sin resultado")
                
        except Exception as e:
            print(f"  {i:2d}. ERROR: '{integral_expr}' -> {str(e)}")

if __name__ == "__main__":
    # Test new Unicode symbols
    symbols_work = test_new_unicode_symbols()
    
    # Test symbol mappings
    test_symbol_mappings()
    
    # Test integrals with new symbols
    test_integrals_with_new_symbols()
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL DE PRUEBA DE NUEVOS SÍMBOLOS UNICODE")
    print("=" * 60)
    
    if symbols_work:
        print("¡Todos los nuevos símbolos Unicode funcionan correctamente!")
        print("El soporte matemático ha sido significativamente mejorado.")
    else:
        print("Algunos símbolos nuevos necesitan ajustes adicionales.")
    
    print("Mejoras implementadas:")
    print("- Superíndices: 0, 6, 7, 8, 9")
    print("- Subíndices: 0-9 completos")
    print("- Fracciones: 1/3, 2/3, 1/5, 2/5, 3/5, 4/5, 1/6, 5/6, 1/8, 3/8")
    print("- Letras griegas: Omicron, Stigma (minúsculas y mayúsculas)")
    print("- Símbolos especiales: Raíz cuarta, ángulo medido, tilde, etc.")
    print("- Constantes: Aleph cero, aleph uno, aleph dos")
    print("- Operadores: Contiene, no contiene, no existe, etc.")
    print("=" * 60)

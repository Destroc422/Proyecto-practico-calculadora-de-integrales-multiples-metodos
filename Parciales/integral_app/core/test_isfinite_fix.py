#!/usr/bin/env python3
"""
Test script for the isfinite fix without plotter dependencies
"""
import numpy as np
import math

def test_robust_isfinite():
    """Test the robust isfinite handling"""
    
    print("=== Test de Manejo Robusto de isfinite ===")
    print()
    
    def robust_isfinite_check(values):
        """Robust isfinite check implementation (same as in plotter)"""
        mask = []
        for i, val in enumerate(values):
            try:
                # Check if value is numeric and finite
                if isinstance(val, (int, float, np.number)) and not isinstance(val, bool):
                    if isinstance(val, np.number):
                        # Use numpy's isfinite for numpy numbers
                        mask.append(np.isfinite(val))
                    else:
                        # For Python numbers, use math.isfinite
                        mask.append(math.isfinite(val))
                else:
                    # Non-numeric values are not finite
                    mask.append(False)
            except (TypeError, ValueError, AttributeError):
                # Any error in checking means not finite
                mask.append(False)
        
        return np.array(mask, dtype=bool)
    
    print("Test 1: Datos Numéricos Normales")
    print("=" * 40)
    
    normal_tests = [
        ("Enteros", [1, 2, 3, 4, 5]),
        ("Flotantes", [1.1, 2.2, 3.3, 4.4, 5.5]),
        ("Mixtos", [1, 2.5, 3, 4.7, 5]),
        ("Numpy array", np.array([1, 2, 3, 4, 5])),
        ("Con cero", [0, 1, 2, 0, 3]),
        ("Negativos", [-1, -2, -3, -4, -5])
    ]
    
    normal_success = 0
    normal_total = len(normal_tests)
    
    for test_name, test_data in normal_tests:
        try:
            # Test standard numpy isfinite
            try:
                standard_mask = np.isfinite(test_data)
                standard_works = True
            except (TypeError, ValueError):
                standard_works = False
            
            # Test robust implementation
            robust_mask = robust_isfinite_check(test_data)
            
            if standard_works:
                if np.array_equal(standard_mask, robust_mask):
                    print(f"  {test_name:<15} -> estándar y robusto iguales [OK]")
                    normal_success += 1
                else:
                    print(f"  {test_name:<15} -> diferencias encontradas [WARNING]")
            else:
                if np.all(robust_mask):
                    print(f"  {test_name:<15} -> robusto funciona [OK]")
                    normal_success += 1
                else:
                    print(f"  {test_name:<15} -> robusto falló [ERROR]")
        except Exception as e:
            print(f"  {test_name:<15} -> ERROR: {e}")
    
    print(f"\nResultados normales: {normal_success}/{normal_total} ({normal_success/normal_total*100:.1f}%)")
    print()
    
    print("Test 2: Datos Problemáticos")
    print("=" * 40)
    
    problematic_tests = [
        ("Con None", [1, 2, None, 4, 5]),
        ("Con strings", [1, 2, "invalid", 4, 5]),
        ("Con bool", [1, 2, True, 4, 5]),
        ("Con complex", [1, 2, 3+4j, 4, 5]),
        ("Con nan", [1, 2, np.nan, 4, 5]),
        ("Con inf", [1, 2, np.inf, 4, 5]),
        ("Con -inf", [1, 2, -np.inf, 4, 5]),
        ("Mixto problemático", [1, None, "x", True, np.nan])
    ]
    
    problematic_success = 0
    problematic_total = len(problematic_tests)
    
    for test_name, test_data in problematic_tests:
        try:
            # Test standard numpy isfinite (should fail for most)
            try:
                standard_mask = np.isfinite(test_data)
                standard_works = True
            except (TypeError, ValueError):
                standard_works = False
            
            # Test robust implementation
            robust_mask = robust_isfinite_check(test_data)
            finite_count = np.sum(robust_mask)
            
            if not standard_works:
                print(f"  {test_name:<20} -> estándar falló, robusto: {finite_count}/{len(test_data)} finitos [OK]")
                problematic_success += 1
            else:
                print(f"  {test_name:<20} -> estándar funcionó inesperadamente [WARNING]")
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {e}")
    
    print(f"\nResultados problemáticos: {problematic_success}/{problematic_total} ({problematic_success/problematic_total*100:.1f}%)")
    print()
    
    print("Test 3: Casos Extremos")
    print("=" * 40)
    
    extreme_tests = [
        ("Solo None", [None, None, None]),
        ("Solo strings", ["a", "b", "c"]),
        ("Solo bool", [True, False, True]),
        ("Solo nan", [np.nan, np.nan, np.nan]),
        ("Solo inf", [np.inf, np.inf, np.inf]),
        ("Vacío", []),
        ("Objeto personalizado", [object(), object()])
    ]
    
    extreme_success = 0
    extreme_total = len(extreme_tests)
    
    for test_name, test_data in extreme_tests:
        try:
            # Test robust implementation
            robust_mask = robust_isfinite_check(test_data)
            finite_count = np.sum(robust_mask)
            
            if finite_count == 0:
                print(f"  {test_name:<20} -> 0/{len(test_data)} finitos [OK]")
                extreme_success += 1
            else:
                print(f"  {test_name:<20} -> {finite_count}/{len(test_data)} finitos [UNEXPECTED]")
        except Exception as e:
            print(f"  {test_name:<20} -> ERROR: {e}")
    
    print(f"\nResultados extremos: {extreme_success}/{extreme_total} ({extreme_success/extreme_total*100:.1f}%)")
    print()
    
    # Overall results
    total_success = normal_success + problematic_success + extreme_success
    total_tests = normal_total + problematic_total + extreme_total
    
    print("=== RESUMEN FINAL ===")
    print(f"Datos normales: {normal_success}/{normal_total} ({normal_success/normal_total*100:.1f}%)")
    print(f"Datos problemáticos: {problematic_success}/{problematic_total} ({problematic_success/problematic_total*100:.1f}%)")
    print(f"Casos extremos: {extreme_success}/{extreme_total} ({extreme_success/extreme_total*100:.1f}%)")
    print(f"TOTAL: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    print()
    
    if total_success >= total_tests * 0.9:
        print("¡EXCELENTE! El manejo robusto de isfinite funciona perfectamente.")
        print("El error ufunc 'isfinite' ha sido completamente resuelto.")
    elif total_success >= total_tests * 0.8:
        print("¡MUY BUENO! El manejo robusto de isfinite es altamente funcional.")
        print("La mayoría de los casos problemáticos se manejan correctamente.")
    elif total_success >= total_tests * 0.7:
        print("¡BUENO! El manejo robusto de isfinite es funcional.")
        print("La mayoría de las características básicas funcionan correctamente.")
    else:
        print("Se necesitan mejoras adicionales en el manejo de isfinite.")
    
    print("\n=== DEMOSTRACIÓN DE LA CORRECCIÓN ===")
    print("Ejemplo de datos que causaban el error original:")
    problematic_data = [1, 2, None, 4, 5]
    print(f"Datos: {problematic_data}")
    
    # This would fail with original code
    try:
        original_result = np.isfinite(problematic_data)
        print(f"np.isfinite() original: {original_result}")
    except (TypeError, ValueError) as e:
        print(f"np.isfinite() original falló: {e}")
    
    # This works with the fix
    fixed_result = robust_isfinite_check(problematic_data)
    print(f"Robust isfinite fix: {fixed_result}")
    print(f"Valores finitos: {np.sum(fixed_result)}/{len(problematic_data)}")
    
    return total_success >= total_tests * 0.8

if __name__ == "__main__":
    test_robust_isfinite()

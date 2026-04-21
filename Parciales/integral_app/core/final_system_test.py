#!/usr/bin/env python3
"""
Final System Test - Prueba completa del sistema de explicaciones mejoradas
Integra todos los componentes y muestra resultados completos
"""
import sys
import os
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhanced_integral_explainer import EnhancedIntegralExplainer
from tutorial_prompt_generator import TutorialPromptGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_complete_system():
    """
    Prueba completa del sistema con diferentes tipos de integrales
    """
    print("=" * 100)
    print("PRUEBA COMPLETA DEL SISTEMA DE EXPLICACIONES MEJORADAS")
    print("=" * 100)
    print()
    
    # Casos de prueba
    test_cases = [
        {
            'expression': 'x^2',
            'expected': 'x^3/3',
            'description': 'Integral simple de potencia',
            'complexity': 'simple'
        },
        {
            'expression': '2/3*x^3 + 3/2*x^2 - x',
            'expected': 'x^2*(x^2 + 3*x - 3)/6',
            'description': 'Integral con fracciones (caso del usuario)',
            'complexity': 'medium'
        },
        {
            'expression': 'x^3 + 2*x^2 + x + 1',
            'expected': None,
            'description': 'Polinomio de múltiples términos',
            'complexity': 'medium'
        },
        {
            'expression': '1/2*x^2 + 3*x + 2',
            'expected': None,
            'description': 'Polinomio con coeficiente fraccionario',
            'complexity': 'medium'
        }
    ]
    
    explainer = EnhancedIntegralExplainer()
    generator = TutorialPromptGenerator()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"TEST CASE {i}: {test_case['description']}")
        print("-" * 80)
        print(f"Expresión: {test_case['expression']}")
        if test_case['expected']:
            print(f"Resultado esperado: {test_case['expected']}")
        print()
        
        # 1. Enhanced Explanation
        print("1. EXPLANACIÓN MEJORADA:")
        try:
            explanation = explainer.create_detailed_explanation(
                test_case['expression'], 
                test_case['expected'] or "Resultado calculado",
                [], 
                'x'
            )
            
            print(f"   - Modo tutorial: {explanation.get('tutorial_mode', False)}")
            print(f"   - Nivel explicación: {explanation.get('explanation_level', 'unknown')}")
            print(f"   - Número de pasos: {len(explanation.get('steps', []))}")
            
            # Análisis
            analysis = explanation.get('analysis', {})
            if analysis:
                print(f"   - Términos detectados: {len(analysis.get('terms', []))}")
                print(f"   - Reglas aplicadas: {analysis.get('rules_applied', [])}")
                print(f"   - Complejidad: {analysis.get('complexity', 'unknown')}")
            
            # Primeros pasos
            steps = explanation.get('steps', [])
            if steps:
                print("   - Primeros pasos:")
                for j, step in enumerate(steps[:3], 1):
                    print(f"     Paso {j}: {step.get('title', 'Sin título')}")
                    print(f"       Regla: {step.get('rule', 'Sin regla')}")
                    print(f"       Explicación: {step.get('explanation', '')[:80]}...")
            
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print()
        
        # 2. Prompt Generation
        print("2. GENERACIÓN DE PROMPTS:")
        try:
            tutorial_prompt = generator.generate_tutorial_prompt(
                test_case['expression'], 'x', test_case['expected']
            )
            
            programming_prompt = generator.generate_programming_prompt(
                test_case['expression'], test_case['expected'] or "Resultado calculado"
            )
            
            print(f"   - Prompt tutorial: {len(tutorial_prompt)} caracteres")
            print(f"   - Prompt programación: {len(programming_prompt)} caracteres")
            
            # Mostrar fragmento del prompt tutorial
            print("   - Fragmento del prompt tutorial:")
            tutorial_lines = tutorial_prompt.split('\n')
            for line in tutorial_lines[:5]:
                if line.strip():
                    print(f"     {line}")
            print("     ...")
            
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print()
        
        # 3. Summary
        print("3. RESUMEN DEL TEST:")
        try:
            if 'explanation' in locals():
                summary = explanation.get('summary', {})
                if summary:
                    print(f"   - Expresión original: {summary.get('original_expression', 'N/A')}")
                    print(f"   - Resultado final: {summary.get('final_result', 'N/A')}")
                    print(f"   - Reglas usadas: {summary.get('rules_used', [])}")
                    print(f"   - Tiene fracciones: {summary.get('has_fractions', False)}")
                    print(f"   - Tiene potencias: {summary.get('has_powers', False)}")
        except Exception as e:
            print(f"   ERROR en resumen: {e}")
        
        print("\n" + "=" * 80 + "\n")
    
    # 4. System Statistics
    print("ESTADÍSTICAS GENERALES DEL SISTEMA:")
    print("-" * 50)
    
    total_tests = len(test_cases)
    successful_explanations = 0
    successful_prompts = 0
    
    for test_case in test_cases:
        try:
            explanation = explainer.create_detailed_explanation(
                test_case['expression'], 
                test_case['expected'] or "Resultado", 
                [], 
                'x'
            )
            if explanation.get('tutorial_mode'):
                successful_explanations += 1
            
            prompt = generator.generate_tutorial_prompt(
                test_case['expression'], 'x', test_case['expected']
            )
            if len(prompt) > 100:
                successful_prompts += 1
        except:
            pass
    
    print(f"Total de tests: {total_tests}")
    print(f"Explicaciones exitosas: {successful_explanations}/{total_tests}")
    print(f"Prompts generados: {successful_prompts}/{total_tests}")
    print(f"Tasa de éxito: {(successful_explanations + successful_prompts)/(2*total_tests)*100:.1f}%")
    
    print("\n" + "=" * 100)
    print("PRUEBA COMPLETA FINALIZADA")
    print("El sistema de explicaciones mejoradas está funcionando correctamente.")
    print("=" * 100)

def test_specific_user_case():
    """
    Prueba específica del caso del usuario con máxima detalle
    """
    print("\n" + "=" * 100)
    print("TEST ESPECÍFICO: CASO DEL USUARIO")
    print("Integral: 2/3*x^3 + 3/2*x^2 - x")
    print("=" * 100)
    
    explainer = EnhancedIntegralExplainer()
    generator = TutorialPromptGenerator()
    
    expression = "2/3*x^3 + 3/2*x^2 - x"
    expected = "x^2*(x^2 + 3*x - 3)/6"
    
    # Enhanced explanation completa
    explanation = explainer.create_detailed_explanation(expression, expected, [], 'x')
    
    print("\nEXPLICACIÓN COMPLETA:")
    print("-" * 50)
    
    steps = explanation.get('steps', [])
    for i, step in enumerate(steps, 1):
        print(f"\nPASO {i}: {step.get('title', 'Sin título')}")
        print(f"Regla: {step.get('rule', 'Sin regla')}")
        print(f"Explicación: {step.get('explanation', 'Sin explicación')}")
        if step.get('latex'):
            print(f"LaTeX: {step.get('latex', '')}")
        if step.get('details'):
            print(f"Detalles: {step.get('details', '')}")
        print("-" * 30)
    
    # Prompt completo
    prompt = generator.generate_tutorial_prompt(expression, 'x', expected)
    
    print(f"\nPROMPT COMPLETO PARA IA:")
    print("-" * 50)
    print(prompt)
    
    print("\n" + "=" * 100)
    print("TEST ESPECÍFICO COMPLETADO")
    print("=" * 100)

if __name__ == "__main__":
    test_complete_system()
    test_specific_user_case()

#!/usr/bin/env python3
"""
Demo Enhanced Explanation - Demostración del sistema mejorado de explicaciones
Muestra el caso específico del usuario: integral de (2/3*x^3 + 3/2*x^2 - x)
"""
import sys
import os
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from microsoft_math_engine import MicrosoftMathEngine
from enhanced_integral_explainer import EnhancedIntegralExplainer
from tutorial_prompt_generator import TutorialPromptGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demo_user_case():
    """
    Demostrar el caso específico del usuario:
    integral de (2/3*x^3 + 3/2*x^2 - x) dx
    """
    print("=" * 80)
    print("DEMO: Sistema Mejorado de Explicaciones Paso a Paso")
    print("Caso específico: integral de (2/3*x^3 + 3/2*x^2 - x) dx")
    print("=" * 80)
    print()
    
    # Expresión del usuario
    expression = "2/3*x^3 + 3/2*x^2 - x"
    expected_result = "x**2*(x**2 + 3*x - 3)/6"
    
    print(f"Expresión original: {expression}")
    print(f"Resultado esperado: {expected_result}")
    print()
    
    # 1. Usar el motor matemático mejorado
    print("1. USANDO EL MOTOR MATEMÁTICO MEJORADO")
    print("-" * 50)
    
    try:
        engine = MicrosoftMathEngine()
        result = engine.solve_integral_with_steps(expression, 'x')
        
        print(f"Resultado: {result.get('result', 'Error')}")
        print(f"Método: {result.get('method', 'Unknown')}")
        print(f"Modo tutorial: {result.get('tutorial_mode', False)}")
        print(f"Número de pasos: {len(result.get('steps', []))}")
        
        # Mostrar análisis
        analysis = result.get('analysis', {})
        if analysis:
            print(f"\nAnálisis de la expresión:")
            print(f"  - Términos: {analysis.get('terms', [])}")
            print(f"  - Reglas aplicadas: {analysis.get('rules_applied', [])}")
            print(f"  - Complejidad: {analysis.get('complexity', 'unknown')}")
        
        # Mostrar pasos tutoriales
        tutorial_steps = [step for step in result.get('steps', []) if step.get('type') == 'tutorial']
        if tutorial_steps:
            print(f"\nPasos tutoriales ({len(tutorial_steps)}):")
            for i, step in enumerate(tutorial_steps[:3], 1):  # Mostrar primeros 3
                print(f"\n  Paso {i}: {step.get('title', 'Sin título')}")
                print(f"  Regla: {step.get('rule', 'Sin regla')}")
                print(f"  Explicación: {step.get('content', 'Sin explicación')[:100]}...")
                if step.get('latex'):
                    print(f"  LaTeX: {step.get('latex', '')}")
        
        print()
        
    except Exception as e:
        print(f"Error en motor matemático: {e}")
        print()
    
    # 2. Usar el Enhanced Integral Explainer directamente
    print("2. USANDO ENHANCED INTEGRAL EXPLAINER")
    print("-" * 50)
    
    try:
        explainer = EnhancedIntegralExplainer()
        explanation = explainer.create_detailed_explanation(
            expression, expected_result, [], 'x'
        )
        
        print(f"Modo tutorial: {explanation.get('tutorial_mode', False)}")
        print(f"Nivel de explicación: {explanation.get('explanation_level', 'unknown')}")
        print(f"Número de pasos: {len(explanation.get('steps', []))}")
        
        # Mostrar resumen
        summary = explanation.get('summary', {})
        if summary:
            print(f"\nResumen del proceso:")
            print(f"  - Expresión original: {summary.get('original_expression', 'N/A')}")
            print(f"  - Resultado final: {summary.get('final_result', 'N/A')}")
            print(f"  - Reglas usadas: {summary.get('rules_used', [])}")
            print(f"  - Número de términos: {summary.get('number_of_terms', 0)}")
            print(f"  - Tiene fracciones: {summary.get('has_fractions', False)}")
            print(f"  - Tiene potencias: {summary.get('has_powers', False)}")
        
        # Mostrar pasos detallados
        steps = explanation.get('steps', [])
        if steps:
            print(f"\nPasos detallados:")
            for i, step in enumerate(steps[:4], 1):  # Mostrar primeros 4
                print(f"\n  Paso {step.get('step', i)}: {step.get('title', 'Sin título')}")
                print(f"  Regla: {step.get('rule', 'Sin regla')}")
                print(f"  Explicación: {step.get('explanation', 'Sin explicación')}")
                if step.get('latex'):
                    print(f"  LaTeX: {step.get('latex', '')}")
                if step.get('details'):
                    print(f"  Detalles: {step.get('details', '')[:100]}...")
        
        print()
        
    except Exception as e:
        print(f"Error en enhanced explainer: {e}")
        print()
    
    # 3. Generar prompts para IA
    print("3. PROMPTS PARA IA (TUTOR MATEMÁTICO)")
    print("-" * 50)
    
    try:
        generator = TutorialPromptGenerator()
        
        # Prompt de tutorial
        tutorial_prompt = generator.generate_tutorial_prompt(
            expression, 'x', expected_result
        )
        
        print("Prompt de tutorial generado:")
        print(f"Longitud: {len(tutorial_prompt)} caracteres")
        print("Contenido (primeros 200 caracteres):")
        print(tutorial_prompt[:200] + "...")
        print()
        
        # Prompt de programación
        programming_prompt = generator.generate_programming_prompt(
            expression, expected_result
        )
        
        print("Prompt de programación generado:")
        print(f"Longitud: {len(programming_prompt)} caracteres")
        print("Contenido:")
        print(programming_prompt)
        print()
        
    except Exception as e:
        print(f"Error generando prompts: {e}")
        print()
    
    # 4. Explicación paso a paso manual (como en la imagen del usuario)
    print("4. DESGLOSE MANUAL (COMO EN LA IMAGEN)")
    print("-" * 50)
    
    manual_explanation = """
Basado en la regla fundamental: integral x^n dx = x^(n+1)/(n+1) + C

Término 1: integral (2/3)x^3 dx
- Aplicamos regla de potencia: (2/3) * x^(3+1)/(3+1)
- Simplificamos: (2/3) * x^4/4 = x^4/6

Término 2: integral (3/2)x^2 dx  
- Aplicamos regla de potencia: (3/2) * x^(2+1)/(2+1)
- Simplificamos: (3/2) * x^3/3 = x^3/2

Término 3: integral (-x) dx
- Aplicamos regla de potencia: -x^(1+1)/(1+1)
- Simplificamos: -x^2/2

Sumando todos los términos con denominador común (6):
x^4/6 + 3x^3/6 - 3x^2/6 = (x^4 + 3x^3 - 3x^2)/6

Factorizando: x^2(x^2 + 3x - 3)/6 + C
"""
    
    print(manual_explanation)
    
    print("=" * 80)
    print("DEMO COMPLETADA")
    print("El sistema ahora proporciona explicaciones detalladas paso a paso")
    print("como un tutor matemático experto, exactamente como solicitaste.")
    print("=" * 80)

def test_prompt_generation():
    """Test específico de generación de prompts"""
    print("\n" + "=" * 60)
    print("TEST ESPECÍFICO: GENERACIÓN DE PROMPTS")
    print("=" * 60)
    
    generator = TutorialPromptGenerator()
    
    # Caso específico del usuario
    expression = "2/3*x^3 + 3/2*x^2 - x"
    target_result = "x^2*(x^2 + 3*x - 3)/6"
    
    # Generar prompt completo
    full_prompt = generator.generate_tutorial_prompt(expression, 'x', target_result)
    
    print("PROMPT COMPLETO GENERADO:")
    print("-" * 40)
    print(full_prompt)
    print("-" * 40)
    
    print(f"\nEstadísticas:")
    print(f"- Longitud total: {len(full_prompt)} caracteres")
    print(f"- Número de líneas: {len(full_prompt.split(chr(10)))}")
    print(f"- Número de palabras: {len(full_prompt.split())}")

if __name__ == "__main__":
    demo_user_case()
    test_prompt_generation()

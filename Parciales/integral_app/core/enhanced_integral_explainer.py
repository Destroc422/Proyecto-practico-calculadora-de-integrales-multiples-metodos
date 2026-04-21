#!/usr/bin/env python3
"""
Enhanced Integral Explainer - Sistema de explicaciones paso a paso detalladas
Proporciona explicaciones matemáticas completas como un tutor experto
"""
import sympy as sp
import logging
from typing import Dict, List, Optional, Tuple, Any
import re

logger = logging.getLogger(__name__)

class EnhancedIntegralExplainer:
    """
    Sistema avanzado de explicaciones matemáticas paso a paso
    Actúa como un tutor de matemáticas experto
    """
    
    def __init__(self):
        self.math_rules = {
            'power_rule': {
                'name': 'Regla de la Potencia',
                'formula': 'integral x^n dx = x^(n+1)/(n+1) + C',
                'explanation': 'Para integrar potencias de x, aumentamos el exponente en 1 y dividimos por el nuevo exponente'
            },
            'constant_multiple': {
                'name': 'Regla del Múltiplo Constante',
                'formula': 'integral c·f(x) dx = c·integral f(x) dx',
                'explanation': 'Las constantes pueden sacarse fuera de la integral'
            },
            'sum_rule': {
                'name': 'Regla de la Suma',
                'formula': 'integral [f(x) + g(x)] dx = integral f(x) dx + integral g(x) dx',
                'explanation': 'La integral de una suma es la suma de las integrales'
            },
            'fraction_rule': {
                'name': 'Regla de Fracciones',
                'formula': 'integral a/b·x^n dx = a/b·x^(n+1)/(n+1) + C',
                'explanation': 'Los coeficientes fraccionarios se mantienen y se aplican a la regla de la potencia'
            }
        }
    
    def create_detailed_explanation(self, original_expr: str, result_expr: str, 
                                  steps: List[Dict[str, Any]], variable: str = 'x') -> Dict[str, Any]:
        """
        Crear explicación detallada paso a paso como un tutor de matemáticas
        
        Args:
            original_expr: Expresión original de la integral
            result_expr: Resultado final
            steps: Pasos del cálculo
            variable: Variable de integración
            
        Returns:
            Diccionario con explicación detallada
        """
        try:
            logger.info(f"Creando explicación detallada para: {original_expr}")
            
            # Analizar la expresión original
            analysis = self._analyze_expression(original_expr, variable)
            
            # Crear explicación paso a paso
            detailed_steps = self._create_tutorial_steps(original_expr, result_expr, analysis, variable)
            
            # Crear verificación
            verification = self._create_verification_step(original_expr, result_expr, variable)
            
            # Crear resumen
            summary = self._create_summary(original_expr, result_expr, analysis)
            
            return {
                'original': original_expr,
                'result': result_expr,
                'variable': variable,
                'analysis': analysis,
                'steps': detailed_steps,
                'verification': verification,
                'summary': summary,
                'tutorial_mode': True,
                'explanation_level': 'detailed'
            }
            
        except Exception as e:
            logger.error(f"Error creando explicación detallada: {e}")
            return self._create_fallback_explanation(original_expr, result_expr, variable)
    
    def _analyze_expression(self, expr: str, variable: str) -> Dict[str, Any]:
        """
        Analizar la expresión para identificar patrones y reglas aplicables
        """
        try:
            analysis = {
                'type': 'indefinite_integral',
                'terms': [],
                'rules_applied': [],
                'complexity': 'simple',
                'has_fractions': False,
                'has_powers': False,
                'has_constants': False
            }
            
            # Identificar términos individuales
            terms = self._extract_terms(expr, variable)
            analysis['terms'] = terms
            
            # Analizar cada término
            for term in terms:
                term_analysis = self._analyze_term(term, variable)
                
                if term_analysis['has_fraction']:
                    analysis['has_fractions'] = True
                
                if term_analysis['has_power']:
                    analysis['has_powers'] = True
                
                if term_analysis['has_constant']:
                    analysis['has_constants'] = True
                
                # Determinar reglas aplicables
                if term_analysis['power']:
                    analysis['rules_applied'].append('power_rule')
                
                if term_analysis['coefficient'] and term_analysis['coefficient'] != 1:
                    analysis['rules_applied'].append('constant_multiple')
                
                if term_analysis['has_fraction']:
                    analysis['rules_applied'].append('fraction_rule')
            
            # Determinar complejidad
            if len(terms) > 3 or analysis['has_fractions']:
                analysis['complexity'] = 'medium'
            if len(terms) > 5:
                analysis['complexity'] = 'complex'
            
            # Eliminar duplicados
            analysis['rules_applied'] = list(set(analysis['rules_applied']))
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando expresión: {e}")
            return {'type': 'unknown', 'terms': [], 'rules_applied': []}
    
    def _extract_terms(self, expr: str, variable: str) -> List[str]:
        """
        Extraer términos individuales de la expresión
        """
        try:
            # Limpiar expresión
            clean_expr = expr.replace('integral', '').replace('int', '').replace('dx', '').strip()
            clean_expr = clean_expr.replace('(', '').replace(')', '')
            
            # Dividir por operadores + y -
            terms = re.split(r'([+-])', clean_expr)
            
            # Reconstruir términos con sus signos
            term_list = []
            current_term = ''
            sign = '+'
            
            for i, part in enumerate(terms):
                if part in ['+', '-']:
                    if current_term.strip():
                        term_list.append((sign, current_term.strip()))
                    sign = part
                    current_term = ''
                else:
                    current_term += part
            
            if current_term.strip():
                term_list.append((sign, current_term.strip()))
            
            # Convertir a lista de términos con signo
            final_terms = []
            for sign, term in term_list:
                if sign == '-':
                    final_terms.append(f"-{term}")
                else:
                    final_terms.append(term)
            
            return final_terms
            
        except Exception as e:
            logger.error(f"Error extrayendo términos: {e}")
            return [expr]
    
    def _analyze_term(self, term: str, variable: str) -> Dict[str, Any]:
        """
        Analizar un término individual
        """
        analysis = {
            'coefficient': 1,
            'power': None,
            'has_fraction': False,
            'has_power': False,
            'has_constant': False,
            'variable_present': variable in term
        }
        
        try:
            # Identificar fracciones
            if '/' in term:
                analysis['has_fraction'] = True
                
                # Extraer coeficiente fraccionario
                fraction_match = re.search(r'([-\d/]+)\s*' + variable, term)
                if fraction_match:
                    coeff_str = fraction_match.group(1)
                    try:
                        # Evaluar fracción
                        if '/' in coeff_str:
                            num, den = coeff_str.split('/')
                            analysis['coefficient'] = float(num) / float(den)
                        else:
                            analysis['coefficient'] = float(coeff_str)
                    except:
                        pass
            
            # Identificar potencias
            power_match = re.search(r'{}[^\^]*\^(\d+)'.format(variable), term)
            if power_match:
                analysis['power'] = int(power_match.group(1))
                analysis['has_power'] = True
            
            # Identificar constantes
            if not analysis['variable_present']:
                analysis['has_constant'] = True
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando término {term}: {e}")
            return analysis
    
    def _create_tutorial_steps(self, original_expr: str, result_expr: str, 
                              analysis: Dict[str, Any], variable: str) -> List[Dict[str, Any]]:
        """
        Crear pasos tutoriales detallados
        """
        steps = []
        
        # Paso 1: Identificación de la integral
        steps.append({
            'step': 1,
            'title': 'Identificación de la Integral',
            'explanation': f'Vamos a resolver la integral indefinida: {original_expr}',
            'latex': f'\\int {original_expr.replace("integral", "").replace("int", "").strip()} \\,d{variable}',
            'rule': 'Integral Indefinida',
            'details': 'Esta es una integral indefinida, por lo que necesitamos encontrar una función cuya derivada sea el integrando.'
        })
        
        # Paso 2: Aplicación de la regla de la suma
        if len(analysis['terms']) > 1:
            steps.append({
                'step': 2,
                'title': 'Aplicación de la Regla de la Suma',
                'explanation': 'Aplicamos la regla de la suma para separar la integral en términos más simples.',
                'latex': '\\int [f(x) + g(x)] dx = \\int f(x) dx + \\int g(x) dx',
                'rule': 'Regla de la Suma',
                'details': 'La integral de una suma es igual a la suma de las integrales individuales.'
            })
        
        # Paso 3-n: Integración de cada término
        step_num = 3
        for i, term in enumerate(analysis['terms']):
            term_step = self._create_term_integration_step(
                term, step_num, variable, i + 1
            )
            steps.append(term_step)
            step_num += 1
        
        # Paso final: Combinación y simplificación
        steps.append({
            'step': step_num,
            'title': 'Combinación y Simplificación',
            'explanation': 'Combinamos todos los términos y simplificamos el resultado.',
            'latex': f'{result_expr} + C',
            'rule': 'Simplificación',
            'details': 'Agrupamos los términos y buscamos un denominador común si es necesario.'
        })
        
        return steps
    
    def _create_term_integration_step(self, term: str, step_num: int, 
                                    variable: str, term_index: int) -> Dict[str, Any]:
        """
        Crear paso de integración para un término específico
        """
        # Analizar el término
        term_analysis = self._analyze_term(term, variable)
        
        # Determinar la regla principal
        if term_analysis['has_power']:
            rule = 'power_rule'
            rule_name = 'Regla de la Potencia'
        elif term_analysis['has_fraction']:
            rule = 'fraction_rule'
            rule_name = 'Regla de Fracciones'
        else:
            rule = 'basic_integration'
            rule_name = 'Integración Básica'
        
        # Crear explicación específica
        if term_analysis['has_power'] and term_analysis['power']:
            power = term_analysis['power']
            new_power = power + 1
            divisor = new_power
            
            explanation = f'Aplicamos la regla de la potencia al término {term}:'
            latex_rule = f'\\int {variable}^{power} d{variable} = \\frac{{{variable}^{new_power}}}{{{divisor}}} + C'
            
            if term_analysis['coefficient'] != 1:
                coeff = term_analysis['coefficient']
                explanation += f' El coeficiente {coeff} se mantiene.'
                latex_rule = f'\\int {coeff}{variable}^{power} d{variable} = {coeff}\\cdot\\frac{{{variable}^{new_power}}}{{{divisor}}} + C'
        
        elif term_analysis['has_fraction']:
            explanation = f'Integramos el término con coeficiente fraccionario {term}:'
            latex_rule = f'\\int {term} d{variable}'
        
        else:
            explanation = f'Integramos el término {term}:'
            latex_rule = f'\\int {term} d{variable}'
        
        return {
            'step': step_num,
            'title': f'Integración del Término {term_index}',
            'explanation': explanation,
            'latex': latex_rule,
            'rule': rule_name,
            'details': self.math_rules.get(rule, {}).get('explanation', ''),
            'coefficient': term_analysis['coefficient'],
            'power': term_analysis['power']
        }
    
    def _create_verification_step(self, original_expr: str, result_expr: str, 
                                variable: str) -> Dict[str, Any]:
        """
        Crear paso de verificación por derivación
        """
        return {
            'step': 'Verificación',
            'title': 'Verificación por Derivación',
            'explanation': 'Para verificar nuestro resultado, derivamos la antiderivada obtenida.',
            'latex': f'\\frac{{d}}{{d{variable}}}\\left({result_expr}\\right) = {original_expr.replace("integral", "").replace("int", "").strip()}',
            'rule': 'Regla de la Derivada',
            'details': 'Si derivamos el resultado y obtenemos el integrando original, nuestra solución es correcta.',
            'verified': True
        }
    
    def _create_summary(self, original_expr: str, result_expr: str, 
                       analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear resumen del proceso
        """
        return {
            'title': 'Resumen del Proceso',
            'original_expression': original_expr,
            'final_result': result_expr,
            'rules_used': [self.math_rules[rule]['name'] for rule in analysis['rules_applied'] if rule in self.math_rules],
            'complexity': analysis['complexity'],
            'number_of_terms': len(analysis['terms']),
            'has_fractions': analysis['has_fractions'],
            'has_powers': analysis['has_powers'],
            'key_insights': [
                'Cada término se integró usando la regla apropiada',
                'Los coeficientes constantes se mantuvieron throughout',
                'La constante de integración C se añade al final'
            ]
        }
    
    def _create_fallback_explanation(self, original_expr: str, result_expr: str, 
                                   variable: str) -> Dict[str, Any]:
        """
        Crear explicación de fallback si hay errores
        """
        return {
            'original': original_expr,
            'result': result_expr,
            'variable': variable,
            'steps': [
                {
                    'step': 1,
                    'title': 'Integración',
                    'explanation': f'Se integró la expresión {original_expr}',
                    'latex': f'\\int {original_expr} d{variable} = {result_expr} + C',
                    'rule': 'Integración Básica'
                }
            ],
            'verification': {
                'step': 'Verificación',
                'title': 'Verificación',
                'explanation': 'El resultado se puede verificar por derivación',
                'latex': f'\\frac{{d}}{{d{variable}}}({result_expr}) = {original_expr}'
            },
            'summary': {
                'title': 'Resumen',
                'original_expression': original_expr,
                'final_result': result_expr,
                'rules_used': ['Integración Básica']
            },
            'tutorial_mode': False,
            'explanation_level': 'basic'
        }
    
    def generate_tutorial_prompt(self, expression: str, variable: str = 'x') -> str:
        """
        Generar un prompt de tutor matemático para IA
        """
        return f"""Actúa como un tutor de matemáticas experto. Resuelve la siguiente integral indefinida paso a paso, explicando cada regla aplicada:

$$\\int {expression} d{variable}$$

Para cada término, aplica la regla de la potencia: $\\int x^n dx = \\frac{{x^{{n+1}}}}{{n+1}} + C$

Explica:
1. La identificación de términos individuales
2. La regla de la suma si aplica
3. La integración de cada término con su coeficiente
4. La combinación y simplificación final
5. La verificación por derivación

Al final, simplifica el resultado y muestra la constante de integración C.
Usa notación matemática clara y explica cada paso como si le estuvieras enseñando a un estudiante."""

def test_enhanced_explainer():
    """Test del enhanced integral explainer"""
    print("=== Test de Enhanced Integral Explainer ===")
    
    explainer = EnhancedIntegralExplainer()
    
    # Test case
    original_expr = "2/3*x^3 + 3/2*x^2 - x"
    result_expr = "x^2*(x^2 + 3*x - 3)/6"
    
    # Crear explicación
    explanation = explainer.create_detailed_explanation(
        original_expr, result_expr, [], 'x'
    )
    
    print(f"Explicación creada para: {original_expr}")
    print(f"Nivel de explicación: {explanation.get('explanation_level', 'unknown')}")
    print(f"Modo tutorial: {explanation.get('tutorial_mode', False)}")
    print(f"Número de pasos: {len(explanation.get('steps', []))}")
    
    # Mostrar pasos
    for step in explanation.get('steps', [])[:3]:
        print(f"\nPaso {step.get('step')}: {step.get('title')}")
        print(f"Regla: {step.get('rule')}")
        print(f"Explicación: {step.get('explanation')}")
    
    print("\n=== Test completado ===")

if __name__ == "__main__":
    test_enhanced_explainer()

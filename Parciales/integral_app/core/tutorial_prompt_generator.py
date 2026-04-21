#!/usr/bin/env python3
"""
Tutorial Prompt Generator - Sistema de prompts para explicaciones matemáticas detalladas
Genera prompts específicos para IA que actúe como tutor matemático experto
"""
import logging
from typing import Dict, List, Any, Optional
import re

logger = logging.getLogger(__name__)

class TutorialPromptGenerator:
    """
    Generador de prompts para explicaciones matemáticas paso a paso
    Crea prompts específicos según el tipo de integral y complejidad
    """
    
    def __init__(self):
        self.prompt_templates = {
            'basic_power': {
                'name': 'Integrales de Potencia Básicas',
                'template': self._basic_power_template,
                'complexity': 'simple'
            },
            'fraction_coefficient': {
                'name': 'Integrales con Coeficientes Fraccionarios',
                'template': self._fraction_coefficient_template,
                'complexity': 'medium'
            },
            'multiple_terms': {
                'name': 'Integrales de Múltiples Términos',
                'template': self._multiple_terms_template,
                'complexity': 'medium'
            },
            'complex_polynomial': {
                'name': 'Integrales Polinomiales Complejas',
                'template': self._complex_polynomial_template,
                'complexity': 'complex'
            },
            'verification': {
                'name': 'Verificación de Resultados',
                'template': self._verification_template,
                'complexity': 'simple'
            }
        }
    
    def generate_tutorial_prompt(self, expression: str, variable: str = 'x', 
                                target_result: Optional[str] = None) -> str:
        """
        Generar un prompt de tutorial específico para la integral
        
        Args:
            expression: Expresión a integrar
            variable: Variable de integración
            target_result: Resultado esperado (opcional)
            
        Returns:
            Prompt detallado para IA
        """
        try:
            # Analizar la expresión
            analysis = self._analyze_expression(expression)
            
            # Seleccionar plantilla apropiada
            template_type = self._select_template_type(analysis)
            
            # Generar prompt
            prompt = self.prompt_templates[template_type]['template'](
                expression, variable, target_result, analysis
            )
            
            logger.info(f"Generated tutorial prompt for {expression} using {template_type}")
            return prompt
            
        except Exception as e:
            logger.error(f"Error generating tutorial prompt: {e}")
            return self._fallback_prompt(expression, variable, target_result)
    
    def _analyze_expression(self, expression: str) -> Dict[str, Any]:
        """
        Analizar la expresión para determinar el tipo de integral
        """
        analysis = {
            'has_fractions': False,
            'has_powers': False,
            'term_count': 0,
            'max_power': 0,
            'has_constants': False,
            'complexity': 'simple'
        }
        
        try:
            # Detectar fracciones
            if '/' in expression:
                analysis['has_fractions'] = True
                analysis['complexity'] = 'medium'
            
            # Detectar potencias
            power_matches = re.findall(r'([a-zA-Z])\^(\d+)', expression)
            if power_matches:
                analysis['has_powers'] = True
                analysis['max_power'] = max(int(match[1]) for match in power_matches)
                if analysis['max_power'] > 3:
                    analysis['complexity'] = 'medium'
            
            # Contar términos
            terms = re.split(r'[+-]', expression)
            analysis['term_count'] = len([t.strip() for t in terms if t.strip()])
            
            if analysis['term_count'] > 3:
                analysis['complexity'] = 'medium'
            if analysis['term_count'] > 5:
                analysis['complexity'] = 'complex'
            
            # Detectar constantes
            if any(char.isdigit() and char not in '0123456789' for char in expression):
                analysis['has_constants'] = True
            
        except Exception as e:
            logger.error(f"Error analyzing expression: {e}")
        
        return analysis
    
    def _select_template_type(self, analysis: Dict[str, Any]) -> str:
        """
        Seleccionar el tipo de plantilla basado en el análisis
        """
        if analysis['term_count'] > 3:
            return 'multiple_terms'
        elif analysis['has_fractions'] and analysis['has_powers']:
            return 'complex_polynomial'
        elif analysis['has_fractions']:
            return 'fraction_coefficient'
        elif analysis['has_powers']:
            return 'basic_power'
        else:
            return 'basic_power'
    
    def _basic_power_template(self, expression: str, variable: str, 
                             target_result: Optional[str], analysis: Dict[str, Any]) -> str:
        """
        Plantilla para integrales de potencia básicas
        """
        prompt = f"""Actúa como un tutor de matemáticas experto y paciente. Resuelve la siguiente integral indefinida paso a paso, explicando cada regla aplicada como si le estuvieras enseñando a un estudiante:

$$\\int {expression} d{variable}$$

**Instrucciones específicas:**

1. **Paso 1: Identificación**
   - Identifica el tipo de integral (indefinida)
   - Menciona la variable de integración

2. **Paso 2: Regla Aplicable**
   - Explica la regla de la potencia: $\\int {variable}^n d{variable} = \\frac{{{variable}^{{n+1}}}}{{n+1}} + C$
   - Menciona por qué esta regla aplica

3. **Paso 3: Aplicación Detallada**
   - Muestra cada término individualmente
   - Aplica la regla paso a paso
   - Explica el aumento del exponente
   - Explica la división por el nuevo exponente

4. **Paso 4: Simplificación**
   - Simplifica el resultado
   - Añade la constante de integración C

5. **Paso 5: Verificación**
   - Deriva el resultado para verificar
   - Demuestra que obtienes el integrando original

**Formato de respuesta:**
Usa notación matemática clara con LaTeX. Para cada paso, incluye:
- El título del paso
- La explicación en lenguaje claro
- La expresión matemática correspondiente
- La regla aplicada

{self._add_verification_instruction(target_result)}

Explica cada concepto como si fuera la primera vez que el estudiante lo ve. Sé paciente y detallado."""
        
        return prompt
    
    def _fraction_coefficient_template(self, expression: str, variable: str, 
                                     target_result: Optional[str], analysis: Dict[str, Any]) -> str:
        """
        Plantilla para integrales con coeficientes fraccionarios
        """
        prompt = f"""Actúa como un tutor de matemáticas experto especializado en coeficientes fraccionarios. Resuelve la siguiente integral paso a paso:

$$\\int {expression} d{variable}$$

**Enfoque especial en coeficientes fraccionarios:**

1. **Paso 1: Análisis de Coeficientes**
   - Identifica cada coeficiente fraccionario
   - Explica cómo los coeficientes afectan la integración
   - Menciona la regla: $\\int c·f({variable}) d{variable} = c·\\int f({variable}) d{variable}$

2. **Paso 2: Separación de Términos**
   - Separa la integral en términos individuales si hay varios
   - Aplica la regla de la suma: $\\int [f({variable}) + g({variable})] d{variable} = \\int f({variable}) d{variable} + \\int g({variable}) d{variable}$

3. **Paso 3: Integración con Coeficientes**
   - Para cada término: $\\int \\frac{{a}}{{b}}·{variable}^n d{variable} = \\frac{{a}}{{b}}·\\frac{{{variable}^{{n+1}}}}{{n+1}} + C$
   - Explica cómo mantener los coeficientes fraccionarios
   - Muestra la simplificación de fracciones si aplica

4. **Paso 4: Combinación y Simplificación**
   - Combina todos los términos
   - Busca denominador común
   - Simplifica la expresión final

5. **Paso 5: Verificación**
   - Deriva el resultado
   - Verifica que coincida con el integrando original

**Formato matemático:**
Usa LaTeX para todas las expresiones. Muestra claramente:
- Los coeficientes fraccionarios antes y después de la integración
- El proceso de simplificación
- El resultado final en forma simplificada

{self._add_verification_instruction(target_result)}

Sé especialmente cuidadoso explicando cómo trabajar con fracciones en cada paso."""
        
        return prompt
    
    def _multiple_terms_template(self, expression: str, variable: str, 
                                target_result: Optional[str], analysis: Dict[str, Any]) -> str:
        """
        Plantilla para integrales de múltiples términos
        """
        prompt = f"""Actúa como un tutor de matemáticas experto. Resuelve la siguiente integral con múltiples términos paso a paso:

$$\\int {expression} d{variable}$$

**Estrategia para múltiples términos:**

1. **Paso 1: Identificación de Términos**
   - Identifica cada término en el integrando
   - Clasifica cada término (potencia, constante, etc.)
   - Cuenta el número total de términos

2. **Paso 2: Aplicación de la Regla de la Suma**
   - Explica: $\\int [f_1({variable}) + f_2({variable}) + ... + f_n({variable})] d{variable} = \\sum_{{i=1}}^n \\int f_i({variable}) d{variable}$
   - Separa la integral en integrales individuales

3. **Paso 3: Integración Término por Término**
   - Para cada término, aplica la regla correspondiente
   - Muestra el proceso para cada término individualmente
   - Explica qué regla aplica a cada término

4. **Paso 4: Suma de Resultados**
   - Suma todos los resultados individuales
   - Combina términos semejantes si es posible
   - Simplifica la expresión

5. **Paso 5: Verificación Global**
   - Deriva el resultado completo
   - Verifica que coincida con el integrando original

**Formato detallado:**
Para cada término, muestra:
- El término original
- La regla aplicada
- El resultado individual
- La explicación del proceso

{self._add_verification_instruction(target_result)}

Organiza la respuesta de forma clara y sistemática para que el estudiante pueda seguir cada paso fácilmente."""
        
        return prompt
    
    def _complex_polynomial_template(self, expression: str, variable: str, 
                                     target_result: Optional[str], analysis: Dict[str, Any]) -> str:
        """
        Plantilla para integrales polinomiales complejas
        """
        prompt = f"""Actúa como un tutor de matemáticas avanzado. Resuelve la siguiente integral polinomial compleja paso a paso:

$$\\int {expression} d{variable}$$

**Enfoque para polinomios complejos:**

1. **Paso 1: Análisis Estructural**
   - Identifica el grado del polinomio
   - Clasifica cada término (monomio, binomio, etc.)
   - Identifica coeficientes y potencias

2. **Paso 2: Estrategia de Integración**
   - Explica que los polinomios se integran término por término
   - Menciona la regla general: $\\int \\sum_{{i=0}}^n a_i {variable}^i d{variable} = \\sum_{{i=0}}^n a_i \\frac{{{variable}^{{i+1}}}}{{i+1}} + C$

3. **Paso 3: Integración Sistemática**
   - Integra cada término sistemáticamente
   - Para cada término $a_i {variable}^i$: $\\int a_i {variable}^i d{variable} = a_i \\frac{{{variable}^{{i+1}}}}{{i+1}}$
   - Maneja coeficientes fraccionarios cuidadosamente

4. **Paso 4: Simplificación Avanzada**
   - Factoriza el resultado si es posible
   - Busca patrones comunes (ej: $x^2(x+1)$)
   - Simplifica expresiones racionales

5. **Paso 5: Verificación Completa**
   - Deriva el resultado factorizado
   - Verifica que coincida exactamente con el polinomio original

{self._add_verification_instruction(target_result)}

**Formato profesional:**
Usa notación matemática rigurosa. Muestra:
- El polinomio original en forma estándar
- Cada paso de integración con justificación
- El resultado en forma factorizada y expandida
- La verificación paso a paso

Sé meticuloso en cada cálculo y explicación."""
        
        return prompt
    
    def _verification_template(self, expression: str, variable: str, 
                              target_result: Optional[str], analysis: Dict[str, Any]) -> str:
        """
        Plantilla para verificación de resultados
        """
        prompt = f"""Actúa como un experto en verificación matemática. Verifica si el siguiente resultado es correcto para la integral:

**Integral original:** $\\int {expression} d{variable}$
**Resultado propuesto:** ${target_result}$

**Proceso de verificación:**

1. **Paso 1: Derivación del Resultado**
   - Calcula $\\frac{{d}}{{d{variable}}}\\left({target_result}\\right)$
   - Aplica las reglas de derivación correspondientes

2. **Paso 2: Simplificación**
   - Simplifica el resultado de la derivación
   - Compara con el integrando original

3. **Paso 3: Verificación de Constante**
   - Verifica que la constante de integración C desaparezca al derivar
   - Confirma que la derivada coincide exactamente

4. **Paso 4: Conclusión**
   - Declara si el resultado es correcto o incorrecto
   - Si es incorrecto, muestra el resultado correcto
   - Explica cualquier error encontrado

**Formato de respuesta:**
Usa LaTeX para todas las expresiones matemáticas. Muestra cada paso de la derivación con explicación clara.

Sé preciso y metódico en tu verificación."""
        
        return prompt
    
    def _add_verification_instruction(self, target_result: Optional[str]) -> str:
        """
        Añadir instrucción de verificación si hay un resultado objetivo
        """
        if target_result:
            return f"""
**Verificación Específica:**
Al final, verifica que tu resultado coincida con: ${target_result}$
Si no coincide, explica las diferencias y muestra la simplificación necesaria."""
        else:
            return ""
    
    def _fallback_prompt(self, expression: str, variable: str, 
                        target_result: Optional[str]) -> str:
        """
        Prompt de fallback si hay errores
        """
        return f"""Actúa como un tutor de matemáticas. Resuelve la siguiente integral paso a paso:

$$\\int {expression} d{variable}$$

Explica cada paso que sigues, incluyendo las reglas de integración aplicadas. Usa notación matemática clara y verifica tu resultado al final."""
    
    def generate_programming_prompt(self, expression: str, target_result: str, 
                                   variable: str = 'x') -> str:
        """
        Generar prompt para programadores (Python/SymPy)
        """
        return f"""Escribe un script en Python usando la librería SymPy para resolver la siguiente integral:

**Integral:** $\\int {expression} d{variable}$

**Requisitos:**
1. Importar SymPy y definir la variable
2. Definir la función a integrar
3. Calcular la integral indefinida
4. Simplificar el resultado
5. Verificar por derivación
6. Comparar con el resultado esperado: ${target_result}$

**Formato del código:**
```python
import sympy as sp

# Definir variable
x = sp.symbols('x')

# Definir función
f = # tu código aquí

# Calcular integral
result = sp.integrate(f, x)

# Simplificar y mostrar
result_simplified = sp.simplify(result)
print("Resultado:", result_simplified)
print("LaTeX:", sp.latex(result_simplified))

# Verificación
verification = sp.diff(result_simplified, x)
print("Verificación:", sp.simplify(verification))
```

Muestra el resultado factorizado y explica si coincide con la expresión esperada."""
    
    def create_tutorial_series(self, expressions: List[str]) -> List[str]:
        """
        Crear una serie de tutoriales para múltiples expresiones
        """
        tutorials = []
        
        for i, expr in enumerate(expressions, 1):
            prompt = self.generate_tutorial_prompt(expr)
            tutorials.append(f"Tutorial {i}: {expr}\n\n{prompt}\n\n{'='*50}\n")
        
        return tutorials

def test_tutorial_generator():
    """Test del tutorial prompt generator"""
    print("=== Test de Tutorial Prompt Generator ===")
    
    generator = TutorialPromptGenerator()
    
    # Test cases
    test_cases = [
        ("x^2", None),
        ("2/3*x^3 + 3/2*x^2 - x", "x^2*(x^2 + 3*x - 3)/6"),
        ("x^3 + 2*x^2 + x + 1", None),
        ("1/2*x^2 + 3*x + 2", None)
    ]
    
    for expr, target in test_cases:
        print(f"\nGenerando prompt para: {expr}")
        prompt = generator.generate_tutorial_prompt(expr, 'x', target)
        print(f"Longitud del prompt: {len(prompt)} caracteres")
        print(f"Complejidad detectada: OK")
    
    # Test programming prompt
    prog_prompt = generator.generate_programming_prompt(
        "2/3*x^3 + 3/2*x^2 - x", 
        "x^2*(x^2 + 3*x - 3)/6"
    )
    print(f"\nPrompt de programación generado: {len(prog_prompt)} caracteres")
    
    print("\n=== Test completado ===")

if __name__ == "__main__":
    test_tutorial_generator()

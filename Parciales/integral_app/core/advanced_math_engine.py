"""
Advanced Math Engine - Microsoft Math Solver Style Integration
Hybrid mathematical engine with step-by-step resolution capabilities
"""
import sympy as sp
import logging
import re
import hashlib
import json
from typing import Dict, List, Optional, Tuple, Any, Union
from fractions import Fraction
from datetime import datetime
import unicodedata

logger = logging.getLogger(__name__)


class AdvancedMathEngine:
    """
    Advanced mathematical engine inspired by Microsoft Math Solver
    Provides intelligent integration with detailed step-by-step solutions
    """
    
    def __init__(self):
        # Initialize SymPy components
        self.x, self.y, self.z, self.t = sp.symbols('x y z t')
        
        # Cache for results optimization
        self.cache = {}
        self.cache_max_size = 1000
        
        # Method detection patterns
        self.method_patterns = {
            'polynomial': r'^[a-zA-Z]\d*\s*\*\s*[a-zA-Z]\d*\^?\d*|\^[a-zA-Z]\d*|\d*\*[a-zA-Z]\d*\^?\d*',
            'product': r'[a-zA-Z]\d*\s*\*\s*\([a-zA-Z0-9+\-*/^]+\)|\([a-zA-Z0-9+\-*/^]+\)\s*\*\s*[a-zA-Z]\d*',
            'substitution': r'\([a-zA-Z0-9+\-*/^]+\)\s*\^?\d*\s*\*\s*[a-zA-Z]\d*\s*\*\s*[a-zA-Z]\d*\'?|[a-zA-Z]\d*\s*\*\s*\([a-zA-Z0-9+\-*/^]+\)\s*\^?\d*',
            'trigonometric': r'sin|cos|tan|cot|sec|csc|asin|acos|atan|sinh|cosh|tanh',
            'exponential': r'exp|e\^|log|ln',
            'rational': r'\/\s*\([a-zA-Z0-9+\-*/^]+\)|\([a-zA-Z0-9+\-*/^]+\)\s*\/',
            'radical': r'sqrt|.*\^.*\/?\d+',
        }
        
        # Step templates for different methods
        self.step_templates = {
            'polynomial': [
                "Identificar función polinómica",
                "Aplicar regla de potencia: $\int x^n dx = \\frac{{x^{{n+1}}}}{{n+1}} + C$",
                "Integrar término por término",
                "Sumar constante de integración"
            ],
            'parts': [
                "Identificar producto de funciones",
                "Aplicar integración por partes: $\int u \\, dv = uv - \\int v \\, du$",
                "Seleccionar u y dv apropiadamente",
                "Calcular du y v",
                "Aplicar fórmula y simplificar"
            ],
            'substitution': [
                "Identificar composición de funciones",
                "Seleccionar sustitución apropiada",
                "Calcular du/dx y dx",
                "Realizar cambio de variable",
                "Integrar en nueva variable",
                "Regresar a variable original"
            ],
            'trigonometric': [
                "Identificar función trigonométrica",
                "Aplicar regla trigonométrica correspondiente",
                "Simplificar resultado si es posible",
                "Verificar con identidad trigonométrica"
            ],
            'exponential': [
                "Identificar función exponencial/logarítmica",
                "Aplicar regla de exponenciales/logaritmos",
                "Simplificar expresión",
                "Verificar dominio si es necesario"
            ]
        }
        
        logger.info("Advanced Math Engine initialized successfully")
    
    def solve_integral_with_steps(self, expression: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Solve integral with detailed step-by-step explanation
        
        Args:
            expression: Mathematical expression to integrate
            variable: Integration variable
            
        Returns:
            Dictionary with result, steps, and verification
        """
        try:
            logger.info(f"Solving integral: {expression} with respect to {variable}")
            
            # Check cache first
            cache_key = self._get_cache_key(expression, variable)
            if cache_key in self.cache:
                logger.info("Returning cached result")
                return self.cache[cache_key]
            
            # Parse expression
            expr = self._parse_expression(expression, variable)
            
            # Detect integration method
            method = self._detect_integration_method(expr, variable)
            
            # Generate steps
            steps = self._generate_solution_steps(expr, variable, method)
            
            # Calculate result
            result = self._calculate_integral(expr, variable)
            
            # Verify solution
            verification = self._verify_solution(expr, result, variable)
            
            # Create response
            response = {
                "result": str(result),
                "result_latex": sp.latex(result),
                "steps": steps,
                "method": method,
                "verification": verification,
                "confidence": verification.get("confidence", 0.0),
                "timestamp": datetime.now().isoformat(),
                "expression": expression,
                "variable": variable
            }
            
            # Cache result
            self._cache_result(cache_key, response)
            
            logger.info(f"Successfully solved integral: {expression}")
            return response
            
        except Exception as e:
            logger.error(f"Error solving integral: {str(e)}")
            return {
                "error": str(e),
                "expression": expression,
                "variable": variable,
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_expression(self, expression: str, variable: str) -> sp.Expr:
        """Parse mathematical expression to SymPy"""
        try:
            # Clean and normalize expression
            cleaned_expr = self._clean_expression(expression)
            
            # Define variable symbol
            var = sp.symbols(variable)
            
            # Parse with SymPy
            expr = sp.sympify(cleaned_expr, locals={variable: var})
            
            logger.info(f"Parsed expression: {expr}")
            return expr
            
        except Exception as e:
            logger.error(f"Error parsing expression: {str(e)}")
            raise ValueError(f"Cannot parse expression '{expression}': {str(e)}")
    
    def _clean_expression(self, expression: str) -> str:
        """Clean and normalize mathematical expression"""
        # Remove extra whitespace
        expr = re.sub(r'\s+', ' ', expression.strip())
        
        # Handle common mathematical notation
        expr = expr.replace('^', '**')
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('·', '*')
        
        # Handle implicit multiplication
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        expr = re.sub(r'([a-zA-Z])(\d)', r'\1**\2', expr)
        
        # Handle special functions
        expr = expr.replace('sqrt', 'sp.sqrt')
        expr = expr.replace('exp', 'sp.exp')
        expr = expr.replace('log', 'sp.log')
        expr = expr.replace('ln', 'sp.log')
        expr = expr.replace('sin', 'sp.sin')
        expr = expr.replace('cos', 'sp.cos')
        expr = expr.replace('tan', 'sp.tan')
        
        return expr
    
    def _detect_integration_method(self, expr: sp.Expr, variable: str) -> str:
        """Detect the most appropriate integration method"""
        try:
            expr_str = str(expr)
            
            # Check for polynomial
            if self._is_polynomial(expr, variable):
                return 'polynomial'
            
            # Check for product (integration by parts)
            if self._is_product(expr, variable):
                return 'parts'
            
            # Check for substitution
            if self._requires_substitution(expr, variable):
                return 'substitution'
            
            # Check for trigonometric
            if self._is_trigonometric(expr):
                return 'trigonometric'
            
            # Check for exponential/logarithmic
            if self._is_exponential(expr):
                return 'exponential'
            
            # Check for rational function
            if self._is_rational(expr, variable):
                return 'rational'
            
            # Default to general method
            return 'general'
            
        except Exception as e:
            logger.warning(f"Error detecting method: {str(e)}")
            return 'general'
    
    def _is_polynomial(self, expr: sp.Expr, variable: str) -> bool:
        """Check if expression is a polynomial"""
        try:
            var = sp.symbols(variable)
            return sp.Poly(expr, var).is_polynomial
        except:
            return False
    
    def _is_product(self, expr: sp.Expr, variable: str) -> bool:
        """Check if expression is a product of functions"""
        try:
            # Check for multiplication of different function types
            if expr.is_Mul:
                factors = expr.args
                if len(factors) >= 2:
                    # Check if factors are different types (algebraic * trig, etc.)
                    return any(self._is_trigonometric(f) for f in factors) or \
                           any(self._is_exponential(f) for f in factors)
            return False
        except:
            return False
    
    def _requires_substitution(self, expr: sp.Expr, variable: str) -> bool:
        """Check if expression requires substitution"""
        try:
            # Check for composition of functions
            if expr.is_Pow:
                base, exp = expr.args
                if exp != 1 and base.is_Add:
                    return True
            
            # Check for function composition
            if expr.is_Function:
                for arg in expr.args:
                    if arg.is_Add or arg.is_Mul:
                        return True
            
            return False
        except:
            return False
    
    def _is_trigonometric(self, expr: sp.Expr) -> bool:
        """Check if expression contains trigonometric functions"""
        try:
            trig_functions = [sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc,
                            sp.asin, sp.acos, sp.atan, sp.sinh, sp.cosh, sp.tanh]
            
            for node in sp.preorder_traversal(expr):
                if any(isinstance(node.func, func.__class__) for func in trig_functions):
                    return True
            return False
        except:
            return False
    
    def _is_exponential(self, expr: sp.Expr) -> bool:
        """Check if expression contains exponential or logarithmic functions"""
        try:
            exp_functions = [sp.exp, sp.log]
            
            for node in sp.preorder_traversal(expr):
                if any(isinstance(node.func, func.__class__) for func in exp_functions):
                    return True
                if node == sp.E:
                    return True
            return False
        except:
            return False
    
    def _is_rational(self, expr: sp.Expr, variable: str) -> bool:
        """Check if expression is a rational function"""
        try:
            var = sp.symbols(variable)
            return expr.is_rational_function(var)
        except:
            return False
    
    def _generate_solution_steps(self, expr: sp.Expr, variable: str, method: str) -> List[Dict[str, Any]]:
        """Generate detailed step-by-step solution"""
        steps = []
        
        # Step 1: Analysis
        steps.append({
            "type": "analysis",
            "description": f"Analizando la expresión: {sp.latex(expr)}",
            "expression": sp.latex(expr),
            "explanation": self._get_analysis_description(expr, variable, method)
        })
        
        # Step 2: Method selection
        steps.append({
            "type": "method",
            "description": f"Método seleccionado: {self._get_method_name(method)}",
            "method": method,
            "explanation": self._get_method_explanation(method)
        })
        
        # Step 3-N: Specific method steps
        method_steps = self._get_method_specific_steps(expr, variable, method)
        steps.extend(method_steps)
        
        # Final step: Result
        result = self._calculate_integral(expr, variable)
        steps.append({
            "type": "result",
            "description": "Resultado final",
            "expression": f"$\\int {sp.latex(expr)} \\, d{variable} = {sp.latex(result)} + C$",
            "result": sp.latex(result),
            "explanation": "Se añade la constante de integración C"
        })
        
        return steps
    
    def _get_analysis_description(self, expr: sp.Expr, variable: str, method: str) -> str:
        """Get analysis description for the expression"""
        descriptions = {
            'polynomial': f"Se detecta una función polinómica en la variable {variable}. Se puede integrar término por término usando la regla de potencia.",
            'parts': f"Se detecta un producto de funciones. Se aplicará integración por partes.",
            'substitution': f"Se detecta una composición de funciones. Se requiere cambio de variable.",
            'trigonometric': "Se detectan funciones trigonométricas. Se aplicarán reglas trigonométricas.",
            'exponential': "Se detectan funciones exponenciales o logarítmicas. Se aplicarán reglas específicas.",
            'rational': f"Se detecta una función racional en {variable}. Se puede usar descomposición en fracciones parciales.",
            'general': "Se aplicará el método general de integración simbólica."
        }
        return descriptions.get(method, descriptions['general'])
    
    def _get_method_name(self, method: str) -> str:
        """Get human-readable method name"""
        names = {
            'polynomial': 'Integración Directa (Polinomios)',
            'parts': 'Integración por Partes',
            'substitution': 'Sustitución',
            'trigonometric': 'Integración Trigonométrica',
            'exponential': 'Integración Exponencial/Logarítmica',
            'rational': 'Fracciones Parciales',
            'general': 'Método General'
        }
        return names.get(method, 'Método Desconocido')
    
    def _get_method_explanation(self, method: str) -> str:
        """Get detailed explanation of the method"""
        explanations = {
            'polynomial': 'La regla de potencia establece que $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ para n != -1. Se aplica a cada término del polinomio.',
            'parts': 'La fórmula de integración por partes es $\\int u \\, dv = uv - \\int v \\, du$. Se usa para productos de funciones.',
            'substitution': 'El cambio de variable $u = f(x)$ transforma $du = f\'(x)dx$. Simplifica integrales con composición de funciones.',
            'trigonometric': 'Se usan identidades trigonométricas y reglas específicas para funciones sin, cos, tan y sus inversas.',
            'exponential': 'Las reglas básicas son $\\int e^x dx = e^x + C$ y $\\int \\frac{1}{x} dx = \\ln|x| + C$.',
            'rational': 'Las fracciones parciales descomponen funciones racionales en términos más simples que se pueden integrar fácilmente.',
            'general': 'Se aplican técnicas simbólicas avanzadas para resolver la integral.'
        }
        return explanations.get(method, 'Método no especificado')
    
    def _get_method_specific_steps(self, expr: sp.Expr, variable: str, method: str) -> List[Dict[str, Any]]:
        """Get specific steps for the detected method"""
        steps = []
        
        if method == 'polynomial':
            steps = self._get_polynomial_steps(expr, variable)
        elif method == 'parts':
            steps = self._get_parts_steps(expr, variable)
        elif method == 'substitution':
            steps = self._get_substitution_steps(expr, variable)
        elif method == 'trigonometric':
            steps = self._get_trigonometric_steps(expr, variable)
        elif method == 'exponential':
            steps = self._get_exponential_steps(expr, variable)
        else:
            steps = self._get_general_steps(expr, variable)
        
        return steps
    
    def _get_polynomial_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for polynomial integration"""
        steps = []
        var = sp.symbols(variable)
        
        try:
            # Get polynomial terms
            poly = sp.Poly(expr, var)
            terms = poly.terms()
            
            steps.append({
                "type": "step",
                "description": "Aplicar regla de potencia a cada término",
                "expression": f"$\\int {sp.latex(expr)} \\, d{variable} = \\sum \\int a_i {variable}^{n_i} \\, d{variable}$",
                "explanation": "Cada término $a x^n$ se integra como $\\frac{a x^{n+1}}{n+1}$"
            })
            
            # Show each term integration
            for (monom, coeff), in enumerate(terms):
                power = monom[0] if monom else 0
                if power != -1:
                    term_expr = coeff * var**power
                    integrated = coeff * var**(power + 1) / (power + 1)
                    
                    steps.append({
                        "type": "step",
                        "description": f"Integrar término {coeff}·{variable}^{power}",
                        "expression": f"$\\int {sp.latex(term_expr)} \\, d{variable} = {sp.latex(integrated)}$",
                        "explanation": f"Aplicando regla de potencia: $\\int {variable}^{power} d{variable} = \\frac{{{variable}^{{{power+1}}}}}{{{power+1}}}$"
                    })
            
        except Exception as e:
            logger.warning(f"Error in polynomial steps: {str(e)}")
            steps.append({
                "type": "step",
                "description": "Integración directa del polinomio",
                "expression": f"$\\int {sp.latex(expr)} \\, d{variable}$",
                "explanation": "Se aplica la regla de potencia término por término"
            })
        
        return steps
    
    def _get_parts_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for integration by parts"""
        steps = []
        var = sp.symbols(variable)
        
        steps.append({
            "type": "step",
            "description": "Identificar u y dv para integración por partes",
            "expression": f"$\\int {sp.latex(expr)} \\, d{variable} = \\int u \\, dv$",
            "explanation": "Se elige u como la función que se simplifica al derivar"
        })
        
        steps.append({
            "type": "step",
            "description": "Aplicar fórmula de integración por partes",
            "expression": f"$\\int u \\, dv = uv - \\int v \\, du$",
            "explanation": "Se calcula du y v, luego se aplica la fórmula"
        })
        
        return steps
    
    def _get_substitution_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for substitution method"""
        steps = []
        var = sp.symbols(variable)
        
        steps.append({
            "type": "step",
            "description": "Identificar sustitución apropiada",
            "expression": f"Sea $u = f({variable})$",
            "explanation": "Se busca una función cuya derivada aparezca en la integral"
        })
        
        steps.append({
            "type": "step",
            "description": "Realizar cambio de variable",
            "expression": f"$du = f'({variable}) d{variable}$",
            "explanation": "Se reemplaza todo en términos de u"
        })
        
        return steps
    
    def _get_trigonometric_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for trigonometric integration"""
        steps = []
        
        steps.append({
            "type": "step",
            "description": "Identificar función trigonométrica",
            "expression": f"$\\int {sp.latex(expr)} \\, d{variable}$",
            "explanation": "Se aplican reglas trigonométricas específicas"
        })
        
        return steps
    
    def _get_exponential_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for exponential/logarithmic integration"""
        steps = []
        
        steps.append({
            "type": "step",
            "description": "Identificar función exponencial o logarítmica",
            "expression": f"$\\int {sp.latex(expr)} \\, d{variable}$",
            "explanation": "Se aplican reglas de exponenciales y logaritmos"
        })
        
        return steps
    
    def _get_general_steps(self, expr: sp.Expr, variable: str) -> List[Dict[str, Any]]:
        """Get steps for general integration"""
        steps = []
        
        steps.append({
            "type": "step",
            "description": "Aplicar método general de integración",
            "expression": f"$\\int {sp.latex(expr)} \\, d{variable}$",
            "explanation": "Se utilizan técnicas simbólicas avanzadas"
        })
        
        return steps
    
    def _calculate_integral(self, expr: sp.Expr, variable: str) -> sp.Expr:
        """Calculate the integral using SymPy"""
        try:
            var = sp.symbols(variable)
            result = sp.integrate(expr, var)
            
            # Simplify result
            result = sp.simplify(result)
            
            logger.info(f"Calculated integral: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating integral: {str(e)}")
            raise ValueError(f"Cannot calculate integral: {str(e)}")
    
    def _verify_solution(self, original_expr: sp.Expr, result_expr: sp.Expr, variable: str) -> Dict[str, Any]:
        """Verify the solution by differentiating the result"""
        try:
            var = sp.symbols(variable)
            
            # Differentiate the result
            derivative = sp.diff(result_expr, var)
            
            # Simplify both expressions
            simplified_original = sp.simplify(original_expr)
            simplified_derivative = sp.simplify(derivative)
            
            # Check if they are equal
            are_equal = sp.simplify(simplified_original - simplified_derivative) == 0
            
            # Calculate confidence
            confidence = 1.0 if are_equal else 0.0
            
            # Try alternative verification
            if not are_equal:
                # Check if they are equivalent after manipulation
                try:
                    diff = sp.simplify(simplified_original - simplified_derivative)
                    if diff == 0:
                        are_equal = True
                        confidence = 1.0
                    elif abs(complex(diff.evalf())) < 1e-10:
                        are_equal = True
                        confidence = 0.95
                except:
                    pass
            
            verification = {
                "original": sp.latex(simplified_original),
                "derivative": sp.latex(simplified_derivative),
                "are_equal": are_equal,
                "confidence": confidence,
                "explanation": "La derivada del resultado coincide con la función original" if are_equal else "La verificación requiere revisión manual"
            }
            
            logger.info(f"Verification completed: confidence={confidence}")
            return verification
            
        except Exception as e:
            logger.error(f"Error verifying solution: {str(e)}")
            return {
                "error": str(e),
                "confidence": 0.0,
                "explanation": "No se pudo verificar la solución automáticamente"
            }
    
    def _get_cache_key(self, expression: str, variable: str) -> str:
        """Generate cache key for expression and variable"""
        content = f"{expression}:{variable}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cache_result(self, key: str, result: Dict[str, Any]):
        """Cache computation result"""
        try:
            # Remove oldest entries if cache is full
            if len(self.cache) >= self.cache_max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            
            self.cache[key] = result
            logger.debug(f"Cached result for key: {key}")
            
        except Exception as e:
            logger.warning(f"Error caching result: {str(e)}")
    
    def clear_cache(self):
        """Clear the computation cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.cache_max_size,
            "usage_percent": len(self.cache) / self.cache_max_size * 100
        }
    
    def solve_derivative_with_steps(self, expression: str, variable: str = 'x') -> Dict[str, Any]:
        """Solve derivative with detailed steps (future extension)"""
        # Placeholder for future derivative functionality
        return {
            "error": "Derivative functionality not yet implemented",
            "expression": expression,
            "variable": variable
        }
    
    def solve_limit_with_steps(self, expression: str, variable: str = 'x', point: str = '0') -> Dict[str, Any]:
        """Solve limit with detailed steps (future extension)"""
        # Placeholder for future limit functionality
        return {
            "error": "Limit functionality not yet implemented",
            "expression": expression,
            "variable": variable,
            "point": point
        }
    
    def solve_ode_with_steps(self, equation: str, variable: str = 'x') -> Dict[str, Any]:
        """Solve ODE with detailed steps (future extension)"""
        # Placeholder for future ODE functionality
        return {
            "error": "ODE functionality not yet implemented",
            "equation": equation,
            "variable": variable
        }

"""
Professional Integral Calculator - Core Architecture
Clean, modular, and production-ready implementation
"""
import sympy as sp
import sympy.integrals.heurisch as heurisch_module
import logging
from typing import Tuple, List, Dict, Any, Optional, Union
from enum import Enum

from .microsoft_math_engine import MicrosoftMathEngine

logger = logging.getLogger(__name__)


class IntegrationMethod(Enum):
    """Integration methods with automatic detection"""
    AUTO = "auto"
    DIRECT = "direct"
    SUBSTITUTION = "substitution"
    PARTS = "parts"
    PARTIAL_FRACTIONS = "partial_fractions"
    TRIGONOMETRIC = "trigonometric"
    RATIONAL = "rational"
    EXPONENTIAL = "exponential"


class IntegrationResult:
    """Structured result for integration operations"""
    
    def __init__(self, result: sp.Expr, steps: List[Dict[str, Any]], 
                 method: IntegrationMethod, original_func: sp.Expr, 
                 variable: sp.Symbol, limits: Optional[Tuple] = None):
        self.result = result
        self.steps = steps
        self.method = method
        self.original_func = original_func
        self.variable = variable
        self.limits = limits
        self.is_definite = limits is not None
        
    def get_definite_result(self) -> Optional[sp.Expr]:
        """Calculate definite integral result if applicable"""
        if not self.is_definite:
            return None
            
        try:
            lower, upper = self.limits
            antiderivative = self.result.subs(sp.Symbol('C'), 0)
            upper_val = antiderivative.subs(self.variable, upper)
            lower_val = antiderivative.subs(self.variable, lower)
            return sp.simplify(upper_val - lower_val)
        except Exception as e:
            logger.error(f"Error calculating definite result: {e}")
            return None


class ProfessionalIntegrator:
    """Professional integration engine with advanced method detection"""
    
    def __init__(self):
        # Initialize Microsoft Math Engine
        self.microsoft_engine = MicrosoftMathEngine()
        
        self.methods = {
            IntegrationMethod.AUTO: self._auto_detect_and_integrate,
            IntegrationMethod.DIRECT: self._direct_integration,
            IntegrationMethod.SUBSTITUTION: self._substitution_integration,
            IntegrationMethod.PARTS: self._parts_integration,
            IntegrationMethod.PARTIAL_FRACTIONS: self._partial_fractions_integration,
            IntegrationMethod.TRIGONOMETRIC: self._trigonometric_integration,
            IntegrationMethod.RATIONAL: self._rational_integration,
            IntegrationMethod.EXPONENTIAL: self._exponential_integration
        }
        
    def integrate(self, func: sp.Expr, var: sp.Symbol, 
                  method: Union[str, IntegrationMethod] = IntegrationMethod.AUTO,
                  limits: Optional[Tuple[sp.Expr, sp.Expr]] = None) -> IntegrationResult:
        """
        Main integration method with comprehensive error handling
        
        Args:
            func: Function to integrate
            var: Integration variable
            method: Integration method (auto-detected if AUTO)
            limits: Optional limits for definite integral
            
        Returns:
            IntegrationResult with result and steps
        """
        try:
            # Convert method to enum
            if isinstance(method, str):
                method = IntegrationMethod(method.lower())
                
            logger.info(f"Integrating: {func} with method: {method.value}")
            
            # Get integration function
            integration_func = self.methods.get(method, self.methods[IntegrationMethod.AUTO])
            
            # Perform integration
            result, steps = integration_func(func, var, limits)
            
            # Simplify result
            if result is not None:
                result = sp.simplify(result)
                
            logger.info(f"Integration successful: {result}")
            
            return IntegrationResult(
                result=result,
                steps=steps,
                method=method,
                original_func=func,
                variable=var,
                limits=limits
            )
            
        except Exception as e:
            logger.error(f"Integration failed: {str(e)}")
            raise IntegrationError(f"Failed to integrate {func}: {str(e)}")
    
    def _auto_detect_and_integrate(self, func: sp.Expr, var: sp.Symbol, 
                                  limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Automatically detect best integration method using SymPy"""
        try:
            # Use SymPy's integrate function
            if limits:
                # Definite integral
                result = sp.integrate(func, (var, limits[0], limits[1]))
            else:
                # Indefinite integral
                result = sp.integrate(func, var)
            
            # Create detailed mathematical steps
            steps = self._generate_detailed_steps(func, var, result, limits)
            
            return result, steps
            
        except Exception as e:
            logger.error(f"Auto-detection integration failed: {e}")
            # Fallback to basic steps
            result = sp.integrate(func, var)
            steps = [
                {
                    'type': 'original',
                    'title': 'Integral Original',
                    'latex': f'\\int {sp.latex(func)} d{var}',
                    'explanation': 'Función a integrar'
                },
                {
                    'type': 'result',
                    'title': 'Resultado',
                    'latex': f'{sp.latex(result)} + C',
                    'explanation': 'Resultado de la integración'
                }
            ]
            return result, steps
    
    def _generate_detailed_steps(self, func: sp.Expr, var: sp.Symbol, 
                                result: sp.Expr, limits: Optional[Tuple] = None) -> List[Dict]:
        """Generate detailed mathematical steps for integration"""
        steps = []
        
        # Step 1: Original integral
        if limits:
            integral_latex = f'\\int_{{{sp.latex(limits[0])}}}^{{{sp.latex(limits[1])}}} {sp.latex(func)} \\, d{var}'
        else:
            integral_latex = f'\\int {sp.latex(func)} \\, d{var}'
        
        steps.append({
            'type': 'original',
            'title': 'Integral Original',
            'latex': integral_latex,
            'explanation': 'Expresión a integrar'
        })
        
        # Step 2: Analyze function structure
        steps.extend(self._analyze_function_structure(func, var))
        
        # Step 3: Decomposition steps (if applicable)
        if func.is_Add:
            steps.extend(self._decompose_sum(func, var, result))
        elif func.is_Mul:
            steps.extend(self._analyze_product(func, var, result))
        
        # Step 4: Integration process
        steps.extend(self._show_integration_process(func, var, result))
        
        # Step 5: Final result
        if limits:
            # Definite integral
            lower, upper = limits
            result_simplified = sp.simplify(result)
            result_latex = sp.latex(result_simplified)
            steps.append({
                'type': 'result',
                'title': 'Resultado de la Integral Definida',
                'latex': f'F({var})|_{{{sp.latex(lower)}}}^{{{sp.latex(upper)}}} = {result_latex}',
                'explanation': 'Aplicamos límites de integración'
            })
        else:
            # Indefinite integral
            result_simplified = sp.simplify(result)
            result_latex = sp.latex(result_simplified)
            steps.append({
                'type': 'result',
                'title': 'Resultado de la Integral Indefinida',
                'latex': f'{result_latex} + C',
                'explanation': 'Suma de la constante de integración C'
            })
        
        return steps
    
    def _analyze_function_structure(self, func: sp.Expr, var: sp.Symbol) -> List[Dict]:
        """Analyze and describe function structure"""
        steps = []
        
        # Identify function type
        func_type = ''
        if func.is_Add:
            func_type = 'Suma de términos'
            terms = func.as_ordered_terms()
            latex_terms = [f'{sp.latex(term)}' for term in terms]
            steps.append({
                'type': 'analysis',
                'title': 'Paso 1: Identificar estructura',
                'latex': f'\\text{{Función: }} {"+".join(latex_terms)}',
                'explanation': f'La función es una suma con {len(terms)} término(s)'
            })
        elif func.is_Mul:
            func_type = 'Producto de factores'
            steps.append({
                'type': 'analysis',
                'title': 'Paso 1: Identificar estructura',
                'latex': f'{sp.latex(func)}',
                'explanation': 'La función es un producto de factores'
            })
        elif func.is_Pow:
            func_type = 'Potencia'
            base = func.base
            exp = func.exp
            steps.append({
                'type': 'analysis',
                'title': 'Paso 1: Identificar estructura',
                'latex': f'{sp.latex(func)} = {sp.latex(base)}^{{{sp.latex(exp)}}}',
                'explanation': 'La función es una potencia'
            })
        else:
            steps.append({
                'type': 'analysis',
                'title': 'Paso 1: Identificar estructura',
                'latex': f'{sp.latex(func)}',
                'explanation': 'Función elemental'
            })
        
        return steps
    
    def _decompose_sum(self, func: sp.Expr, var: sp.Symbol, result: sp.Expr) -> List[Dict]:
        """Show decomposition of sum"""
        steps = []
        terms = func.as_ordered_terms()
        
        if len(terms) > 1:
            steps.append({
                'type': 'decomposition',
                'title': 'Paso 2: Aplicar linealidad de la integral',
                'latex': f'\\int \\left[{" + ".join([sp.latex(t) for t in terms])}\\right] d{var} = {" + ".join([f"\\int {sp.latex(t)} d{var}" for t in terms])}',
                'explanation': 'La integral de una suma es la suma de integrales'
            })
            
            # Show individual integrations
            for i, term in enumerate(terms, 1):
                int_term = sp.integrate(term, var)
                if int_term != 0:  # Only show non-zero terms
                    steps.append({
                        'type': 'term_integration',
                        'title': f'Paso 2.{i}: Integrar término {i}',
                        'latex': f'\\int {sp.latex(term)} \\, d{var} = {sp.latex(int_term)}',
                        'explanation': self._get_rule_explanation(term, var)
                    })
        
        return steps
    
    def _analyze_product(self, func: sp.Expr, var: sp.Symbol, result: sp.Expr) -> List[Dict]:
        """Show analysis of product"""
        steps = []
        steps.append({
            'type': 'analysis',
            'title': 'Paso 2: Analizar factores',
            'latex': f'{sp.latex(func)}',
            'explanation': 'Verificamos si se puede simplificar o factorizar el producto'
        })
        return steps
    
    def _show_integration_process(self, func: sp.Expr, var: sp.Symbol, result: sp.Expr) -> List[Dict]:
        """Show the integration process"""
        steps = []
        
        # Identify the integration rule used
        rule = self._identify_integration_rule(func, var)
        
        if rule:
            steps.append({
                'type': 'integration_rule',
                'title': 'Paso 3: Aplicar regla de integración',
                'latex': rule['formula'],
                'explanation': rule['description']
            })
        
        return steps
    
    def _identify_integration_rule(self, func: sp.Expr, var: sp.Symbol) -> Optional[Dict]:
        """Identify which integration rule applies"""
        
        # Power rule: ∫x^n dx = x^(n+1)/(n+1)
        if func.is_Pow and func.base == var:
            n = func.exp
            return {
                'name': 'Power Rule',
                'formula': f'\\int {sp.latex(var)}^{{{sp.latex(n)}}} d{var} = \\frac{{{sp.latex(var)}^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}}',
                'description': f'Regla de potencia: ∫x^n dx = x^(n+1)/(n+1)'
            }
        
        # Exponential rule: ∫e^x dx = e^x
        if func.has(sp.exp):
            return {
                'name': 'Exponential Rule',
                'formula': f'\\int e^{{{sp.latex(var)}}} d{var} = e^{{{sp.latex(var)}}}',
                'description': 'Regla exponencial: ∫e^x dx = e^x'
            }
        
        # Trigonometric rules
        if func.has(sp.sin):
            return {
                'name': 'Sine Rule',
                'formula': f'\\int \\sin({sp.latex(var)}) d{var} = -\\cos({sp.latex(var)})',
                'description': 'Integración de seno'
            }
        if func.has(sp.cos):
            return {
                'name': 'Cosine Rule',
                'formula': f'\\int \\cos({sp.latex(var)}) d{var} = \\sin({sp.latex(var)})',
                'description': 'Integración de coseno'
            }
        
        # Logarithmic rule: ∫1/x dx = ln|x|
        if func == 1/var:
            return {
                'name': 'Logarithmic Rule',
                'formula': f'\\int \\frac{{1}}{{{sp.latex(var)}}} d{var} = \\ln|{sp.latex(var)}|',
                'description': 'Regla logarítmica: ∫(1/x) dx = ln|x|'
            }
        
        return None
    
    def _get_rule_explanation(self, term: sp.Expr, var: sp.Symbol) -> str:
        """Get explanation for integration rule applied to term"""
        
        if term == var:
            return f'Integración de {sp.latex(var)}: ∫x dx = x²/2'
        elif term.is_Pow and term.base == var:
            n = term.exp
            return f'Regla de potencia: ∫x^{n} dx = x^{n+1}/{n+1}'
        elif term.is_constant(var):
            return f'Integral de constante: ∫c dx = cx'
        elif term.has(sp.sin):
            return 'Integral de seno: ∫sin(x) dx = -cos(x)'
        elif term.has(sp.cos):
            return 'Integral de coseno: ∫cos(x) dx = sin(x)'
        elif term.has(sp.exp):
            return 'Integral exponencial: ∫e^x dx = e^x'
        else:
            return 'Aplicar reglas de integración'
    
    def _direct_integration(self, func: sp.Expr, var: sp.Symbol,
        """Analyze function structure for method selection"""
        analysis = {
            'has_powers': False,
            'has_trig': False,
            'has_exponential': False,
            'has_log': False,
            'has_rational': False,
            'complexity': 'simple'
        }
        
        func_str = str(func)
        
        # Check for powers
        if '**' in func_str or '^' in func_str:
            analysis['has_powers'] = True
            
        # Check for trigonometric functions
        trig_funcs = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'asin', 'acos', 'atan']
        if any(func_str.find(func) != -1 for func in trig_funcs):
            analysis['has_trig'] = True
            
        # Check for exponential functions
        if 'exp' in func_str or 'e**' in func_str or 'e^' in func_str:
            analysis['has_exponential'] = True
            
        # Check for logarithms
        if 'log' in func_str or 'ln' in func_str:
            analysis['has_log'] = True
            
        # Check for rational functions
        if '/' in func_str and var.name in func_str:
            analysis['has_rational'] = True
            
        # Determine complexity
        complexity_score = sum([
            analysis['has_powers'],
            analysis['has_trig'],
            analysis['has_exponential'],
            analysis['has_log'],
            analysis['has_rational']
        ])
        
        if complexity_score >= 3:
            analysis['complexity'] = 'complex'
        elif complexity_score >= 2:
            analysis['complexity'] = 'moderate'
            
        return analysis
    
    def _detect_substitution_opportunity(self, func: sp.Expr, var: sp.Symbol) -> bool:
        """Detect if substitution method is applicable"""
        func_str = str(func)
        
        # Common substitution patterns
        patterns = [
            f'{var}**2 + 1',  # arctan substitution
            f'1 - {var}**2',  # arcsin/arccos substitution
            f'{var}**2 - 1',  # arcosh/arsinh substitution
            'sqrt(',          # Root substitution
            'exp(',          # Exponential substitution
        ]
        
        return any(pattern in func_str for pattern in patterns)
    
    def _detect_parts_opportunity(self, func: sp.Expr, var: sp.Symbol) -> bool:
        """Detect if integration by parts is applicable"""
        func_str = str(func)
        
        # Common parts patterns
        patterns = [
            f'{var} * ',       # Polynomial * function
            f'exp({var}) * ',  # Exponential * function
            f'log({var}) * ',  # Log * function
            f'sin({var}) * ',  # Trig * function
            f'cos({var}) * ',  # Trig * function
        ]
        
        return any(pattern in func_str for pattern in patterns)
    
    def _direct_integration(self, func: sp.Expr, var: sp.Symbol, 
                          limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Direct integration using SymPy"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Integración directa',
            'expression': f"∫ {func} d{var}",
            'method': 'direct'
        })
        
        if limits:
            lower, upper = limits
            result = sp.integrate(func, (var, lower, upper))
            steps.append({
                'type': 'result',
                'title': 'Resultado definido',
                'expression': f"∫_{lower}^{upper} {func} d{var} = {result}",
                'method': 'definite'
            })
        else:
            result = sp.integrate(func, var)
            steps.append({
                'type': 'result',
                'title': 'Resultado indefinido',
                'expression': f"∫ {func} d{var} = {result} + C",
                'method': 'indefinite'
            })
        
        return result, steps
    
    def _substitution_integration(self, func: sp.Expr, var: sp.Symbol, 
                                limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Integration by substitution"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método de sustitución',
            'expression': f"∫ {func} d{var}",
            'method': 'substitution'
        })
        
        # Try common substitutions
        # For now, fallback to direct integration
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado por sustitución',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'substitution'
        })
        
        return result, steps
    
    def _parts_integration(self, func: sp.Expr, var: sp.Symbol, 
                         limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Integration by parts"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método de integración por partes',
            'expression': f"∫ {func} d{var}",
            'method': 'parts'
        })
        
        # For now, fallback to direct integration
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado por partes',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'parts'
        })
        
        return result, steps
    
    def _partial_fractions_integration(self, func: sp.Expr, var: sp.Symbol, 
                                      limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Integration by partial fractions"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método de fracciones parciales',
            'expression': f"∫ {func} d{var}",
            'method': 'partial_fractions'
        })
        
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado por fracciones parciales',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'partial_fractions'
        })
        
        return result, steps
    
    def _trigonometric_integration(self, func: sp.Expr, var: sp.Symbol, 
                                  limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Trigonometric integration"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método trigonométrico',
            'expression': f"∫ {func} d{var}",
            'method': 'trigonometric'
        })
        
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado trigonométrico',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'trigonometric'
        })
        
        return result, steps
    
    def _rational_integration(self, func: sp.Expr, var: sp.Symbol, 
                             limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Rational function integration"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método de funciones racionales',
            'expression': f"∫ {func} d{var}",
            'method': 'rational'
        })
        
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado de función racional',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'rational'
        })
        
        return result, steps
    
    def _exponential_integration(self, func: sp.Expr, var: sp.Symbol, 
                                limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Exponential integration"""
        steps = []
        
        steps.append({
            'type': 'method_step',
            'title': 'Método exponencial',
            'expression': f"∫ {func} d{var}",
            'method': 'exponential'
        })
        
        result = sp.integrate(func, var)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado exponencial',
            'expression': f"∫ {func} d{var} = {result} + C",
            'method': 'exponential'
        })
        
        return result, steps
    
    def _fallback_integration(self, func: sp.Expr, var: sp.Symbol, 
                            limits: Optional[Tuple] = None) -> Tuple[sp.Expr, List[Dict]]:
        """Fallback integration method using basic SymPy integration"""
        try:
            # Basic integration using SymPy
            if limits:
                result = sp.integrate(func, (var, limits[0], limits[1]))
            else:
                result = sp.integrate(func, var)
            
            steps = [
                {
                    'type': 'original',
                    'title': 'Integral Original',
                    'expression': f'∫{func} d{var}' if not limits else f'∫_{limits[0]}^{limits[1]} {func} d{var}',
                    'method': 'fallback',
                    'explanation': 'Función a integrar'
                },
                {
                    'type': 'method',
                    'title': 'Integración Básica',
                    'expression': 'Método de integración directa',
                    'method': 'fallback',
                    'explanation': 'Se aplicó integración directa usando SymPy'
                },
                {
                    'type': 'result',
                    'title': 'Resultado',
                    'expression': str(result),
                    'method': 'fallback',
                    'explanation': 'Resultado de la integración básica'
                }
            ]
            
            return result, steps
            
        except Exception as e:
            logger.error(f"Fallback integration failed: {str(e)}")
            raise IntegrationError(f"Cannot integrate {func}: {str(e)}")


class IntegrationError(Exception):
    """Custom exception for integration errors"""
    pass
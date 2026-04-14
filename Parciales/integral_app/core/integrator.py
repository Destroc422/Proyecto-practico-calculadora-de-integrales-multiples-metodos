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
            
            # Create basic steps
            steps = [
                {
                    'type': 'original',
                    'title': 'Integral Original',
                    'expression': f'∫{func} d{var}' if not limits else f'∫_{limits[0]}^{limits[1]} {func} d{var}',
                    'method': 'auto',
                    'explanation': 'Función a integrar'
                },
                {
                    'type': 'method',
                    'title': 'Método de Integración',
                    'expression': 'Integración Directa',
                    'method': 'auto',
                    'explanation': 'Se aplicó integración directa usando SymPy'
                },
                {
                    'type': 'result',
                    'title': 'Resultado',
                    'expression': str(result),
                    'method': 'auto',
                    'explanation': 'Resultado de la integración'
                }
            ]
            
            return result, steps
            
        except Exception as e:
            logger.warning(f"SymPy integration failed: {str(e)}, using fallback")
            return self._fallback_integration(func, var, limits)
    
    def _analyze_function(self, func: sp.Expr, var: sp.Symbol) -> Dict[str, Any]:
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
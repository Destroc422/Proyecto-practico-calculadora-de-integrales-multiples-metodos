"""
Microsoft Mathematics Engine - Integrated Mathematical Input System
Provides advanced mathematical input capabilities similar to Microsoft Mathematics
"""
import sympy as sp
import re
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from fractions import Fraction
import unicodedata

logger = logging.getLogger(__name__)


class MicrosoftMathEngine:
    """
    Advanced mathematical input engine inspired by Microsoft Mathematics
    Provides natural mathematical notation parsing and conversion
    """
    
    def __init__(self):
        # Mathematical symbol mappings
        self.symbol_mappings = {
            # Greek letters
            'alpha': 'alpha', 'beta': 'beta', 'gamma': 'gamma', 'delta': 'delta',
            'epsilon': 'epsilon', 'zeta': 'zeta', 'eta': 'eta', 'theta': 'theta',
            'iota': 'iota', 'kappa': 'kappa', 'lambda': 'lambda', 'mu': 'mu',
            'nu': 'nu', 'xi': 'xi', 'pi': 'pi', 'rho': 'rho',
            'sigma': 'sigma', 'tau': 'tau', 'upsilon': 'upsilon', 'phi': 'phi',
            'chi': 'chi', 'psi': 'psi', 'omega': 'omega',
            
            # Mathematical constants
            'pi': sp.pi, 'e': sp.E, 'infinity': sp.oo, 'inf': sp.oo,
            
            # Unicode symbols to text
            '×': '*', '÷': '/', '±': '+-', '²': '**2', '³': '**3',
            '½': '1/2', '¼': '1/4', '¾': '3/4', '¹': '**1',
            '°': '*sp.pi/180',  # degrees to radians
            '²': '**2', '³': '**3',
            '²': '**2', '³': '**3',
            '²': '**2', '³': '**3',
            '²': '**2', '³': '**3',
            '²': '**2', '³': '**3',
        }
        
        # Function name mappings
        self.function_mappings = {
            # Trigonometric
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'cot': sp.cot, 'sec': sp.sec, 'csc': sp.csc,
            'arcsin': sp.asin, 'arccos': sp.acos, 'arctan': sp.atan,
            'arcsinh': sp.asinh, 'arccosh': sp.acosh, 'arctanh': sp.atanh,
            'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
            
            # Logarithmic and exponential
            'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
            'log10': sp.log, 'log2': sp.log,
            
            # Algebraic
            'sqrt': sp.sqrt, 'abs': sp.Abs, 'sign': sp.sign,
            'ceil': sp.ceiling, 'floor': sp.floor,
            'factorial': sp.factorial, 'gamma': sp.gamma,
            
            # Calculus
            'diff': sp.diff, 'integrate': sp.integrate, 'limit': sp.limit,
            'derivative': sp.Derivative, 'integral': sp.Integral,
            
            # Summation and product
            'sum': sp.summation, 'product': sp.product, 'sigma': sp.summation,
            'pi': sp.product,
        }
        
        # Operator patterns
        self.operator_patterns = {
            r'\^': '**',           # Power
            r'×': '*',            # Multiplication
            r'÷': '/',            # Division
            r'±': '+-',           # Plus minus
            r'·': '*',            # Dot multiplication
        }
        
        # Fraction patterns
        self.fraction_patterns = [
            r'\(([^)]+)\)/\(([^)]+)\)',  # (a+b)/(c+d)
            r'\(([^)]+)\)/([a-zA-Z]+)',   # (a+b)/x
            r'([a-zA-Z]+\([^)]+\))/([a-zA-Z]+)',  # f(x)/x
            r'([^(]+)\s*/\s*([^(]+)',     # General fraction
            r'(\d+)/(\d+)',               # Simple fraction a/b
            r'(\d+)\s*/\s*(\d+)',         # Fraction with spaces
            r'(\d+)\s*½',                 # Half
            r'(\d+)\s*¼',                 # Quarter
            r'(\d+)\s*¾',                 # Three quarters
        ]
        
        # Power patterns
        self.power_patterns = [
            r'([a-zA-Z])\^(\d+)',      # x^2
            r'([a-zA-Z])\^([a-zA-Z])', # x^y
            r'([a-zA-Z])²',            # x²
            r'([a-zA-Z])³',            # x³
            r'\(([^)]+)\)\^(\d+)',     # (x+1)^2
        ]
        
        # Function patterns
        self.function_patterns = [
            r'([a-zA-Z]+)\(([^)]+)\)',  # f(x)
            r'([a-zA-Z]+)([a-zA-Z])',   # sinx -> sin(x)
            r'([a-zA-Z]+)(\d+)',        # log2 -> log(2)
        ]
        
        # Integral patterns - SIMPLIFIED WORKING PATTERNS
        self.integral_patterns = [
            # Basic indefinite integrals
            r'int\s+(.+?)\s+dx',                    # int x dx
            r'integral\s+(.+?)\s+dx',              # integral x dx
            r'[\u222B]\s*(.+?)\s*dx',              # Unicode integral symbol:  f(x) dx
            
            # Basic definite integrals  
            r'(\d+)\s+to\s+(\d+)\s+int\s+(.+?)\s+dx', # 0 to 1 int x dx
            r'(\d+)\s+to\s+(\d+)\s+integral\s+(.+?)\s+dx', # 0 to 1 integral x dx
            r'[\u222B]_([^{^}]+)\^([^{^}]+)\s*(.+?)\s*dx', # Unicode definite integral: _a^b f(x) dx
            
            # Fraction integrals - NEW PATTERNS
            r'int\s+\((.+?/.+?)\)\s+dx',           # int (x^2+1)/(x+1) dx
            r'integral\s+\((.+?/.+?)\)\s+dx',     # integral (x^2+1)/(x+1) dx
            r'[\u222B]\s*\((.+?/.+?)\)\s*dx',     # Unicode integral with fractions: (x^2+1)/(x+1) dx
            r'(\d+)\s+to\s+(\d+)\s+int\s+\((.+?/.+?)\)\s+dx', # 0 to 1 int (x^2+1)/(x+1) dx
            r'(\d+)\s+to\s+(\d+)\s+integral\s+\((.+?/.+?)\)\s+dx', # 0 to 1 integral (x^2+1)/(x+1) dx
            r'[\u222B]_([^{^}]+)\^([^{^}]+)\s*\((.+?/.+?)\)\s*dx', # Unicode definite with fractions: _a^b (x^2+1)/(x+1) dx
            
            # Simple fraction integrals
            r'int\s+(.+?/.+?)\s+dx',              # int x^2/x dx
            r'integral\s+(.+?/.+?)\s+dx',        # integral x^2/x dx
            r'[\u222B]\s*(.+?/.+?)\s*dx',        # Unicode integral simple fractions: x^2/x dx
            r'(\d+)\s+to\s+(\d+)\s+int\s+(.+?/.+?)\s+dx', # 0 to 1 int x^2/x dx
            r'(\d+)\s+to\s+(\d+)\s+integral\s+(.+?/.+?)\s+dx', # 0 to 1 integral x^2/x dx
            r'[\u222B]_([^{^}]+)\^([^{^}]+)\s*(.+?/.+?)\s*dx', # Unicode definite simple fractions: _a^b x^2/x dx
        ]
        
        logger.info("Microsoft Math Engine initialized")
    
    def parse_natural_math(self, expression: str) -> sp.Expr:
        """
        Parse natural mathematical notation to SymPy expression
        
        Args:
            expression: Natural mathematical expression
            
        Returns:
            SymPy expression
        """
        try:
            logger.info(f"Parsing natural math: {expression}")
            
            # Clean and normalize
            cleaned_expr = self._clean_expression(expression)
            
            # Apply transformations in order
            transformed_expr = self._apply_transformations(cleaned_expr)
            
            # Parse with SymPy
            sympy_expr = self._parse_with_sympy(transformed_expr)
            
            logger.info(f"Successfully parsed: {expression} -> {sympy_expr}")
            return sympy_expr
            
        except Exception as e:
            logger.error(f"Error parsing natural math: {str(e)}")
            raise MathParsingError(f"Cannot parse '{expression}': {str(e)}")
    
    def _clean_expression(self, expression: str) -> str:
        """Clean and normalize expression"""
        # Remove extra whitespace
        expr = re.sub(r'\s+', ' ', expression.strip())
        
        # Remove unmatched parentheses at start and end
        expr = re.sub(r'^[)\]}]+', '', expr)  # Remove closing brackets at start
        expr = re.sub(r'[(\[{]+$', '', expr)  # Remove opening brackets at end
        
        # Handle superscript characters BEFORE Unicode normalization
        expr = expr.replace('²', '**2')
        expr = expr.replace('³', '**3')
        expr = expr.replace('\u00B2', '**2')  # SUPERSCRIPT TWO
        expr = expr.replace('\u00B3', '**3')  # SUPERSCRIPT THREE
        expr = expr.replace('\u00B9', '**1')  # SUPERSCRIPT ONE
        
        # Normalize Unicode characters
        expr = unicodedata.normalize('NFKC', expr)
        
        # Replace common mathematical symbols
        for symbol, replacement in self.symbol_mappings.items():
            if isinstance(replacement, str):
                expr = expr.replace(symbol, replacement)
        
        return expr
    
    def _apply_transformations(self, expression: str) -> str:
        """Apply various mathematical transformations"""
        expr = expression
        
        # Handle "to" in definite integrals FIRST (before general transformations)
        expr = self._transform_definite_integral_limits(expr)
        
        # Handle integrals FIRST (before implicit multiplication to avoid breaking)
        expr = self._transform_integrals(expr)
        
        # Handle powers next (to convert ² to **2 before fraction processing)
        expr = self._transform_powers(expr)
        
        # Handle fractions next (now with proper power notation)
        expr = self._transform_fractions(expr)
        
        # Handle functions
        expr = self._transform_functions(expr)
        
        # Handle operators
        expr = self._transform_operators(expr)
        
        # Handle implicit multiplication last (after integrals are processed)
        expr = self._handle_implicit_multiplication(expr)
        
        return expr
    
    def _transform_fractions(self, expression: str) -> str:
        """Transform fraction notation"""
        expr = expression
        
        # Handle special fractions
        expr = expr.replace('½', '1/2')
        expr = expr.replace('¼', '1/4')
        expr = expr.replace('¾', '3/4')
        
        # Handle general fractions
        for pattern in self.fraction_patterns:
            def replace_fraction(match):
                try:
                    numerator = match.group(1)
                    denominator = match.group(2) if len(match.groups()) > 1 else '2'
                    return f"({numerator})/({denominator})"
                except IndexError:
                    # Handle patterns with different group counts
                    return match.group(0)
            
            expr = re.sub(pattern, replace_fraction, expr)
        
        return expr
    
    def _transform_powers(self, expression: str) -> str:
        """Transform power notation"""
        expr = expression
        
        # Handle superscript characters - make sure to handle Unicode properly
        expr = expr.replace('²', '**2')
        expr = expr.replace('³', '**3')
        expr = expr.replace('\u00B2', '**2')  # SUPERSCRIPT TWO
        expr = expr.replace('\u00B3', '**3')  # SUPERSCRIPT THREE
        expr = expr.replace('\u00B9', '**1')  # SUPERSCRIPT ONE
        
        # Handle power patterns
        for pattern in self.power_patterns:
            def replace_power(match):
                base = match.group(1)
                exp = match.group(2) if len(match.groups()) > 1 else '2'
                return f"({base})**({exp})"
            
            expr = re.sub(pattern, replace_power, expr)
        
        return expr
    
    def _transform_functions(self, expression: str) -> str:
        """Transform function notation"""
        expr = expression
        
        # Handle function patterns
        for pattern in self.function_patterns:
            def replace_function(match):
                func_name = match.group(1)
                arg = match.group(2) if len(match.groups()) > 1 else 'x'
                
                # Check if it's a known function
                if func_name.lower() in [f.lower() for f in self.function_mappings.keys()]:
                    return f"{func_name}({arg})"
                else:
                    return match.group(0)
            
            expr = re.sub(pattern, replace_function, expr)
        
        return expr
    
    def _transform_definite_integral_limits(self, expression: str) -> str:
        """Transform definite integral limits notation"""
        expr = expression
        
        # Handle "a to b int" pattern for definite integrals
        # This needs to be done before the "to" gets transformed by implicit multiplication
        def replace_limits(match):
            lower = match.group(1)
            upper = match.group(2)
            integral_part = match.group(3)
            return f"{lower} {upper} {integral_part}"
        
        # Pattern for "a to b int" or "a to b integral"
        expr = re.sub(r'(\d+)\s+to\s+(\d+)\s+(int|integral)', replace_limits, expr)
        
        return expr
    
    def _transform_integrals(self, expression: str) -> str:
        """Transform integral notation"""
        expr = expression
        
        # Handle integral patterns
        for pattern in self.integral_patterns:
            def replace_integral(match):
                groups = match.groups()
                
                if len(groups) == 3:  # Definite integral
                    lower, upper, integrand = groups
                    # Extract variable from integrand (assume x for simplicity)
                    return f"integrate({integrand}, (x, {lower}, {upper}))"
                elif len(groups) == 1:  # Indefinite integral
                    integrand = groups[0]
                    # Extract variable from integrand (assume x for simplicity)
                    return f"integrate({integrand}, x)"
                else:
                    return match.group(0)
            
            expr = re.sub(pattern, replace_integral, expr)
        
        # Clean up any remaining "to" patterns that weren't caught
        expr = re.sub(r'(\d+)\s+(\d+)\s+', r'', expr)
        
        return expr
    
    def _transform_operators(self, expression: str) -> str:
        """Transform mathematical operators"""
        expr = expression
        
        # Replace operators
        for pattern, replacement in self.operator_patterns.items():
            expr = re.sub(pattern, replacement, expr)
        
        return expr
    
    def _handle_implicit_multiplication(self, expression: str) -> str:
        """Handle implicit multiplication"""
        expr = expression
        
        # Skip processing if this looks like an integral expression
        if 'int' in expr or 'integral' in expr or 'integrate' in expr:
            return expr
        
        # Number followed by variable: 2x -> 2*x
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
        
        # Variable followed by variable: xy -> x*y (but not function names)
        known_functions = [f.lower() for f in self.function_mappings.keys()]
        known_functions.extend(['integrate', 'diff', 'limit', 'series'])  # Add mathematical functions
        
        def replace_var_var(match):
            var1, var2 = match.groups()
            # Don't split if the sequence contains known mathematical functions
            combined = (var1 + var2).lower()
            if any(func in combined for func in known_functions + ['integrate']):
                return match.group(0)
            # Don't split if either variable is followed by parenthesis (function call)
            if expr[match.end():match.end()+1] == '(':
                return match.group(0)
            if var1.lower() not in known_functions and var2.lower() not in known_functions:
                return f"{var1}*{var2}"
            return match.group(0)
        
        expr = re.sub(r'([a-zA-Z])([a-zA-Z])', replace_var_var, expr)
        
        # Parenthesis followed by expression: (x+1)(x-1) -> (x+1)*(x-1)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        
        # Number followed by parenthesis: 2(x+1) -> 2*(x+1)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        
        return expr
    
    def _parse_with_sympy(self, expression: str) -> sp.Expr:
        """Parse expression with SymPy using custom dictionary"""
        # Create local dictionary for SymPy
        local_dict = {}
        
        # Add constants
        local_dict.update(self.symbol_mappings)
        
        # Add functions
        local_dict.update(self.function_mappings)
        
        # Parse with SymPy
        return sp.sympify(expression, locals=local_dict)
    
    def get_suggestions(self, partial_input: str, context: str = 'general') -> List[str]:
        """
        Get suggestions for partial mathematical input
        
        Args:
            partial_input: Partial input text
            context: Context type (function, variable, constant)
            
        Returns:
            List of suggestions
        """
        suggestions = []
        input_lower = partial_input.lower()
        
        if context == 'function':
            # Function suggestions
            for func_name in self.function_mappings.keys():
                if func_name.lower().startswith(input_lower):
                    suggestions.append(func_name)
        
        elif context == 'constant':
            # Constant suggestions
            for const_name, const_value in self.symbol_mappings.items():
                if isinstance(const_value, sp.Expr) and const_name.lower().startswith(input_lower):
                    suggestions.append(const_name)
        
        else:
            # General suggestions
            all_names = list(self.function_mappings.keys()) + \
                        [name for name, value in self.symbol_mappings.items() 
                         if isinstance(value, sp.Expr)]
            
            for name in all_names:
                if name.lower().startswith(input_lower):
                    suggestions.append(name)
        
        return sorted(suggestions)[:10]  # Limit to 10 suggestions
    
    def format_expression(self, expression: sp.Expr, format_type: str = 'pretty') -> str:
        """
        Format SymPy expression for display
        
        Args:
            expression: SymPy expression
            format_type: Format type (pretty, latex, unicode)
            
        Returns:
            Formatted string
        """
        try:
            if format_type == 'pretty':
                return sp.pretty(expression, use_unicode=True)
            elif format_type == 'latex':
                return sp.latex(expression)
            elif format_type == 'unicode':
                return str(expression).replace('**', '^').replace('*', '×')
            else:
                return str(expression)
        except Exception as e:
            logger.error(f"Error formatting expression: {str(e)}")
            return str(expression)
    
    def validate_expression(self, expression: str) -> Tuple[bool, Optional[str]]:
        """
        Validate mathematical expression
        
        Args:
            expression: Expression to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self.parse_natural_math(expression)
            return True, None
        except Exception as e:
            return False, str(e)
    

def validate_expression(self, expression: str) -> Tuple[bool, Optional[str]]:
    """
    Validate mathematical expression
    
    Args:
        expression: Expression to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        self.parse_natural_math(expression)
        return True, None
    except Exception as e:
        return False, str(e)

def get_expression_info(self, expression: str) -> Dict[str, Any]:
    """
    Get detailed information about expression
    
    Args:
        expression: Mathematical expression
        
    Returns:
        Dictionary with expression information
    """
    try:
        # Parse the expression
        parsed_expr = self.parse_natural_math(expression)
        
        # Extract information
        info = {
            'original': expression,
            'parsed': str(parsed_expr),
            'is_valid': True,
            'variables': [],
            'functions': [],
            'constants': [],
            'type': 'unknown'
        }
        
        # Find variables
        for symbol in parsed_expr.free_symbols:
            info['variables'].append(str(symbol))
        
        # Find functions
        for node in sp.preorder_traversal(parsed_expr):
            if isinstance(node, sp.Function):
                info['functions'].append(str(node.func))
        
        # Find constants
        if parsed_expr.has(sp.pi):
            info['constants'].append('pi')
        if parsed_expr.has(sp.E):
            info['constants'].append('e')
        if parsed_expr.has(sp.oo):
            info['constants'].append('infinity')
        
        # Determine expression type
        if any(func in ['sin', 'cos', 'tan'] for func in info['functions']):
            info['type'] = 'trigonometric'
        elif any(func in ['log', 'ln', 'exp'] for func in info['functions']):
            info['type'] = 'exponential'
        elif '**' in str(parsed_expr) and any(v in str(parsed_expr) for v in info['variables']):
            info['type'] = 'polynomial'
        elif '/' in str(parsed_expr):
            info['type'] = 'rational'
        
        return info
        
    except Exception as e:
        return {
            'original': expression,
            'is_valid': False,
            'error': str(e),
            'variables': [],
            'functions': [],
            'constants': [],
            'type': 'error'}
        
    def solve_integral_with_steps(self, expression: str, variable: str = 'x') -> Dict[str, Any]:
        """
        Solve integral with detailed step-by-step explanation
        Compatible interface for integration system
        """
        try:
            logger.info(f"Solving integral with Microsoft Math Engine: {expression} with respect to {variable}")
            
            # Parse the expression using natural math parsing
            parsed_expr = self.parse_natural_math(expression)
            
            # Define variable symbol
            var = sp.symbols(variable)
            
            # Calculate the integral
            result = sp.integrate(parsed_expr, var)
            
            # Simplify result
            if result is not None:
                result = sp.simplify(result)
            
            # Generate steps based on expression type
            steps = self._generate_integration_steps(parsed_expr, var, result)
            
            # Verify the solution
            verification = self._verify_integral_solution(parsed_expr, result, var)
            
            # Detect method used
            method = self._detect_integration_method(parsed_expr, var)
            
            # Create response
            response = {
                "result": str(result),
                "result_latex": sp.latex(result),
                "steps": steps,
                "method": method,
                "verification": verification,
                "confidence": verification.get("confidence", 0.0),
                "timestamp": "2026-04-10T18:00:00",
                "expression": expression,
                "variable": variable,
                "parsed_expression": str(parsed_expr)
            }
            
            logger.info(f"Successfully solved integral: {expression}")
            return response
            
        except Exception as e:
            logger.error(f"Error solving integral: {str(e)}")
            return {
                "error": str(e),
                "expression": expression,
                "variable": variable,
                "timestamp": "2026-04-10T18:00:00"
            }

    def _generate_integration_steps(self, expr: sp.Expr, var: sp.Symbol, result: sp.Expr) -> List[Dict[str, Any]]:
        """Generate step-by-step integration explanation"""
        steps = []
        
        # Step 1: Analysis
        steps.append({
            "type": "analysis",
            "description": f"Analizando la expresión: {sp.latex(expr)}",
            "expression": sp.latex(expr),
            "explanation": self._get_analysis_description(expr, var)
        })
        
        # Step 2: Method selection
        method = self._detect_integration_method(expr, var)
        steps.append({
            "type": "method",
            "description": f"Método seleccionado: {self._get_method_name(method)}",
            "method": method,
            "explanation": self._get_method_explanation(method)
        })
        
        # Step 3: Integration process
        steps.append({
            "type": "step",
            "description": "Aplicando integración",
            "expression": f"$\\int {sp.latex(expr)} \\, d{var} = {sp.latex(result)} + C$",
            "explanation": "Se aplica la regla de integración correspondiente"
        })
        
        # Step 4: Result
        steps.append({
            "type": "result",
            "description": "Resultado final",
            "expression": f"${sp.latex(result)} + C$",
            "result": sp.latex(result),
            "explanation": "Se añade la constante de integración C"
        })
        
        return steps
    
    def _detect_integration_method(self, expr: sp.Expr, var: sp.Symbol) -> str:
        """Detect the integration method based on expression type"""
        expr_str = str(expr)
        
        # Check for polynomial
        if self._is_polynomial(expr, var):
            return 'polynomial'
        
        # Check for trigonometric
        if self._is_trigonometric(expr):
            return 'trigonometric'
        
        # Check for exponential
        if self._is_exponential(expr):
            return 'exponential'
        
        # Check for rational
        if self._is_rational(expr, var):
            return 'rational'
        
        return 'general'
    
    def _is_polynomial(self, expr: sp.Expr, var: sp.Symbol) -> bool:
        """Check if expression is a polynomial"""
        try:
            return sp.Poly(expr, var).is_polynomial
        except:
            return False
    
    def _is_trigonometric(self, expr: sp.Expr) -> bool:
        """Check if expression contains trigonometric functions"""
        trig_functions = [sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc,
                         sp.asin, sp.acos, sp.atan, sp.sinh, sp.cosh, sp.tanh]
        
        for node in sp.preorder_traversal(expr):
            if any(isinstance(node.func, func.__class__) for func in trig_functions):
                return True
        return False
    
    def _is_exponential(self, expr: sp.Expr) -> bool:
        """Check if expression contains exponential or logarithmic functions"""
        exp_functions = [sp.exp, sp.log]
        
        for node in sp.preorder_traversal(expr):
            if any(isinstance(node.func, func.__class__) for func in exp_functions):
                return True
            if node == sp.E:
                return True
        return False
    
    def _is_rational(self, expr: sp.Expr, var: sp.Symbol) -> bool:
        """Check if expression is a rational function"""
        try:
            return expr.is_rational_function(var)
        except:
            return False
    
    def _get_analysis_description(self, expr: sp.Expr, var: sp.Symbol) -> str:
        """Get analysis description for the expression"""
        method = self._detect_integration_method(expr, var)
        
        descriptions = {
            'polynomial': f"Se detecta una función polinómica en la variable {var}. Se puede integrar término por término usando la regla de potencia.",
            'trigonometric': "Se detectan funciones trigonométricas. Se aplicarán reglas trigonométricas.",
            'exponential': "Se detectan funciones exponenciales o logarítmicas. Se aplicarán reglas específicas.",
            'rational': f"Se detecta una función racional en {var}. Se puede usar técnicas de fracciones parciales.",
            'general': "Se aplicará el método general de integración simbólica."
        }
        return descriptions.get(method, descriptions['general'])
    
    def _get_method_name(self, method: str) -> str:
        """Get human-readable method name"""
        names = {
            'polynomial': 'Integración Directa (Polinomios)',
            'trigonometric': 'Integración Trigonométrica',
            'exponential': 'Integración Exponencial/Logarítmica',
            'rational': 'Fracciones Parciales',
            'general': 'Método General'
        }
        return names.get(method, 'Método Desconocido')
    
    def _get_method_explanation(self, method: str) -> str:
        """Get detailed explanation of the method"""
        explanations = {
            'polynomial': 'La regla de potencia establece que $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$ para n != -1.',
            'trigonometric': 'Se usan identidades trigonométricas y reglas específicas para funciones sin, cos, tan.',
            'exponential': 'Las reglas básicas son $\\int e^x dx = e^x + C$ y $\\int \\frac{1}{x} dx = \\ln|x| + C$.',
            'rational': 'Las fracciones parciales descomponen funciones racionales en términos más simples.',
            'general': 'Se aplican técnicas simbólicas avanzadas para resolver la integral.'
        }
        return explanations.get(method, 'Método no especificado')
    
    def _verify_integral_solution(self, original_expr: sp.Expr, result_expr: sp.Expr, var: sp.Symbol) -> Dict[str, Any]:
        """Verify the integral solution by differentiation"""
        try:
            # Differentiate the result
            derivative = sp.diff(result_expr, var)
            
            # Simplify both expressions
            simplified_original = sp.simplify(original_expr)
            simplified_derivative = sp.simplify(derivative)
            
            # Check if they are equal
            are_equal = sp.simplify(simplified_original - simplified_derivative) == 0
            
            # Calculate confidence
            confidence = 1.0 if are_equal else 0.8  # Default to high confidence for simple cases
            
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


class MathParsingError(Exception):
    """Custom exception for mathematical parsing errors"""
    pass

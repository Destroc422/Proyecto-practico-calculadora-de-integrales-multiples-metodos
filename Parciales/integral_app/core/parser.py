"""
Professional Math Parser - Robust and production-ready
Handles complex mathematical expressions with comprehensive error handling
"""
import sympy as sp
import logging
from typing import Union, Optional, Dict, Any
import re

logger = logging.getLogger(__name__)


class ProfessionalMathParser:
    """Professional mathematical expression parser"""
    
    def __init__(self):
        # Predefined symbols for common mathematical constants
        self.constants = {
            'pi': sp.pi,
            'e': sp.E,
            'inf': sp.oo,
            'nan': sp.nan
        }
        
        # Predefined functions
        self.functions = {
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'cot': sp.cot,
            'sec': sp.sec,
            'csc': sp.csc,
            'asin': sp.asin,
            'acos': sp.acos,
            'atan': sp.atan,
            'sinh': sp.sinh,
            'cosh': sp.cosh,
            'tanh': sp.tanh,
            'asinh': sp.asinh,
            'acosh': sp.acosh,
            'atanh': sp.atanh,
            'log': sp.log,
            'ln': sp.log,
            'exp': sp.exp,
            'sqrt': sp.sqrt,
            'abs': sp.Abs,
            'sign': sp.sign,
            'ceil': sp.ceiling,
            'floor': sp.floor,
            'factorial': sp.factorial,
            'gamma': sp.gamma,
            'beta': sp.beta,
            'zeta': sp.zeta,
            'integrate': sp.integrate,
            'diff': sp.diff,
            'limit': sp.limit,
            'Sum': sp.summation,
            'Product': sp.product,
            'Derivative': sp.Derivative
        }
        
        # Variable symbols cache
        self.symbols = {}
        
    def parse(self, expression: str, variable: str = 'x') -> sp.Expr:
        """
        Parse mathematical expression into SymPy expression
        
        Args:
            expression: Mathematical expression string
            variable: Integration variable name
            
        Returns:
            SymPy expression
            
        Raises:
            ParseError: If expression cannot be parsed
        """
        try:
            logger.info(f"Parsing expression: {expression}")
            
            # Clean and preprocess expression
            cleaned_expr = self._preprocess_expression(expression)
            logger.info(f"Cleaned expression: {cleaned_expr}")
            
            # Get or create variable symbol
            var_symbol = self._get_symbol(variable)
            
            # Parse with SymPy
            sympy_expr = sp.sympify(cleaned_expr, locals=self._get_sympy_dict())
            
            # Validate the expression
            self._validate_expression(sympy_expr, var_symbol)
            
            logger.info(f"Successfully parsed: {expression} -> {sympy_expr}")
            
            return sympy_expr
            
        except Exception as e:
            logger.error(f"Failed to parse expression '{expression}': {str(e)}")
            raise ParseError(f"Cannot parse expression '{expression}': {str(e)}")
    
    def _preprocess_expression(self, expression: str) -> str:
        """Preprocess expression for SymPy parsing"""
        # Remove whitespace
        expr = expression.strip()
        
        # Convert common notations - Fixed to avoid over-processing
        conversions = {
            r'×': '*',              # Multiplication symbol
            r'÷': '/',              # Division symbol
            r'π': 'pi',             # Pi symbol
            r'∞': 'oo',             # Infinity symbol
            r'√': 'sqrt',           # Square root
            r'∑': 'Sum',            # Summation
            r'∏': 'Product',        # Product
            r'∫': 'integrate',      # Integral
            r'∂': 'Derivative',     # Partial derivative
            r'∇': 'Gradient',       # Gradient
            r'∈': 'in',             # Element of
            r'∉': 'NotElement',      # Not element of
            r'⊂': 'subset',         # Subset
            r'⊃': 'superset',       # Superset
            r'∪': 'Union',          # Union
            r'∩': 'Intersection',    # Intersection
            r'∅': 'EmptySet',       # Empty set
            r'ℝ': 'Reals',          # Real numbers
            r'ℤ': 'Integers',       # Integers
            r'ℕ': 'Naturals',       # Natural numbers
            r'ℂ': 'Complexes',      # Complex numbers
            r'ℚ': 'Rationals',      # Rational numbers
        }
        
        for pattern, replacement in conversions.items():
            expr = re.sub(pattern, replacement, expr)
        
        # Handle implicit multiplication (e.g., "2x" -> "2*x") - DISABLED for now
        # expr = self._handle_implicit_multiplication(expr)
        
        # Handle function notation (e.g., "sinx" -> "sin(x)")
        expr = self._handle_function_notation(expr)
        
        return expr
    
    def _handle_implicit_multiplication(self, expression: str) -> str:
        """Handle implicit multiplication in expressions"""
        # Only apply to simple cases to avoid breaking function calls
        
        # Pattern: number followed by variable (e.g., "2x" -> "2*x")
        pattern1 = r'(\d)([a-zA-Z])'
        expression = re.sub(pattern1, r'\1*\2', expression)
        
        # Pattern: variable followed by number in parentheses (e.g., "x(2)" -> "x*(2)")
        # But avoid function calls by checking if it's a known function
        def replace_var_paren(match):
            var = match.group(1)
            paren = match.group(2)
            # Check if this looks like a function call
            if var in ['integrate', 'diff', 'limit', 'sin', 'cos', 'tan', 
                      'log', 'ln', 'exp', 'sqrt', 'abs', 'sum', 'product']:
                return var + paren  # Don't add multiplication
            return var + '*' + paren  # Add multiplication
        
        pattern2 = r'([a-zA-Z])(\d*\()'
        expression = re.sub(pattern2, replace_var_paren, expression)
        
        # Pattern: closing parenthesis followed by opening parenthesis (e.g., "(2)(3)" -> "(2)*(3)")
        pattern3 = r'(\))(\()'
        expression = re.sub(pattern3, r'\1*\2', expression)
        
        # Pattern: variable followed by variable (e.g., "xy" -> "x*y")
        # Only for single variables, not function names
        pattern4 = r'\b([a-z])\b([a-z])\b'
        expression = re.sub(pattern4, r'\1*\2', expression)
        
        return expression
    
    def _handle_function_notation(self, expression: str) -> str:
        """Handle function notation without parentheses"""
        # Common functions that need parentheses
        functions = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 
                    'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                    'log', 'ln', 'exp', 'sqrt', 'abs', 'sign']
        
        for func in functions:
            pattern = rf'\b{func}([a-zA-Z])'
            replacement = rf'{func}(\1)'
            expression = re.sub(pattern, replacement, expression)
        
        return expression
    
    def _get_symbol(self, name: str) -> sp.Symbol:
        """Get or create a Symbol"""
        if name not in self.symbols:
            self.symbols[name] = sp.Symbol(name)
        return self.symbols[name]
    
    def _get_sympy_dict(self) -> Dict[str, Any]:
        """Get dictionary for SymPy parsing"""
        sympy_dict = {}
        
        # Add constants
        sympy_dict.update(self.constants)
        
        # Add functions
        sympy_dict.update(self.functions)
        
        # Add symbols
        sympy_dict.update(self.symbols)
        
        return sympy_dict
    
    def _validate_expression(self, expr: sp.Expr, var_symbol: sp.Symbol) -> None:
        """Validate parsed expression"""
        # Check if expression is valid
        if expr is None:
            raise ParseError("Expression is None")
        
        # Check if it contains the integration variable
        if not expr.has(var_symbol):
            logger.warning(f"Expression does not contain variable {var_symbol}")
        
        # Check for invalid operations
        if expr.has(sp.zoo):
            logger.warning("Expression contains complex infinity")
    
    def is_valid_expression(self, expression: str, variable: str = 'x') -> bool:
        """
        Check if expression is valid without raising exceptions
        
        Args:
            expression: Mathematical expression string
            variable: Integration variable name
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.parse(expression, variable)
            return True
        except Exception:
            return False
    
    def get_variables(self, expression: str) -> list:
        """
        Get all variables used in expression
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            List of variable names
        """
        try:
            expr = self.parse(expression)
            variables = []
            
            for symbol in expr.free_symbols:
                if symbol.is_Symbol:
                    variables.append(str(symbol))
            
            return sorted(variables)
            
        except Exception:
            return []
    
    def simplify_expression(self, expression: str, variable: str = 'x') -> str:
        """
        Simplify mathematical expression
        
        Args:
            expression: Mathematical expression string
            variable: Integration variable name
            
        Returns:
            Simplified expression string
        """
        try:
            expr = self.parse(expression, variable)
            simplified = sp.simplify(expr)
            return str(simplified)
        except Exception as e:
            logger.error(f"Failed to simplify expression: {str(e)}")
            return expression


class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass

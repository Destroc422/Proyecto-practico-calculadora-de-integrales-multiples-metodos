"""
Domain Validator Module - Advanced Function Analysis
Prevents graphing errors by validating function domains before plotting
"""
import sympy as sp
import numpy as np
import logging
from typing import List, Tuple, Dict, Optional, Union
import math

logger = logging.getLogger(__name__)


class DomainValidator:
    """Advanced domain validation for mathematical functions"""
    
    def __init__(self):
        """Initialize domain validator"""
        self.restricted_functions = {
            'log': self._validate_logarithm,
            'ln': self._validate_logarithm,
            'sqrt': self._validate_square_root,
            'cbrt': self._validate_cube_root,
            'asin': self._validate_arcsin,
            'acos': self._validate_arccos,
            'atan': self._validate_arctan,
            'acot': self._validate_arccot,
            'sec': self._validate_secant,
            'csc': self._validate_cosecant,
            'cot': self._validate_cotangent,
            'tan': self._validate_tangent,
            '1/': self._validate_rational,
            'abs': self._validate_absolute,
            'exp': self._validate_exponential
        }
    
    def validate_function_domain(self, func: sp.Expr, var: sp.Symbol, 
                                x_range: Tuple[float, float]) -> Dict:
        """
        Comprehensive domain validation for mathematical functions
        
        Args:
            func: SymPy expression to validate
            var: Variable symbol
            x_range: Tuple of (start, end) for x range
            
        Returns:
            Dict with validation results and recommendations
        """
        try:
            result = {
                'valid': True,
                'warnings': [],
                'errors': [],
                'recommendations': [],
                'safe_ranges': [x_range],
                'problematic_points': [],
                'asymptotes': [],
                'discontinuities': []
            }
            
            # Convert to string for pattern matching
            func_str = str(func)
            
            # Check for restricted functions
            for pattern, validator in self.restricted_functions.items():
                if pattern in func_str:
                    validation_result = validator(func, var, x_range)
                    self._merge_validation_results(result, validation_result)
            
            # Check for rational expressions
            if '/' in func_str and var.name in func_str:
                rational_result = self._validate_rational(func, var, x_range)
                self._merge_validation_results(result, rational_result)
            
            # Check for even roots
            if 'sqrt' in func_str or '**(1/2)' in func_str or '**0.5' in func_str:
                root_result = self._validate_even_roots(func, var, x_range)
                self._merge_validation_results(result, root_result)
            
            # Check for logarithms with complex arguments
            if any(log_func in func_str for log_func in ['log', 'ln']):
                log_result = self._validate_logarithm(func, var, x_range)
                self._merge_validation_results(result, log_result)
            
            # Generate safe ranges
            result['safe_ranges'] = self._generate_safe_ranges(x_range, result['problematic_points'])
            
            # Final validation
            result['valid'] = len(result['errors']) == 0
            
            logger.info(f"Domain validation completed: {len(result['warnings'])} warnings, {len(result['errors'])} errors")
            return result
            
        except Exception as e:
            logger.error(f"Error in domain validation: {str(e)}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'recommendations': ["Use a simpler function or check syntax"],
                'safe_ranges': [(x_range[0], x_range[1])],
                'problematic_points': [],
                'asymptotes': [],
                'discontinuities': []
            }
    
    def _merge_validation_results(self, main_result: Dict, new_result: Dict):
        """Merge validation results"""
        main_result['warnings'].extend(new_result.get('warnings', []))
        main_result['errors'].extend(new_result.get('errors', []))
        main_result['recommendations'].extend(new_result.get('recommendations', []))
        main_result['problematic_points'].extend(new_result.get('problematic_points', []))
        main_result['asymptotes'].extend(new_result.get('asymptotes', []))
        main_result['discontinuities'].extend(new_result.get('discontinuities', []))
    
    def _validate_logarithm(self, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float]) -> Dict:
        """Validate logarithmic functions"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        try:
            # Find points where argument <= 0
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y_vals = f(x_vals)
                
                # Check for negative or zero arguments
                problem_indices = []
                for i, y in enumerate(y_vals):
                    if isinstance(y, (int, float)) and y <= 0:
                        problem_indices.append(i)
                
                if problem_indices:
                    # Find problematic x values
                    problem_x = [x_vals[i] for i in problem_indices]
                    result['problematic_points'] = problem_x
                    result['warnings'].append(f"Logarithm has {len(problem_x)} points with non-positive arguments")
                    result['recommendations'].append("Avoid regions where logarithm argument <= 0")
                
                # Check for vertical asymptotes
                for i in range(1, len(x_vals)):
                    if (isinstance(y_vals[i-1], (int, float)) and isinstance(y_vals[i], (int, float)) and
                        (y_vals[i-1] > 0 and y_vals[i] <= 0)) or (y_vals[i-1] <= 0 and y_vals[i] > 0):
                        result['asymptotes'].append(x_vals[i])
                        result['warnings'].append(f"Vertical asymptote detected near x = {x_vals[i]:.3f}")
                
            except Exception as e:
                result['warnings'].append(f"Could not evaluate logarithm: {str(e)}")
                result['recommendations'].append("Check logarithm syntax and domain")
                
        except Exception as e:
            result['errors'].append(f"Logarithm validation error: {str(e)}")
        
        return result
    
    def _validate_square_root(self, func: sp.Expr, var: sp.Symbol, 
                            x_range: Tuple[float, float]) -> Dict:
        """Validate square root functions"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        try:
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y_vals = f(x_vals)
                
                # Check for negative values under square root
                problem_indices = []
                for i, y in enumerate(y_vals):
                    if isinstance(y, complex) or (isinstance(y, (int, float)) and y < 0):
                        problem_indices.append(i)
                
                if problem_indices:
                    problem_x = [x_vals[i] for i in problem_indices]
                    result['problematic_points'] = problem_x
                    result['warnings'].append(f"Square root has {len(problem_x)} points with negative arguments")
                    result['recommendations'].append("Use domain where square root argument >= 0")
                
            except Exception as e:
                result['warnings'].append(f"Could not evaluate square root: {str(e)}")
                
        except Exception as e:
            result['errors'].append(f"Square root validation error: {str(e)}")
        
        return result
    
    def _validate_rational(self, func: sp.Expr, var: sp.Symbol, 
                         x_range: Tuple[float, float]) -> Dict:
        """Validate rational functions (denominator zeros)"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        try:
            # Find denominator
            if func.is_Mul or func.is_Add:
                # For complex expressions, try to find denominator
                denominator = sp.denom(func)
                if denominator != 1:
                    # Find zeros of denominator
                    zeros = sp.solve(denominator, var)
                    
                    for zero in zeros:
                        try:
                            zero_val = float(zero.evalf())
                            if x_range[0] <= zero_val <= x_range[1]:
                                result['asymptotes'].append(zero_val)
                                result['problematic_points'].append(zero_val)
                                result['warnings'].append(f"Vertical asymptote at x = {zero_val:.3f}")
                        except:
                            continue
            
            # Numerical validation
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y_vals = f(x_vals)
                
                # Check for very large values (near asymptotes)
                for i, y in enumerate(y_vals):
                    if isinstance(y, (int, float, np.number)) and abs(y) > 1e6:
                        result['problematic_points'].append(x_vals[i])
                        if x_vals[i] not in result['asymptotes']:
                            result['warnings'].append(f"Large value detected near x = {x_vals[i]:.3f}")
                
            except Exception as e:
                result['warnings'].append(f"Could not evaluate rational function: {str(e)}")
                
        except Exception as e:
            result['errors'].append(f"Rational function validation error: {str(e)}")
        
        return result
    
    def _validate_even_roots(self, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> Dict:
        """Validate even root functions"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        try:
            x_vals = np.linspace(x_range[0], x_range[1], 1000)
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y_vals = f(x_vals)
                
                # Check for complex results
                for i, y in enumerate(y_vals):
                    if isinstance(y, complex):
                        result['problematic_points'].append(x_vals[i])
                
                if result['problematic_points']:
                    result['warnings'].append(f"Even root has {len(result['problematic_points'])} points with complex results")
                    result['recommendations'].append("Ensure even root arguments are non-negative")
                
            except Exception as e:
                result['warnings'].append(f"Could not evaluate even roots: {str(e)}")
                
        except Exception as e:
            result['errors'].append(f"Even root validation error: {str(e)}")
        
        return result
    
    def _validate_trigonometric(self, func: sp.Expr, var: sp.Symbol, 
                              x_range: Tuple[float, float]) -> Dict:
        """Validate trigonometric functions"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        func_str = str(func)
        
        # Check for tan, cot, sec, csc (have asymptotes)
        if 'tan' in func_str:
            # Tan has asymptotes at pi/2 + k*pi
            k_min = math.floor((x_range[0] - math.pi/2) / math.pi)
            k_max = math.ceil((x_range[1] - math.pi/2) / math.pi)
            
            for k in range(k_min, k_max + 1):
                asymptote = math.pi/2 + k * math.pi
                if x_range[0] <= asymptote <= x_range[1]:
                    result['asymptotes'].append(asymptote)
                    result['problematic_points'].append(asymptote)
                    result['warnings'].append(f"Tangent asymptote at x = {asymptote:.3f}")
        
        elif 'cot' in func_str:
            # Cot has asymptotes at k*pi
            k_min = math.floor(x_range[0] / math.pi)
            k_max = math.ceil(x_range[1] / math.pi)
            
            for k in range(k_min, k_max + 1):
                asymptote = k * math.pi
                if x_range[0] <= asymptote <= x_range[1]:
                    result['asymptotes'].append(asymptote)
                    result['problematic_points'].append(asymptote)
                    result['warnings'].append(f"Cotangent asymptote at x = {asymptote:.3f}")
        
        return result
    
    def _validate_arcsin(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Validate arcsin function (domain [-1, 1])"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        result['recommendations'].append("Arcsin argument must be in [-1, 1]")
        result['warnings'].append("Check arcsin domain restrictions")
        
        return result
    
    def _validate_arccos(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Validate arccos function (domain [-1, 1])"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        result['recommendations'].append("Arccos argument must be in [-1, 1]")
        result['warnings'].append("Check arccos domain restrictions")
        
        return result
    
    def _validate_arctan(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Validate arctan function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Arctan is defined for all real numbers
        return result
    
    def _validate_arccot(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Validate arccot function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Arccot is defined for all real numbers
        return result
    
    def _validate_secant(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Validate secant function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Sec has asymptotes where cos = 0 (pi/2 + k*pi)
        k_min = math.floor((x_range[0] - math.pi/2) / math.pi)
        k_max = math.ceil((x_range[1] - math.pi/2) / math.pi)
        
        for k in range(k_min, k_max + 1):
            asymptote = math.pi/2 + k * math.pi
            if x_range[0] <= asymptote <= x_range[1]:
                result['asymptotes'].append(asymptote)
                result['problematic_points'].append(asymptote)
                result['warnings'].append(f"Secant asymptote at x = {asymptote:.3f}")
        
        return result
    
    def _validate_cosecant(self, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float]) -> Dict:
        """Validate cosecant function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Csc has asymptotes where sin = 0 (k*pi)
        k_min = math.floor(x_range[0] / math.pi)
        k_max = math.ceil(x_range[1] / math.pi)
        
        for k in range(k_min, k_max + 1):
            asymptote = k * math.pi
            if x_range[0] <= asymptote <= x_range[1]:
                result['asymptotes'].append(asymptote)
                result['problematic_points'].append(asymptote)
                result['warnings'].append(f"Cosecant asymptote at x = {asymptote:.3f}")
        
        return result
    
    def _validate_cotangent(self, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> Dict:
        """Validate cotangent function"""
        return self._validate_trigonometric(func, var, x_range)
    
    def _validate_tangent(self, func: sp.Expr, var: sp.Symbol, 
                         x_range: Tuple[float, float]) -> Dict:
        """Validate tangent function"""
        return self._validate_trigonometric(func, var, x_range)
    
    def _validate_absolute(self, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float]) -> Dict:
        """Validate absolute value function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Absolute value is defined for all real numbers
        return result
    
    def _validate_exponential(self, func: sp.Expr, var: sp.Symbol, 
                             x_range: Tuple[float, float]) -> Dict:
        """Validate exponential function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Exponential is defined for all real numbers
        return result
    
    def _validate_cube_root(self, func: sp.Expr, var: sp.Symbol, 
                            x_range: Tuple[float, float]) -> Dict:
        """Validate cube root function"""
        result = {'warnings': [], 'errors': [], 'recommendations': [], 
                 'problematic_points': [], 'asymptotes': [], 'discontinuities': []}
        
        # Cube root is defined for all real numbers
        return result
    
    def _generate_safe_ranges(self, original_range: Tuple[float, float], 
                           problematic_points: List[float]) -> List[Tuple[float, float]]:
        """Generate safe ranges avoiding problematic points"""
        if not problematic_points:
            return [original_range]
        
        # Sort problematic points
        sorted_points = sorted(problematic_points)
        safe_ranges = []
        
        # Start with the original range
        start = original_range[0]
        
        for point in sorted_points:
            if point > start + 0.1:  # Add small buffer
                safe_ranges.append((start, point - 0.1))
            start = point + 0.1
        
        # Add final range if needed
        if start < original_range[1]:
            safe_ranges.append((start, original_range[1]))
        
        return safe_ranges if safe_ranges else [original_range]


# Create singleton instance
domain_validator = DomainValidator()

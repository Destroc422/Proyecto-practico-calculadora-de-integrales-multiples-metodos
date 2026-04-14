"""
Advanced Mathematics Module
Extended mathematical capabilities beyond basic integration
"""
import sympy as sp
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
import math

logger = logging.getLogger(__name__)


class AdvancedMathematics:
    """Advanced mathematical operations and analysis"""
    
    def __init__(self):
        """Initialize advanced mathematics module"""
        self.series_cache = {}
        self.transform_cache = {}
        
    def taylor_series(self, func: sp.Expr, var: sp.Symbol, point: float = 0, 
                      order: int = 5) -> Dict:
        """
        Calculate Taylor series expansion
        
        Args:
            func: Function to expand
            var: Variable
            point: Expansion point
            order: Order of expansion
            
        Returns:
            Dict with series information
        """
        try:
            logger.info(f"Calculating Taylor series of order {order} at point {point}")
            
            # Convert point to sympy
            point_sym = sp.nsimplify(point)
            
            # Calculate Taylor series
            taylor_series = sp.series(func, var, point_sym, order + 1)
            
            # Remove O(x^n) term for polynomial
            polynomial = taylor_series.removeO()
            
            # Calculate remainder estimate
            remainder_estimate = self._estimate_series_remainder(func, var, point, order)
            
            # Calculate convergence radius (if possible)
            convergence_radius = self._estimate_convergence_radius(func, var, point)
            
            result = {
                'original_function': func,
                'variable': var,
                'expansion_point': point,
                'order': order,
                'series': str(taylor_series),
                'polynomial': polynomial,
                'polynomial_str': str(polynomial),
                'remainder_estimate': remainder_estimate,
                'convergence_radius': convergence_radius,
                'coefficients': self._extract_series_coefficients(polynomial, var, point),
                'valid_for': f'|x - {point}| < {convergence_radius}' if convergence_radius else 'Unknown',
                'success': True
            }
            
            logger.info(f"Taylor series calculated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating Taylor series: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def fourier_series(self, func: sp.Expr, var: sp.Symbol, period: float = 2*np.pi, 
                       terms: int = 5) -> Dict:
        """
        Calculate Fourier series expansion
        
        Args:
            func: Function to expand
            var: Variable
            period: Period of function
            terms: Number of terms
            
        Returns:
            Dict with Fourier series information
        """
        try:
            logger.info(f"Calculating Fourier series with {terms} terms")
            
            # Calculate Fourier coefficients
            a0, an_coeffs, bn_coeffs = self._calculate_fourier_coefficients(
                func, var, period, terms
            )
            
            # Construct Fourier series
            fourier_series = self._construct_fourier_series(a0, an_coeffs, bn_coeffs, var, period)
            
            # Parseval's theorem check
            parseval_check = self._parseval_theorem_check(func, a0, an_coeffs, bn_coeffs, period)
            
            result = {
                'original_function': func,
                'variable': var,
                'period': period,
                'terms': terms,
                'a0': a0,
                'an_coefficients': an_coeffs,
                'bn_coefficients': bn_coeffs,
                'series': fourier_series,
                'parseval_check': parseval_check,
                'convergence': 'Pointwise (Dirichlet conditions)',
                'success': True
            }
            
            logger.info(f"Fourier series calculated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating Fourier series: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def laplace_transform(self, func: sp.Expr, var: sp.Symbol, 
                         s_var: sp.Symbol = None) -> Dict:
        """
        Calculate Laplace transform
        
        Args:
            func: Function to transform
            var: Original variable (usually t)
            s_var: Transform variable (usually s)
            
        Returns:
            Dict with Laplace transform information
        """
        try:
            logger.info("Calculating Laplace transform")
            
            # Use s if not provided
            if s_var is None:
                s_var = sp.symbols('s', positive=True)
            
            # Calculate Laplace transform
            laplace_transform = sp.laplace_transform(func, var, s_var)
            
            # Extract transform and conditions
            transform_expr = laplace_transform[0]
            convergence_conditions = laplace_transform[1]
            
            # Region of convergence
            roc = self._determine_region_of_convergence(convergence_conditions)
            
            # Check for common transforms
            transform_properties = self._analyze_transform_properties(func, transform_expr)
            
            result = {
                'original_function': func,
                'original_variable': var,
                'transform_variable': s_var,
                'transform': transform_expr,
                'transform_str': str(transform_expr),
                'convergence_conditions': str(convergence_conditions),
                'region_of_convergence': roc,
                'properties': transform_properties,
                'success': True
            }
            
            logger.info(f"Laplace transform calculated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating Laplace transform: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def solve_differential_equation(self, equation: str, dependent_var: str, 
                                 independent_var: str = 'x') -> Dict:
        """
        Solve ordinary differential equations
        
        Args:
            equation: Differential equation as string
            dependent_var: Dependent variable name (e.g., 'y')
            independent_var: Independent variable name (e.g., 'x')
            
        Returns:
            Dict with solution information
        """
        try:
            logger.info(f"Solving differential equation: {equation}")
            
            # Define symbols
            x = sp.symbols(independent_var)
            y = sp.Function(dependent_var)
            
            # Parse equation (simplified approach)
            # This is a basic implementation - full parsing would be more complex
            parsed_eq = self._parse_differential_equation(equation, y, x)
            
            # Solve the equation
            solution = sp.dsolve(parsed_eq, y(x))
            
            # Extract solution information
            general_solution = solution.rhs
            integration_constants = self._find_integration_constants(solution)
            
            # Solution properties
            solution_properties = self._analyze_solution_properties(solution)
            
            result = {
                'equation': equation,
                'dependent_variable': dependent_var,
                'independent_variable': independent_var,
                'solution': solution,
                'general_solution': general_solution,
                'solution_str': str(solution),
                'integration_constants': integration_constants,
                'properties': solution_properties,
                'success': True
            }
            
            logger.info(f"Differential equation solved successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error solving differential equation: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def vector_calculus_analysis(self, vector_field: Dict, variables: List[str]) -> Dict:
        """
        Analyze vector field (divergence, curl, etc.)
        
        Args:
            vector_field: Dictionary with vector components
            variables: List of variable names
            
        Returns:
            Dict with vector analysis results
        """
        try:
            logger.info("Analyzing vector field")
            
            # Define symbols
            vars_sym = [sp.symbols(var) for var in variables]
            
            # Create vector functions
            vector_functions = []
            for component_name, component_expr in vector_field.items():
                func = sp.sympify(component_expr)
                vector_functions.append(func)
            
            # Calculate divergence
            divergence = self._calculate_divergence(vector_functions, vars_sym)
            
            # Calculate curl (for 3D)
            curl = None
            if len(vector_functions) == 3 and len(vars_sym) == 3:
                curl = self._calculate_curl(vector_functions, vars_sym)
            
            # Calculate gradient of magnitude
            magnitude = sp.sqrt(sum(f**2 for f in vector_functions))
            gradient_magnitude = self._calculate_gradient(magnitude, vars_sym)
            
            # Check if conservative
            is_conservative = self._is_conservative_field(vector_functions, vars_sym)
            
            result = {
                'vector_field': vector_field,
                'variables': variables,
                'vector_functions': vector_functions,
                'divergence': divergence,
                'curl': curl,
                'magnitude': magnitude,
                'gradient_magnitude': gradient_magnitude,
                'is_conservative': is_conservative,
                'success': True
            }
            
            logger.info("Vector field analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"Error in vector calculus analysis: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def linear_algebra_operations(self, matrix_data: List[List[float]], 
                                operation: str) -> Dict:
        """
        Perform linear algebra operations
        
        Args:
            matrix_data: Matrix as list of lists
            operation: Operation to perform
            
        Returns:
            Dict with operation results
        """
        try:
            logger.info(f"Performing linear algebra operation: {operation}")
            
            # Create sympy matrix
            matrix = sp.Matrix(matrix_data)
            
            result = {'matrix': matrix, 'operation': operation}
            
            if operation == 'determinant':
                if matrix.is_square:
                    result['determinant'] = matrix.det()
                else:
                    raise ValueError("Matrix must be square for determinant")
            
            elif operation == 'inverse':
                if matrix.is_square:
                    det = matrix.det()
                    if det != 0:
                        result['inverse'] = matrix.inv()
                    else:
                        raise ValueError("Matrix is singular (determinant = 0)")
                else:
                    raise ValueError("Matrix must be square for inverse")
            
            elif operation == 'eigenvalues':
                if matrix.is_square:
                    eigenvals = matrix.eigenvals()
                    result['eigenvalues'] = eigenvals
                else:
                    raise ValueError("Matrix must be square for eigenvalues")
            
            elif operation == 'eigenvectors':
                if matrix.is_square:
                    eigenvects = matrix.eigenvects()
                    result['eigenvectors'] = eigenvects
                else:
                    raise ValueError("Matrix must be square for eigenvectors")
            
            elif operation == 'rank':
                result['rank'] = matrix.rank()
            
            elif operation == 'rref':
                result['rref'] = matrix.rref()
            
            elif operation == 'transpose':
                result['transpose'] = matrix.T
            
            elif operation == 'trace':
                if matrix.is_square:
                    result['trace'] = matrix.trace()
                else:
                    raise ValueError("Matrix must be square for trace")
            
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            result['success'] = True
            logger.info(f"Linear algebra operation {operation} completed")
            return result
            
        except Exception as e:
            logger.error(f"Error in linear algebra operation: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def _estimate_series_remainder(self, func: sp.Expr, var: sp.Symbol, 
                                point: float, order: int) -> str:
        """Estimate remainder term for Taylor series"""
        try:
            # Get (n+1)th derivative
            nth_derivative = sp.diff(func, var, order + 1)
            
            # Lagrange remainder form
            remainder = f"R_{order} = (f^({order + 1})(c) / {order + 1}!) * (x - {point})^{order + 1}"
            
            return remainder
            
        except Exception:
            return "Remainder estimation not available"
    
    def _estimate_convergence_radius(self, func: sp.Expr, var: sp.Symbol, 
                                   point: float) -> Optional[float]:
        """Estimate radius of convergence for power series"""
        try:
            # This is a simplified estimation
            # Full implementation would require more sophisticated analysis
            return None
            
        except Exception:
            return None
    
    def _extract_series_coefficients(self, polynomial: sp.Expr, var: sp.Symbol, 
                                  point: float) -> Dict:
        """Extract coefficients from Taylor polynomial"""
        try:
            coefficients = {}
            
            # Expand polynomial
            expanded = sp.expand(polynomial)
            
            # Extract coefficients
            for i in range(sp.degree(expanded, var) + 1):
                coeff = sp.expand(expanded).coeff(var, i)
                if coeff != 0:
                    coefficients[i] = coeff
            
            return coefficients
            
        except Exception as e:
            logger.error(f"Error extracting coefficients: {str(e)}")
            return {}
    
    def _calculate_fourier_coefficients(self, func: sp.Expr, var: sp.Symbol, 
                                       period: float, terms: int) -> Tuple[float, List[float], List[float]]:
        """Calculate Fourier series coefficients"""
        try:
            # This is a simplified implementation
            # Full implementation would require numerical integration
            
            # a0 coefficient (average value)
            a0 = (2/period) * sp.integrate(func, (var, 0, period))
            
            # an coefficients (cosine terms)
            an_coeffs = []
            for n in range(1, terms + 1):
                an = (2/period) * sp.integrate(func * sp.cos(2*sp.pi*n*var/period), (var, 0, period))
                an_coeffs.append(sp.simplify(an))
            
            # bn coefficients (sine terms)
            bn_coeffs = []
            for n in range(1, terms + 1):
                bn = (2/period) * sp.integrate(func * sp.sin(2*sp.pi*n*var/period), (var, 0, period))
                bn_coeffs.append(sp.simplify(bn))
            
            return a0, an_coeffs, bn_coeffs
            
        except Exception as e:
            logger.error(f"Error calculating Fourier coefficients: {str(e)}")
            return 0, [], []
    
    def _construct_fourier_series(self, a0: float, an_coeffs: List[float], 
                                bn_coeffs: List[float], var: sp.Symbol, 
                                period: float) -> str:
        """Construct Fourier series from coefficients"""
        try:
            series = f"{a0/2}"
            
            for n, (an, bn) in enumerate(zip(an_coeffs, bn_coeffs), 1):
                term_an = f" + {an} * cos({2*sp.pi*n}*var/{period})"
                term_bn = f" + {bn} * sin({2*sp.pi*n}*var/{period})"
                series += term_an + term_bn
            
            return series
            
        except Exception as e:
            logger.error(f"Error constructing Fourier series: {str(e)}")
            return "Fourier series construction failed"
    
    def _parseval_theorem_check(self, func: sp.Expr, a0: float, 
                               an_coeffs: List[float], bn_coeffs: List[float], 
                               period: float) -> str:
        """Check Parseval's theorem"""
        try:
            # Left side: (1/period) * integral of f^2
            left_side = (1/period) * sp.integrate(func**2, (var, 0, period))
            
            # Right side: a0^2/2 + sum(an^2 + bn^2)
            right_side = a0**2/2
            for an, bn in zip(an_coeffs, bn_coeffs):
                right_side += an**2 + bn**2
            
            return f"Parseval: {left_side} = {right_side}"
            
        except Exception:
            return "Parseval theorem check not available"
    
    def _determine_region_of_convergence(self, conditions) -> str:
        """Determine region of convergence from conditions"""
        try:
            if conditions:
                return str(conditions)
            else:
                return "All s > 0"
        except Exception:
            return "Unknown"
    
    def _analyze_transform_properties(self, original_func: sp.Expr, 
                                    transform_expr: sp.Expr) -> Dict:
        """Analyze properties of the transform"""
        try:
            properties = {}
            
            # Check if transform is rational
            if transform_expr.is_rational_function(sp.symbols('s')):
                properties['type'] = 'Rational transform'
            
            # Check for common transform patterns
            transform_str = str(transform_expr)
            if 'exp' in transform_str:
                properties['has_exponential'] = True
            
            if 's**' in transform_str:
                properties['has_poles'] = True
            
            return properties
            
        except Exception:
            return {}
    
    def _parse_differential_equation(self, equation: str, y_func, x_var) -> sp.Eq:
        """Parse differential equation string"""
        try:
            # This is a simplified parser
            # Full implementation would require more sophisticated parsing
            
            # Replace common notation
            eq_str = equation.replace("y'", f"diff({y_func(x)}, {x_var})")
            eq_str = eq_str.replace("y''", f"diff({y_func(x)}, {x_var}, 2)")
            eq_str = eq_str.replace("y", f"{y_func}(x)")
            
            # Parse as sympy expression
            parsed = sp.sympify(eq_str)
            
            # Convert to equation if not already
            if not isinstance(parsed, sp.Eq):
                parsed = sp.Eq(parsed, 0)
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing differential equation: {str(e)}")
            raise
    
    def _find_integration_constants(self, solution: sp.Expr) -> List[str]:
        """Find integration constants in solution"""
        try:
            constants = []
            solution_str = str(solution)
            
            # Look for C1, C2, etc.
            import re
            matches = re.findall(r'C\d+', solution_str)
            constants.extend(matches)
            
            return list(set(constants))
            
        except Exception:
            return []
    
    def _analyze_solution_properties(self, solution: sp.Expr) -> Dict:
        """Analyze properties of differential equation solution"""
        try:
            properties = {}
            
            solution_str = str(solution)
            
            # Check solution type
            if 'exp' in solution_str:
                properties['has_exponential'] = True
            
            if 'sin' in solution_str or 'cos' in solution_str:
                properties['has_trigonometric'] = True
            
            if 'log' in solution_str:
                properties['has_logarithm'] = True
            
            return properties
            
        except Exception:
            return {}
    
    def _calculate_divergence(self, vector_functions: List[sp.Expr], 
                           variables: List[sp.Symbol]) -> sp.Expr:
        """Calculate divergence of vector field"""
        try:
            divergence = 0
            for func, var in zip(vector_functions, variables):
                divergence += sp.diff(func, var)
            
            return sp.simplify(divergence)
            
        except Exception as e:
            logger.error(f"Error calculating divergence: {str(e)}")
            return sp.sympify("Error")
    
    def _calculate_curl(self, vector_functions: List[sp.Expr], 
                       variables: List[sp.Symbol]) -> List[sp.Expr]:
        """Calculate curl of 3D vector field"""
        try:
            if len(vector_functions) != 3 or len(variables) != 3:
                raise ValueError("Curl requires 3D vector field")
            
            Fx, Fy, Fz = vector_functions
            x, y, z = variables
            
            # Curl components
            curl_x = sp.diff(Fz, y) - sp.diff(Fy, z)
            curl_y = sp.diff(Fx, z) - sp.diff(Fz, x)
            curl_z = sp.diff(Fy, x) - sp.diff(Fx, y)
            
            return [sp.simplify(curl_x), sp.simplify(curl_y), sp.simplify(curl_z)]
            
        except Exception as e:
            logger.error(f"Error calculating curl: {str(e)}")
            return [sp.sympify("Error")] * 3
    
    def _calculate_gradient(self, scalar_func: sp.Expr, 
                          variables: List[sp.Symbol]) -> List[sp.Expr]:
        """Calculate gradient of scalar function"""
        try:
            gradient = []
            for var in variables:
                partial_derivative = sp.diff(scalar_func, var)
                gradient.append(sp.simplify(partial_derivative))
            
            return gradient
            
        except Exception as e:
            logger.error(f"Error calculating gradient: {str(e)}")
            return [sp.sympify("Error")] * len(variables)
    
    def _is_conservative_field(self, vector_functions: List[sp.Expr], 
                              variables: List[sp.Symbol]) -> bool:
        """Check if vector field is conservative"""
        try:
            # For 2D: check if partial derivatives match
            if len(vector_functions) == 2 and len(variables) == 2:
                Fx, Fy = vector_functions
                x, y = variables
                
                # Check if dFx/dy = dFy/dx
                dFx_dy = sp.diff(Fx, y)
                dFy_dx = sp.diff(Fy, x)
                
                return sp.simplify(dFx_dy - dFy_dx) == 0
            
            # For 3D: check if curl = 0
            elif len(vector_functions) == 3 and len(variables) == 3:
                curl = self._calculate_curl(vector_functions, variables)
                return all(component == 0 for component in curl)
            
            return False
            
        except Exception:
            return False


# Create singleton instance
advanced_mathematics = AdvancedMathematics()

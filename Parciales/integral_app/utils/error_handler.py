"""
Enhanced Error Handler for Plotting System
Provides intelligent error recovery and user-friendly error messages
"""
import logging
import traceback
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import sympy as sp

logger = logging.getLogger(__name__)


class PlottingErrorHandler:
    """Advanced error handling for plotting operations"""
    
    def __init__(self):
        """Initialize error handler"""
        self.error_patterns = {
            'ufunc.*isfinite': self._handle_ufunc_error,
            'division.*zero': self._handle_division_error,
            'domain.*error': self._handle_domain_error,
            'overflow': self._handle_overflow_error,
            'memory.*error': self._handle_memory_error,
            'value.*error': self._handle_value_error,
            'type.*error': self._handle_type_error,
            'attribute.*error': self._handle_attribute_error
        }
        
        self.recovery_strategies = {
            'reduce_range': self._reduce_plotting_range,
            'lower_resolution': self._lower_resolution,
            'simplify_function': self._simplify_function,
            'use_numeric': self._use_numeric_methods,
            'skip_problematic': self._skip_problematic_points
        }
    
    def handle_plotting_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float], context: Dict = None) -> Dict:
        """
        Handle plotting errors with intelligent recovery strategies
        
        Args:
            error: The exception that occurred
            func: SymPy expression being plotted
            var: Variable symbol
            x_range: Original plotting range
            context: Additional context information
            
        Returns:
            Dict with error analysis and recovery suggestions
        """
        try:
            error_info = {
                'original_error': error,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context or {},
                'recovery_attempts': [],
                'suggestions': [],
                'can_recover': False,
                'recovered_range': x_range,
                'recovered_resolution': 1000
            }
            
            # Analyze error pattern
            error_str = str(error).lower()
            matched_pattern = None
            
            for pattern, handler in self.error_patterns.items():
                if any(word in error_str for word in pattern.split('.*')):
                    matched_pattern = pattern
                    recovery_result = handler(error, func, var, x_range, context)
                    error_info.update(recovery_result)
                    break
            
            # If no pattern matched, use generic handler
            if not matched_pattern:
                recovery_result = self._handle_generic_error(error, func, var, x_range, context)
                error_info.update(recovery_result)
            
            # Log error analysis
            logger.info(f"Error analysis completed: {error_info['error_type']} - "
                        f"Can recover: {error_info['can_recover']}")
            
            return error_info
            
        except Exception as e:
            logger.error(f"Error in error handler: {str(e)}")
            return {
                'original_error': error,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'can_recover': False,
                'suggestions': ['Check function syntax', 'Use simpler expression', 'Reduce plotting range'],
                'recovered_range': x_range,
                'recovered_resolution': 500
            }
    
    def _handle_ufunc_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle ufunc 'isfinite' errors"""
        logger.info("Handling ufunc 'isfinite' error")
        
        recovery_attempts = []
        suggestions = []
        can_recover = True
        recovered_range = x_range
        recovered_resolution = 1000
        
        # Strategy 1: Reduce range
        if x_range[1] - x_range[0] > 10:
            new_range = (x_range[0] + 1, x_range[1] - 1)
            recovery_attempts.append(('reduce_range', new_range))
            recovered_range = new_range
            suggestions.append("Reduced plotting range to avoid problematic regions")
        
        # Strategy 2: Lower resolution
        if 1000 > 500:
            recovered_resolution = 500
            recovery_attempts.append(('lower_resolution', 500))
            suggestions.append("Lowered resolution to reduce computational load")
        
        # Strategy 3: Check for problematic functions
        func_str = str(func)
        problematic_funcs = ['log', 'ln', 'sqrt', 'tan', 'cot', 'sec', 'csc', '1/']
        
        for prob_func in problematic_funcs:
            if prob_func in func_str:
                suggestions.append(f"Function contains {prob_func} - check domain restrictions")
                break
        
        return {
            'recovery_attempts': recovery_attempts,
            'suggestions': suggestions,
            'can_recover': can_recover,
            'recovered_range': recovered_range,
            'recovered_resolution': recovered_resolution
        }
    
    def _handle_division_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                              x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle division by zero errors"""
        logger.info("Handling division by zero error")
        
        suggestions = ["Function has vertical asymptotes", "Avoid regions where denominator = 0"]
        
        # Try to find asymptotes
        try:
            denominator = sp.denom(func)
            if denominator != 1:
                zeros = sp.solve(denominator, var)
                asymptotes = []
                for zero in zeros:
                    try:
                        zero_val = float(zero.evalf())
                        if x_range[0] <= zero_val <= x_range[1]:
                            asymptotes.append(zero_val)
                    except:
                        continue
                
                if asymptotes:
                    suggestions.append(f"Vertical asymptotes detected at: {asymptotes}")
                    
                    # Create safe ranges
                    sorted_asymptotes = sorted(asymptotes)
                    safe_ranges = []
                    start = x_range[0]
                    
                    for asymptote in sorted_asymptotes:
                        if asymptote > start + 0.1:
                            safe_ranges.append((start, asymptote - 0.1))
                        start = asymptote + 0.1
                    
                    if start < x_range[1]:
                        safe_ranges.append((start, x_range[1]))
                    
                    if safe_ranges:
                        # Use the largest safe range
                        largest_range = max(safe_ranges, key=lambda r: r[1] - r[0])
                        return {
                            'recovery_attempts': [('skip_problematic', safe_ranges)],
                            'suggestions': suggestions + [f"Using safe range: {largest_range}"],
                            'can_recover': True,
                            'recovered_range': largest_range,
                            'recovered_resolution': 1000
                        }
        except:
            pass
        
        return {
            'recovery_attempts': [],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _handle_domain_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle domain errors"""
        logger.info("Handling domain error")
        
        func_str = str(func)
        suggestions = []
        
        if 'log' in func_str or 'ln' in func_str:
            suggestions.append("Logarithm argument must be positive")
        if 'sqrt' in func_str:
            suggestions.append("Square root argument must be non-negative")
        if 'asin' in func_str or 'acos' in func_str:
            suggestions.append("Arcsin/arccos argument must be in [-1, 1]")
        
        return {
            'recovery_attempts': [],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _handle_overflow_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                              x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle overflow errors"""
        logger.info("Handling overflow error")
        
        suggestions = ["Function values too large - reduce range or use logarithmic scale"]
        
        # Reduce range significantly
        range_center = (x_range[0] + x_range[1]) / 2
        new_range = (range_center - 2, range_center + 2)
        
        return {
            'recovery_attempts': [('reduce_range', new_range)],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': new_range,
            'recovered_resolution': 500
        }
    
    def _handle_memory_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle memory errors"""
        logger.info("Handling memory error")
        
        suggestions = ["Insufficient memory - using lower resolution"]
        
        return {
            'recovery_attempts': [('lower_resolution', 200)],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': x_range,
            'recovered_resolution': 200
        }
    
    def _handle_value_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle value errors"""
        logger.info("Handling value error")
        
        suggestions = ["Invalid function values - check function syntax"]
        
        return {
            'recovery_attempts': [],
            'suggestions': suggestions,
            'can_recover': False,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _handle_type_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle type errors"""
        logger.info("Handling type error")
        
        suggestions = ["Type conversion error - function may return non-numeric values"]
        
        return {
            'recovery_attempts': [('use_numeric', True)],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _handle_attribute_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                              x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle attribute errors"""
        logger.info("Handling attribute error")
        
        suggestions = ["Attribute error - check function syntax and imports"]
        
        return {
            'recovery_attempts': [],
            'suggestions': suggestions,
            'can_recover': False,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _handle_generic_error(self, error: Exception, func: sp.Expr, var: sp.Symbol, 
                             x_range: Tuple[float, float], context: Dict) -> Dict:
        """Handle generic errors"""
        logger.info("Handling generic error")
        
        suggestions = [
            "Unknown error occurred",
            "Try simplifying the function",
            "Reduce plotting range",
            "Check function syntax"
        ]
        
        return {
            'recovery_attempts': [('lower_resolution', 500)],
            'suggestions': suggestions,
            'can_recover': True,
            'recovered_range': x_range,
            'recovered_resolution': 500
        }
    
    def _reduce_plotting_range(self, current_range: Tuple[float, float]) -> Tuple[float, float]:
        """Reduce plotting range to avoid problematic regions"""
        range_width = current_range[1] - current_range[0]
        center = (current_range[0] + current_range[1]) / 2
        
        # Reduce range by 50%
        new_width = range_width * 0.5
        return (center - new_width/2, center + new_width/2)
    
    def _lower_resolution(self, current_resolution: int) -> int:
        """Lower plotting resolution"""
        return max(200, current_resolution // 2)
    
    def _simplify_function(self, func: sp.Expr) -> sp.Expr:
        """Simplify mathematical function"""
        try:
            return sp.simplify(func)
        except:
            return func
    
    def _use_numeric_methods(self, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> bool:
        """Switch to numerical methods"""
        return True
    
    def _skip_problematic_points(self, func: sp.Expr, var: sp.Symbol, 
                                x_range: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Identify and skip problematic points"""
        # This would need to be implemented based on specific function analysis
        return [x_range]
    
    def create_user_friendly_message(self, error_info: Dict) -> str:
        """Create user-friendly error message"""
        error_type = error_info['error_type']
        suggestions = error_info['suggestions']
        
        message = f"Error al graficar ({error_type}):\n\n"
        message += f"Detalles: {error_info['error_message']}\n\n"
        
        if suggestions:
            message += "Sugerencias:\n"
            for i, suggestion in enumerate(suggestions, 1):
                message += f"{i}. {suggestion}\n"
        
        if error_info['can_recover']:
            message += "\nIntentando recuperar automáticamente..."
        
        return message


# Create singleton instance
error_handler = PlottingErrorHandler()

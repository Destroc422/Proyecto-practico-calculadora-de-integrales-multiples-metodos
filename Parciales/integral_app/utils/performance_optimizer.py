"""
Performance Optimizer for Plotting System
Optimizes rendering performance with adaptive resolution and caching
"""
import logging
import time
import functools
from typing import Dict, List, Tuple, Optional, Any, Callable
import numpy as np
import sympy as sp
import threading
from concurrent.futures import ThreadPoolExecutor
import hashlib

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """Advanced performance optimization for plotting operations"""
    
    def __init__(self):
        """Initialize performance optimizer"""
        self.cache = {}
        self.cache_max_size = 100
        self.performance_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_plots': 0,
            'average_render_time': 0.0,
            'optimization_suggestions': []
        }
        
        # Function complexity analysis
        self.complexity_weights = {
            'simple': 1.0,      # Linear, constant functions
            'moderate': 0.7,    # Quadratic, cubic, basic trig
            'complex': 0.5,     # Higher degree, composite functions
            'very_complex': 0.3  # Nested, special functions
        }
        
        # Adaptive resolution settings
        self.base_resolution = 1000
        self.min_resolution = 200
        self.max_resolution = 2000
        
        # Threading pool for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def optimize_plotting_params(self, func: sp.Expr, var: sp.Symbol, 
                               x_range: Tuple[float, float], 
                               quality: str = 'auto') -> Dict:
        """
        Optimize plotting parameters based on function complexity and range
        
        Args:
            func: SymPy expression
            var: Variable symbol
            x_range: Plotting range
            quality: Quality setting ('low', 'medium', 'high', 'auto')
            
        Returns:
            Dict with optimized parameters
        """
        try:
            # Analyze function complexity
            complexity = self._analyze_function_complexity(func)
            
            # Determine optimal resolution
            if quality == 'auto':
                resolution = self._calculate_optimal_resolution(func, x_range, complexity)
            else:
                resolution = self._get_quality_based_resolution(quality)
            
            # Determine optimal point distribution
            point_distribution = self._optimize_point_distribution(x_range, complexity)
            
            # Check if caching is beneficial
            use_cache = self._should_use_cache(func, x_range, resolution)
            
            # Calculate estimated render time
            estimated_time = self._estimate_render_time(complexity, resolution, x_range)
            
            params = {
                'resolution': resolution,
                'point_distribution': point_distribution,
                'use_cache': use_cache,
                'complexity': complexity,
                'estimated_time': estimated_time,
                'optimization_applied': True,
                'suggestions': self._generate_optimization_suggestions(complexity, x_range)
            }
            
            logger.info(f"Optimized plotting parameters: resolution={resolution}, "
                       f"complexity={complexity}, estimated_time={estimated_time:.3f}s")
            
            return params
            
        except Exception as e:
            logger.error(f"Error in performance optimization: {str(e)}")
            # Return default parameters
            return {
                'resolution': self.base_resolution,
                'point_distribution': 'uniform',
                'use_cache': False,
                'complexity': 'moderate',
                'estimated_time': 0.1,
                'optimization_applied': False,
                'suggestions': ['Using default parameters due to optimization error']
            }
    
    def _analyze_function_complexity(self, func: sp.Expr) -> str:
        """Analyze function complexity"""
        try:
            func_str = str(func)
            
            # Count operations
            operation_count = 0
            operation_count += func_str.count('+') + func_str.count('-')
            operation_count += func_str.count('*') + func_str.count('/')
            operation_count += func_str.count('**')
            
            # Count special functions
            special_functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'asin', 'acos', 'atan']
            special_count = sum(func_str.count(func) for func in special_functions)
            
            # Check for nested functions
            nesting_level = func_str.count('(')
            
            # Check for powers
            power_count = func_str.count('**')
            
            # Determine complexity
            complexity_score = (
                operation_count * 1.0 +
                special_functions * 2.0 +
                nesting_level * 1.5 +
                power_count * 1.5
            )
            
            if complexity_score <= 3:
                return 'simple'
            elif complexity_score <= 8:
                return 'moderate'
            elif complexity_score <= 15:
                return 'complex'
            else:
                return 'very_complex'
                
        except Exception as e:
            logger.warning(f"Error analyzing function complexity: {str(e)}")
            return 'moderate'
    
    def _calculate_optimal_resolution(self, func: sp.Expr, x_range: Tuple[float, float], 
                                   complexity: str) -> int:
        """Calculate optimal resolution based on function and range"""
        try:
            range_width = x_range[1] - x_range[0]
            
            # Base resolution adjusted by range
            if range_width <= 1:
                base_res = 800
            elif range_width <= 5:
                base_res = 1000
            elif range_width <= 20:
                base_res = 1200
            else:
                base_res = 1500
            
            # Adjust by complexity
            complexity_factor = self.complexity_weights.get(complexity, 0.7)
            optimal_resolution = int(base_res * complexity_factor)
            
            # Ensure within bounds
            optimal_resolution = max(self.min_resolution, min(self.max_resolution, optimal_resolution))
            
            return optimal_resolution
            
        except Exception as e:
            logger.warning(f"Error calculating optimal resolution: {str(e)}")
            return self.base_resolution
    
    def _get_quality_based_resolution(self, quality: str) -> int:
        """Get resolution based on quality setting"""
        quality_map = {
            'low': self.min_resolution,
            'medium': int((self.min_resolution + self.base_resolution) / 2),
            'high': self.base_resolution,
            'ultra': self.max_resolution
        }
        return quality_map.get(quality, self.base_resolution)
    
    def _optimize_point_distribution(self, x_range: Tuple[float, float], 
                                    complexity: str) -> str:
        """Optimize point distribution strategy"""
        range_width = x_range[1] - x_range[0]
        
        if complexity == 'simple' and range_width <= 10:
            return 'uniform'  # Simple functions need uniform distribution
        elif complexity in ['complex', 'very_complex']:
            return 'adaptive'  # Complex functions need adaptive distribution
        elif range_width > 50:
            return 'logarithmic'  # Large ranges benefit from logarithmic distribution
        else:
            return 'uniform'
    
    def _should_use_cache(self, func: sp.Expr, x_range: Tuple[float, float], 
                         resolution: int) -> bool:
        """Determine if caching should be used"""
        # Cache if function is complex and resolution is high
        complexity = self._analyze_function_complexity(func)
        return complexity in ['complex', 'very_complex'] and resolution >= 800
    
    def _estimate_render_time(self, complexity: str, resolution: int, 
                             x_range: Tuple[float, float]) -> float:
        """Estimate render time in seconds"""
        try:
            # Base time per point
            complexity_factor = {'simple': 0.0001, 'moderate': 0.0002, 
                               'complex': 0.0005, 'very_complex': 0.001}
            
            base_time_per_point = complexity_factor.get(complexity, 0.0002)
            range_factor = min(2.0, (x_range[1] - x_range[0]) / 10.0)
            
            estimated_time = resolution * base_time_per_point * range_factor
            return estimated_time
            
        except Exception as e:
            logger.warning(f"Error estimating render time: {str(e)}")
            return 0.1
    
    def _generate_optimization_suggestions(self, complexity: str, 
                                         x_range: Tuple[float, float]) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []
        
        if complexity == 'very_complex':
            suggestions.append("Consider using lower resolution for faster rendering")
            suggestions.append("Function is very complex - caching enabled")
        
        range_width = x_range[1] - x_range[0]
        if range_width > 100:
            suggestions.append("Large range detected - consider logarithmic distribution")
        elif range_width < 0.1:
            suggestions.append("Very small range - higher resolution recommended")
        
        return suggestions
    
    def generate_adaptive_points(self, x_range: Tuple[float, float], 
                                resolution: int, 
                                distribution: str = 'uniform') -> np.ndarray:
        """Generate adaptive point distribution"""
        try:
            if distribution == 'uniform':
                return np.linspace(x_range[0], x_range[1], resolution)
            
            elif distribution == 'adaptive':
                # More points in regions where function might change rapidly
                center = (x_range[0] + x_range[1]) / 2
                # Use cosine distribution for more points in center
                t = np.linspace(0, np.pi, resolution)
                scale = (x_range[1] - x_range[0]) / 2
                return center + scale * np.cos(t)
            
            elif distribution == 'logarithmic':
                # Logarithmic distribution for large ranges
                if x_range[0] <= 0:
                    # Can't use log with negative or zero start
                    return np.linspace(x_range[0], x_range[1], resolution)
                
                log_start = np.log10(max(x_range[0], 0.001))
                log_end = np.log10(x_range[1])
                log_points = np.linspace(log_start, log_end, resolution)
                return 10 ** log_points
            
            else:
                return np.linspace(x_range[0], x_range[1], resolution)
                
        except Exception as e:
            logger.warning(f"Error generating adaptive points: {str(e)}")
            return np.linspace(x_range[0], x_range[1], resolution)
    
    def get_cache_key(self, func: sp.Expr, var: sp.Symbol, 
                     x_range: Tuple[float, float], resolution: int) -> str:
        """Generate cache key for function evaluation"""
        try:
            # Create unique hash
            func_str = str(func)
            var_str = str(var)
            range_str = f"{x_range[0]:.6f}_{x_range[1]:.6f}_{resolution}"
            
            combined = f"{func_str}_{var_str}_{range_str}"
            return hashlib.md5(combined.encode()).hexdigest()
            
        except Exception as e:
            logger.warning(f"Error generating cache key: {str(e)}")
            return f"fallback_{time.time()}"
    
    def cache_function_evaluation(self, cache_key: str, x_values: np.ndarray, 
                                y_values: np.ndarray):
        """Cache function evaluation results"""
        try:
            # Check cache size
            if len(self.cache) >= self.cache_max_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            
            # Store in cache
            self.cache[cache_key] = {
                'x_values': x_values,
                'y_values': y_values,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.warning(f"Error caching function evaluation: {str(e)}")
    
    def get_cached_evaluation(self, cache_key: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """Get cached function evaluation"""
        try:
            if cache_key in self.cache:
                self.performance_stats['cache_hits'] += 1
                cached_data = self.cache[cache_key]
                return cached_data['x_values'], cached_data['y_values']
            else:
                self.performance_stats['cache_misses'] += 1
                return None
                
        except Exception as e:
            logger.warning(f"Error getting cached evaluation: {str(e)}")
            return None
    
    def evaluate_function_optimized(self, func: sp.Expr, var: sp.Symbol, 
                                  x_values: np.ndarray, 
                                  use_cache: bool = True) -> np.ndarray:
        """Optimized function evaluation with caching"""
        try:
            # Check cache first
            if use_cache:
                cache_key = self.get_cache_key(func, var, (x_values[0], x_values[-1]), len(x_values))
                cached_result = self.get_cached_evaluation(cache_key)
                
                if cached_result is not None:
                    cached_x, cached_y = cached_result
                    # Check if x values match (within tolerance)
                    if np.allclose(cached_x, x_values, rtol=1e-6):
                        return cached_y
            
            # Evaluate function
            start_time = time.time()
            f = sp.lambdify(var, func, 'numpy')
            y_values = f(x_values)
            evaluation_time = time.time() - start_time
            
            # Cache result if beneficial
            if use_cache and evaluation_time > 0.01:  # Only cache if evaluation took time
                self.cache_function_evaluation(cache_key, x_values, y_values)
            
            # Update stats
            self.performance_stats['total_plots'] += 1
            self._update_average_render_time(evaluation_time)
            
            return y_values
            
        except Exception as e:
            logger.error(f"Error in optimized function evaluation: {str(e)}")
            # Fallback to basic evaluation
            f = sp.lambdify(var, func, 'numpy')
            return f(x_values)
    
    def _update_average_render_time(self, render_time: float):
        """Update average render time statistics"""
        current_avg = self.performance_stats['average_render_time']
        total_plots = self.performance_stats['total_plots']
        
        if total_plots == 1:
            self.performance_stats['average_render_time'] = render_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.performance_stats['average_render_time'] = (
                alpha * render_time + (1 - alpha) * current_avg
            )
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        cache_hit_rate = 0.0
        if self.performance_stats['cache_hits'] + self.performance_stats['cache_misses'] > 0:
            total_cache_requests = (self.performance_stats['cache_hits'] + 
                                  self.performance_stats['cache_misses'])
            cache_hit_rate = self.performance_stats['cache_hits'] / total_cache_requests
        
        return {
            **self.performance_stats,
            'cache_hit_rate': cache_hit_rate,
            'cache_size': len(self.cache),
            'cache_efficiency': 'Good' if cache_hit_rate > 0.5 else 'Needs improvement'
        }
    
    def clear_cache(self):
        """Clear performance cache"""
        self.cache.clear()
        logger.info("Performance cache cleared")
    
    def optimize_for_memory(self, array_size: int) -> bool:
        """Check if memory optimization is needed"""
        # Simple heuristic: if array is larger than 10MB, optimize
        array_memory_mb = array_size * 8 / (1024 * 1024)  # Assuming float64
        return array_memory_mb > 10


# Create singleton instance
performance_optimizer = PerformanceOptimizer()


def cache_function_results(maxsize: int = 128):
    """Decorator for caching function results"""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                return cache[key]
            
            # Compute and cache result
            result = func(*args, **kwargs)
            
            # Manage cache size
            if len(cache) >= maxsize:
                # Remove oldest entry
                oldest_key = next(iter(cache))
                del cache[oldest_key]
            
            cache[key] = result
            return result
        
        return wrapper
    return decorator

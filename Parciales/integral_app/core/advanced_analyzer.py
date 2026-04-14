"""
Advanced Mathematical Function Analyzer
Comprehensive analysis of mathematical functions with detailed properties
"""
import sympy as sp
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
import math

logger = logging.getLogger(__name__)


class AdvancedFunctionAnalyzer:
    """Advanced analyzer for mathematical function properties"""
    
    def __init__(self):
        """Initialize advanced analyzer"""
        self.analysis_cache = {}
        self.numerical_tolerance = 1e-10
        
    def analyze_function_comprehensive(self, func: sp.Expr, var: sp.Symbol, 
                                     x_range: Tuple[float, float]) -> Dict:
        """
        Perform comprehensive analysis of mathematical function
        
        Args:
            func: SymPy expression to analyze
            var: Variable symbol
            x_range: Analysis range
            
        Returns:
            Dict with comprehensive analysis results
        """
        try:
            analysis_id = f"{str(func)}_{var}_{x_range}"
            
            # Check cache
            if analysis_id in self.analysis_cache:
                logger.info("Using cached analysis results")
                return self.analysis_cache[analysis_id]
            
            logger.info(f"Starting comprehensive analysis of {func}")
            
            result = {
                'function': func,
                'variable': var,
                'range': x_range,
                'domain_analysis': self._analyze_domain(func, var, x_range),
                'critical_points': self._find_critical_points(func, var, x_range),
                'extrema': self._find_extrema(func, var, x_range),
                'monotonicity': self._analyze_monotonicity(func, var, x_range),
                'concavity': self._analyze_concavity(func, var, x_range),
                'asymptotes': self._find_asymptotes(func, var, x_range),
                'symmetry': self._analyze_symmetry(func, var),
                'periodicity': self._analyze_periodicity(func, var),
                'intersections': self._find_intersections(func, var, x_range),
                'behavior_at_bounds': self._analyze_behavior_at_bounds(func, var, x_range),
                'special_points': self._find_special_points(func, var, x_range),
                'function_properties': self._determine_function_properties(func, var),
                'numerical_summary': self._generate_numerical_summary(func, var, x_range)
            }
            
            # Cache results
            self.analysis_cache[analysis_id] = result
            
            logger.info(f"Comprehensive analysis completed for {func}")
            return result
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            return {
                'function': func,
                'variable': var,
                'range': x_range,
                'error': str(e),
                'analysis_completed': False
            }
    
    def _analyze_domain(self, func: sp.Expr, var: sp.Symbol, 
                       x_range: Tuple[float, float]) -> Dict:
        """Analyze function domain restrictions"""
        try:
            domain_info = {
                'domain_type': 'all_real',
                'restrictions': [],
                'problematic_points': [],
                'safe_intervals': [x_range],
                'domain_description': 'All real numbers'
            }
            
            func_str = str(func)
            
            # Check for logarithms
            if 'log' in func_str or 'ln' in func_str:
                domain_info['restrictions'].append('logarithm: argument > 0')
                domain_info['domain_type'] = 'restricted'
                
                # Find where log argument <= 0
                # This is simplified - full analysis would require solving inequalities
                domain_info['problematic_points'].append('logarithm_boundary')
            
            # Check for square roots
            if 'sqrt' in func_str or '**(1/2)' in func_str:
                domain_info['restrictions'].append('square_root: argument >= 0')
                domain_info['domain_type'] = 'restricted'
                domain_info['problematic_points'].append('sqrt_boundary')
            
            # Check for rational expressions
            if '/' in func_str:
                domain_info['restrictions'].append('denominator != 0')
                domain_info['domain_type'] = 'restricted'
                
                # Find denominator zeros
                try:
                    denominator = sp.denom(func)
                    if denominator != 1:
                        zeros = sp.solve(denominator, var)
                        for zero in zeros:
                            try:
                                zero_val = float(zero.evalf())
                                if x_range[0] <= zero_val <= x_range[1]:
                                    domain_info['problematic_points'].append(zero_val)
                            except:
                                continue
                except:
                    pass
            
            # Check for trigonometric restrictions
            trig_restrictions = {
                'asin': 'argument in [-1, 1]',
                'acos': 'argument in [-1, 1]',
                'atan': 'no restrictions'
            }
            
            for trig_func, restriction in trig_restrictions.items():
                if trig_func in func_str:
                    domain_info['restrictions'].append(f'{trig_func}: {restriction}')
                    if restriction != 'no restrictions':
                        domain_info['domain_type'] = 'restricted'
            
            # Generate domain description
            if domain_info['domain_type'] == 'all_real':
                domain_info['domain_description'] = 'All real numbers'
            else:
                domain_info['domain_description'] = f'Restricted: {", ".join(domain_info["restrictions"])}'
            
            return domain_info
            
        except Exception as e:
            logger.error(f"Error analyzing domain: {str(e)}")
            return {'domain_type': 'unknown', 'error': str(e)}
    
    def _find_critical_points(self, func: sp.Expr, var: sp.Symbol, 
                             x_range: Tuple[float, float]) -> Dict:
        """Find critical points (where derivative = 0 or undefined)"""
        try:
            critical_points = {
                'points': [],
                'types': [],  # 'stationary', 'singular'
                'coordinates': [],
                'analysis': []
            }
            
            # Find first derivative
            try:
                derivative = sp.diff(func, var)
                
                # Solve derivative = 0
                solutions = sp.solve(derivative, var)
                
                for solution in solutions:
                    try:
                        point_val = float(solution.evalf())
                        if x_range[0] <= point_val <= x_range[1]:
                            # Calculate function value at critical point
                            func_val = func.subs(var, point_val)
                            func_val_num = float(func_val.evalf())
                            
                            critical_points['points'].append(point_val)
                            critical_points['coordinates'].append((point_val, func_val_num))
                            critical_points['types'].append('stationary')
                            
                            # Classify critical point
                            classification = self._classify_critical_point(func, var, point_val)
                            critical_points['analysis'].append(classification)
                            
                    except (ValueError, TypeError, ZeroDivisionError):
                        continue
                        
            except Exception as e:
                logger.warning(f"Error finding critical points: {str(e)}")
            
            # Find points where derivative is undefined (singular points)
            try:
                derivative = sp.diff(func, var)
                denominator = sp.denom(derivative)
                
                if denominator != 1:
                    singular_solutions = sp.solve(denominator, var)
                    for solution in singular_solutions:
                        try:
                            point_val = float(solution.evalf())
                            if x_range[0] <= point_val <= x_range[1]:
                                critical_points['points'].append(point_val)
                                critical_points['types'].append('singular')
                                critical_points['analysis'].append('Derivative undefined')
                        except:
                            continue
                            
            except Exception as e:
                logger.warning(f"Error finding singular points: {str(e)}")
            
            # Sort points
            sorted_data = sorted(zip(critical_points['points'], 
                                   critical_points['coordinates'], 
                                   critical_points['types'], 
                                   critical_points['analysis']))
            
            if sorted_data:
                critical_points['points'], critical_points['coordinates'], \
                critical_points['types'], critical_points['analysis'] = zip(*sorted_data)
            
            return critical_points
            
        except Exception as e:
            logger.error(f"Error finding critical points: {str(e)}")
            return {'points': [], 'error': str(e)}
    
    def _classify_critical_point(self, func: sp.Expr, var: sp.Symbol, 
                                point: float) -> str:
        """Classify critical point using second derivative test"""
        try:
            # Second derivative
            second_derivative = sp.diff(func, var, 2)
            second_val = second_derivative.subs(var, point)
            second_num = float(second_val.evalf())
            
            if abs(second_num) < self.numerical_tolerance:
                return 'inconclusive - higher order test needed'
            elif second_num > 0:
                return 'local minimum'
            else:
                return 'local maximum'
                
        except Exception as e:
            return f'classification error: {str(e)}'
    
    def _find_extrema(self, func: sp.Expr, var: sp.Symbol, 
                      x_range: Tuple[float, float]) -> Dict:
        """Find local and global extrema"""
        try:
            extrema = {
                'local_minima': [],
                'local_maxima': [],
                'global_minimum': None,
                'global_maximum': None,
                'absolute_extrema': []
            }
            
            # Get critical points
            critical_analysis = self._find_critical_points(func, var, x_range)
            
            for i, point in enumerate(critical_analysis['points']):
                classification = critical_analysis['analysis'][i]
                coord = critical_analysis['coordinates'][i]
                
                if 'minimum' in classification.lower():
                    extrema['local_minima'].append(coord)
                elif 'maximum' in classification.lower():
                    extrema['local_maxima'].append(coord)
            
            # Check endpoints for absolute extrema
            try:
                left_val = func.subs(var, x_range[0])
                right_val = func.subs(var, x_range[1])
                
                left_num = float(left_val.evalf())
                right_num = float(right_val.evalf())
                
                endpoint_values = [(x_range[0], left_num), (x_range[1], right_num)]
                
                # Include critical points
                all_points = endpoint_values + list(critical_analysis['coordinates'])
                
                if all_points:
                    # Find global minimum and maximum
                    global_min = min(all_points, key=lambda p: p[1])
                    global_max = max(all_points, key=lambda p: p[1])
                    
                    extrema['global_minimum'] = global_min
                    extrema['global_maximum'] = global_max
                    extrema['absolute_extrema'] = [global_min, global_max]
                    
            except Exception as e:
                logger.warning(f"Error finding absolute extrema: {str(e)}")
            
            return extrema
            
        except Exception as e:
            logger.error(f"Error finding extrema: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_monotonicity(self, func: sp.Expr, var: sp.Symbol, 
                             x_range: Tuple[float, float]) -> Dict:
        """Analyze monotonicity (increasing/decreasing intervals)"""
        try:
            monotonicity = {
                'intervals': [],
                'increasing_intervals': [],
                'decreasing_intervals': [],
                'constant_intervals': [],
                'monotonic_type': 'neither'
            }
            
            # First derivative
            derivative = sp.diff(func, var)
            
            # Sample points to determine monotonicity
            sample_points = np.linspace(x_range[0], x_range[1], 50)
            
            current_interval = [x_range[0]]
            current_trend = None
            
            for i in range(1, len(sample_points)):
                x_val = sample_points[i]
                
                try:
                    deriv_val = derivative.subs(var, x_val)
                    deriv_num = float(deriv_val.evalf())
                    
                    # Determine trend
                    if abs(deriv_num) < self.numerical_tolerance:
                        trend = 'constant'
                    elif deriv_num > 0:
                        trend = 'increasing'
                    else:
                        trend = 'decreasing'
                    
                    # Check if trend changed
                    if current_trend is None:
                        current_trend = trend
                    elif trend != current_trend:
                        # Trend changed, close current interval
                        current_interval.append(x_val)
                        
                        interval_info = {
                            'start': current_interval[0],
                            'end': current_interval[1],
                            'trend': current_trend
                        }
                        monotonicity['intervals'].append(interval_info)
                        
                        if current_trend == 'increasing':
                            monotonicity['increasing_intervals'].append((current_interval[0], current_interval[1]))
                        elif current_trend == 'decreasing':
                            monotonicity['decreasing_intervals'].append((current_interval[0], current_interval[1]))
                        else:
                            monotonicity['constant_intervals'].append((current_interval[0], current_interval[1]))
                        
                        # Start new interval
                        current_interval = [x_val]
                        current_trend = trend
                        
                except (ValueError, TypeError, ZeroDivisionError):
                    # Skip problematic points
                    continue
            
            # Close final interval
            if len(current_interval) > 1:
                current_interval.append(x_range[1])
                
                interval_info = {
                    'start': current_interval[0],
                    'end': current_interval[1],
                    'trend': current_trend
                }
                monotonicity['intervals'].append(interval_info)
                
                if current_trend == 'increasing':
                    monotonicity['increasing_intervals'].append((current_interval[0], current_interval[1]))
                elif current_trend == 'decreasing':
                    monotonicity['decreasing_intervals'].append((current_interval[0], current_interval[1]))
                else:
                    monotonicity['constant_intervals'].append((current_interval[0], current_interval[1]))
            
            # Determine overall monotonicity
            if len(monotonicity['increasing_intervals']) > 0 and len(monotonicity['decreasing_intervals']) == 0:
                monotonicity['monotonic_type'] = 'increasing'
            elif len(monotonicity['decreasing_intervals']) > 0 and len(monotonicity['increasing_intervals']) == 0:
                monotonicity['monotonic_type'] = 'decreasing'
            elif len(monotonicity['constant_intervals']) > 0 and len(monotonicity['intervals']) == 1:
                monotonicity['monotonic_type'] = 'constant'
            else:
                monotonicity['monotonic_type'] = 'neither'
            
            return monotonicity
            
        except Exception as e:
            logger.error(f"Error analyzing monotonicity: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_concavity(self, func: sp.Expr, var: sp.Symbol, 
                          x_range: Tuple[float, float]) -> Dict:
        """Analyze concavity (concave up/down intervals)"""
        try:
            concavity = {
                'intervals': [],
                'concave_up_intervals': [],
                'concave_down_intervals': [],
                'inflection_points': [],
                'inflection_coordinates': []
            }
            
            # Second derivative
            second_derivative = sp.diff(func, var, 2)
            
            # Sample points to determine concavity
            sample_points = np.linspace(x_range[0], x_range[1], 50)
            
            current_interval = [x_range[0]]
            current_concavity = None
            
            for i in range(1, len(sample_points)):
                x_val = sample_points[i]
                
                try:
                    second_val = second_derivative.subs(var, x_val)
                    second_num = float(second_val.evalf())
                    
                    # Determine concavity
                    if abs(second_num) < self.numerical_tolerance:
                        concavity_type = 'linear'
                    elif second_num > 0:
                        concavity_type = 'concave_up'
                    else:
                        concavity_type = 'concave_down'
                    
                    # Check if concavity changed
                    if current_concavity is None:
                        current_concavity = concavity_type
                    elif concavity_type != current_concavity:
                        # Concavity changed, close current interval
                        current_interval.append(x_val)
                        
                        interval_info = {
                            'start': current_interval[0],
                            'end': current_interval[1],
                            'concavity': current_concavity
                        }
                        concavity['intervals'].append(interval_info)
                        
                        if current_concavity == 'concave_up':
                            concavity['concave_up_intervals'].append((current_interval[0], current_interval[1]))
                        elif current_concavity == 'concave_down':
                            concavity['concave_down_intervals'].append((current_interval[0], current_interval[1]))
                        
                        # Potential inflection point
                        if current_concavity != 'linear' and concavity_type != 'linear':
                            concavity['inflection_points'].append(x_val)
                            
                            # Calculate function value at inflection point
                            func_val = func.subs(var, x_val)
                            func_num = float(func_val.evalf())
                            concavity['inflection_coordinates'].append((x_val, func_num))
                        
                        # Start new interval
                        current_interval = [x_val]
                        current_concavity = concavity_type
                        
                except (ValueError, TypeError, ZeroDivisionError):
                    # Skip problematic points
                    continue
            
            # Close final interval
            if len(current_interval) > 1:
                current_interval.append(x_range[1])
                
                interval_info = {
                    'start': current_interval[0],
                    'end': current_interval[1],
                    'concavity': current_concavity
                }
                concavity['intervals'].append(interval_info)
                
                if current_concavity == 'concave_up':
                    concavity['concave_up_intervals'].append((current_interval[0], current_interval[1]))
                elif current_concavity == 'concave_down':
                    concavity['concave_down_intervals'].append((current_interval[0], current_interval[1]))
            
            return concavity
            
        except Exception as e:
            logger.error(f"Error analyzing concavity: {str(e)}")
            return {'error': str(e)}
    
    def _find_asymptotes(self, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
        """Find asymptotes (vertical, horizontal, oblique)"""
        try:
            asymptotes = {
                'vertical': [],
                'horizontal': [],
                'oblique': [],
                'slant': []
            }
            
            # Vertical asymptotes (denominator = 0)
            try:
                denominator = sp.denom(func)
                if denominator != 1:
                    zeros = sp.solve(denominator, var)
                    for zero in zeros:
                        try:
                            zero_val = float(zero.evalf())
                            if x_range[0] <= zero_val <= x_range[1]:
                                asymptotes['vertical'].append({
                                    'x': zero_val,
                                    'type': 'vertical',
                                    'equation': f'x = {zero_val:.6f}'
                                })
                        except:
                            continue
            except:
                pass
            
            # Horizontal asymptotes (limit as x -> ±infinity)
            try:
                # Limit as x -> infinity
                limit_inf = sp.limit(func, var, sp.oo)
                if limit_inf.is_finite():
                    limit_val = float(limit_inf.evalf())
                    asymptotes['horizontal'].append({
                        'y': limit_val,
                        'type': 'horizontal',
                        'equation': f'y = {limit_val:.6f}',
                        'direction': '+infinity'
                    })
                
                # Limit as x -> -infinity
                limit_neg_inf = sp.limit(func, var, -sp.oo)
                if limit_neg_inf.is_finite():
                    limit_val = float(limit_neg_inf.evalf())
                    asymptotes['horizontal'].append({
                        'y': limit_val,
                        'type': 'horizontal',
                        'equation': f'y = {limit_val:.6f}',
                        'direction': '-infinity'
                    })
                    
            except:
                pass
            
            # Oblique/slant asymptotes (for rational functions)
            try:
                # Check if it's a rational function
                if func.is_Mul or func.is_Add:
                    # Simplified check - full analysis would require polynomial division
                    degree_num = self._get_polynomial_degree(sp.simplify(sp.together(func).as_numer_denom()[0]), var)
                    degree_den = self._get_polynomial_degree(sp.simplify(sp.together(func).as_numer_denom()[1]), var)
                    
                    if degree_num == degree_den + 1:
                        # Potential slant asymptote
                        asymptotes['slant'].append({
                            'type': 'slant',
                            'note': 'Potential slant asymptote detected'
                        })
                        
            except:
                pass
            
            return asymptotes
            
        except Exception as e:
            logger.error(f"Error finding asymptotes: {str(e)}")
            return {'error': str(e)}
    
    def _get_polynomial_degree(self, expr: sp.Expr, var: sp.Symbol) -> int:
        """Get polynomial degree of expression"""
        try:
            return sp.degree(expr, var)
        except:
            return 0
    
    def _analyze_symmetry(self, func: sp.Expr, var: sp.Symbol) -> Dict:
        """Analyze function symmetry (even, odd, periodic)"""
        try:
            symmetry = {
                'is_even': False,
                'is_odd': False,
                'symmetry_type': 'none',
                'symmetry_description': 'No symmetry detected'
            }
            
            # Test for even function: f(-x) = f(x)
            try:
                func_neg = func.subs(var, -var)
                func_neg_simplified = sp.simplify(func_neg)
                
                if sp.simplify(func_neg_simplified - func) == 0:
                    symmetry['is_even'] = True
                    symmetry['symmetry_type'] = 'even'
                    symmetry['symmetry_description'] = 'Even function: f(-x) = f(x)'
                    
            except:
                pass
            
            # Test for odd function: f(-x) = -f(x)
            if not symmetry['is_even']:
                try:
                    func_neg = func.subs(var, -var)
                    func_neg_simplified = sp.simplify(func_neg)
                    
                    if sp.simplify(func_neg_simplified + func) == 0:
                        symmetry['is_odd'] = True
                        symmetry['symmetry_type'] = 'odd'
                        symmetry['symmetry_description'] = 'Odd function: f(-x) = -f(x)'
                        
                except:
                    pass
            
            return symmetry
            
        except Exception as e:
            logger.error(f"Error analyzing symmetry: {str(e)}")
            return {'symmetry_type': 'unknown', 'error': str(e)}
    
    def _analyze_periodicity(self, func: sp.Expr, var: sp.Symbol) -> Dict:
        """Analyze periodicity"""
        try:
            periodicity = {
                'is_periodic': False,
                'period': None,
                'fundamental_period': None,
                'periodicity_type': 'non_periodic'
            }
            
            func_str = str(func)
            
            # Check for common periodic functions
            periodic_functions = {
                'sin': (2 * np.pi, 'Trigonometric'),
                'cos': (2 * np.pi, 'Trigonometric'),
                'tan': (np.pi, 'Trigonometric'),
                'cot': (np.pi, 'Trigonometric'),
                'sec': (2 * np.pi, 'Trigonometric'),
                'csc': (2 * np.pi, 'Trigonometric')
            }
            
            for func_name, (period, ptype) in periodic_functions.items():
                if func_name in func_str:
                    periodicity['is_periodic'] = True
                    periodicity['period'] = period
                    periodicity['fundamental_period'] = period
                    periodicity['periodicity_type'] = ptype
                    periodicity['description'] = f'{ptype} function with period {period:.6f}'
                    break
            
            return periodicity
            
        except Exception as e:
            logger.error(f"Error analyzing periodicity: {str(e)}")
            return {'periodicity_type': 'unknown', 'error': str(e)}
    
    def _find_intersections(self, func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> Dict:
        """Find intersections with axes"""
        try:
            intersections = {
                'x_intercepts': [],  # f(x) = 0
                'y_intercept': None,  # f(0)
                'origin': False  # passes through origin
            }
            
            # Y-intercept (f(0))
            try:
                if x_range[0] <= 0 <= x_range[1]:
                    y_val = func.subs(var, 0)
                    y_num = float(y_val.evalf())
                    intersections['y_intercept'] = (0, y_num)
                    
                    # Check if passes through origin
                    if abs(y_num) < self.numerical_tolerance:
                        intersections['origin'] = True
            except:
                pass
            
            # X-intercepts (f(x) = 0)
            try:
                solutions = sp.solve(func, var)
                for solution in solutions:
                    try:
                        x_val = float(solution.evalf())
                        if x_range[0] <= x_val <= x_range[1]:
                            intersections['x_intercepts'].append((x_val, 0.0))
                    except:
                        continue
            except:
                pass
            
            return intersections
            
        except Exception as e:
            logger.error(f"Error finding intersections: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_behavior_at_bounds(self, func: sp.Expr, var: sp.Symbol, 
                                   x_range: Tuple[float, float]) -> Dict:
        """Analyze function behavior at range boundaries"""
        try:
            behavior = {
                'left_bound': {},
                'right_bound': {},
                'trend_at_bounds': []
            }
            
            # Left bound behavior
            try:
                left_val = func.subs(var, x_range[0])
                left_num = float(left_val.evalf())
                behavior['left_bound'] = {
                    'x': x_range[0],
                    'f(x)': left_num,
                    'finite': True
                }
            except:
                behavior['left_bound'] = {
                    'x': x_range[0],
                    'f(x)': 'undefined',
                    'finite': False
                }
            
            # Right bound behavior
            try:
                right_val = func.subs(var, x_range[1])
                right_num = float(right_val.evalf())
                behavior['right_bound'] = {
                    'x': x_range[1],
                    'f(x)': right_num,
                    'finite': True
                }
            except:
                behavior['right_bound'] = {
                    'x': x_range[1],
                    'f(x)': 'undefined',
                    'finite': False
                }
            
            # Overall trend
            if behavior['left_bound'].get('finite') and behavior['right_bound'].get('finite'):
                left_y = behavior['left_bound']['f(x)']
                right_y = behavior['right_bound']['f(x)']
                
                if right_y > left_y:
                    behavior['trend_at_bounds'].append('increasing')
                elif right_y < left_y:
                    behavior['trend_at_bounds'].append('decreasing')
                else:
                    behavior['trend_at_bounds'].append('constant')
            
            return behavior
            
        except Exception as e:
            logger.error(f"Error analyzing behavior at bounds: {str(e)}")
            return {'error': str(e)}
    
    def _find_special_points(self, func: sp.Expr, var: sp.Symbol, 
                            x_range: Tuple[float, float]) -> Dict:
        """Find special mathematical points"""
        try:
            special_points = {
                'discontinuities': [],
                'singularities': [],
                'points_of_non_differentiability': [],
                'interesting_points': []
            }
            
            # This is a simplified implementation
            # Full implementation would require more sophisticated analysis
            
            return special_points
            
        except Exception as e:
            logger.error(f"Error finding special points: {str(e)}")
            return {'error': str(e)}
    
    def _determine_function_properties(self, func: sp.Expr, var: sp.Symbol) -> Dict:
        """Determine general function properties"""
        try:
            properties = {
                'function_type': 'unknown',
                'is_polynomial': False,
                'is_rational': False,
                'is_trigonometric': False,
                'is_exponential': False,
                'is_logarithmic': False,
                'is_algebraic': False,
                'is_transcendental': False,
                'complexity_level': 'moderate'
            }
            
            func_str = str(func)
            
            # Check function type
            if any(op in func_str for op in ['+', '-', '*', '**']) and not any(special in func_str for special in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt']):
                properties['is_polynomial'] = True
                properties['function_type'] = 'polynomial'
            elif '/' in func_str:
                properties['is_rational'] = True
                properties['function_type'] = 'rational'
            elif any(trig in func_str for trig in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc']):
                properties['is_trigonometric'] = True
                properties['function_type'] = 'trigonometric'
            elif 'exp' in func_str:
                properties['is_exponential'] = True
                properties['function_type'] = 'exponential'
            elif any(log in func_str for log in ['log', 'ln']):
                properties['is_logarithmic'] = True
                properties['function_type'] = 'logarithmic'
            
            # Determine if transcendental
            if properties['is_trigonometric'] or properties['is_exponential'] or properties['is_logarithmic']:
                properties['is_transcendental'] = True
            
            # Complexity level
            operation_count = func_str.count('+') + func_str.count('-') + func_str.count('*') + func_str.count('/')
            if operation_count <= 2:
                properties['complexity_level'] = 'simple'
            elif operation_count <= 5:
                properties['complexity_level'] = 'moderate'
            else:
                properties['complexity_level'] = 'complex'
            
            return properties
            
        except Exception as e:
            logger.error(f"Error determining function properties: {str(e)}")
            return {'error': str(e)}
    
    def _generate_numerical_summary(self, func: sp.Expr, var: sp.Symbol, 
                                  x_range: Tuple[float, float]) -> Dict:
        """Generate numerical summary of function over range"""
        try:
            summary = {
                'sample_points': 100,
                'min_value': None,
                'max_value': None,
                'mean_value': None,
                'standard_deviation': None,
                'range_width': x_range[1] - x_range[0],
                'function_range': None
            }
            
            # Sample function
            x_samples = np.linspace(x_range[0], x_range[1], summary['sample_points'])
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y_samples = f(x_samples)
                
                # Filter out invalid values
                valid_mask = np.isfinite(y_samples)
                if np.any(valid_mask):
                    valid_y = y_samples[valid_mask]
                    valid_x = x_samples[valid_mask]
                    
                    summary['min_value'] = float(np.min(valid_y))
                    summary['max_value'] = float(np.max(valid_y))
                    summary['mean_value'] = float(np.mean(valid_y))
                    summary['standard_deviation'] = float(np.std(valid_y))
                    summary['function_range'] = (summary['min_value'], summary['max_value'])
                    
            except Exception as e:
                logger.warning(f"Error in numerical sampling: {str(e)}")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating numerical summary: {str(e)}")
            return {'error': str(e)}


# Create singleton instance
advanced_analyzer = AdvancedFunctionAnalyzer()

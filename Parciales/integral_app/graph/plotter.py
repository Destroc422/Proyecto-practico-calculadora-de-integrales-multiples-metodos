
"""
Plotter module for Integral Calculator
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sympy as sp
import logging
from typing import Tuple, Optional, List
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider, Button

# Import domain validator and error handler
from utils.domain_validator import domain_validator
from utils.error_handler import error_handler

# Configure matplotlib for professional plotting
matplotlib.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'font.family': 'DejaVu Sans',
    'mathtext.fontset': 'dejavusans'
})

logger = logging.getLogger(__name__)


class ProfessionalPlotter:
    """Professional mathematical plotter with advanced features"""
    
    def __init__(self):
        """Initialize the plotter"""
        try:
            # Color schemes
            self.colors = {
                'function': '#3498db',
                'derivative': '#e74c3c',
                'integral': '#27ae60',
                'area': '#3498db',
                'grid': '#ecf0f1',
                'background': '#ffffff',
                'text': '#2c3e50'
            }
            
            logger.info("Professional plotter initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing plotter: {str(e)}")
            raise
    
    def plot_interactive(self, func: sp.Expr, var: sp.Symbol, a: float, b: float, 
                        limits: Optional[Tuple[float, float]] = None, 
                        show_area: bool = False) -> plt.Figure:
        """
        Create interactive plot with professional quality
        
        Args:
            func: SymPy expression to plot
            var: Variable symbol
            a: Start of x range
            b: End of x range
            limits: Optional integration limits for area shading
            show_area: Whether to shade area under curve
            
        Returns:
            matplotlib Figure
        """
        try:
            # Validate function domain before plotting
            domain_validation = domain_validator.validate_function_domain(func, var, (a, b))
            
            # Log validation results
            if domain_validation['warnings']:
                for warning in domain_validation['warnings']:
                    logger.warning(f"Domain validation warning: {warning}")
            if domain_validation['errors']:
                for error in domain_validation['errors']:
                    logger.error(f"Domain validation error: {error}")
            
            # Use safe ranges if available
            safe_ranges = domain_validation['safe_ranges']
            if len(safe_ranges) > 1 or not domain_validation['valid']:
                logger.info(f"Using {len(safe_ranges)} safe ranges for plotting")
            
            # Create figure with better proportions
            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor(self.colors['background'])
            ax.set_facecolor(self.colors['background'])
            
            # Generate points using safe ranges (simplified approach)
            if len(safe_ranges) == 1 and domain_validation['valid']:
                current_range = safe_ranges[0]
            else:
                # Use the largest safe range
                current_range = max(safe_ranges, key=lambda r: r[1] - r[0])
                logger.info(f"Using range {current_range} for plotting")
            
            # Generate points with standard resolution
            x = np.linspace(current_range[0], current_range[1], 1000)
            logger.info(f"Using standard resolution: 1000 points")
            
            try:
                # Convert to numpy function and evaluate
                f = sp.lambdify(var, func, 'numpy')
                y = f(x)
                
                # Enhanced validation for ufunc 'isfinite' error
                if y is None:
                    raise ValueError("Function returned None")
                
                # Convert to numpy array if needed
                if not isinstance(y, np.ndarray):
                    try:
                        y = np.array(y, dtype=float)
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"Cannot convert function output to numeric array: {str(e)}")
                
                # Check for object dtype which causes ufunc errors
                if y.dtype == object:
                    try:
                        # Try to convert to float
                        y = y.astype(float)
                    except (ValueError, TypeError):
                        # Filter out non-numeric elements
                        numeric_mask = np.array([isinstance(val, (int, float, np.number)) and not isinstance(val, bool) for val in y])
                        if not np.any(numeric_mask):
                            raise ValueError("No numeric values in function output")
                        y = np.array([y[i] for i in range(len(y)) if numeric_mask[i]], dtype=float)
                        x = x[numeric_mask]
                
                # Handle potential infinities or NaNs with robust validation
                try:
                    # Try standard numpy isfinite first
                    mask = np.isfinite(y)
                except (TypeError, ValueError) as e:
                    logger.warning(f"Standard isfinite failed: {e}, using robust fallback")
                    # Robust fallback: manual check for finite values
                    mask = []
                    for i, val in enumerate(y):
                        try:
                            # Check if value is numeric and finite
                            if isinstance(val, (int, float, np.number)) and not isinstance(val, bool):
                                if isinstance(val, np.number):
                                    # Use numpy's isfinite for numpy numbers
                                    mask.append(np.isfinite(val))
                                else:
                                    # For Python numbers, use math.isfinite
                                    import math
                                    mask.append(math.isfinite(val))
                            else:
                                # Non-numeric values are not finite
                                mask.append(False)
                        except (TypeError, ValueError, AttributeError):
                            # Any error in checking means not finite
                            mask.append(False)
                    
                    mask = np.array(mask, dtype=bool)
                
                if not np.any(mask):
                    raise ValueError("No finite values to plot")
                
                x_clean = x[mask]
                y_clean = y[mask]
                
                # Plot main function
                ax.plot(x_clean, y_clean, color=self.colors['function'], 
                       linewidth=2.5, label=f'f({var.name}) = {func}', 
                       zorder=3)
                
                # Shade area if requested
                if show_area and limits:
                    self._shade_integral_area(ax, f, x, limits, var.name)
                
                # Add grid
                ax.grid(True, alpha=0.3, color=self.colors['grid'], linestyle='-', linewidth=0.5)
                
                # Set labels and title
                ax.set_xlabel(f'{var.name}', fontsize=12, color=self.colors['text'])
                ax.set_ylabel('f({})'.format(var.name), fontsize=12, color=self.colors['text'])
                ax.set_title(f'Gráfica de {func}', fontsize=14, color=self.colors['text'], pad=20)
                
                # Set axis limits
                ax.set_xlim(a, b)
                
                # Auto-scale y axis with some padding
                y_min, y_max = np.min(y_clean), np.max(y_clean)
                y_range = y_max - y_min
                if y_range > 0:
                    ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                
                # Add legend
                ax.legend(loc='best', framealpha=0.9, fontsize=10)
                
                # Add zero lines
                ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                
                # Add integration limits markers if specified
                if limits:
                    ax.axvline(x=limits[0], color='red', linestyle='--', alpha=0.7, linewidth=1.5, label=f'a = {limits[0]}')
                    ax.axvline(x=limits[1], color='red', linestyle='--', alpha=0.7, linewidth=1.5, label=f'b = {limits[1]}')
                    ax.legend(loc='best', framealpha=0.9, fontsize=10)
                
                plt.tight_layout()
                
                return fig
                
            except Exception as e:
                logger.error(f"Error plotting function: {str(e)}")
                
                # Use intelligent error handler
                error_info = error_handler.handle_plotting_error(e, func, var, (a, b), {
                    'method': 'plot_interactive',
                    'original_range': (a, b),
                    'show_area': show_area
                })
                
                # Try recovery if possible
                if error_info['can_recover']:
                    logger.info("Attempting automatic recovery...")
                    
                    # Apply recovery strategies
                    for attempt in error_info['recovery_attempts']:
                        strategy, value = attempt
                        logger.info(f"Trying recovery strategy: {strategy}")
                        
                        if strategy == 'reduce_range':
                            new_a, new_b = value
                            x = np.linspace(new_a, new_b, error_info['recovered_resolution'])
                        elif strategy == 'lower_resolution':
                            x = np.linspace(a, b, value)
                        else:
                            x = np.linspace(a, b, error_info['recovered_resolution'])
                        
                        try:
                            f = sp.lambdify(var, func, 'numpy')
                            y = f(x)
                            
                            # Enhanced validation
                            if y is None:
                                continue
                            
                            if not isinstance(y, np.ndarray):
                                try:
                                    y = np.array(y, dtype=float)
                                except (ValueError, TypeError):
                                    continue
                            
                            if y.dtype == object:
                                try:
                                    y = y.astype(float)
                                except (ValueError, TypeError):
                                    numeric_mask = np.array([isinstance(val, (int, float, np.number)) and not isinstance(val, bool) for val in y])
                                    if not np.any(numeric_mask):
                                        continue
                                    y = np.array([y[i] for i in range(len(y)) if numeric_mask[i]], dtype=float)
                                    x = x[numeric_mask]
                            
                            try:
                                mask = np.isfinite(y)
                            except (TypeError, ValueError):
                                mask = np.array([isinstance(val, (int, float, np.number)) and 
                                               not isinstance(val, bool) and 
                                               np.isfinite(val) if isinstance(val, np.number) else True 
                                               for val in y])
                            
                            if np.any(mask):
                                x_clean = x[mask]
                                y_clean = y[mask]
                                
                                # Plot recovered function
                                ax.plot(x_clean, y_clean, color=self.colors['function'], 
                                       linewidth=2.5, label=f'f({var.name}) = {func} (recovered)', 
                                       zorder=3)
                                
                                # Add recovery notice
                                ax.text(0.02, 0.98, f'Recuperado automáticamente: {len(error_info["recovery_attempts"])} intentos', 
                                       transform=ax.transAxes, va='top', fontsize=10, 
                                       color='green', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
                                
                                # Complete plot setup
                                ax.grid(True, alpha=0.3, color=self.colors['grid'], linestyle='-', linewidth=0.5)
                                ax.set_xlabel(f'{var.name}', fontsize=12, color=self.colors['text'])
                                ax.set_ylabel('f({})'.format(var.name), fontsize=12, color=self.colors['text'])
                                ax.set_title(f'Gráfica de {func} (Recuperada)', fontsize=14, color=self.colors['text'], pad=20)
                                ax.set_xlim(x_clean[0], x_clean[-1])
                                
                                y_min, y_max = np.min(y_clean), np.max(y_clean)
                                y_range = y_max - y_min
                                if y_range > 0:
                                    ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                                
                                ax.legend(loc='best', framealpha=0.9, fontsize=10)
                                ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                                ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                                
                                plt.tight_layout()
                                logger.info("Automatic recovery successful!")
                                return fig
                                
                        except Exception as recovery_error:
                            logger.warning(f"Recovery attempt failed: {str(recovery_error)}")
                            continue
                
                # If all recovery attempts failed, show detailed error message
                user_message = error_handler.create_user_friendly_message(error_info)
                ax.text(0.5, 0.5, user_message, 
                       transform=ax.transAxes, ha='center', va='center', 
                       fontsize=10, color='red', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
                return fig
                
        except Exception as e:
            logger.error(f"Error in plot_interactive: {str(e)}")
            # Create minimal figure
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f'Error: {str(e)}', 
                   transform=ax.transAxes, ha='center', va='center', 
                   fontsize=12, color='red')
            return fig
    
    def plot_with_analysis(self, func: sp.Expr, var: sp.Symbol, a: float, b: float, 
                          limits: Optional[Tuple[float, float]] = None) -> plt.Figure:
        """
        Create comprehensive analysis plot with function, derivative, and integral
        
        Args:
            func: SymPy expression to plot
            var: Variable symbol
            a: Start of x range
            b: End of x range
            limits: Optional integration limits
            
        Returns:
            matplotlib Figure
        """
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.patch.set_facecolor(self.colors['background'])
            
            # Flatten axes for easier access
            ax_main, ax_derivative, ax_integral, ax_analysis = axes.flatten()
            
            # Generate points
            x = np.linspace(a, b, 1000)
            
            # Convert to numpy functions
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y = f(x)
                
                # Enhanced validation for ufunc 'isfinite' error
                if y is None:
                    raise ValueError("Function returned None")
                
                # Convert to numpy array if needed
                if not isinstance(y, np.ndarray):
                    try:
                        y = np.array(y, dtype=float)
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"Cannot convert function output to numeric array: {str(e)}")
                
                # Check for object dtype which causes ufunc errors
                if y.dtype == object:
                    try:
                        # Try to convert to float
                        y = y.astype(float)
                    except (ValueError, TypeError):
                        # Filter out non-numeric elements
                        numeric_mask = np.array([isinstance(val, (int, float, np.number)) and not isinstance(val, bool) for val in y])
                        if not np.any(numeric_mask):
                            raise ValueError("No numeric values in function output")
                        y = np.array([y[i] for i in range(len(y)) if numeric_mask[i]], dtype=float)
                        x = x[numeric_mask]
                
                # Handle potential infinities or NaNs with robust validation
                try:
                    # Try standard numpy isfinite first
                    mask = np.isfinite(y)
                except (TypeError, ValueError) as e:
                    logger.warning(f"Standard isfinite failed: {e}, using robust fallback")
                    # Robust fallback: manual check for finite values
                    mask = []
                    for i, val in enumerate(y):
                        try:
                            # Check if value is numeric and finite
                            if isinstance(val, (int, float, np.number)) and not isinstance(val, bool):
                                if isinstance(val, np.number):
                                    # Use numpy's isfinite for numpy numbers
                                    mask.append(np.isfinite(val))
                                else:
                                    # For Python numbers, use math.isfinite
                                    import math
                                    mask.append(math.isfinite(val))
                            else:
                                # Non-numeric values are not finite
                                mask.append(False)
                        except (TypeError, ValueError, AttributeError):
                            # Any error in checking means not finite
                            mask.append(False)
                    
                    mask = np.array(mask, dtype=bool)
                
                if not np.any(mask):
                    raise ValueError("No finite values to plot")
                
                x_clean = x[mask]
                y_clean = y[mask]
                
                # === MAIN FUNCTION ===
                ax_main.plot(x_clean, y_clean, color=self.colors['function'], 
                            linewidth=2.5, label=f'f({var.name}) = {func}')
                
                if limits:
                    self._shade_integral_area(ax_main, f, x, limits, var.name)
                    ax_main.axvline(x=limits[0], color='red', linestyle='--', alpha=0.7, linewidth=1.5)
                    ax_main.axvline(x=limits[1], color='red', linestyle='--', alpha=0.7, linewidth=1.5)
                
                ax_main.set_title('Función Principal', fontsize=12, color=self.colors['text'])
                ax_main.grid(True, alpha=0.3, color=self.colors['grid'])
                ax_main.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                ax_main.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                
                # === DERIVATIVE ===
                try:
                    derivative = sp.diff(func, var)
                    f_prime = sp.lambdify(var, derivative, 'numpy')
                    y_prime = f_prime(x)
                    
                    mask_prime = np.isfinite(y_prime)
                    if np.any(mask_prime):
                        x_prime_clean = x[mask_prime]
                        y_prime_clean = y_prime[mask_prime]
                        
                        ax_derivative.plot(x_prime_clean, y_prime_clean, color=self.colors['derivative'], 
                                         linewidth=2.5, label=f"f'({var.name}) = {derivative}")
                    
                    ax_derivative.set_title('Derivada', fontsize=12, color=self.colors['text'])
                    ax_derivative.grid(True, alpha=0.3, color=self.colors['grid'])
                    ax_derivative.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                    ax_derivative.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                    
                except Exception as e:
                    ax_derivative.text(0.5, 0.5, f'Error en derivada: {str(e)}', 
                                    transform=ax_derivative.transAxes, ha='center', va='center', 
                                    fontsize=10, color='red')
                    ax_derivative.set_title('Derivada (Error)', fontsize=12, color=self.colors['text'])
                
                # === INTEGRAL ===
                try:
                    integral = sp.integrate(func, var)
                    F = sp.lambdify(var, integral, 'numpy')
                    y_integral = F(x)
                    
                    # Normalize integral (subtract minimum to avoid large constants)
                    y_integral_norm = y_integral - np.min(y_integral[np.isfinite(y_integral)])
                    
                    mask_integral = np.isfinite(y_integral_norm)
                    if np.any(mask_integral):
                        x_integral_clean = x[mask_integral]
                        y_integral_clean = y_integral_norm[mask_integral]
                        
                        ax_integral.plot(x_integral_clean, y_integral_clean, color=self.colors['integral'], 
                                       linewidth=2.5, label=f'F({var.name}) = {integral}')
                    
                    ax_integral.set_title('Integral (Normalizada)', fontsize=12, color=self.colors['text'])
                    ax_integral.grid(True, alpha=0.3, color=self.colors['grid'])
                    ax_integral.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                    ax_integral.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                    
                except Exception as e:
                    ax_integral.text(0.5, 0.5, f'Error en integral: {str(e)}', 
                                    transform=ax_integral.transAxes, ha='center', va='center', 
                                    fontsize=10, color='red')
                    ax_integral.set_title('Integral (Error)', fontsize=12, color=self.colors['text'])
                
                # === ANALYSIS ===
                # Critical points analysis
                try:
                    derivative = sp.diff(func, var)
                    critical_points = sp.solve(derivative, var)
                    
                    if critical_points:
                        # Filter critical points within range
                        valid_points = []
                        for point in critical_points:
                            try:
                                point_val = float(point.evalf())
                                if a <= point_val <= b:
                                    valid_points.append(point_val)
                            except:
                                continue
                        
                        if valid_points:
                            # Plot critical points on main function
                            for point in valid_points:
                                try:
                                    y_val = f(point)
                                    if np.isfinite(y_val):
                                        ax_main.plot(point, y_val, 'ro', markersize=8, zorder=5)
                                        ax_analysis.plot(point, y_val, 'ro', markersize=8, zorder=5)
                                except:
                                    continue
                    
                    # Create analysis summary
                    analysis_text = f"Análisis de {func}\n\n"
                    analysis_text += f"Rango: [{a}, {b}]\n"
                    analysis_text += f"Puntos críticos: {len(valid_points) if valid_points else 0}\n"
                    
                    if limits:
                        analysis_text += f"Límites de integración: [{limits[0]}, {limits[1]}]\n"
                        
                        # Calculate definite integral
                        try:
                            definite_result = sp.integrate(func, (var, limits[0], limits[1]))
                            analysis_text += f"Integral definida: {definite_result}\n"
                            
                            # Calculate numeric value
                            try:
                                numeric_result = float(definite_result.evalf())
                                analysis_text += f"Valor numérico: {numeric_result:.6f}\n"
                            except:
                                pass
                        except Exception as e:
                            analysis_text += f"Error en integral definida: {str(e)}\n"
                    
                    ax_analysis.text(0.05, 0.95, analysis_text, transform=ax_analysis.transAxes, 
                                   fontsize=10, verticalalignment='top', fontfamily='monospace',
                                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                    
                    # Plot function on analysis axis
                    ax_analysis.plot(x_clean, y_clean, color=self.colors['function'], 
                                   linewidth=1.5, alpha=0.7)
                    ax_analysis.grid(True, alpha=0.3, color=self.colors['grid'])
                    ax_analysis.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                    ax_analysis.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                    ax_analysis.set_title('Análisis Completo', fontsize=12, color=self.colors['text'])
                    
                except Exception as e:
                    ax_analysis.text(0.5, 0.5, f'Error en análisis: {str(e)}', 
                                    transform=ax_analysis.transAxes, ha='center', va='center', 
                                    fontsize=10, color='red')
                    ax_analysis.set_title('Análisis (Error)', fontsize=12, color=self.colors['text'])
                
                # Adjust layout
                plt.tight_layout()
                
                return fig
                
            except Exception as e:
                logger.error(f"Error in plot_with_analysis: {str(e)}")
                # Create error plot
                for ax in axes.flatten():
                    ax.text(0.5, 0.5, f'Error: {str(e)}', 
                           transform=ax.transAxes, ha='center', va='center', 
                           fontsize=10, color='red')
                return fig
                
        except Exception as e:
            logger.error(f"Error creating analysis plot: {str(e)}")
            # Create minimal figure
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f'Error: {str(e)}', 
                   transform=ax.transAxes, ha='center', va='center', 
                   fontsize=12, color='red')
            return fig
    
    def _shade_integral_area(self, ax, f, x, limits: Tuple[float, float], var_name: str):
        """Shade the area under the curve for definite integrals"""
        try:
            lower, upper = limits
            
            # Generate points for the area
            x_area = np.linspace(lower, upper, 200)
            y_area = f(x_area)
            
            # Handle infinities or NaNs
            mask = np.isfinite(y_area)
            if np.any(mask):
                x_area_clean = x_area[mask]
                y_area_clean = y_area[mask]
                
                # Shade the area
                ax.fill_between(x_area_clean, 0, y_area_clean, 
                             alpha=0.3, color=self.colors['area'], 
                             label=f'Área de ∫_{lower}^{upper} f({var_name}) d{var_name}')
                
        except Exception as e:
            logger.error(f"Error shading integral area: {str(e)}")
    
    def create_interactive_plot(self, func: sp.Expr, var: sp.Symbol, a: float, b: float) -> plt.Figure:
        """
        Create an interactive plot with sliders
        
        Args:
            func: SymPy expression to plot
            var: Variable symbol
            a: Initial start of x range
            b: Initial end of x range
            
        Returns:
            matplotlib Figure with interactive controls
        """
        try:
            # Create figure with space for sliders
            fig = plt.figure(figsize=(12, 8))
            fig.patch.set_facecolor(self.colors['background'])
            
            # Main plot
            ax = plt.subplot2grid((4, 4), (0, 0), colspan=4, rowspan=3)
            ax.set_facecolor(self.colors['background'])
            
            # Slider axes
            ax_xmin = plt.subplot2grid((4, 4), (3, 0), colspan=2)
            ax_xmax = plt.subplot2grid((4, 4), (3, 2), colspan=2)
            
            # Initial plot
            x = np.linspace(a, b, 1000)
            f = sp.lambdify(var, func, 'numpy')
            
            try:
                y = f(x)
                mask = np.isfinite(y)
                
                if np.any(mask):
                    x_clean = x[mask]
                    y_clean = y[mask]
                    
                    line, = ax.plot(x_clean, y_clean, color=self.colors['function'], 
                                  linewidth=2.5, label=f'f({var.name}) = {func}')
                    
                    ax.set_xlabel(f'{var.name}', fontsize=12, color=self.colors['text'])
                    ax.set_ylabel('f({})'.format(var.name), fontsize=12, color=self.colors['text'])
                    ax.set_title(f'Gráfica Interactiva de {func}', fontsize=14, color=self.colors['text'])
                    ax.grid(True, alpha=0.3, color=self.colors['grid'])
                    ax.axhline(y=0, color='black', linewidth=0.5, alpha=0.5)
                    ax.axvline(x=0, color='black', linewidth=0.5, alpha=0.5)
                    ax.legend(loc='best', framealpha=0.9, fontsize=10)
                    
                    # Create sliders
                    slider_xmin = Slider(ax_xmin, 'X min', a-5, a, valinit=a, valstep=0.1)
                    slider_xmax = Slider(ax_xmax, 'X max', b, b+5, valinit=b, valstep=0.1)
                    
                    # Update function for sliders
                    def update(val):
                        try:
                            new_a = slider_xmin.val
                            new_b = slider_xmax.val
                            
                            if new_a < new_b:
                                x_new = np.linspace(new_a, new_b, 1000)
                                y_new = f(x_new)
                                
                                mask_new = np.isfinite(y_new)
                                if np.any(mask_new):
                                    x_clean_new = x_new[mask_new]
                                    y_clean_new = y_new[mask_new]
                                    
                                    line.set_data(x_clean_new, y_clean_new)
                                    ax.set_xlim(new_a, new_b)
                                    
                                    # Auto-scale y axis
                                    if len(y_clean_new) > 0:
                                        y_min, y_max = np.min(y_clean_new), np.max(y_clean_new)
                                        y_range = y_max - y_min
                                        if y_range > 0:
                                            ax.set_ylim(y_min - 0.1*y_range, y_max + 0.1*y_range)
                                    
                                fig.canvas.draw_idle()
                        except Exception as e:
                            logger.error(f"Error updating plot: {str(e)}")
                    
                    # Connect sliders to update function
                    slider_xmin.on_changed(update)
                    slider_xmax.on_changed(update)
                    
                    plt.tight_layout()
                    return fig
                else:
                    raise ValueError("No finite values to plot")
                    
            except Exception as e:
                logger.error(f"Error creating interactive plot: {str(e)}")
                ax.text(0.5, 0.5, f'Error: {str(e)}', 
                       transform=ax.transAxes, ha='center', va='center', 
                       fontsize=12, color='red')
                return fig
                
        except Exception as e:
            logger.error(f"Error in create_interactive_plot: {str(e)}")
            # Create minimal figure
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, f'Error: {str(e)}', 
                   transform=ax.transAxes, ha='center', va='center', 
                   fontsize=12, color='red')
            return fig
    
    def save_plot(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """
        Save plot to file with high quality
        
        Args:
            fig: matplotlib Figure
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        try:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight', 
                       facecolor=self.colors['background'], edgecolor='none')
            logger.info(f"Plot saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving plot: {str(e)}")
            raise


# Create backward compatibility
class AdvancedPlotter(ProfessionalPlotter):
    """Advanced plotter with more features"""
    
    def __init__(self):
        super().__init__()
        self.interactive_mode = True


# Create backward compatibility
Plotter = ProfessionalPlotter

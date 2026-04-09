"""
Validators for Integral Calculator
Robust validation with comprehensive error handling
"""
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class ExpressionValidator:
    """Professional expression validator with comprehensive checks"""
    
    def __init__(self):
        """Initialize the validator"""
        try:
            # Valid mathematical patterns
            self.valid_patterns = [
                r'^[a-zA-Z0-9+\-*/^()_.,\s]+$',  # Basic mathematical characters
                r'^[a-zA-Z0-9+\-*/^()_.,\sπ∞√∑∏∫∂∇∈∉⊂⊃∪∩∅ℝℤℕℂℚ]+$',  # With Unicode symbols
            ]
            
            # Invalid patterns
            self.invalid_patterns = [
                r'[^\w+\-*/^()_.,\sπ∞√∑∏∫∂∇∈∉⊂⊃∪∩∅ℝℤℕℂℚ]',  # Invalid characters
                r'[+\-*/^]{2,}',  # Multiple operators
                r'[+\-*/^]$',  # Operator at end
                r'^[+\-*/^]',  # Operator at start
            ]
            
            logger.info("ExpressionValidator initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ExpressionValidator: {str(e)}")
            raise
    
    def validate(self, expression: str) -> Dict[str, Any]:
        """
        Validate a mathematical expression
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            Dictionary with validation results
        """
        try:
            result = {
                'valid': False,
                'errors': [],
                'warnings': [],
                'suggestions': []
            }
            
            # Basic checks
            if not expression:
                result['errors'].append("Expression is empty")
                return result
            
            if not expression.strip():
                result['errors'].append("Expression contains only whitespace")
                return result
            
            # Check for valid characters
            valid_chars = True
            for pattern in self.valid_patterns:
                if re.match(pattern, expression):
                    valid_chars = True
                    break
            else:
                valid_chars = False
            
            if not valid_chars:
                result['errors'].append("Expression contains invalid characters")
            
            # Check for invalid patterns
            for pattern in self.invalid_patterns:
                if re.search(pattern, expression):
                    result['warnings'].append(f"Potentially invalid pattern: {pattern}")
            
            # Check parentheses balance
            if not self._check_parentheses(expression):
                result['errors'].append("Unbalanced parentheses")
            
            # Check for common issues
            self._check_common_issues(expression, result)
            
            # If no errors, mark as valid
            if not result['errors']:
                result['valid'] = True
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating expression: {str(e)}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'suggestions': []
            }
    
    def _check_parentheses(self, expression: str) -> bool:
        """Check if parentheses are balanced"""
        try:
            stack = []
            pairs = {'(': ')', '[': ']', '{': '}'}
            
            for char in expression:
                if char in pairs.keys():
                    stack.append(char)
                elif char in pairs.values():
                    if not stack:
                        return False
                    last = stack.pop()
                    if pairs[last] != char:
                        return False
            
            return len(stack) == 0
            
        except Exception as e:
            logger.error(f"Error checking parentheses: {str(e)}")
            return False
    
    def _check_common_issues(self, expression: str, result: Dict[str, Any]):
        """Check for common expression issues"""
        try:
            # Check for consecutive operators
            if re.search(r'[+\-*/^]{2,}', expression):
                result['warnings'].append("Consecutive operators detected")
            
            # Check for missing multiplication
            if re.search(r'[a-zA-Z]\d', expression):
                result['suggestions'].append("Consider adding * between variables and numbers")
            
            # Check for missing parentheses in functions
            functions = ['sin', 'cos', 'tan', 'log', 'ln', 'exp', 'sqrt', 'abs']
            for func in functions:
                if re.search(rf'\b{func}\b[^(]', expression):
                    result['suggestions'].append(f"Add parentheses after {func}")
            
            # Check for power notation
            if '**' in expression:
                result['suggestions'].append("Consider using ^ instead of ** for powers")
            
        except Exception as e:
            logger.error(f"Error checking common issues: {str(e)}")
    
    def is_valid(self, expression: str) -> bool:
        """Quick validation check"""
        try:
            result = self.validate(expression)
            return result['valid']
        except Exception as e:
            logger.error(f"Error in quick validation: {str(e)}")
            return False


def validate_input(expr_str: str) -> bool:
    """Valida la entrada de la función con manejo robusto de errores"""
    try:
        if not expr_str or not expr_str.strip():
            raise ValueError("La función está vacía")
        
        # Verificar caracteres peligrosos
        dangerous_patterns = [
            r';',  # Separadores de comandos
            r'import',  # Importaciones
            r'exec',  # Ejecución de código
            r'eval',  # Evaluación de código
            r'__[a-zA-Z0-9_]+__',  # Métodos especiales
            r'lambda',  # Funciones lambda
            r'def\s+',  # Definiciones de funciones
            r'class\s+',  # Definiciones de clases
            r'for\s+',  # Bucles
            r'while\s+',  # Bucles
            r'if\s+',  # Condicionales
        ]
        
        expr_lower = expr_str.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, expr_lower):
                raise ValueError(f"Patrón no permitido: {pattern}")
        
        # Preprocesar la expresión
        processed_expr = _preprocess_expression(expr_str)
        
        # Intentar parsear la expresión
        try:
            # Usar transformaciones estándar
            transformations = standard_transformations + (implicit_multiplication_application,)
            
            # Diccionario local seguro
            local_dict = {
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'asin': sp.asin,
                'acos': sp.acos,
                'atan': sp.atan,
                'sinh': sp.sinh,
                'cosh': sp.cosh,
                'tanh': sp.tanh,
                'exp': sp.exp,
                'log': sp.log,
                'ln': sp.log,
                'sqrt': sp.sqrt,
                'abs': sp.Abs,
                'pi': sp.pi,
                'e': sp.E,
                'oo': sp.oo,
                'I': sp.I,
            }
            
            expr = parse_expr(processed_expr, 
                            local_dict=local_dict,
                            transformations=transformations,
                            evaluate=True)
            
        except Exception as parse_error:
            # Intentar parseo más simple como fallback
            try:
                expr = sp.sympify(processed_expr)
            except Exception as sympify_error:
                raise ValueError(f"Error de sintaxis: {str(parse_error)}")
        
        # Verificar que sea una expresión válida
        if not isinstance(expr, sp.Expr):
            raise ValueError("No es una expresión matemática válida")
        
        # Verificar que no contenga operaciones indefinidas
        _check_undefined_operations(expr)
        
        logger.info(f"Expression validated successfully: {expr}")
        return True
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in validation: {str(e)}")
        raise ValueError(f"Error inesperado en la validación: {str(e)}")


def validate_limits(lower_str: str, upper_str: str) -> tuple:
    """Valida y convierte los límites de integración"""
    try:
        if not lower_str or not upper_str:
            raise ValueError("Ambos límites deben ser proporcionados")
        
        # Limpiar y convertir
        lower_clean = _preprocess_expression(lower_str)
        upper_clean = _preprocess_expression(upper_str)
        
        lower = sp.sympify(lower_clean)
        upper = sp.sympify(upper_clean)
        
        # Verificar que sean números o expresiones numéricas
        if not (lower.is_number or lower.is_real):
            raise ValueError("El límite inferior debe ser un valor numérico")
        
        if not (upper.is_number or upper.is_real):
            raise ValueError("El límite superior debe ser un valor numérico")
        
        # Convertir a float para comparación (si es posible)
        try:
            lower_val = float(lower.evalf())
            upper_val = float(upper.evalf())
            
            if lower_val >= upper_val:
                raise ValueError("El límite inferior debe ser menor que el superior")
        except (TypeError, ValueError):
            # Si no se pueden convertir a float, verificar con SymPy
            if lower >= upper:
                raise ValueError("El límite inferior debe ser menor que el superior")
        
        return lower, upper
        
    except ValueError:
        raise
    except Exception as e:
        if "sympify" in str(e).lower():
            raise ValueError("Los límites deben ser expresiones numéricas válidas")
        else:
            raise ValueError(f"Error en los límites: {str(e)}")


def validate_variable(var_str: str) -> sp.Symbol:
    """Valida y retorna el símbolo de la variable"""
    try:
        if not var_str or not var_str.strip():
            raise ValueError("La variable no puede estar vacía")
        
        var_str = var_str.strip()
        
        # Variables permitidas
        valid_vars = ['x', 'y', 'z', 't', 'u', 'v', 'w', 's', 'r', 'a', 'b']
        
        if var_str not in valid_vars:
            raise ValueError(f"Variable no válida. Use una de: {', '.join(valid_vars)}")
        
        return sp.Symbol(var_str)
        
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Error en la variable: {str(e)}")


def sanitize_expression(expr_str: str) -> str:
    """Limpia y sanitiza la expresión"""
    try:
        if not expr_str:
            return ""
        
        # Eliminar espacios extra
        expr_str = ' '.join(expr_str.split())
        
        # Reemplazar caracteres comunes
        replacements = {
            '^': '**',
            '×': '*',
            '·': '*',
            '÷': '/',
            'π': 'pi',
            '∞': 'oo',
            '√': 'sqrt(',
            '∑': 'summation(',
            '∏': 'product(',
            '∂': 'diff(',
            '∫': 'integrate(',
        }
        
        for old, new in replacements.items():
            expr_str = expr_str.replace(old, new)
        
        # Manejar casos especiales
        expr_str = _handle_special_cases(expr_str)
        
        return expr_str
        
    except Exception as e:
        logger.error(f"Error sanitizing expression: {str(e)}")
        return expr_str


def _preprocess_expression(expr_str: str) -> str:
    """Preprocesa la expresión para parseo"""
    try:
        # Aplicar sanitización básica
        expr_str = sanitize_expression(expr_str)
        
        # Manejar paréntesis desbalanceados
        open_count = expr_str.count('(')
        close_count = expr_str.count(')')
        
        if open_count > close_count:
            expr_str += ')' * (open_count - close_count)
        elif close_count > open_count:
            # Eliminar paréntesis extra (con cuidado)
            expr_str = _remove_extra_parentheses(expr_str)
        
        return expr_str
        
    except Exception as e:
        logger.error(f"Error preprocessing expression: {str(e)}")
        return expr_str


def _handle_special_cases(expr_str: str) -> str:
    """Maneja casos especiales en la expresión"""
    try:
        # Multiplicación implícita
        expr_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr_str)
        expr_str = re.sub(r'(\))(\d)', r'\1*\2', expr_str)
        expr_str = re.sub(r'(\))(\()', r'\1*\2', expr_str)
        expr_str = re.sub(r'([a-zA-Z])(\()', r'\1*\2', expr_str)
        
        # Funciones sin paréntesis
        functions_without_parens = ['sqrt', 'log', 'ln', 'sin', 'cos', 'tan', 'exp']
        for func in functions_without_parens:
            pattern = rf'{func}([a-zA-Z0-9]+)'
            expr_str = re.sub(pattern, rf'{func}(\1)', expr_str)
        
        return expr_str
        
    except Exception as e:
        logger.error(f"Error handling special cases: {str(e)}")
        return expr_str


def _remove_extra_parentheses(expr_str: str) -> str:
    """Elimina paréntesis extra de forma segura"""
    try:
        # Implementación simple - eliminar paréntesis de cierre extra
        result = []
        open_count = 0
        close_count = 0
        
        for char in expr_str:
            if char == '(':
                open_count += 1
                result.append(char)
            elif char == ')':
                if open_count > close_count:
                    close_count += 1
                    result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)
        
    except Exception as e:
        logger.error(f"Error removing extra parentheses: {str(e)}")
        return expr_str


def _check_undefined_operations(expr: sp.Expr) -> None:
    """Verifica operaciones indefinidas"""
    try:
        # Buscar divisiones por cero
        for node in sp.preorder_traversal(expr):
            if isinstance(node, sp.Pow):
                # Verificar potencias negativas de cero
                if node.exp.is_negative and node.base == 0:
                    raise ValueError("División por cero detectada")
            elif isinstance(node, sp.Mul):
                # Verificar multiplicación por infinito de forma incorrecta
                factors = node.args
                if 0 in factors and sp.oo in factors:
                    raise ValueError("Operación indefinida: 0 * ∞")
        
    except Exception as e:
        logger.error(f"Error checking undefined operations: {str(e)}")
        # No lanzar excepción para no interrumpir el parseo


def is_safe_expression(expr_str: str) -> bool:
    """Verifica si una expresión es segura para evaluar"""
    try:
        validate_input(expr_str)
        return True
    except:
        return False


def get_expression_complexity(expr_str: str) -> str:
    """Determina la complejidad de una expresión"""
    try:
        expr = sp.sympify(_preprocess_expression(expr_str))
        
        # Contar operaciones
        ops = len(list(sp.preorder_traversal(expr)))
        
        # Contar variables
        vars_count = len(expr.free_symbols)
        
        # Contar funciones
        func_count = sum(1 for node in sp.preorder_traversal(expr) if node.is_Function)
        
        if ops < 5 and vars_count <= 1 and func_count <= 1:
            return "Simple"
        elif ops < 15 and vars_count <= 2 and func_count <= 3:
            return "Media"
        else:
            return "Compleja"
            
    except:
        return "Desconocida"

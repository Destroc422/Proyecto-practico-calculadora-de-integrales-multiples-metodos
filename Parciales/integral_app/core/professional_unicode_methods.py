#!/usr/bin/env python3
"""
Professional Unicode Methods - Sistema de Métodos Unicode Profesionales
Implementa métodos Unicode pulcros y profesionales para todas las secciones
"""
import logging
import re
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class UnicodeStyle(Enum):
    """Estilos de visualización Unicode"""
    PROFESSIONAL = "professional"  # Estilo profesional limpio
    ELEGANT = "elegant"           # Estilo elegante decorativo
    TECHNICAL = "technical"       # Estilo técnico preciso
    ACADEMIC = "academic"         # Estilo académico formal


@dataclass
class UnicodeMethod:
    """Método de conversión Unicode especializado"""
    name: str
    pattern: str
    replacement: str
    style: UnicodeStyle
    priority: int
    description: str
    category: str


class ProfessionalUnicodeMethods:
    """Sistema profesional de métodos Unicode para máxima pulcritud"""
    
    def __init__(self):
        self.methods: Dict[str, UnicodeMethod] = {}
        self.style_configurations: Dict[UnicodeStyle, Dict[str, Any]] = {}
        self.cache: Dict[str, str] = {}
        
        self._initialize_methods()
        self._initialize_style_configurations()
        
        logger.info("Professional Unicode Methods inicializado")
    
    def _initialize_methods(self):
        """Inicializar métodos Unicode profesionales"""
        
        # Integrales - Estilo Profesional
        self.methods['integral_professional'] = UnicodeMethod(
            name='integral_professional',
            pattern=r'\bintegrate\s*\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Integral con estilo profesional',
            category='integrals'
        )
        
        self.methods['integral_elegant'] = UnicodeMethod(
            name='integral_elegant',
            pattern=r'\bintegral\s*\(',
            replacement='integral(',
            style=UnicodeStyle.ELEGANT,
            priority=1,
            description='Integral con estilo elegante',
            category='integrals'
        )
        
        # Símbolo real de integral Unicode
        self.methods['integral_unicode_real'] = UnicodeMethod(
            name='integral_unicode_real',
            pattern=r'\bintegral\s*\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Integral con símbolo Unicode real',
            category='integrals'
        )
        
        
        # Símbolo real de integral Unicode
        self.methods['integral_unicode_symbol'] = UnicodeMethod(
            name='integral_unicode_symbol',
            pattern=r'\bintegral\s*\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Integral con símbolo Unicode real',
            category='integrals'
        )
        
        # Reemplazar integrate por símbolo Unicode real
        self.methods['integrate_to_unicode'] = UnicodeMethod(
            name='integrate_to_unicode',
            pattern=r'\bintegrate\s*\(',
            replacement='integral(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Convertir integrate a símbolo Unicode real',
            category='integrals'
        )
# Potencias - Estilo Profesional
        self.methods['power_2_professional'] = UnicodeMethod(
            name='power_2_professional',
            pattern=r'\*\*2\b',
            replacement='²',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Cuadrado profesional',
            category='powers'
        )
        
        self.methods['power_3_professional'] = UnicodeMethod(
            name='power_3_professional',
            pattern=r'\*\*3\b',
            replacement='³',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Cubo profesional',
            category='powers'
        )
        
        self.methods['power_n_professional'] = UnicodeMethod(
            name='power_n_professional',
            pattern=r'\*\*([a-zA-Z])\b',
            replacement=r'^\1',
            style=UnicodeStyle.PROFESSIONAL,
            priority=2,
            description='Potencia variable profesional',
            category='powers'
        )
        
        # Operadores - Estilo Profesional
        self.methods['multiply_professional'] = UnicodeMethod(
            name='multiply_professional',
            pattern=r'\*',
            replacement='×',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Multiplicación profesional',
            category='operators'
        )
        
        self.methods['divide_professional'] = UnicodeMethod(
            name='divide_professional',
            pattern=r'(?<!\^)/',
            replacement='÷',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='División profesional',
            category='operators'
        )
        
        # Fracciones - Estilo Profesional
        self.methods['fraction_2_3_professional'] = UnicodeMethod(
            name='fraction_2_3_professional',
            pattern=r'\b2/3\b',
            replacement='2/3',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Dos tercios profesional',
            category='fractions'
        )
        
        self.methods['fraction_3_2_professional'] = UnicodeMethod(
            name='fraction_3_2_professional',
            pattern=r'\b3/2\b',
            replacement='3/2',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Tres medios profesional',
            category='fractions'
        )
        
        self.methods['fraction_1_2_professional'] = UnicodeMethod(
            name='fraction_1_2_professional',
            pattern=r'\b1/2\b',
            replacement='1/2',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Un medio profesional',
            category='fractions'
        )
        
        # Constantes - Estilo Profesional
        self.methods['pi_professional'] = UnicodeMethod(
            name='pi_professional',
            pattern=r'\bpi\b',
            replacement='pi',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Constante Pi profesional',
            category='constants'
        )
        
        self.methods['infinity_professional'] = UnicodeMethod(
            name='infinity_professional',
            pattern=r'\b(inf|infinity)\b',
            replacement='inf',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Infinito profesional',
            category='constants'
        )
        
        # Funciones - Estilo Profesional
        self.methods['sqrt_professional'] = UnicodeMethod(
            name='sqrt_professional',
            pattern=r'\bsqrt\s*\(',
            replacement='sqrt(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Raíz cuadrada profesional',
            category='functions'
        )
        
        self.methods['sin_professional'] = UnicodeMethod(
            name='sin_professional',
            pattern=r'\bsin\s*\(',
            replacement='sin(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Seno profesional',
            category='functions'
        )
        
        self.methods['cos_professional'] = UnicodeMethod(
            name='cos_professional',
            pattern=r'\bcos\s*\(',
            replacement='cos(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Coseno profesional',
            category='functions'
        )
        
        self.methods['tan_professional'] = UnicodeMethod(
            name='tan_professional',
            pattern=r'\btan\s*\(',
            replacement='tan(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Tangente profesional',
            category='functions'
        )
        
        self.methods['ln_professional'] = UnicodeMethod(
            name='ln_professional',
            pattern=r'\bln\s*\(',
            replacement='ln(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Logaritmo natural profesional',
            category='functions'
        )
        
        self.methods['log_professional'] = UnicodeMethod(
            name='log_professional',
            pattern=r'\blog\s*\(',
            replacement='log(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Logaritmo profesional',
            category='functions'
        )
        
        self.methods['exp_professional'] = UnicodeMethod(
            name='exp_professional',
            pattern=r'\bexp\s*\(',
            replacement='exp(',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Exponencial profesional',
            category='functions'
        )
        
        # Relaciones - Estilo Profesional
        self.methods['equals_professional'] = UnicodeMethod(
            name='equals_professional',
            pattern=r'=',
            replacement='=',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Igualdad profesional',
            category='relations'
        )
        
        self.methods['not_equals_professional'] = UnicodeMethod(
            name='not_equals_professional',
            pattern=r'!=',
            replacement='!=',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Desigualdad profesional',
            category='relations'
        )
        
        self.methods['approx_professional'] = UnicodeMethod(
            name='approx_professional',
            pattern=r'~',
            replacement='~',
            style=UnicodeStyle.PROFESSIONAL,
            priority=1,
            description='Aproximación profesional',
            category='relations'
        )
        
        logger.info(f"Inicializados {len(self.methods)} métodos Unicode profesionales")
    
    def _initialize_style_configurations(self):
        """Inicializar configuraciones de estilo"""
        
        self.style_configurations[UnicodeStyle.PROFESSIONAL] = {
            'font_family': 'Segoe UI',
            'font_size': 12,
            'color_scheme': 'professional',
            'spacing': 'normal',
            'precision': 'high',
            'formatting': 'clean'
        }
        
        self.style_configurations[UnicodeStyle.ELEGANT] = {
            'font_family': 'Times New Roman',
            'font_size': 14,
            'color_scheme': 'elegant',
            'spacing': 'enhanced',
            'precision': 'maximum',
            'formatting': 'decorative'
        }
        
        self.style_configurations[UnicodeStyle.TECHNICAL] = {
            'font_family': 'Consolas',
            'font_size': 11,
            'color_scheme': 'technical',
            'spacing': 'compact',
            'precision': 'exact',
            'formatting': 'minimal'
        }
        
        self.style_configurations[UnicodeStyle.ACADEMIC] = {
            'font_family': 'Latin Modern',
            'font_size': 12,
            'color_scheme': 'academic',
            'spacing': 'formal',
            'precision': 'scholarly',
            'formatting': 'traditional'
        }
    
    def apply_professional_unicode(self, expression: str, style: UnicodeStyle = UnicodeStyle.PROFESSIONAL) -> str:
        """Aplica métodos Unicode profesionales a una expresión"""
        
        cache_key = f"{hash(expression)}_{style.value}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = expression
        
        # Filtrar métodos por estilo
        style_methods = [method for method in self.methods.values() 
                        if method.style == style]
        
        # Ordenar por prioridad
        style_methods.sort(key=lambda x: x.priority)
        
        # Aplicar métodos en orden de prioridad
        for method in style_methods:
            try:
                if method.pattern.startswith('\\b'):
                    # Expresión regular con word boundaries
                    result = re.sub(method.pattern, method.replacement, result)
                else:
                    # Reemplazo simple
                    result = result.replace(method.pattern, method.replacement)
                
            except Exception as e:
                logger.warning(f"Error aplicando método {method.name}: {e}")
                continue
        
        # Aplicar post-procesamiento según estilo
        result = self._post_process_by_style(result, style)
        
        # Cache del resultado
        self.cache[cache_key] = result
        
        return result
    
    def _post_process_by_style(self, expression: str, style: UnicodeStyle) -> str:
        """Post-procesamiento según estilo"""
        
        if style == UnicodeStyle.PROFESSIONAL:
            # Estilo profesional: limpio y directo
            return self._apply_professional_formatting(expression)
        
        elif style == UnicodeStyle.ELEGANT:
            # Estilo elegante: con espaciado mejorado
            return self._apply_elegant_formatting(expression)
        
        elif style == UnicodeStyle.TECHNICAL:
            # Estilo técnico: preciso y compacto
            return self._apply_technical_formatting(expression)
        
        elif style == UnicodeStyle.ACADEMIC:
            # Estilo académico: formal y tradicional
            return self._apply_academic_formatting(expression)
        
        return expression
    
    def _apply_professional_formatting(self, expression: str) -> str:
        """Aplica formato profesional"""
        
        # Espaciado consistente alrededor de operadores
        expression = re.sub(r'\s*([×÷=])\s*', r' \1 ', expression)
        
        # Limpiar espacios múltiples
        expression = re.sub(r'\s+', ' ', expression).strip()
        
        return expression
    
    def _apply_elegant_formatting(self, expression: str) -> str:
        """Aplica formato elegante"""
        
        # Espaciado mejorado para legibilidad
        expression = re.sub(r'\s*([×÷=])\s*', r' \1 ', expression)
        
        # Espaciado adicional después de funciones
        expression = re.sub(r'(integral|sqrt|sin|cos|tan|ln|log|exp)(\s*\()', r'\1\2', expression)
        
        # Espaciado consistente
        expression = re.sub(r'\s+', ' ', expression).strip()
        
        return expression
    
    def _apply_technical_formatting(self, expression: str) -> str:
        """Aplica formato técnico"""
        
        # Espaciado mínimo para compacidad
        expression = re.sub(r'\s*([×÷=])\s*', r'\1', expression)
        
        # Sin espacios extra
        expression = re.sub(r'\s+', '', expression).strip()
        
        return expression
    
    def _apply_academic_formatting(self, expression: str) -> str:
        """Aplica formato académico"""
        
        # Espaciado formal
        expression = re.sub(r'\s*([×÷=])\s*', r' \1 ', expression)
        
        # Formato de funciones tradicional
        expression = re.sub(r'(integral|sqrt|sin|cos|tan|ln|log|exp)(\s*\()', r'\1\2', expression)
        
        # Espaciado académico consistente
        expression = re.sub(r'\s+', ' ', expression).strip()
        
        return expression
    
    def get_methods_by_category(self, category: str) -> List[UnicodeMethod]:
        """Obtener métodos por categoría"""
        return [method for method in self.methods.values() 
                if method.category == category]
    
    def get_methods_by_style(self, style: UnicodeStyle) -> List[UnicodeMethod]:
        """Obtener métodos por estilo"""
        return [method for method in self.methods.values() 
                if method.style == style]
    
    def add_custom_method(self, method: UnicodeMethod):
        """Añadir método personalizado"""
        self.methods[method.name] = method
        self.cache.clear()  # Limpiar cache
        logger.info(f"Método personalizado añadido: {method.name}")
    
    def remove_method(self, method_name: str) -> bool:
        """Eliminar método"""
        if method_name in self.methods:
            del self.methods[method_name]
            self.cache.clear()  # Limpiar cache
            logger.info(f"Método eliminado: {method_name}")
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema"""
        return {
            'total_methods': len(self.methods),
            'methods_by_style': {
                style.value: len(self.get_methods_by_style(style))
                for style in UnicodeStyle
            },
            'methods_by_category': {
                category: len(self.get_methods_by_category(category))
                for category in set(method.category for method in self.methods.values())
            },
            'cache_size': len(self.cache),
            'available_styles': [style.value for style in UnicodeStyle]
        }
    
    def test_conversion(self, expression: str, style: UnicodeStyle = UnicodeStyle.PROFESSIONAL) -> Dict[str, Any]:
        """Prueba de conversión"""
        original = expression
        converted = self.apply_professional_unicode(expression, style)
        
        return {
            'original': original,
            'converted': converted,
            'style': style.value,
            'changed': original != converted,
            'methods_applied': len(self.get_methods_by_style(style))
        }


# Instancia global
professional_unicode = ProfessionalUnicodeMethods()


def get_professional_unicode() -> ProfessionalUnicodeMethods:
    """Obtener instancia global de métodos Unicode profesionales"""
    return professional_unicode


# Funciones de conveniencia
def apply_professional_style(expression: str) -> str:
    """Aplica estilo profesional Unicode"""
    return professional_unicode.apply_professional_unicode(expression, UnicodeStyle.PROFESSIONAL)


def apply_elegant_style(expression: str) -> str:
    """Aplica estilo elegante Unicode"""
    return professional_unicode.apply_professional_unicode(expression, UnicodeStyle.ELEGANT)


def apply_technical_style(expression: str) -> str:
    """Aplica estilo técnico Unicode"""
    return professional_unicode.apply_professional_unicode(expression, UnicodeStyle.TECHNICAL)


def apply_academic_style(expression: str) -> str:
    """Aplica estilo académico Unicode"""
    return professional_unicode.apply_professional_unicode(expression, UnicodeStyle.ACADEMIC)


if __name__ == "__main__":
    # Demostración del sistema
    print("=== Professional Unicode Methods - Demostración ===")
    print()
    
    unicode_methods = get_professional_unicode()
    
    # Mostrar estadísticas
    stats = unicode_methods.get_statistics()
    print("Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Expresiones de prueba
    test_expressions = [
        "integrate(x**2, x)",
        "x**2 + 2*x + 1 = (x+1)**2",
        "2/3*x**3 + 3/2*x**2 - x",
        "sin(x) + cos(x) = 1",
        "integral(x**2, x) + pi/2",
        "sqrt(x**2 + 1)",
        "exp(x) + ln(x) = y"
    ]
    
    styles = [UnicodeStyle.PROFESSIONAL, UnicodeStyle.ELEGANT, UnicodeStyle.TECHNICAL, UnicodeStyle.ACADEMIC]
    
    print("Pruebas de conversión por estilo:")
    print("=" * 80)
    
    for expr in test_expressions:
        print(f"\nExpresión original: {expr}")
        print("-" * 40)
        
        for style in styles:
            result = unicode_methods.apply_professional_unicode(expr, style)
            print(f"  {style.value:12}: {result}")
    
    print()
    print("=== Demostración completada ===")

# Función para convertir a símbolo Unicode real de integral
def apply_integral_unicode_symbol(expression: str) -> str:
    """Aplica símbolo Unicode real de integral a expresiones"""
    unicode_methods = get_professional_unicode()
    
    # Reemplazar 'integrate(' y 'integral(' por 'integral('
    expression = expression.replace('integrate(', 'integral(')
    expression = expression.replace('integral(', 'integral(')
    
    return expression

#!/usr/bin/env python3
"""
Unicode Profile Manager - Sistema Centralizado de Perfiles Unicode
Maneja toda la simbología matemática con perfiles configurables para diferentes contextos
"""
import logging
import json
import os
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


class SymbolContext(Enum):
    """Contextos de uso para símbolos Unicode"""
    INPUT = "input"           # Entrada de usuario
    DISPLAY = "display"       # Visualización en pantalla
    LATEX = "latex"          # Renderizado LaTeX
    CALCULATION = "calculation" # Cálculos matemáticos
    EXPORT = "export"         # Exportación de resultados
    PRINT = "print"           # Impresión


class SymbolCategory(Enum):
    """Categorías de símbolos matemáticos"""
    INTEGRALS = "integrals"
    DERIVATIVES = "derivatives"
    OPERATORS = "operators"
    FUNCTIONS = "functions"
    CONSTANTS = "constants"
    GREEK = "greek"
    ARROWS = "arrows"
    RELATIONS = "relations"
    SETS = "sets"
    LOGIC = "logic"
    FRACTIONS = "fractions"
    SUPERSCRIPTS = "superscripts"
    SUBSCRIPTS = "subscripts"
    SPECIAL = "special"


@dataclass
class SymbolMapping:
    """Mapeo de símbolo con sus variantes por contexto"""
    name: str
    category: SymbolCategory
    latex: str
    unicode: str
    ascii: str
    description: str
    contexts: Dict[SymbolContext, str]
    priority: int = 1  # Prioridad de reemplazo (1 = más alta)


@dataclass
class UnicodeProfile:
    """Perfil de configuración Unicode"""
    name: str
    description: str
    context: SymbolContext
    enabled_symbols: List[str]
    custom_mappings: Dict[str, str]
    font_preferences: Dict[str, str]
    rendering_options: Dict[str, Any]


class UnicodeProfileManager:
    """Gestor centralizado de perfiles Unicode"""
    
    def __init__(self):
        self.profiles: Dict[str, UnicodeProfile] = {}
        self.symbol_mappings: Dict[str, SymbolMapping] = {}
        self.active_profile: Optional[str] = None
        self.cache: Dict[str, str] = {}
        
        # Inicializar símbolos y perfiles
        self._initialize_symbol_mappings()
        self._initialize_default_profiles()
        self._load_custom_profiles()
        
        logger.info("Unicode Profile Manager inicializado")
    
    def _initialize_symbol_mappings(self):
        """Inicializar todos los mapeos de símbolos"""
        
        # Integrales con símbolo Unicode real
        self.symbol_mappings.update({
            'integrate': 'integral',
            'integral': 'integral',
        })
    
    def _initialize_default_profiles(self):
        """Inicializar perfiles por defecto"""
        # Método placeholder - la implementación real está en el archivo original
        pass
    
    def _load_custom_profiles(self):
        """Cargar perfiles personalizados"""
        # Método placeholder - la implementación real está en el archivo original
        pass



# Instancia global del gestor
unicode_manager = UnicodeProfileManager()


def get_unicode_manager() -> UnicodeProfileManager:
    """Obtener instancia global del gestor Unicode"""
    return unicode_manager


# Funciones de conveniencia
def convert_to_display(expression: str) -> str:
    """Convertir expresión para visualización"""
    return unicode_manager.convert_expression(expression, SymbolContext.DISPLAY)


def convert_to_latex(expression: str) -> str:
    """Convertir expresión para LaTeX"""
    return unicode_manager.convert_expression(expression, SymbolContext.LATEX)


def convert_to_input(expression: str) -> str:
    """Convertir expresión para entrada"""
    return unicode_manager.convert_expression(expression, SymbolContext.INPUT)


def convert_to_calculation(expression: str) -> str:
    """Convertir expresión para cálculos"""
    return unicode_manager.convert_expression(expression, SymbolContext.CALCULATION)


def convert_to_export(expression: str) -> str:
    """Convertir expresión para exportación"""
    return unicode_manager.convert_expression(expression, SymbolContext.EXPORT)


def convert_to_print(expression: str) -> str:
    """Convertir expresión para impresión"""
    return unicode_manager.convert_expression(expression, SymbolContext.PRINT)


def set_profile(profile_name: str) -> bool:
    """Establecer perfil activo"""
    return unicode_manager.set_active_profile(profile_name)


def get_symbol_info(symbol_name: str) -> Optional[SymbolMapping]:
    """Obtener información de símbolo"""
    return unicode_manager.get_symbol_info(symbol_name)


def get_symbols_by_category(category: SymbolCategory) -> List[SymbolMapping]:
    """Obtener símbolos por categoría"""
    return unicode_manager.get_symbols_by_category(category)


if __name__ == "__main__":
    # Demostración del gestor de perfiles Unicode
    manager = get_unicode_manager()
    
    print("=== Unicode Profile Manager - Demostración ===")
    print()
    
    # Mostrar estadísticas
    stats = manager.get_statistics()
    print("Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Probar conversiones
    test_expressions = [
        "integrate(x**2, x)",
        "x**2 + 2*x + 1 = (x+1)**2",
        "2/3*x**3 + 3/2*x**2 - x",
        "sin(x) + cos(x) = 1",
        "integral(x**2, x) + pi/2"
    ]
    
    contexts = [SymbolContext.DISPLAY, SymbolContext.LATEX, SymbolContext.INPUT, SymbolContext.CALCULATION]
    
    print("Pruebas de conversión:")
    for expr in test_expressions:
        print(f"\nExpresión original: {expr}")
        for context in contexts:
            result = manager.convert_expression(expr, context)
            print(f"  {context.value}: {result}")
    
    print()
    print("=== Demostración completada ===")

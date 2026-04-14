# **Calculadora de Integrales Pro v4.0 - Documentación Completa**

## **Tabla de Contenidos**

1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Guía de Instalación](#guía-de-instalación)
4. [Guía de Usuario](#guía-de-usuario)
5. [Referencia de API](#referencia-de-api)
6. [Desarrollo de Plugins](#desarrollo-de-plugins)
7. [Solución de Problemas](#solución-de-problemas)
8. [Mejoras Implementadas](#mejoras-implementadas)

---

## **Introducción**

### **¿Qué es Calculadora de Integrales Pro?**

Calculadora de Integrales Pro v4.0 es una aplicación matemática profesional diseñada para el cálculo simbólico y numérico de integrales, con capacidades avanzadas de visualización, análisis y exportación.

### **Características Principales**

- **Cálculo de Integrales**: 8 métodos de integración diferentes
- **Visualización Profesional**: Gráficos interactivos con zoom y análisis
- **Análisis Avanzado**: Propiedades matemáticas completas de funciones
- **Sistema de Plugins**: Extensible mediante plugins personalizados
- **Exportación Múltiple**: Formatos de imagen, datos e informes
- **Validación de Dominio**: Prevención automática de errores
- **Recuperación de Errores**: Manejo inteligente de errores con recuperación automática
- **Optimización de Rendimiento**: Caching y resolución adaptativa

---

## **Arquitectura del Sistema**

### **Estructura de Directorios**

```
integral_app/
|-- main.py                          # Punto de entrada principal
|-- requirements.txt                 # Dependencias del proyecto
|-- docs/                            # Documentación completa
|   |-- COMPLETE_DOCUMENTATION.md    # Este archivo
|   |-- API_REFERENCE.md             # Referencia de API
|   |-- PLUGIN_DEVELOPMENT.md        # Guía de desarrollo de plugins
|-- ui/                              # Interfaz de usuario
|   |-- professional_main_window.py  # Ventana principal profesional
|   |-- enhanced_controls.py        # Controles avanzados de gráficos
|   |-- latex_renderer.py           # Renderizado LaTeX
|   |-- theme_manager.py            # Gestor de temas
|-- core/                            # Motor matemático
|   |-- integrator.py               # Motor de integración
|   |-- parser.py                   # Parser matemático
|   |-- steps_engine.py             # Motor de pasos
|   |-- advanced_analyzer.py        # Analizador avanzado de funciones
|   |-- advanced_mathematics.py     # Funcionalidades matemáticas avanzadas
|-- graph/                           # Sistema de gráficos
|   |-- plotter.py                  # Sistema de gráficos mejorado
|-- utils/                           # Utilidades
|   |-- domain_validator.py          # Validación de dominio
|   |-- error_handler.py            # Manejo avanzado de errores
|   |-- performance_optimizer.py     # Optimización de rendimiento
|   |-- export_manager.py           # Gestor de exportación
|   |-- validators.py               # Validadores
|-- plugins/                         # Sistema de plugins
|   |-- plugin_manager.py           # Gestor de plugins
|   |-- plugins/                    # Directorio de plugins
|-- data/                            # Gestión de datos
|   |-- history_manager.py          # Gestor de historial
```

### **Componentes Principales**

#### **1. ProfessionalIntegralCalculator**
Ventana principal con diseño profesional y características avanzadas:
- Layout responsivo con paneles redimensionables
- Teclado científico avanzado con 40+ símbolos
- Sistema de gráficas interactivo
- Diseño moderno con glassmorphism
- Multi-threading para UI fluida

#### **2. Motor de Integración**
Sistema completo de cálculo de integrales:
- 8 métodos de integración diferentes
- Detección automática del mejor método
- Generación de pasos detallados
- Validación de resultados

#### **3. Sistema de Gráficos**
Visualización avanzada con matplotlib:
- Gráficos interactivos con zoom y pan
- Análisis de funciones con múltiples vistas
- Animaciones y transiciones suaves
- Exportación en alta calidad

#### **4. Analizador Avanzado**
Análisis matemático completo:
- Análisis de dominio y rango
- Puntos críticos y extremos
- Monotonía y concavidad
- Asíntotas y simetría
- Propiedades numéricas

---

## **Guía de Instalación**

### **Requisitos del Sistema**

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria RAM**: 4GB mínimo (8GB recomendado)
- **Espacio en Disco**: 500MB

### **Dependencias**

```bash
pip install -r requirements.txt
```

### **Dependencias Principales**

- **sympy**: Cálculo simbólico (>= 1.12)
- **matplotlib**: Gráficos (>= 3.7.0)
- **numpy**: Computación numérica (>= 1.24.0)
- **tkinter**: Interfaz gráfica (incluido con Python)

### **Instalación Paso a Paso**

1. **Clonar el repositorio**:
```bash
git clone https://github.com/usuario/calculadora-integrales-pro.git
cd calculadora-integrales-pro
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**:
```bash
python main.py
```

### **Verificación de Instalación**

Para verificar que la instalación es correcta:

```python
# Verificar importaciones principales
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

# Verificar módulos personalizados
from core.integrator import ProfessionalIntegrator
from graph.plotter import ProfessionalPlotter
from ui.professional_main_window import ProfessionalIntegralCalculator

print("¡Instalación verificada correctamente!")
```

---

## **Guía de Usuario**

### **Interfaz Principal**

La interfaz principal se divide en varias secciones:

#### **1. Barra de Herramientas**
- Botones de acceso rápido
- Selector de métodos de integración
- Controles de visualización

#### **2. Panel de Entrada**
- Editor matemático con resaltado de sintaxis
- Configuración de variables y límites
- Validación en tiempo real

#### **3. Teclado Científico**
5 pestañas con símbolos matemáticos:
- **Básicos**: +, -, ×, ÷, ^, ()
- **Funciones**: sin, cos, tan, log, exp, sqrt
- **Símbolos**: pi, e, infinity, etc.
- **Griegas**: alpha, beta, gamma, etc.
- **Avanzados**: integral, derivada, límite, etc.

#### **4. Panel de Resultados**
- **Pestaña de Resultados**: Integral y valor numérico
- **Pestaña de Pasos**: Proceso paso a paso
- **Pestaña de Gráfico**: Visualización interactiva

### **Uso Básico**

#### **Calcular una Integral Simple**

1. **Ingresar la función**:
   ```
   x^2 + 3*x + 2
   ```

2. **Seleccionar variable**: `x`

3. **Elegir método**: `Auto` (recomendado)

4. **Hacer clic en "Calcular"**

#### **Integral Definida**

1. **Ingresar la función**: `sin(x)`

2. **Establecer límites**:
   - Límite inferior: `0`
   - Límite superior: `pi`

3. **Hacer clic en "Calcular Integral Definida"**

#### **Gráficos Interactivos**

1. **Calcular una integral**

2. **Ir a la pestaña "Gráfico"**

3. **Usar los controles**:
   - **Zoom**: Rueda del mouse o botones de zoom
   - **Pan**: Clic y arrastrar
   - **Calidad**: Selector de calidad de renderizado
   - **Exportación**: Botones de exportación rápida

### **Funciones Avanzadas**

#### **Análisis de Funciones**

1. **Calcular una integral**

2. **Hacer clic en "Análisis Completo"**

3. **Ver resultados**:
   - Dominio y rango
   - Puntos críticos
   - Monotonía y concavidad
   - Asíntotas

#### **Exportación**

1. **Preparar el gráfico o resultados**

2. **Usar el gestor de exportación**:
   - **Formatos de imagen**: PNG, SVG, PDF
   - **Datos**: JSON, CSV, Excel
   - **Informes**: HTML, LaTeX, Markdown

#### **Plugins**

1. **Ir a "Plugins" en el menú**

2. **Ver plugins disponibles**

3. **Activar/desactivar plugins**

4. **Configurar ajustes de plugins**

---

## **Referencia de API**

### **Clases Principales**

#### **ProfessionalIntegrator**

```python
class ProfessionalIntegrator:
    def integrate(self, func: str, var: str, method: str = 'auto') -> Dict:
        """
        Calcular integral
        
        Args:
            func: Función a integrar (string)
            var: Variable de integración (string)
            method: Método de integración ('auto', 'direct', 'by_parts', etc.)
            
        Returns:
            Dict con resultado, pasos y metadatos
        """
        
    def get_available_methods(self) -> List[str]:
        """Obtener métodos de integración disponibles"""
        
    def validate_function(self, func: str) -> Dict:
        """Validar sintaxis de función"""
```

#### **ProfessionalPlotter**

```python
class ProfessionalPlotter:
    def plot_interactive(self, func: sp.Expr, var: sp.Symbol, 
                        a: float, b: float, limits: Optional[Tuple] = None) -> plt.Figure:
        """
        Crear gráfico interactivo
        
        Args:
            func: Expresión sympy
            var: Variable sympy
            a: Límite inferior
            b: Límite superior
            limits: Límites de integración opcional
            
        Returns:
            Figure de matplotlib
        """
        
    def plot_with_analysis(self, func: sp.Expr, var: sp.Symbol, 
                          a: float, b: float) -> plt.Figure:
        """Crear gráfico con análisis completo"""
```

#### **AdvancedAnalyzer**

```python
class AdvancedFunctionAnalyzer:
    def analyze_function_comprehensive(self, func: sp.Expr, var: sp.Symbol, 
                                      x_range: Tuple[float, float]) -> Dict:
        """
        Análisis completo de función
        
        Returns:
            Dict con análisis de dominio, puntos críticos, etc.
        """
```

### **Funciones de Utilidad**

#### **DomainValidator**

```python
def validate_function_domain(func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> Dict:
    """Validar dominio de función y generar rangos seguros"""
```

#### **ErrorHandler**

```python
def handle_plotting_error(error: Exception, func: sp.Expr, var: sp.Symbol, 
                        x_range: Tuple[float, float]) -> Dict:
    """Manejar errores de graficación con recuperación automática"""
```

#### **PerformanceOptimizer**

```python
def optimize_plotting_params(func: sp.Expr, var: sp.Symbol, 
                           x_range: Tuple[float, float]) -> Dict:
    """Optimizar parámetros de graficación"""
```

---

## **Desarrollo de Plugins**

### **Estructura de un Plugin**

```python
from plugins.plugin_manager import PluginInterface
from typing import List, Dict, Optional

class MyPlugin(PluginInterface):
    def get_name(self) -> str:
        return "Mi Plugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Descripción de mi plugin"
    
    def get_author(self) -> str:
        return "Mi Nombre"
    
    def initialize(self, main_app) -> bool:
        """Inicializar plugin"""
        self.main_app = main_app
        return True
    
    def get_menu_items(self) -> List[Dict]:
        """Items de menú para el plugin"""
        return [
            {
                'label': 'Mi Función',
                'command': self.my_function,
                'menu': 'Plugins'
            }
        ]
    
    def my_function(self):
        """Función principal del plugin"""
        pass
```

### **Creación de Plugins**

1. **Usar el gestor de plugins**:
```python
from plugins.plugin_manager import plugin_manager

# Crear plantilla
result = plugin_manager.install_plugin_from_template("MiPlugin", "MiNombre")
```

2. **Editar el archivo del plugin**
3. **Implementar la funcionalidad deseada**
4. **Probar el plugin**

### **API de Plugins**

#### **Acceso a la Aplicación Principal**

```python
def initialize(self, main_app):
    self.main_app = main_app
    
    # Acceso al integrador
    integrator = self.main_app.integrator
    
    # Acceso al plotter
    plotter = self.main_app.plotter
    
    # Acceso a la UI
    ui = self.main_app.ui
```

#### **Menús y Diálogos**

```python
def get_menu_items(self):
    return [
        {
            'label': 'Mi Herramienta',
            'command': self.show_dialog,
            'menu': 'Plugins',
            'shortcut': 'Ctrl+M'
        }
    ]

def show_dialog(self):
    # Crear diálogo usando tkinter
    dialog = tk.Toplevel(self.main_app.root)
    # ... configurar diálogo
```

---

## **Solución de Problemas**

### **Problemas Comunes**

#### **Error: "ufunc 'isfinite' not supported"**

**Causa**: Tipos de datos incompatibles en numpy arrays

**Solución**: El sistema ahora maneja este error automáticamente con:
- Validación de tipos de datos
- Conversión automática a arrays numéricos
- Fallback a verificación manual

#### **Error: "No se puede importar matplotlib"**

**Causa**: matplotlib no está instalado

**Solución**:
```bash
pip install matplotlib
```

#### **Error: "Sintaxis inválida en f-string"**

**Causa**: Caracteres especiales en f-strings

**Solución**: El sistema usa concatenación de strings para expresiones LaTeX

#### **Rendimiento Lento**

**Causa**: Funciones complejas con alta resolución

**Solución**:
- Usar calidad 'auto' o 'media'
- Reducir rango de visualización
- Habilitar caché en configuración

### **Depuración**

#### **Activar Logging**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Verificar Dependencias**

```python
import sys
print("Python version:", sys.version)
print("Sympy version:", sp.__version__)
print("Matplotlib version:", plt.__version__)
```

#### **Probar Componentes**

```python
# Probar integrador
from core.integrator import ProfessionalIntegrator
integrator = ProfessionalIntegrator()
result = integrator.integrate("x^2", "x")
print(result)

# Probar plotter
from graph.plotter import ProfessionalPlotter
plotter = ProfessionalPlotter()
import sympy as sp
x = sp.symbols('x')
fig = plotter.plot_interactive(x**2, x, -5, 5)
plt.show()
```

---

## **Mejoras Implementadas**

### **Fase 1: Mejoras Críticas (Completado)**

#### **1. Validación de Dominio de Funciones**
- **Archivo**: `utils/domain_validator.py`
- **Funcionalidades**:
  - Detección de restricciones (logaritmos, raíces, trigonométricas)
  - Identificación de asíntotas y discontinuidades
  - Generación automática de rangos seguros
  - Validación preventiva antes de graficar

#### **2. Manejo Mejorado de Errores**
- **Archivo**: `utils/error_handler.py`
- **Funcionalidades**:
  - Análisis automático de patrones de error
  - Estrategias de recuperación automática
  - Mensajes de error amigables
  - Recuperación con reducción de rango y resolución

#### **3. Optimización de Rendimiento**
- **Archivo**: `utils/performance_optimizer.py`
- **Funcionalidades**:
  - Análisis de complejidad de funciones
  - Resolución adaptativa automática
  - Distribución inteligente de puntos
  - Caching de evaluaciones
  - Estimación de tiempo de renderizado

### **Fase 2: Mejoras a Mediano Plazo (Completado)**

#### **4. Sistema de Análisis Extendido**
- **Archivo**: `core/advanced_analyzer.py`
- **Funcionalidades**:
  - Análisis completo de propiedades matemáticas
  - Puntos críticos y extremos
  - Monotonía y concavidad
  - Asíntotas y simetría
  - Análisis numérico y estadístico

#### **5. Mejoras en Interfaz de Usuario**
- **Archivo**: `ui/enhanced_controls.py`
- **Funcionalidades**:
  - Panel de control flotante
  - Controles de zoom y pan avanzados
  - Sistema de animación
  - Historial con deshacer/rehacer
  - Toolbar mejorado

#### **6. Exportación Mejorada**
- **Archivo**: `utils/export_manager.py`
- **Funcionalidades**:
  - Múltiples formatos de exportación
  - Exportación por lotes
  - Exportación a Base64
  - Generación de informes
  - Historial de exportaciones

### **Fase 3: Funcionalidades Avanzadas (Completado)**

#### **7. Funcionalidades Matemáticas Avanzadas**
- **Archivo**: `core/advanced_mathematics.py`
- **Funcionalidades**:
  - Series de Taylor y Fourier
  - Transformada de Laplace
  - Ecuaciones diferenciales
  - Cálculo vectorial
  - Álgebra lineal

#### **8. Sistema de Plugins**
- **Archivo**: `plugins/plugin_manager.py`
- **Funcionalidades**:
  - Arquitectura extensible
  - Gestión automática de plugins
  - Validación de plugins
  - Configuración de plugins
  - Plantillas para desarrollo

#### **9. Documentación Completa**
- **Archivo**: `docs/COMPLETE_DOCUMENTATION.md`
- **Funcionalidades**:
  - Documentación completa del sistema
  - Guías de usuario y desarrollador
  - Referencia de API
  - Solución de problemas

---

## **Conclusión**

Calculadora de Integrales Pro v4.0 representa una evolución significativa desde la versión original, incorporando:

- **Estabilidad Mejorada**: Manejo robusto de errores y validación preventiva
- **Rendimiento Optimizado**: Caching y resolución adaptativa
- **Funcionalidades Extendidas**: Análisis matemático completo y cálculos avanzados
- **Experiencia de Usuario Superior**: Interfaz profesional y controles intuitivos
- **Extensibilidad**: Sistema de plugins para personalización
- **Documentación Completa**: Guías detalladas para usuarios y desarrolladores

El sistema está listo para uso en producción y puede extenderse fácilmente mediante el sistema de plugins para satisfacer necesidades específicas.

---

## **Información de Contacto y Soporte**

- **Versión**: 4.0.0
- **Última Actualización**: 2026
- **Licencia**: MIT
- **Repositorio**: GitHub
- **Soporte**: Documentación y comunidad de usuarios

---

*Esta documentación es parte del proyecto Calculadora de Integrales Pro v4.0 y está mantenida activamente.*

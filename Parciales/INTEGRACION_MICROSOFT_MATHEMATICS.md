# Integración de Microsoft Mathematics - Guía Completa

## Overview

Se ha implementado una integración completa de Microsoft Mathematics directamente en la Calculadora de Integrales PRO. Esta funcionalidad permite una entrada matemática natural y avanzada similar a la experiencia de Microsoft Mathematics.

## Características Principales

### 1. Motor Matemático Avanzado (`microsoft_math_engine.py`)

**Funcionalidades:**
- **Entrada Natural**: Escribe expresiones matemáticas como lo harías en papel
- **Conversión Inteligente**: Transforma notación matemática a SymPy automáticamente
- **Validación en Tiempo Real**: Verifica la sintaxis mientras escribes
- **Soporte Completo**: Funciones, constantes, operadores y símbolos especiales

**Notación Soportada:**
```
Potencias:        x², x³, x^2, x^5
Fracciones:       1/2, ¾, ¼, 3/4
Funciones:        sin(x), cos(x), tan(x), log(x), exp(x)
Constantes:       pi, e, infinity
Operadores:       ×, ÷, ±, ·
Integrales:       int x dx, 0 to 1 int x dx
```

### 2. Editor Matemático Avanzado (`advanced_math_editor.py`)

**Componentes:**
- **Editor Principal**: Con resaltado de sintaxis y validación
- **Barra de Herramientas**: Símbolos y funciones comunes
- **Paleta de Símbolos**: 8 categorías con 50+ símbolos matemáticos
- **Autocompletado**: Sugerencias inteligentes mientras escribes
- **Validador**: Verificación en tiempo real de expresiones

**Categorías de Símbolos:**
1. **Básicos**: +, -, ×, ÷, =, (), [], {}, <>
2. **Potencias**: ², ³, ¹, ¼, ½, ¾, ^, sqrt, nroot
3. **Griegas**: alpha, beta, gamma, delta, theta, pi, sigma, omega
4. **Funciones**: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
5. **Logaritmos**: log, ln, exp, log2, log10
6. **Cálculo**: int, d/dx, sum, prod, limit, partial
7. **Constantes**: pi, e, infinity, i
8. **Operadores**: ±, !, °, mod, gcd, lcm

## Uso del Sistema

### 1. Entrada Básica

**Ejemplos de Notación Natural:**

| Notación Natural | Equivalente SymPy | Descripción |
|------------------|-------------------|-------------|
| `x² + 2*x + 1` | `x**2 + 2*x + 1` | Polinomio cuadrático |
| `sin(x) + cos(x)` | `sin(x) + cos(x)` | Funciones trigonométricas |
| `1/(x² + 1)` | `1/(x**2 + 1)` | Fracción racional |
| `sqrt(x² + y²)` | `sqrt(x**2 + y**2)` | Raíz cuadrada |
| `exp(-x²)` | `exp(-x**2)` | Función exponencial |
| `log(x + 1)` | `log(x + 1)` | Logaritmo natural |
| `int x dx` | `integrate(x, x)` | Integral indefinida |
| `0 to 1 int x² dx` | `integrate(x**2, (x, 0, 1))` | Integral definida |

### 2. Funciones Avanzadas

**Funciones Trigonométricas:**
```
sin(x), cos(x), tan(x), cot(x), sec(x), csc(x)
asin(x), acos(x), atan(x)  # Inversas
sinh(x), cosh(x), tanh(x)  # Hiperbólicas
```

**Funciones Logarítmicas:**
```
log(x)    # Logaritmo natural
ln(x)     # Logaritmo natural (alias)
exp(x)    # Exponencial
```

**Funciones Algebraicas:**
```
sqrt(x)   # Raíz cuadrada
abs(x)    # Valor absoluto
factorial(x) # Factorial
```

### 3. Constantes Matemáticas

```
pi        # Número pi (3.14159...)
e         # Número e (2.71828...)
infinity  # Infinito
i         # Unidad imaginaria
```

### 4. Operadores Especiales

```
×         # Multiplicación
÷         # División
±         # Más-menos
·         # Multiplicación (punto)
², ³      # Potencias (superíndice)
½, ¼, ¾  # Fracciones comunes
°         # Grados (convierte a radianes)
```

## Integración con la UI Principal

### 1. Botón "Math Editor"

En la barra de herramientas principal, encontrarás el botón **"Math Editor"** que activa el modo avanzado de entrada matemática.

### 2. Editor Integrado

El editor avanzado está directamente integrado en la sección de entrada de expresiones:

- **Validación en Tiempo Real**: Muestra si la expresión es válida
- **Autocompletado**: Sugiere funciones y variables mientras escribes
- **Resaltado de Sintaxis**: Colores diferentes para funciones, números, variables
- **Paleta de Símbolos**: Acceso rápido a símbolos matemáticos

### 3. Métodos de Programación

Para desarrolladores, aquí están los métodos principales:

```python
# Inicialización
math_engine = MicrosoftMathEngine()
advanced_editor = AdvancedMathEditor(parent, callback)

# Parseo de expresiones
expr = math_engine.parse_natural_math("x² + sin(x)")

# Validación
is_valid, error = math_engine.validate_expression("x² + sin(x)")

# Información detallada
info = math_engine.get_expression_info("x² + sin(x)")

# Formateo
pretty = math_engine.format_expression(expr, 'pretty')
latex = math_engine.format_expression(expr, 'latex')
```

## Ejemplos Prácticos

### 1. Integrales Básicas

**Entrada Natural:**
```
x² + 3*x + 2
```
**Resultado:**
```
x**3/3 + 3*x**2/2 + 2*x + C
```

### 2. Funciones Trigonométricas

**Entrada Natural:**
```
sin(x) * cos(x)
```
**Resultado:**
```
sin(x)**2/2 + C
```

### 3. Funciones Exponenciales

**Entrada Natural:**
```
exp(-x²)
```
**Resultado:**
```
sqrt(pi)*erf(x)/2 + C
```

### 4. Fracciones Racionales

**Entrada Natural:**
```
1/(x² + 1)
```
**Resultado:**
```
atan(x) + C
```

### 5. Integrales Definidas

**Entrada Natural:**
```
0 to pi/2 sin(x) dx
```
**Resultado:**
```
1
```

## Características Técnicas

### 1. Motor de Parseo

El motor utiliza expresiones regulares y transformaciones secuenciales:

1. **Limpieza**: Normalización Unicode y espacios
2. **Fracciones**: Conversión de notación fraccional
3. **Potencias**: Manejo de superíndices y operador ^
4. **Funciones**: Detección automática de llamadas a funciones
5. **Integrales**: Reconocimiento de notación integral
6. **Operadores**: Reemplazo de símbolos matemáticos
7. **Multiplicación Implícita**: Adición automática de *

### 2. Validación

La validación se realiza en múltiples niveles:

- **Sintaxis**: Verificación de estructura matemática
- **Semántica**: Comprobación de funciones y variables válidas
- **Tipos**: Aseguramiento de tipos de datos correctos

### 3. Autocompletado

El sistema de autocompletado:

- **Contextual**: Sugiere basado en el contexto (función, variable, constante)
- **Inteligente**: Filtra resultados según lo que se ha escrito
- **Rápido**: Respuesta en tiempo real mientras se escribe

## Personalización

### 1. Agregar Nuevas Funciones

```python
# En microsoft_math_engine.py
self.function_mappings['mi_funcion'] = mi_funcion_sympy
```

### 2. Agregar Nuevos Símbolos

```python
# En advanced_math_editor.py
symbols = ["+", "-", "×", "÷", "mi_simbolo"]
```

### 3. Modificar Patrones

```python
# En microsoft_math_engine.py
self.function_patterns.append(r'mi_patron_regex')
```

## Solución de Problemas

### 1. Errores Comunes

**Error: "Cannot parse expression"**
- Verifica la sintaxis matemática
- Asegúrate de usar paréntesis correctamente
- Revisa que las funciones estén bien escritas

**Error: "Invalid expression"**
- Comprueba que las variables sean válidas (x, y, z, t)
- Verifica que las constantes existan (pi, e)
- Asegúrate de que los operadores sean correctos

### 2. Problemas de Visualización

**Símbolos no se muestran correctamente:**
- Verifica la codificación UTF-8
- Asegúrate de tener las fuentes matemáticas instaladas
- Reinicia la aplicación

**Autocompletado no funciona:**
- Escribe al menos 2 caracteres
- Espera un momento para que aparezcan las sugerencias
- Usa Tab o Enter para aceptar sugerencias

### 3. Rendimiento

**Lentitud al escribir:**
- El autocompletado puede causar ligera demora
- Desactiva validación si no es necesaria
- Usa expresiones más simples durante pruebas

## Extensiones Futuras

### 1. Planificado

- **Integrales Múltiples**: Soporte para dobles y triples integrales
- **Ecuaciones Diferenciales**: Entrada natural de ODEs
- **Series y Sumatorias**: Notación de series infinitas
- **Transformadas**: Laplace, Fourier, etc.
- **Geometría**: Ecuaciones de curvas y superficies

### 2. Sugerencias de Usuarios

- **Exportación a LaTeX**: Generación de código LaTeX
- **Importación desde Word**: Pegado desde Microsoft Word
- **Gestos**: Entrada manuscrita (tableta)
- **Voz**: Dictado de expresiones matemáticas

## Conclusión

La integración de Microsoft Mathematics proporciona una experiencia de entrada matemática profesional y natural que facilita enormemente el trabajo con expresiones complejas. El sistema está diseñado para ser intuitivo, potente y extensible, permitiendo a los usuarios concentrarse en las matemáticas en lugar de la sintaxis.

**Beneficios Principales:**
- **Productividad**: Entrada más rápida y natural
- **Precisión**: Menos errores de sintaxis
- **Intuitividad**: Notación matemática estándar
- **Flexibilidad**: Soporte para expresiones complejas
- **Integración**: Perfectamente integrado en la calculadora

Esta implementación representa un avance significativo en la usabilidad de herramientas matemáticas educativas y profesionales.

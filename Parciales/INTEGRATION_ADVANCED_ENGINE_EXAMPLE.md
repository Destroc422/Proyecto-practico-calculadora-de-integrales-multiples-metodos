# Ejemplo de Uso - Motor Matemático Avanzado

## Demostración Completa del Sistema

### 1. Ejecución del Programa

```bash
cd Parciales/integral_app
python main.py
```

### 2. Ejemplos de Integrales con Pasos Detallados

#### Ejemplo 1: Polinomio Simple
**Entrada:** `x**2 + 3*x + 2`

**Pasos Generados:**
1. **Análisis:** Se detecta una función polinómica en la variable x
2. **Método:** Integración Directa (Polinomios)
3. **Paso 1:** Aplicar regla de potencia: $\int x^n dx = \frac{x^{n+1}}{n+1} + C$
4. **Paso 2:** Integrar término por término
5. **Resultado:** $x^3/3 + 3*x^2/2 + 2*x + C$

**Verificación:** La derivada del resultado coincide con la función original (100% confianza)

---

#### Ejemplo 2: Función Trigonométrica
**Entrada:** `sin(x) + cos(x)`

**Pasos Generados:**
1. **Análisis:** Se detectan funciones trigonométricas
2. **Método:** Integración Trigonométrica
3. **Paso 1:** Aplicar regla trigonométrica: $\int \sin(x) dx = -\cos(x) + C$
4. **Paso 2:** Aplicar regla trigonométrica: $\int \cos(x) dx = \sin(x) + C$
5. **Resultado:** $-\cos(x) + \sin(x) + C$

**Verificación:** La derivada del resultado coincide con la función original (100% confianza)

---

#### Ejemplo 3: Función Exponencial
**Entrada:** `exp(-x**2)`

**Pasos Generados:**
1. **Análisis:** Se detecta función exponencial
2. **Método:** Integración Exponencial
3. **Paso 1:** Identificar función exponencial
4. **Paso 2:** Aplicar regla de exponenciales
5. **Resultado:** $\sqrt{\pi} \cdot \text{erf}(x)/2 + C$

**Verificación:** La derivada del resultado coincide con la función original (100% confianza)

---

#### Ejemplo 4: Fracción Racional
**Entrada:** `1/(x**2 + 1)`

**Pasos Generados:**
1. **Análisis:** Se detecta una función racional en x
2. **Método:** Integración Racional
3. **Paso 1:** Identificar forma estándar $\int \frac{1}{x^2 + a^2} dx$
4. **Paso 2:** Aplicar regla de arco tangente
5. **Resultado:** $\arctan(x) + C$

**Verificación:** La derivada del resultado coincide con la función original (100% confianza)

---

### 3. Uso del Editor Matemático Avanzado

#### Notación Natural Soportada

| Notación Natural | Resultado | Descripción |
|------------------|-----------|-------------|
| `x² + 2*x + 1` | `x**2 + 2*x + 1` | Potencias con superíndice |
| `sin(x) + cos(x)` | `sin(x) + cos(x)` | Funciones trigonométricas |
| `1/(x² + 1)` | `1/(x**2 + 1)` | Fracciones racionales |
| `sqrt(x² + y²)` | `sqrt(x**2 + y**2)` | Raíces cuadradas |
| `exp(-x²)` | `exp(-x**2)` | Funciones exponenciales |
| `log(x + 1)` | `log(x + 1)` | Logaritmos |
| `int x dx` | `integrate(x, x)` | Integrales |
| `0 to 1 int x² dx` | `integrate(x**2, (x, 0, 1))` | Integrales definidas |

#### Autocompletado

1. **Escribe** `si` y presiona **Tab** para completar `sin`
2. **Escribe** `x^` y aparecerán sugerencias de potencias
3. **Escribe** `int` y presiona **Tab** para `integrate`

#### Paleta de Símbolos

- **Básicos:** +, -, ×, ÷, =, ( ), [ ], { }
- **Potencias:** ², ³, ¹, ¼, ½, ¾, ^, sqrt
- **Griegas:** alpha, beta, gamma, delta, theta, pi, sigma, omega
- **Funciones:** sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
- **Constantes:** pi, e, infinity, i

---

### 4. Visualización de Pasos Detallados

#### Ventana de Solución

Cuando calculas una integral, el sistema muestra:

1. **Ventana Principal:** Resultado básico con método y confianza
2. **Ventana de Pasos:** Solución detallada con 3 pestañas:
   - **Pasos Detallados:** Explicación paso a paso
   - **LaTeX:** Código LaTeX para exportar
   - **Análisis:** Información técnica y verificación

#### Información Mostrada

- **Método Detectado:** Auto-detección del mejor método
- **Confianza:** Porcentaje de certeza del resultado
- **Verificación:** Validación automática por derivación
- **Pasos:** Explicación matemática detallada
- **Exportación:** Opciones para LaTeX y texto

---

### 5. Ejemplo de Código de Uso

```python
# Importar el motor avanzado
from core.advanced_math_engine import AdvancedMathEngine

# Crear instancia
engine = AdvancedMathEngine()

# Resolver integral con pasos
solution = engine.solve_integral_with_steps("x**2 + 3*x + 2", "x")

# Acceder a los resultados
print(f"Resultado: {solution['result']}")
print(f"Método: {solution['method']}")
print(f"Confianza: {solution['confidence']:.1%}")

# Mostrar pasos
for i, step in enumerate(solution['steps'], 1):
    print(f"{i}. {step['description']}")
    if step['expression']:
        print(f"   {step['expression']}")
    if step['explanation']:
        print(f"   Explicación: {step['explanation']}")

# Verificación
verification = solution['verification']
print(f"Verificación: {'Exitosa' if verification['are_equal'] else 'Fallida'}")
```

---

### 6. Características Avanzadas

#### Detección Automática de Métodos

El sistema analiza la expresión y selecciona automáticamente:

- **Polinomios** -> Integración directa
- **Productos** -> Integración por partes
- **Composición** -> Sustitución
- **Trigonométricas** -> Reglas trigonométricas
- **Exponenciales** -> Reglas exponenciales
- **Racionales** -> Fracciones parciales

#### Verificación Automática

Cada resultado se verifica automáticamente:

1. **Derivación** del resultado obtenido
2. **Comparación** con la función original
3. **Cálculo** de porcentaje de confianza
4. **Reporte** del estado de verificación

#### Caché de Resultados

- **Almacenamiento** de resultados frecuentes
- **Optimización** de tiempos de respuesta
- **Recuperación** rápida de cálculos previos

---

### 7. Integración con la UI Principal

#### Botón "Math Editor"

En la barra de herramientas principal:

1. **Activa** el editor matemático avanzado
2. **Muestra** diálogo de confirmación
3. **Habilita** entrada natural y autocompletado
4. **Integra** paleta de símbolos completa

#### Flujo de Trabajo

1. **Entrada** usando notación natural
2. **Validación** en tiempo real
3. **Cálculo** con motor avanzado
4. **Visualización** de pasos detallados
5. **Verificación** automática
6. **Exportación** de resultados

---

### 8. Casos de Prueba Recomendados

#### Para Probar el Sistema

1. **Simple:** `x**2 + 2*x + 1`
2. **Trigonométrico:** `sin(x) * cos(x)`
3. **Exponencial:** `x * exp(x)`
4. **Racional:** `1/(x**2 + 1)`
5. **Compuesto:** `sqrt(x**2 + 1)`
6. **Definido:** `0 to pi/2 sin(x) dx`

#### Resultados Esperados

- **Pasos detallados** para cada método
- **Verificación automática** >95% confianza
- **Exportación LaTeX** funcional
- **Autocompletado** trabajando correctamente

---

### 9. Solución de Problemas

#### Errores Comunes

1. **"Cannot parse expression"**
   - Verifica la sintaxis matemática
   - Usa paréntesis correctamente
   - Revisa nombres de funciones

2. **"Invalid expression"**
   - Variables válidas: x, y, z, t
   - Constantes: pi, e, infinity
   - Operadores correctos

3. **"Advanced engine failed"**
   - El sistema usa fallback automático
   - Revisa la expresión
   - Prueba con notación SymPy estándar

#### Rendimiento

- **Lentitud:** El autocompletado puede causar pequeña demora
- **Memoria:** El caché optimiza cálculos frecuentes
- **Recursos:** El motor usa SymPy como base

---

### 10. Extensiones Futuras

#### Planificado

- **Ecuaciones Diferenciales:** Entrada y solución paso a paso
- **Límites:** Cálculo y explicación de límites
- **Derivadas:** Cálculo diferencial detallado
- **Series:** Sumatorias y series infinitas

#### Sugerencias de Usuarios

- **Exportación a Word:** Integración con Microsoft Word
- **Entrada por Voz:** Dictado de expresiones matemáticas
- **Gestos:** Entrada manuscrita con tableta
- **API Externa:** Conexión con servicios en la nube

---

## Conclusión

El motor matemático avanzado proporciona una experiencia completa tipo Microsoft Math Solver:

- **Entrada Natural:** Escribe matemáticas como en papel
- **Pasos Detallados:** Explicación completa del proceso
- **Verificación Automática:** Validación de resultados
- **Exportación Múltiple:** LaTeX, texto, impresión
- **Integración Total:** Perfectamente integrado en la UI

Este sistema representa un avance significativo en la usabilidad de herramientas matemáticas educativas y profesionales.

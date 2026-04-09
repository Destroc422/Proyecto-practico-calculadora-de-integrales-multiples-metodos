# Calculadora de Integrales PRO - Paso a Paso

Una aplicación avanzada en Python para resolver integrales desde Cálculo 1 hasta Cálculo 3, con explicaciones detalladas paso a paso y visualización interactiva.

## 🚀 Características Principales

### 🎓 Niveles de Cálculo Completos

**Cálculo 1 - Integrales Básicas:**
- Integrales simples de polinomios y funciones algebraicas
- Funciones trigonométricas, exponenciales y logarítmicas
- Teorema Fundamental del Cálculo con evaluación numérica
- Identificación automática de técnicas de integración

**Cálculo 2 - Técnicas Avanzadas:**
- **Integración por sustitución:** Identificación automática de patrones u-substitution
- **Integración por partes:** Aplicación de la regla LIATE con fórmula ∫u dv = uv - ∫v du
- **Funciones racionales:** Descomposición en fracciones parciales automática
- **Integrales trigonométricas:** Aplicación de identidades y reducción de potencias

**Cálculo 3 - Multivariable:**
- **Integrales dobles:** ∫∫ f(x,y) dx dy con análisis paso a paso
- **Integrales triples:** ∫∫∫ f(x,y,z) dx dy dz
- **Visualización 3D:** Superficies y volúmenes

### 🖥️ Interfaz de Usuario Moderna
- **Diseño multi-pestañas:** Calculadora, Historial, Ejemplos
- **Panel de símbolos matemáticos:** 48 símbolos organizados por categorías
- **Entrada inteligente:** Autocompletado y validación en tiempo real
- **Visualización avanzada:** Gráficas con áreas sombreadas y límites marcados

### 📚 Características Educativas
- **Explicación paso a paso:** Cada integral se resuelve mostrando:
  - Análisis de la estructura de la función
  - Identificación del método apropiado
  - Aplicación detallada de fórmulas
  - Simplificación y resultado final
- **Sistema de historial:** Guarda y reutiliza problemas anteriores
- **Ejemplos integrados:** 20+ ejemplos clasificados por nivel
- **Ayuda contextual:** Guías interactivas y consejos

## 🛠️ Arquitectura del Sistema

### Estructura Modular
```
integral_app/
├── main.py                 # Punto de entrada
├── core/                   # Lógica matemática
│   ├── integrator.py      # Motor de integración avanzado
│   ├── parser.py          # Parser de expresiones
│   └── steps_engine.py    # Motor de explicaciones
├── ui/                     # Interfaz de usuario
│   └── main_window.py     # Ventana principal
├── graph/                  # Visualización
│   └── plotter.py         # Motor de gráficas
├── data/                   # Gestión de datos
│   └── history_manager.py # Historial de problemas
└── utils/                  # Utilidades
    └── validators.py     # Validación de entrada
```

### 🧠 Motor de Integración Avanzado

**Identificación Automática de Métodos:**
- Análisis de estructura de funciones (suma, producto, potencia)
- Detección de patrones de sustitución
- Aplicación de la regla LIATE para integración por partes
- Reconocimiento de funciones racionales y trigonométricas

**Técnicas Implementadas:**
1. **Integración directa:** Reglas básicas y tablas de integrales
2. **Sustitución:** Método u con identificación automática
3. **Por partes:** Fórmula uv - ∫v du con selección inteligente
4. **Fracciones parciales:** Descomposición automática
5. **Trigonométricas:** Identidades y reducción de potencias
6. **Multivariable:** Integrales dobles y triples

### 📊 Motor de Visualización

**Gráficas 2D:**
- Funciones con áreas sombreadas
- Límites de integración marcados
- Ejes y cuadrícula mejorada
- Leyendas informativas

**Gráficas 3D:**
- Superficies para funciones de dos variables
- Mapas de color y contornos
- Visualización de volúmenes

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación Rápida
```bash
# Clonar o descargar el proyecto
cd Parciales

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
cd integral_app
python main.py
```

### Dependencias
- **sympy>=1.11.1:** Matemáticas simbólicas y computación algebraica
- **matplotlib>=3.5.0:** Visualización de gráficas 2D/3D
- **numpy>=1.21.0:** Computación numérica de alto rendimiento
- **scipy>=1.9.0:** Funciones científicas avanzadas

## 🎯 Uso Avanzado

### Sintaxis Matemática
| Operación | Sintaxis | Ejemplo |
|-----------|----------|---------|
| Potencias | `**` | `x**2` para x² |
| Multiplicación | `*` | `2*x` para 2x |
| Fracciones | `()` | `1/(x+1)` |
| Funciones | `nombre()` | `sin(x)`, `exp(x)` |
| Constantes | `pi`, `e` | `pi/2` |

### Panel de Símbolos

**Categorías Disponibles:**
- **Básicos:** ∫ ∬ ∭ ∂ ∞ π e √ ∑ ∏
- **Operadores:** ± ≠ ≈ ≤ ≥ → ↔ ∈ ∉ ⊂ ⊃ ∪ ∩
- **Griegas:** α β γ δ ε θ λ μ π σ τ φ χ ψ ω
- **Funciones:** sin cos tan asin acos atan sinh cosh tanh log ln exp

### Ejemplos por Nivel

#### 📐 Cálculo 1
```python
# Polinomio simple
x**2 + 3*x + 2

# Función trigonométrica
sin(x) + cos(x)

# Exponencial
exp(x) + 2

# Racional simple
1/(x**2 + 1)
```

#### 🔧 Cálculo 2
```python
# Sustitución (u = x²)
2*x*cos(x**2)

# Por partes (u = x, dv = e^x dx)
x*exp(x)

# Fracciones parciales
1/(x**2 - 1)

# Trigonométrica con identidad
sin(x)**2
```

#### 🌐 Cálculo 3
```python
# Integral doble
x**2 + y**2

# Integral triple
x + y + z

# Función compuesta
exp(x*y)

# Producto trigonométrico
sin(x)*cos(y)
```

## 🔧 Características Técnicas

### Motor de Explicaciones

**Estructura de Pasos:**
1. **Análisis inicial:** Identificación de tipo y estructura
2. **Selección de método:** Justificación de la técnica elegida
3. **Aplicación paso a paso:** Detalle matemático completo
4. **Simplificación:** Proceso algebraico detallado
5. **Resultado final:** Verificación y constantes

**Formato Enriquecido:**
- Emojis para categorización visual
- Colores diferenciados por tipo de contenido
- Fórmulas en formato matemático
- Notas y consejos adicionales

### Sistema de Historial

**Funcionalidades:**
- **Almacenamiento persistente:** JSON con hasta 100 entradas
- **Metadatos completos:** Función, tipo, fecha, timestamp
- **Exportación:** Archivos de texto formateados
- **Búsqueda rápida:** Por función o tipo

### Validación y Seguridad

**Validaciones Implementadas:**
- **Sintaxis matemática:** Verificación de expresiones válidas
- **Caracteres peligrosos:** Prevención de inyección de código
- **Límites numéricos:** Verificación de rangos válidos
- **Variables permitidas:** x, y, z, t, u, v, w

## 🎨 Personalización

### Temas y Apariencia
- **Fuente monoespaciada:** Courier para expresiones matemáticas
- **Esquema de colores:** Grises suaves con acentos azules
- **Iconos emoji:** Interface moderna e intuitiva

### Configuración Avanzada
```python
# Personalizar límites de gráficas
plot_range = (-10, 10)

# Número máximo de entradas en historial
max_history_entries = 100

# Tiempo de animación de pasos (milisegundos)
step_animation_delay = 800
```

## 🚀 Rendimiento y Optimización

### Algoritmos Optimizados
- **Caching de resultados:** Evita recomputación
- **Parsing eficiente:** Expresiones pre-procesadas
- **Gráficas vectoriales:** Renderizado rápido
- **Memoria controlada:** Límites de almacenamiento

### Mejoras de Usabilidad
- **Autocompletado:** Sugerencias de funciones
- **Atajos de teclado:** Navegación rápida
- **Tooltips:** Ayuda contextual
- **Validación en tiempo real:** Feedback inmediato

## 🔮 Extensiones Futuras

### Planificado para Próximas Versiones
- [ ] **Integrales impropias:** Límites infinitos y discontinuidades
- [ ] **Series de Taylor:** Expansión y aproximación
- [ ] **Ecuaciones diferenciales:** ODEs básicas
- [ ] **Transformadas:** Laplace y Fourier
- [ ] **Coordenadas especializadas:** Polares, cilíndricas, esféricas
- [ ] **Modo educativo:** Tutoriales interactivos
- [ ] **Exportación múltiple:** PDF, LaTeX, Markdown
- [ ] **API REST:** Integración con otras aplicaciones

### Contribuciones

**Áreas de Contribución:**
- 🧮 **Nuevos métodos de integración:** Técnicas especializadas
- 🎨 **Mejoras visuales:** Temas y animaciones
- 📚 **Contenido educativo:** Ejemplos y tutoriales
- 🔧 **Optimización:** Rendimiento y memoria
- 🌐 **Internacionalización:** Múltiples idiomas

## 📄 Licencia

Este proyecto es de código abierto y disponible para uso educativo y comercial bajo licencia MIT.

## 🤝 Soporte y Comunidad

### Obtener Ayuda
1. **Documentación integrada:** Menú Ayuda en la aplicación
2. **Ejemplos interactivos:** Pestaña Ejemplos con 20+ casos
3. **Historial:** Revisa problemas resueltos anteriormente
4. **Validación:** Mensajes de error descriptivos

### Reportar Problemas
- **Errores de cálculo:** Verifica con herramientas externas
- **Problemas de interfaz:** Describe pasos para reproducir
- **Sugerencias:** Ideas para nuevas características

### Comunidad
- **GitHub:** Issues y Pull Requests
- **Foros:** Discusiones educativas
- **Tutoriales:** Videos y guías

---

**🎓 Desarrollado para estudiantes y educadores que quieren entender profundamente el proceso de integración, no solo obtener respuestas rápidas.**

**🚀 Versión PRO con características avanzadas para aprendizaje efectivo del cálculo integral.**

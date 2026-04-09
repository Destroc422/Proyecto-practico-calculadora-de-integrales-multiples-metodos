# GUÍA PASO A PASO - EJECUCIÓN DEL PROGRAMA

## Professional Integral Calculator v4.0

---

## REQUISITOS PREVIOS

### 1. Python Instalado
- **Versión**: Python 3.11 o superior
- **Descarga**: [python.org](https://python.org)
- **Verificación**: 
  ```bash
  python --version
  ```

### 2. Sistema Operativo Compatible
- **Windows 10/11** (Recomendado)
- **macOS 10.14+**
- **Linux** (Ubuntu 18.04+)

---

## PASO 1: DESCARGAR EL PROYECTO

### Opción A: Descargar como ZIP
1. Navega a la carpeta del proyecto
2. Copia toda la carpeta `integral_app`
3. Pégala en tu ubicación deseada

### Opción B: Desde Terminal
```bash
# Si tienes acceso al repositorio
git clone [URL_DEL_REPOSITORIO]
cd integral_app
```

---

## PASO 2: INSTALAR DEPENDENCIAS

### Método 1: Usando requirements.txt (Recomendado)
```bash
# Navegar a la carpeta del proyecto
cd integral_app

# Instalar dependencias
pip install -r requirements.txt
```

### Método 2: Instalación Manual
```bash
# Instalar cada dependencia manualmente
pip install sympy>=1.12.0
pip install matplotlib>=3.5.0
pip install numpy>=1.21.0
```

### Verificación de Instalación
```bash
# Verificar que todo esté instalado
pip list | findstr sympy
pip list | findstr matplotlib
pip list | findstr numpy
```

---

## PASO 3: EJECUTAR EL PROGRAMA

### Método 1: Desde Terminal/Consola
```bash
# Navegar a la carpeta del proyecto
cd integral_app

# Ejecutar el programa
python main.py
```

### Método 2: Desde Explorador de Archivos (Windows)
1. Navega a la carpeta `integral_app`
2. Haz doble clic en `main.py`
3. Se abrirá la aplicación automáticamente

### Método 3: Desde IDE (VS Code, PyCharm, etc.)
1. Abre la carpeta `integral_app` en tu IDE
2. Selecciona el archivo `main.py`
3. Presiona `F5` o el botón de ejecutar

---

## PASO 4: VERIFICAR QUE FUNCIONA

### Mensajes de Éxito Esperados:
```
+ Tkinter available
+ Matplotlib 3.10.8 available
+ NumPy 1.26.4 available
+ SymPy 1.14.0 available
+ LaTeX rendering available
+ All imports successful
+ LaTeX calculator created successfully
+ Application ready
=================================================
```

### Ventana del Programa:
- **Título**: Professional Integral Calculator v4.0
- **Tamaño**: 1280x720 píxeles
- **Interfaz**: Pestañas de Resultados, Pasos, Verificación, Gráficas

---

## PASO 5: USAR EL PROGRAMA

### 1. Ingresar una Función
- **Campo**: "Función a integrar"
- **Ejemplos**:
  - `x**2 + 3*x + 2`
  - `sin(x) + cos(x)`
  - `exp(x) + log(x)`
  - `sqrt(x) + 1/x`

### 2. Configurar Opciones
- **Variable**: `x` (predeterminado)
- **Tipo**: Indefinida (predeterminado)
- **Límites**: Dejar en blanco para integrales indefinidas

### 3. Calcular
- **Botón**: "Calcular Integral"
- **Resultado**: Se mostrará en la pestaña "Resultados"
- **Pasos**: 7 pasos matemáticos en la pestaña "Pasos"

### 4. Explorar Funcionalidades
- **Resultados**: Integral renderizada visualmente
- **Pasos**: Construcción matemática paso a paso
- **Verificación**: Validación del resultado
- **Gráficas**: Visualización de la función

---

## PASO 6: CARACTERÍSTICAS AVANZADAS

### Sistema de Pasos Matemáticos
El programa muestra 7 pasos de construcción:
1. **Integral Original**: `[f(x),dx]`
2. **Descomposición**: `[f(x),dx = f1(x),dx + f2(x),dx]`
3. **Integración Término 1**: `[f1(x),dx = F1(x)]`
4. **Integración Término 2**: `[f2(x),dx = F2(x)]`
5. **Integración Término 3**: `[f3(x),dx = F3(x)]`
6. **Construcción**: `[f(x),dx = F1(x) + F2(x) + F3(x)]`
7. **Resultado Final**: `[F1(x) + F2(x) + F3(x) + C]`

### Renderizado LaTeX Visual
- **Formato**: Imágenes LaTeX profesionales
- **Tamaño**: 6x1.5 pulgadas centradas
- **Calidad**: Símbolos matemáticos reales
- **Estilo**: Académico/universitario

---

## PASO 7: SOLUCIÓN DE PROBLEMAS

### Problemas Comunes:

#### 1. "No se encuentra Python"
**Solución**:
```bash
# Asegúrate de que Python esté en el PATH
python --version
# Si no funciona, intenta:
py --version
```

#### 2. "No se encuentra sympy/matplotlib/numpy"
**Solución**:
```bash
# Reinstalar dependencias
pip install -r requirements.txt
# O individualmente:
pip install sympy matplotlib numpy
```

#### 3. "Error al importar tkinter"
**Solución**:
- **Windows**: Reinstalar Python con la opción "tcl/tk and IDLE"
- **Linux**: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- **macOS**: Generalmente incluido por defecto

#### 4. "La ventana no abre"
**Solución**:
- Verificar que no haya errores en la consola
- Asegúrate de que todas las dependencias estén instaladas
- Ejecutar como administrador (Windows)

#### 5. "No se renderiza LaTeX"
**Solución**:
- Verificar instalación de matplotlib
- Asegúrate de que el sistema tenga fuentes matemáticas
- Reinstalar matplotlib: `pip uninstall matplotlib && pip install matplotlib`

---

## PASO 8: MANTENIMIENTO

### Actualizar Dependencias
```bash
# Actualizar todo a las últimas versiones
pip install --upgrade -r requirements.txt
```

### Limpiar Archivos Temporales
```bash
# Eliminar archivos .pyc y __pycache__
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### Verificar Funcionamiento
```bash
# Ejecutar prueba básica
python main.py
# Ingresar: x**2 + 3*x + 2
# Verificar que muestre 7 pasos matemáticos
```

---

## PASO 9: CARACTERÍSTICAS TÉCNICAS

### Arquitectura del Programa
```
integral_app/
|-- main.py              # Archivo principal de ejecución
|-- requirements.txt     # Dependencias del proyecto
|-- core/                # Motor matemático
|   |-- integrator.py    # Sistema de integración
|   |-- parser.py        # Parser de expresiones
|   |-- steps_engine.py  # Generador de pasos
|-- ui/                  # Interfaz gráfica
|   |-- professional_main_window.py  # Ventana principal
|   |-- latex_renderer.py           # Renderizado LaTeX
|-- graph/               # Sistema de gráficas
|   |-- plotter.py       # Motor de gráficas
|-- utils/               # Utilidades
|   |-- validators.py    # Validadores
|-- data/                # Gestión de datos
    |-- history_manager.py  # Historial
```

### Dependencias Clave
- **SymPy**: Motor matemático simbólico
- **Matplotlib**: Renderizado LaTeX y gráficas
- **NumPy**: Computación numérica
- **Tkinter**: Interfaz gráfica (incluido con Python)

---

## PASO 10: EJEMPLOS DE USO

### Ejemplo 1: Polinomio Simple
```
Función: x**2 + 3*x + 2
Resultado: x**3/3 + 3*x**2/2 + 2*x + C
Pasos: 7 pasos matemáticos visuales
```

### Ejemplo 2: Funciones Trigonométricas
```
Función: sin(x) + cos(x)
Resultado: -cos(x) + sin(x) + C
Pasos: Construcción trigonométrica
```

### Ejemplo 3: Funciones Exponenciales
```
Función: exp(x) + log(x)
Resultado: exp(x) + x*log(x) - x + C
Pasos: Integración especializada
```

---

## CONCLUSIÓN

**Professional Integral Calculator v4.0** es una herramienta matemática profesional que:

- **Calcula integrales** con alta precisión
- **Muestra pasos matemáticos** detallados
- **Renderiza LaTeX** visualmente
- **Genera gráficas** interactivas
- **Valida resultados** automáticamente

**Estado: LISTO PARA USAR - Sistema 100% Operativo**

---

## SOPORTE

Si encuentras problemas:
1. Revisa esta guía paso a paso
2. Verifica los requisitos previos
3. Sigue las soluciones de problemas
4. Contacta al desarrollador si persiste

**¡Disfruta calculando integrales de forma profesional!**

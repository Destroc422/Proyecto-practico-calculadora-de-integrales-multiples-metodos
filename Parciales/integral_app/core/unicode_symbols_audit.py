#!/usr/bin/env python3
"""
Unicode Symbols Audit - Auditoría completa de símbolos Unicode matemáticos
Identifica qué símbolos faltan en el sistema
"""

# Lista completa de símbolos Unicode matemáticos por categoría
COMPREHENSIVE_UNICODE_SYMBOLS = {
    'Integrales y Cálculo': {
        'símbolos': ['\u222b', '\u222c', '\u222d', '\u2202', '\u2207', '\u2211', '\u220f', '\u2206', '\u220e'],
        'nombres': ['integral', 'doble_integral', 'triple_integral', 'parcial', 'nabla', 'suma', 'producto', 'incremento', 'integral_contorno'],
        'estado': {}
    },
    
    'Operadores Relacionales': {
        'símbolos': ['\u2248', '\u2249', '\u2260', '\u2261', '\u2262', '\u2264', '\u2265', '\u226a', '\u226b', '\u226c', '\u226d', '\u2272', '\u2273'],
        'nombres': ['aproximadamente_igual', 'no_aproximadamente_igual', 'diferente', 'idéntico', 'no_idéntico', 'menor_igual', 'mayor_igual', 'mucho_menor', 'mucho_mayor', 'entre', 'no_entre', 'menor_o_equivalente', 'mayor_o_equivalente'],
        'estado': {}
    },
    
    'Operadores Lógicos y Conjuntos': {
        'símbolos': ['\u2208', '\u2209', '\u220b', '\u220c', '\u2282', '\u2283', '\u2284', '\u2285', '\u2286', '\u2287', '\u2229', '\u222a', '\u2205', '\u2227', '\u2228'],
        'nombres': ['pertenece', 'no_pertenece', 'contiene', 'no_contiene', 'subconjunto', 'superconjunto', 'no_subconjunto', 'no_superconjunto', 'subconjunto_o_igual', 'superconjunto_o_igual', 'intersección', 'unión', 'conjunto_vacío', 'y', 'o'],
        'estado': {}
    },
    
    'Flechas e Implicaciones': {
        'símbolos': ['\u2192', '\u2194', '\u2190', '\u2191', '\u2193', '\u21d2', '\u21d4', '\u21d0', '\u21d1', '\u21a6', '\u21a4'],
        'nombres': ['flecha_derecha', 'flecha_doble', 'flecha_izquierda', 'flecha_arriba', 'flecha_abajo', 'implica', 'equivalente', 'implicado_por', 'implica_hacia_abajo', 'mapeo_a', 'mapeo_desde'],
        'estado': {}
    },
    
    'Cuantificadores': {
        'símbolos': ['\u2200', '\u2203', '\u2204'],
        'nombres': ['para_todo', 'existe', 'no_existe'],
        'estado': {}
    },
    
    'Conjuntos Numéricos': {
        'símbolos': ['\u2115', '\u2124', '\u211d', '\u211a', '\u2102', '\u2119', '\u211c'],
        'nombres': ['naturales', 'enteros', 'reales', 'racionales', 'complejos', 'primos', 'imaginarios'],
        'estado': {}
    },
    
    'Letras Griegas Minúsculas': {
        'símbolos': ['\u03b1', '\u03b2', '\u03b3', '\u03b4', '\u03b5', '\u03b6', '\u03b7', '\u03b8', '\u03b9', '\u03ba', '\u03bb', '\u03bc', '\u03bd', '\u03be', '\u03bf', '\u03c0', '\u03c1', '\u03c2', '\u03c3', '\u03c4', '\u03c5', '\u03c6', '\u03c7', '\u03c8', '\u03c9'],
        'nombres': ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'stigma', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'],
        'estado': {}
    },
    
    'Letras Griegas Mayúsculas': {
        'símbolos': ['\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039a', '\u039b', '\u039c', '\u039d', '\u039e', '\u039f', '\u03a0', '\u03a1', '\u03a3', '\u03a4', '\u03a5', '\u03a6', '\u03a7', '\u03a8', '\u03a9'],
        'nombres': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega'],
        'estado': {}
    },
    
    'Superíndices y Subíndices': {
        'símbolos': ['\u2070', '\u00b9', '\u00b2', '\u00b3', '\u2074', '\u2075', '\u2076', '\u2077', '\u2078', '\u2079', '\u2080', '\u2081', '\u2082', '\u2083', '\u2084', '\u2085', '\u2086', '\u2087', '\u2088', '\u2089'],
        'nombres': ['cero_super', 'uno_super', 'dos_super', 'tres_super', 'cuatro_super', 'cinco_super', 'seis_super', 'siete_super', 'ocho_super', 'nueve_super', 'cero_sub', 'uno_sub', 'dos_sub', 'tres_sub', 'cuatro_sub', 'cinco_sub', 'seis_sub', 'siete_sub', 'ocho_sub', 'nueve_sub'],
        'estado': {}
    },
    
    'Fracciones y Operaciones': {
        'símbolos': ['\u00d7', '\u00f7', '\u00b1', '\u2213', '\u2044', '\u2153', '\u2154', '\u2155', '\u2156', '\u2157', '\u2158', '\u2159', '\u215a', '\u215b', '\u215c', '\u215d', '\u215e', '\u215f'],
        'nombres': ['multiplicacion', 'division', 'mas_menos', 'menos_mas', 'fraccion', 'un_tercio', 'dos_tercios', 'un_cuarto', 'tres_cuartos', 'un_quinto', 'dos_quintos', 'tres_quintos', 'cuatro_quintos', 'un_sexto', 'cinco_sextos', 'un_octavo', 'tres_octavos', 'un_soleado'],
        'estado': {}
    },
    
    'Símbolos Matemáticos Especiales': {
        'símbolos': ['\u221e', '\u221a', '\u221b', '\u221c', '\u2220', '\u2221', '\u223c', '\u223d', '\u2250', '\u2252', '\u2253', '\u2260', '\u2261', '\u2264', '\u2265'],
        'nombres': ['infinito', 'raiz_cuadrada', 'raiz_cubica', 'raiz_cuarta', 'angulo', 'angulo_medido', 'tilde', 'igual_tilde', 'diferente_definido', 'aproximadamente_igual_definido', 'realmente_igual_a', 'diferente', 'identico', 'menor_igual', 'mayor_igual'],
        'estado': {}
    },
    
    'Constantes y Funciones': {
        'símbolos': ['\u03c0', '\u03b8', '\u03c6', '\u03b5', '\u2135', '\u2136', '\u2137'],
        'nombres': ['pi', 'theta', 'phi', 'epsilon', 'aleph_cero', 'aleph_uno', 'aleph_dos'],
        'estado': {}
    }
}

def audit_current_system():
    """
    Audita el sistema actual para identificar símbolos faltantes
    """
    print("=== AUDITORÍA COMPLETA DE SÍMBOLOS UNICODE MATEMÁTICOS ===")
    print()
    
    # Símbolos actualmente implementados (basado en el análisis del código)
    current_symbols = set()
    
    # Del motor matemático
    from microsoft_math_engine import MicrosoftMathEngine
    try:
        engine = MicrosoftMathEngine()
        current_symbols.update(engine.symbol_mappings.keys())
    except:
        pass
    
    # Del teclado científico
    try:
        with open('../ui/scientific_keypad.py', 'r', encoding='utf-8') as f:
            keypad_content = f.read()
            # Extraer símbolos Unicode del teclado
            import re
            unicode_matches = re.findall(r'\(\'([^\']*)\',', keypad_content)
            current_symbols.update(unicode_matches)
    except:
        pass
    
    print(f"Símbolos actualmente implementados: {len(current_symbols)}")
    print()
    
    # Analizar cada categoría
    total_missing = 0
    total_symbols = 0
    
    for categoria, info in COMPREHENSIVE_UNICODE_SYMBOLS.items():
        print(f"Categoría: {categoria}")
        print("-" * 50)
        
        categoria_missing = 0
        categoria_total = len(info['símbolos'])
        
        for i, (simbolo, nombre) in enumerate(zip(info['símbolos'], info['nombres'])):
            esta_implementado = simbolo in current_symbols
            info['estado'][nombre] = esta_implementado
            
            if not esta_implementado:
                print(f"  FALTA: {simbolo} ({nombre})")
                categoria_missing += 1
                total_missing += 1
            else:
                print(f"  OK:    {simbolo} ({nombre})")
            
            total_symbols += 1
        
        print(f"  Estado: {categoria_total - categoria_missing}/{categoria_total} implementados")
        print()
    
    print("=" * 70)
    print("RESUMEN DE AUDITORÍA")
    print("=" * 70)
    print(f"Símbolos totales analizados: {total_symbols}")
    print(f"Símbolos implementados: {total_symbols - total_missing}")
    print(f"Símbolos faltantes: {total_missing}")
    print(f"Tasa de implementación: {((total_symbols - total_missing) / total_symbols * 100):.1f}%")
    
    return COMPREHENSIVE_UNICODE_SYMBOLS

def generate_missing_symbols_additions():
    """
    Genera el código para agregar los símbolos faltantes
    """
    print("\n" + "=" * 70)
    print("CÓDIGO PARA AGREGAR SÍMBOLOS FALTANTES")
    print("=" * 70)
    
    missing_symbols = []
    
    for categoria, info in COMPREHENSIVE_UNICODE_SYMBOLS.items():
        for simbolo, nombre, estado in zip(info['símbolos'], info['nombres'], info['estado'].values()):
            if not estado:
                missing_symbols.append((simbolo, nombre, categoria))
    
    if missing_symbols:
        print("Símbolos faltantes para agregar al teclado científico:")
        print()
        
        additions = []
        for simbolo, nombre, categoria in missing_symbols:
            # Determinar el texto a insertar
            if 'integral' in nombre.lower():
                insert_text = 'int '
            elif 'suma' in nombre.lower():
                insert_text = 'sum '
            elif 'producto' in nombre.lower():
                insert_text = 'product '
            elif 'raiz' in nombre.lower():
                insert_text = 'sqrt('
            elif 'super' in nombre.lower():
                power = nombre.replace('_super', '').replace('cero', '0').replace('uno', '1').replace('dos', '2').replace('tres', '3').replace('cuatro', '4').replace('cinco', '5').replace('seis', '6').replace('siete', '7').replace('ocho', '8').replace('nueve', '9')
                insert_text = f'**{power}'
            elif 'sub' in nombre.lower():
                insert_text = f'_sub'  # Necesitará manejo especial
            elif 'pertenece' in nombre.lower():
                insert_text = 'in '
            elif 'infinito' in nombre.lower():
                insert_text = 'infinity '
            elif nombre in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']:
                insert_text = f'{nombre} '
            else:
                insert_text = f'{simbolo} '
            
            additions.append(f"            ('{simbolo}', '{insert_text}'),")
        
        print("Para agregar al teclado científico (scientific_keypad.py):")
        print("Agrega estas líneas a la lista unicode_symbols:")
        print()
        for addition in additions:
            print(addition)
        
        print("\nPara agregar al motor matemático (microsoft_math_engine.py):")
        print("Agrega estos mapeos a symbol_mappings:")
        print()
        
        engine_additions = []
        for simbolo, nombre, categoria in missing_symbols:
            if nombre in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']:
                engine_additions.append(f"            '{nombre}': sp.{nombre},")
            elif 'infinito' in nombre.lower():
                engine_additions.append("            'infinito': sp.oo,")
            elif 'pi' in nombre.lower():
                engine_additions.append("            'pi': sp.pi,")
            else:
                engine_additions.append(f"            '{simbolo}': '{simbolo}',")
        
        for addition in engine_additions:
            print(addition)
    
    else:
        print("¡Todos los símbolos ya están implementados!")

if __name__ == "__main__":
    # Ejecutar auditoría
    symbols_data = audit_current_system()
    
    # Generar adiciones
    generate_missing_symbols_additions()

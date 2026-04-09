import sympy as sp
from typing import List, Tuple, Dict, Any

class StepsEngine:
    
    def __init__(self):
        self.C = sp.Symbol('C')
    
    def get_comprehensive_steps(self, func, var, method=None, limits=None) -> List[Dict[str, Any]]:
        """Genera pasos matemáticos de construcción para resolver una integral"""
        steps = []
        
        # Paso 0: Integral original
        steps.append({
            "type": "integral",
            "title": "",
            "content": f"\\int {func} d{var}",
            "latex": f"\\int {func} d{var}"
        })
        
        if limits:
            steps[-1]["content"] = f"\\int_{{{limits[0]}}}^{{{limits[1]}}} {func} d{var}"
            steps[-1]["latex"] = f"\\int_{{{limits[0]}}}^{{{limits[1]}}} {func} d{var}"
        
        # Paso 1: Descomposición de términos
        decomposition_steps = self._get_decomposition_steps(func, var)
        steps.extend(decomposition_steps)
        
        # Paso 2: Aplicación de reglas de integración
        integration_steps = self._get_integration_construction_steps(func, var)
        steps.extend(integration_steps)
        
        # Paso 3: Construcción del resultado final
        construction_steps = self._get_result_construction_steps(func, var)
        steps.extend(construction_steps)
        
        # Paso 4: Resultado final
        final_result = self._get_final_result_expression(func, var)
        steps.append({
            "type": "result",
            "title": "",
            "content": final_result,
            "latex": final_result
        })
        
        return steps
    
    def _analyze_function(self, func, var) -> Dict[str, Any]:
        """Analiza la función y determina su tipo"""
        analysis = {
            "description": "",
            "details": []
        }
        
        # Identificar estructura
        if func.is_Add:
            analysis["description"] = "La función es una suma de términos"
            terms = func.as_ordered_terms()
            analysis["details"] = [f"Término {i+1}: {term}" for i, term in enumerate(terms)]
        
        elif func.is_Mul:
            analysis["description"] = "La función es un producto de factores"
            factors = func.as_ordered_factors()
            analysis["details"] = [f"Factor {i+1}: {factor}" for i, factor in enumerate(factors)]
        
        elif func.is_Pow:
            analysis["description"] = "La función es una potencia"
            analysis["details"] = [f"Base: {func.base}", f"Exponente: {func.exp}"]
        
        else:
            analysis["description"] = "Función simple"
        
        # Identificar funciones especiales
        special_functions = []
        if func.has(sp.sin, sp.cos, sp.tan):
            special_functions.append("Trigonométrica")
        if func.has(sp.exp):
            special_functions.append("Exponencial")
        if func.has(sp.log):
            special_functions.append("Logarítmica")
        if func.is_rational_function(var):
            special_functions.append("Racional")
        
        if special_functions:
            analysis["details"].append(f"Funciones especiales: {', '.join(special_functions)}")
        
        return analysis
    
    def _get_method_description(self, method) -> Dict[str, str]:
        """Obtiene descripción del método"""
        methods = {
            "parts": {
                "description": "Integración por partes usando la fórmula ∫u dv = uv - ∫v du",
                "formula": "∫u dv = uv - ∫v du"
            },
            "substitution": {
                "description": "Integración por sustitución (método u)",
                "formula": "Si u = f(x), entonces du = f'(x) dx"
            },
            "rational": {
                "description": "Descomposición en fracciones parciales",
                "formula": "A/(x-a) + B/(x-b) + ..."
            },
            "trigonometric": {
                "description": "Usando identidades trigonométricas",
                "formula": "sin²x = (1-cos2x)/2, cos²x = (1+cos2x)/2"
            },
            "direct": {
                "description": "Integración directa usando reglas básicas",
                "formula": "∫x^n dx = x^(n+1)/(n+1) + C"
            }
        }
        
        return methods.get(method, {"description": "Método desconocido"})
    
    def _get_method_specific_steps(self, func, var, method) -> List[Dict[str, Any]]:
        """Genera pasos específicos para cada método"""
        steps = []
        
        if method == "parts":
            steps.extend(self._get_parts_steps(func, var))
        elif method == "substitution":
            steps.extend(self._get_substitution_steps(func, var))
        elif method == "rational":
            steps.extend(self._get_rational_steps(func, var))
        elif method == "trigonometric":
            steps.extend(self._get_trigonometric_steps(func, var))
        else:
            steps.extend(self._get_direct_steps(func, var))
        
        return steps
    
    def _get_parts_steps(self, func, var) -> List[Dict[str, Any]]:
        """Pasos para integración por partes"""
        steps = []
        
        steps.append({
            "type": "method_step",
            "title": "Paso 1: Aplicar regla LIATE",
            "content": "Seleccionamos u y dv según prioridad: Logarítmica > Inversa > Algebraica > Trigonométrica > Exponencial"
        })
        
        # Identificar u y dv (simplificado)
        factors = func.as_ordered_factors()
        u = None
        
        for factor in factors:
            if factor.has(sp.log):
                u = factor
                break
            elif factor.is_polynomial(var):
                u = factor
                break
        
        if u:
            dv = func / u
            du = sp.diff(u, var)
            v = sp.integrate(dv, var)
            
            steps.append({
                "type": "method_step",
                "title": "Paso 2: Identificar u y dv",
                "content": f"u = {u}, dv = {dv}",
                "details": [f"du = {du}", f"v = {v}"]
            })
            
            steps.append({
                "type": "method_step",
                "title": "Paso 3: Aplicar fórmula",
                "content": "∫u dv = uv - ∫v du",
                "details": [f"= {u}·{v} - ∫{v}·{du}"]
            })
        
        return steps
    
    def _get_substitution_steps(self, func, var) -> List[Dict[str, Any]]:
        """Pasos para integración por sustitución"""
        steps = []
        
        steps.append({
            "type": "method_step",
            "title": "Paso 1: Identificar sustitución",
            "content": "Buscamos una función u tal que du aparece en la expresión"
        })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 2: Realizar cambio de variable",
            "content": "Reemplazamos x por u y dx por du/f'(x)"
        })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 3: Integrar en términos de u",
            "content": "Integramos la nueva expresión más simple"
        })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 4: Regresar a variable original",
            "content": "Reemplazamos u por la expresión original"
        })
        
        return steps
    
    def _get_rational_steps(self, func, var) -> List[Dict[str, Any]]:
        """Pasos para fracciones parciales"""
        steps = []
        
        steps.append({
            "type": "method_step",
            "title": "Paso 1: Factorizar denominador",
            "content": "Descomponemos el denominador en factores lineales o cuadráticos"
        })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 2: Descomposición en fracciones parciales",
            "content": "Escribimos la función como suma de fracciones más simples"
        })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 3: Integrar cada fracción",
            "content": "Integramos cada término por separado usando reglas básicas"
        })
        
        return steps
    
    def _get_trigonometric_steps(self, func, var) -> List[Dict[str, Any]]:
        """Pasos para integrales trigonométricas"""
        steps = []
        
        steps.append({
            "type": "method_step",
            "title": "Paso 1: Identificar identidades útiles",
            "content": "Buscamos identidades que simplifiquen la expresión"
        })
        
        if func.has(sp.sin(var)**2) or func.has(sp.cos(var)**2):
            steps.append({
                "type": "method_step",
                "title": "Paso 2: Aplicar identidades de reducción",
                "content": "Usamos sin²x = (1-cos2x)/2 o cos²x = (1+cos2x)/2"
            })
        
        steps.append({
            "type": "method_step",
            "title": "Paso 3: Simplificar e integrar",
            "content": "Simplificamos la expresión y aplicamos reglas básicas"
        })
        
        return steps
    
    def _get_decomposition_steps(self, func, var) -> List[Dict[str, Any]]:
        """Genera pasos de descomposición matemática"""
        steps = []
        
        if func.is_Add:
            # Descomponer suma
            terms = func.as_ordered_terms()
            steps.append({
                "type": "decomposition",
                "title": "",
                "content": f"\\int {func} d{var} = " + " + ".join([f"\\int {term} d{var}" for term in terms]),
                "latex": f"\\int {func} d{var} = " + " + ".join([f"\\int {term} d{var}" for term in terms])
            })
            
        elif func.is_Mul:
            # Descomponer producto
            factors = func.as_ordered_factors()
            steps.append({
                "type": "decomposition", 
                "title": "",
                "content": f"\\int {func} d{var} = \\int " + " · ".join([str(factor) for factor in factors]) + f" d{var}",
                "latex": f"\\int {func} d{var} = \\int " + " · ".join([str(factor) for factor in factors]) + f" d{var}"
            })
            
        else:
            # Función simple
            steps.append({
                "type": "decomposition",
                "title": "",
                "content": f"\\int {func} d{var}",
                "latex": f"\\int {func} d{var}"
            })
            
        return steps
    
    def _get_integration_construction_steps(self, func, var) -> List[Dict[str, Any]]:
        """Genera pasos de construcción de integración"""
        steps = []
        
        if func.is_Add:
            terms = func.as_ordered_terms()
            for i, term in enumerate(terms):
                integrated_term = self._integrate_term(term, var)
                steps.append({
                    "type": "integration",
                    "title": "",
                    "content": f"\\int {term} d{var} = {integrated_term}",
                    "latex": f"\\int {term} d{var} = {integrated_term}"
                })
                
        elif func.is_Pow and func.exp != -1:
            # Regla de potencias
            base = func.base
            exp = func.exp
            new_exp = exp + 1
            integrated = f"\\frac{{{base}^{{{new_exp}}}}}{{{new_exp}}}"
            steps.append({
                "type": "integration",
                "title": "",
                "content": f"\\int {func} d{var} = {integrated}",
                "latex": f"\\int {func} d{var} = {integrated}"
            })
            
        else:
            # Integración directa
            integrated_term = self._integrate_term(func, var)
            steps.append({
                "type": "integration",
                "title": "",
                "content": f"\\int {func} d{var} = {integrated_term}",
                "latex": f"\\int {func} d{var} = {integrated_term}"
            })
            
        return steps
    
    def _get_result_construction_steps(self, func, var) -> List[Dict[str, Any]]:
        """Genera pasos de construcción del resultado final"""
        steps = []
        
        if func.is_Add:
            terms = func.as_ordered_terms()
            integrated_terms = [self._integrate_term(term, var) for term in terms]
            result = " + ".join(integrated_terms) + f" + {self.C}"
            
            steps.append({
                "type": "construction",
                "title": "",
                "content": f"\\int {func} d{var} = {result}",
                "latex": f"\\int {func} d{var} = {result}"
            })
            
        else:
            integrated_term = self._integrate_term(func, var)
            result = f"{integrated_term} + {self.C}"
            
            steps.append({
                "type": "construction",
                "title": "",
                "content": f"\\int {func} d{var} = {result}",
                "latex": f"\\int {func} d{var} = {result}"
            })
            
        return steps
    
    def _get_final_result_expression(self, func, var) -> str:
        """Obtiene la expresión final del resultado"""
        try:
            result = sp.integrate(func, var)
            return f"{result}"
        except:
            # Fallback a construcción manual
            if func.is_Add:
                terms = func.as_ordered_terms()
                integrated_terms = [self._integrate_term(term, var) for term in terms]
                return " + ".join(integrated_terms) + f" + {self.C}"
            else:
                integrated_term = self._integrate_term(func, var)
                return f"{integrated_term} + {self.C}"
    
    def _integrate_term(self, term, var) -> str:
        """Integra un término específico"""
        try:
            result = sp.integrate(term, var)
            return str(result)
        except:
            # Reglas básicas de integración
            if term.is_Pow and term.exp != -1:
                base = term.base
                exp = term.exp
                new_exp = exp + 1
                return f"\\frac{{{base}^{{{new_exp}}}}}{{{new_exp}}}"
            elif term.has(sp.sin):
                return f"-cos({var})"
            elif term.has(sp.cos):
                return f"sin({var})"
            elif term.has(sp.exp):
                return f"exp({var})"
            elif term.has(sp.log):
                return f"{var}·log({var}) - {var}"
            else:
                return f"\\int {term} d{var}"
    
    def _get_direct_steps(self, func, var) -> List[Dict[str, Any]]:
        """Pasos para integración directa"""
        steps = []
        
        if func.is_Add:
            steps.append({
                "type": "method_step",
                "title": "Paso 1: Aplicar propiedad de linealidad",
                "content": "∫[f(x) + g(x)] dx = ∫f(x) dx + ∫g(x) dx"
            })
            
            terms = func.as_ordered_terms()
            for i, term in enumerate(terms):
                steps.append({
                    "type": "method_step",
                    "title": f"Paso {i+2}: Integrar término {i+1}",
                    "content": f"∫{term} d{var}"
                })
        else:
            steps.append({
                "type": "method_step",
                "title": "Paso 1: Aplicar regla de integración",
                "content": "Usamos la regla apropiada para esta función"
            })
        
        return steps
    
    def _get_finalization_steps(self, func, var, limits=None) -> List[Dict[str, Any]]:
        """Pasos finales del proceso"""
        steps = []
        
        steps.append({
            "type": "finalization",
            "title": "Paso Final: Agregar constante de integración",
            "content": "Resultado: F(x) + C",
            "note": "C es la constante de integración"
        })
        
        if limits:
            steps.append({
                "type": "evaluation",
                "title": "Evaluación Definida",
                "content": f"Aplicamos el Teorema Fundamental del Cálculo:",
                "formula": f"∫{limits[0]}^{limits[1]} f(x) dx = F({limits[1]}) - F({limits[0]})"
            })
        
        return steps
    
    def get_simple_steps(self, func, var) -> List[str]:
        """Método simplificado para compatibilidad"""
        comprehensive_steps = self.get_comprehensive_steps(func, var)
        
        # Convertir a formato simple de strings
        simple_steps = []
        for step in comprehensive_steps:
            if step["type"] == "info":
                simple_steps.append(f"Integral original: ∫ {func} d{var}")
            elif step["type"] == "analysis":
                simple_steps.append(step["content"])
                simple_steps.extend(step["details"])
            elif step["type"] == "method_step":
                simple_steps.append(step["title"])
                simple_steps.append(step["content"])
                if "details" in step:
                    simple_steps.extend(step["details"])
            elif step["type"] == "finalization":
                simple_steps.append(step["content"])
        
        return simple_steps
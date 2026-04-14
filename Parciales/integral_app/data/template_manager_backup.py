"""
Mathematical Template Repository Manager
Provides a comprehensive repository of mathematical function templates
for easy access to common integrals and mathematical expressions
"""
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MathematicalTemplate:
    """Represents a mathematical function template"""

    def __init__(self, name: str, expression: str, category: str,
                 description: str = "", difficulty: str = "beginner",
                 tags: List[str] = None, latex_form: str = ""):
        self.name = name
        self.expression = expression
        self.category = category
        self.description = description
        self.difficulty = difficulty  # beginner, intermediate, advanced
        self.tags = tags or []
        self.latex_form = latex_form or expression
        self.created_date = datetime.now().isoformat()
        self.usage_count = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            'name': self.name,
            'expression': self.expression,
            'category': self.category,
            'description': self.description,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'latex_form': self.latex_form,
            'created_date': self.created_date,
            'usage_count': self.usage_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MathematicalTemplate':
        """Create template from dictionary"""
        template = cls(
            name=data['name'],
            expression=data['expression'],
            category=data['category'],
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 'beginner'),
            tags=data.get('tags', []),
            latex_form=data.get('latex_form', '')
        )
        template.created_date = data.get('created_date', datetime.now().isoformat())
        template.usage_count = data.get('usage_count', 0)
        return template


class TemplateRepository:
    """Repository for mathematical function templates"""

    def __init__(self, templates_file: str = "data/templates.json"):
        self.templates_file = templates_file
        self.ensure_data_directory()
        self.templates: List[MathematicalTemplate] = []
        self.load_templates()
        self.initialize_default_templates()

    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.templates_file), exist_ok=True)

    def load_templates(self):
        """Load templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.templates = [MathematicalTemplate.from_dict(item) for item in data]
                logger.info(f"Loaded {len(self.templates)} templates from {self.templates_file}")
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
            self.templates = []

    def save_templates(self):
        """Save templates to file"""
        try:
            data = [template.to_dict() for template in self.templates]
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.templates)} templates to {self.templates_file}")
        except Exception as e:
            logger.error(f"Error saving templates: {e}")

    def initialize_default_templates(self):
        """Initialize default mathematical templates if repository is empty"""
        if self.templates:
            return

        logger.info("Initializing default mathematical templates...")

        # Polinomiales
        self.add_template(MathematicalTemplate(
            name="Polinomio cuadrático",
            expression="x**2 + 3*x + 2",
            category="Polinomiales",
            description="Función polinomial de grado 2",
            difficulty="beginner",
            tags=["polinomio", "cuadrático", "básico"],
            latex_form="x^{2} + 3x + 2"
        ))

        self.add_template(MathematicalTemplate(
            name="Polinomio cúbico",
            expression="x**3 + 2*x**2 + x + 1",
            category="Polinomiales",
            description="Función polinomial de grado 3",
            difficulty="beginner",
            tags=["polinomio", "cúbico", "básico"],
            latex_form="x^{3} + 2x^{2} + x + 1"
        ))

        # Trigonométricas
        self.add_template(MathematicalTemplate(
            name="Seno básico",
            expression="sin(x)",
            category="Trigonométricas",
            description="Función seno básica",
            difficulty="beginner",
            tags=["trigonométrica", "seno", "básico"],
            latex_form="\\sin(x)"
        ))

        self.add_template(MathematicalTemplate(
            name="Coseno básico",
            expression="cos(x)",
            category="Trigonométricas",
            description="Función coseno básica",
            difficulty="beginner",
            tags=["trigonométrica", "coseno", "básico"],
            latex_form="\\cos(x)"
        ))

        self.add_template(MathematicalTemplate(
            name="Seno + Coseno",
            expression="sin(x) + cos(x)",
            category="Trigonométricas",
            description="Combinación de funciones trigonométricas",
            difficulty="intermediate",
            tags=["trigonométrica", "seno", "coseno", "combinación"],
            latex_form="\\sin(x) + \\cos(x)"
        ))

        # Exponenciales y Logarítmicas
        self.add_template(MathematicalTemplate(
            name="Exponencial básica",
            expression="exp(x)",
            category="Exponenciales",
            description="Función exponencial natural",
            difficulty="beginner",
            tags=["exponencial", "euler", "básico"],
            latex_form="e^{x}"
        ))

        self.add_template(MathematicalTemplate(
            name="Logaritmo natural",
            expression="log(x)",
            category="Logarítmicas",
            description="Logaritmo natural (base e)",
            difficulty="beginner",
            tags=["logaritmo", "natural", "básico"],
            latex_form="\\ln(x)"
        ))

        self.add_template(MathematicalTemplate(
            name="Exponencial compleja",
            expression="exp(-x**2)",
            category="Exponenciales",
            description="Función exponencial con argumento cuadrático",
            difficulty="intermediate",
            tags=["exponencial", "gaussiana", "avanzado"],
            latex_form="e^{-x^{2}}"
        ))

        # Racionales
        self.add_template(MathematicalTemplate(
            name="Fracción simple",
            expression="1/(x + 1)",
            category="Racionales",
            description="Fracción racional simple",
            difficulty="beginner",
            tags=["racional", "fracción", "básico"],
            latex_form="\\frac{1}{x + 1}"
        ))

        self.add_template(MathematicalTemplate(
            name="Fracción cuadrática",
            expression="1/(x**2 + 1)",
            category="Racionales",
            description="Fracción con denominador cuadrático",
            difficulty="intermediate",
            tags=["racional", "cuadrático", "trigonométrico"],
            latex_form="\\frac{1}{x^{2} + 1}"
        ))

        # Radicales
        self.add_template(MathematicalTemplate(
            name="Raíz cuadrada",
            expression="sqrt(x)",
            category="Radicales",
            description="Raíz cuadrada básica",
            difficulty="beginner",
            tags=["raíz", "cuadrada", "básico"],
            latex_form="\\sqrt{x}"
        ))

        self.add_template(MathematicalTemplate(
            name="Raíz cuadrada compleja",
            expression="sqrt(x**2 + 1)",
            category="Radicales",
            description="Raíz cuadrada de expresión cuadrática",
            difficulty="intermediate",
            tags=["raíz", "cuadrada", "trigonométrico"],
            latex_form="\\sqrt{x^{2} + 1}"
        ))

        # Integrales Definidas
        self.add_template(MathematicalTemplate(
            name="Integral definida simple",
            expression="integrate(x**2, (x, 0, 1))",
            category="Integrales Definidas",
            description="Integral definida de polinomio cuadrático",
            difficulty="intermediate",
            tags=["integral", "definida", "polinomio"],
            latex_form="\\int_{0}^{1} x^{2} \\, dx"
        ))

        # Funciones Especiales
        self.add_template(MathematicalTemplate(
            name="Error function",
            expression="erf(x)",
            category="Funciones Especiales",
            description="Función de error",
            difficulty="advanced",
            tags=["error", "especial", "estadística"],
            latex_form="\\erf(x)"
        ))

        self.save_templates()
        logger.info(f"Initialized {len(self.templates)} default templates")

    def add_template(self, template: MathematicalTemplate):
        """Add a template to the repository"""
        self.templates.append(template)
        logger.info(f"Added template: {template.name}")

    def remove_template(self, name: str) -> bool:
        """Remove a template by name"""
        for i, template in enumerate(self.templates):
            if template.name == name:
                del self.templates[i]
                self.save_templates()
                logger.info(f"Removed template: {name}")
                return True
        return False

    def get_template(self, name: str) -> Optional[MathematicalTemplate]:
        """Get a template by name"""
        for template in self.templates:
            if template.name == name:
                template.usage_count += 1
                self.save_templates()
                return template
        return None

    def get_templates_by_category(self, category: str) -> List[MathematicalTemplate]:
        """Get all templates in a category"""
        return [t for t in self.templates if t.category == category]

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(t.category for t in self.templates))

    def search_templates(self, query: str, category: str = None,
                        difficulty: str = None) -> List[MathematicalTemplate]:
        """Search templates by query, category, and difficulty"""
        results = []

        for template in self.templates:
            # Check category filter
            if category and template.category != category:
                continue

            # Check difficulty filter
            if difficulty and template.difficulty != difficulty:
                continue

            # Check search query
            if query.lower() in template.name.lower() or \
               query.lower() in template.description.lower() or \
               any(query.lower() in tag.lower() for tag in template.tags):
                results.append(template)

        return results

    def get_popular_templates(self, limit: int = 10) -> List[MathematicalTemplate]:
        """Get most popular templates by usage count"""
        return sorted(self.templates, key=lambda t: t.usage_count, reverse=True)[:limit]

    def get_recent_templates(self, limit: int = 10) -> List[MathematicalTemplate]:
        """Get most recently added templates"""
        return sorted(self.templates, key=lambda t: t.created_date, reverse=True)[:limit]

    def import_from_file(self, file_path: str) -> int:
        """Import templates from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            imported_count = 0
            for item in data:
                # Check if template already exists
                if not any(t.name == item['name'] for t in self.templates):
                    template = MathematicalTemplate.from_dict(item)
                    self.add_template(template)
                    imported_count += 1

            if imported_count > 0:
                self.save_templates()

            logger.info(f"Imported {imported_count} templates from {file_path}")
            return imported_count

        except Exception as e:
            logger.error(f"Error importing templates from {file_path}: {e}")
            return 0

    def export_to_file(self, file_path: str, category: str = None) -> int:
        """Export templates to a JSON file"""
        try:
            templates_to_export = self.templates
            if category:
                templates_to_export = [t for t in self.templates if t.category == category]

            data = [t.to_dict() for t in templates_to_export]

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Exported {len(templates_to_export)} templates to {file_path}")
            return len(templates_to_export)

        except Exception as e:
            logger.error(f"Error exporting templates to {file_path}: {e}")
            return 0


# Convenience functions
def get_template_repository() -> TemplateRepository:
    """Get the global template repository instance"""
    if not hasattr(get_template_repository, '_instance'):
        get_template_repository._instance = TemplateRepository()
    return get_template_repository._instance
<parameter name="filePath">c:\Users\Wilder\OneDrive\Documentos\GitHub\Proyecto-practico-calculadora-de-integrales-multiples-metodos\Parciales\integral_app\data\template_manager.py
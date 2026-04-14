"""
Mathematical Template Browser Widget
Provides a user-friendly interface for browsing and selecting mathematical templates
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional, Callable, List
from data.template_manager import TemplateRepository, MathematicalTemplate

logger = logging.getLogger(__name__)


class TemplateBrowser(ttk.Frame):
    """Widget for browsing mathematical function templates"""

    def __init__(self, parent, on_template_select: Optional[Callable] = None, template_repo: Optional[TemplateRepository] = None):
        super().__init__(parent)
        self.on_template_select = on_template_select
        self.template_repo = template_repo or TemplateRepository()

        # Current filters
        self.current_category = "Todas"
        self.current_difficulty = "Todas"
        self.current_search = ""

        self.create_widgets()
        self.load_templates()

    def create_widgets(self):
        """Create the template browser interface"""
        # Main container
        main_frame = ttk.LabelFrame(self, text="📚 Repositorio de Plantillas Matemáticas", padding=10)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Search and filter controls
        self.create_filter_controls(main_frame)

        # Templates list
        self.create_templates_list(main_frame)

        # Template details
        self.create_template_details(main_frame)

        # Action buttons
        self.create_action_buttons(main_frame)

    def create_filter_controls(self, parent):
        """Create search and filter controls"""
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill="x", pady=(0, 10))

        # Search
        ttk.Label(filter_frame, text="Buscar:").pack(side="left", padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)

        # Category filter
        ttk.Label(filter_frame, text="Categoría:").pack(side="left", padx=(0, 5))
        self.category_var = tk.StringVar(value="Todas")
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                         state="readonly", width=15)
        self.category_combo.pack(side="left", padx=(0, 10))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_change)

        # Difficulty filter
        ttk.Label(filter_frame, text="Dificultad:").pack(side="left", padx=(0, 5))
        self.difficulty_var = tk.StringVar(value="Todas")
        self.difficulty_combo = ttk.Combobox(filter_frame, textvariable=self.difficulty_var,
                                           state="readonly", width=12)
        self.difficulty_combo.pack(side="left")
        self.difficulty_combo.bind('<<ComboboxSelected>>', self.on_difficulty_change)

        # Update filter options
        self.update_filter_options()

    def create_templates_list(self, parent):
        """Create the templates list widget"""
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Templates treeview
        columns = ('Nombre', 'Categoría', 'Dificultad', 'Uso')
        self.templates_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)

        # Configure columns
        self.templates_tree.heading('Nombre', text='Nombre')
        self.templates_tree.heading('Categoría', text='Categoría')
        self.templates_tree.heading('Dificultad', text='Dificultad')
        self.templates_tree.heading('Uso', text='Uso')

        self.templates_tree.column('Nombre', width=200)
        self.templates_tree.column('Categoría', width=120)
        self.templates_tree.column('Dificultad', width=100)
        self.templates_tree.column('Uso', width=60)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.templates_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.templates_tree.xview)

        self.templates_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack widgets
        self.templates_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        # Bind selection event
        self.templates_tree.bind('<<TreeviewSelect>>', self.on_template_select_event)

    def create_template_details(self, parent):
        """Create template details display"""
        details_frame = ttk.LabelFrame(parent, text="Detalles de la Plantilla", padding=5)
        details_frame.pack(fill="x", pady=(0, 10))

        # Details text
        self.details_text = tk.Text(details_frame, height=4, wrap=tk.WORD,
                                  bg='#f8f9fa', relief=tk.FLAT)
        self.details_text.pack(fill="both", expand=True)

        # Make it read-only
        self.details_text.config(state='disabled')

    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill="x")

        # Load template button
        self.load_btn = ttk.Button(buttons_frame, text="📥 Cargar Plantilla",
                                 command=self.load_selected_template, state='disabled')
        self.load_btn.pack(side="left", padx=(0, 10))

        # Refresh button
        ttk.Button(buttons_frame, text="🔄 Actualizar", command=self.load_templates).pack(side="left", padx=(0, 10))

        # Statistics button
        ttk.Button(buttons_frame, text="📊 Estadísticas", command=self.show_statistics).pack(side="left")

    def update_filter_options(self):
        """Update filter combobox options"""
        categories = ["Todas"] + self.template_repo.get_categories()
        self.category_combo['values'] = categories

        difficulties = ["Todas", "beginner", "intermediate", "advanced"]
        self.difficulty_combo['values'] = difficulties

    def load_templates(self):
        """Load and display templates"""
        # Clear current items
        for item in self.templates_tree.get_children():
            self.templates_tree.delete(item)

        # Get filtered templates
        templates = self.get_filtered_templates()

        # Add to treeview
        for template in templates:
            difficulty_text = {
                'beginner': 'Principiante',
                'intermediate': 'Intermedio',
                'advanced': 'Avanzado'
            }.get(template.difficulty, template.difficulty)

            self.templates_tree.insert('', 'end', values=(
                template.name,
                template.category,
                difficulty_text,
                template.usage_count
            ))

        logger.info(f"Loaded {len(templates)} templates")

    def get_filtered_templates(self) -> List[MathematicalTemplate]:
        """Get templates based on current filters"""
        category = None if self.current_category == "Todas" else self.current_category
        difficulty = None if self.current_difficulty == "Todas" else self.current_difficulty

        if self.current_search:
            return self.template_repo.search_templates(self.current_search, category, difficulty)
        else:
            if category:
                return self.template_repo.get_templates_by_category(category)
            else:
                return self.template_repo.templates

    def on_search_change(self, event):
        """Handle search input change"""
        self.current_search = self.search_var.get()
        self.load_templates()

    def on_category_change(self, event):
        """Handle category filter change"""
        self.current_category = self.category_var.get()
        self.load_templates()

    def on_difficulty_change(self, event):
        """Handle difficulty filter change"""
        self.current_difficulty = self.difficulty_var.get()
        self.load_templates()

    def on_template_select_event(self, event):
        """Handle template selection"""
        selection = self.templates_tree.selection()
        if selection:
            item = self.templates_tree.item(selection[0])
            template_name = item['values'][0]

            template = self.template_repo.get_template(template_name)
            if template:
                self.display_template_details(template)
                self.load_btn.config(state='normal')
        else:
            self.clear_template_details()
            self.load_btn.config(state='disabled')

    def display_template_details(self, template: MathematicalTemplate):
        """Display template details"""
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)

        details = f"""Nombre: {template.name}
Categoría: {template.category}
Dificultad: {template.difficulty}
Descripción: {template.description}

Expresión: {template.expression}
LaTeX: {template.latex_form}

Etiquetas: {', '.join(template.tags)}
Usos: {template.usage_count}
Creado: {template.created_date[:10]}
"""

        self.details_text.insert('1.0', details)
        self.details_text.config(state='disabled')

    def clear_template_details(self):
        """Clear template details display"""
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', tk.END)
        self.details_text.config(state='disabled')

    def load_selected_template(self):
        """Load the selected template"""
        selection = self.templates_tree.selection()
        if not selection:
            return

        item = self.templates_tree.item(selection[0])
        template_name = item['values'][0]

        template = self.template_repo.get_template(template_name)
        if template and self.on_template_select:
            self.on_template_select(template.expression)
            messagebox.showinfo("Plantilla Cargada",
                              f"Se ha cargado la plantilla: {template.name}\n\nExpresión: {template.expression}")

    def show_statistics(self):
        """Show template usage statistics"""
        total_templates = len(self.template_repo.templates)
        categories = self.template_repo.get_categories()
        popular = self.template_repo.get_popular_templates(5)

        stats = f"""📊 Estadísticas del Repositorio

Total de plantillas: {total_templates}
Categorías: {len(categories)}

Categorías disponibles:
{chr(10).join(f"• {cat}" for cat in categories)}

Plantillas más populares:
"""

        for i, template in enumerate(popular, 1):
            stats += f"{i}. {template.name} ({template.usage_count} usos)\n"

        messagebox.showinfo("Estadísticas", stats)


class QuickTemplateSelector(ttk.Frame):
    """Quick template selector for common functions"""

    def __init__(self, parent, on_template_select: Optional[Callable] = None):
        super().__init__(parent)
        self.on_template_select = on_template_select
        self.template_repo = TemplateRepository()

        self.create_widgets()

    def create_widgets(self):
        """Create quick selector interface"""
        # Main frame
        main_frame = ttk.LabelFrame(self, text="🚀 Plantillas Rápidas", padding=5)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Common categories
        categories = ["Polinomiales", "Trigonométricas", "Exponenciales", "Racionales"]

        for category in categories:
            self.create_category_section(main_frame, category)

    def create_category_section(self, parent, category):
        """Create a section for a template category"""
        frame = ttk.LabelFrame(parent, text=f"📐 {category}", padding=5)
        frame.pack(fill="x", pady=(0, 5))

        templates = self.template_repo.get_templates_by_category(category)[:4]  # Limit to 4

        # Create buttons for templates
        for i, template in enumerate(templates):
            btn = ttk.Button(frame, text=template.name,
                           command=lambda t=template: self.select_template(t))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")

        # Configure grid
        for i in range(2):
            frame.grid_columnconfigure(i, weight=1)

    def select_template(self, template: MathematicalTemplate):
        """Select a template"""
        if self.on_template_select:
            self.on_template_select(template.expression)
            logger.info(f"Quick selected template: {template.name}")


# Convenience function to create template browser dialog
def show_template_browser_dialog(parent, on_template_select: Optional[Callable] = None):
    """Show template browser in a dialog window"""
    dialog = tk.Toplevel(parent)
    dialog.title("Repositorio de Plantillas Matemáticas")
    dialog.geometry("800x600")
    dialog.resizable(True, True)

    # Center dialog
    dialog.transient(parent)
    dialog.grab_set()

    # Create browser
    browser = TemplateBrowser(dialog, on_template_select)
    browser.pack(fill="both", expand=True, padx=10, pady=10)

    # Close button
    ttk.Button(dialog, text="Cerrar", command=dialog.destroy).pack(pady=10)

    return dialog
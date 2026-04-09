import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Gestor de temas para la aplicación"""
    
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "select_bg": "#0078D4",
                "select_fg": "#FFFFFF",
                "button_bg": "#F0F0F0",
                "button_fg": "#000000",
                "entry_bg": "#FFFFFF",
                "entry_fg": "#000000",
                "frame_bg": "#F8F9FA",
                "label_fg": "#495057",
                "success": "#28A745",
                "warning": "#FFC107",
                "error": "#DC3545",
                "info": "#17A2B8"
            },
            "dark": {
                "bg": "#1E1E1E",
                "fg": "#FFFFFF",
                "select_bg": "#404040",
                "select_fg": "#FFFFFF",
                "button_bg": "#2D2D30",
                "button_fg": "#FFFFFF",
                "entry_bg": "#2D2D30",
                "entry_fg": "#FFFFFF",
                "frame_bg": "#252526",
                "label_fg": "#CCCCCC",
                "success": "#4EC9B0",
                "warning": "#CE9178",
                "error": "#F48771",
                "info": "#75BEFF"
            }
        }
    
    def get_theme(self):
        """Obtiene el tema actual"""
        return self.themes[self.current_theme]
    
    def toggle_theme(self):
        """Cambia entre temas claro y oscuro"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        return self.current_theme
    
    def apply_theme(self, root):
        """Aplica el tema a la ventana principal"""
        theme = self.get_theme()
        root.configure(bg=theme["bg"])
        
        # Configurar estilos de ttk
        style = ttk.Style()
        
        if self.current_theme == "dark":
            # Tema oscuro
            style.theme_use('clam')
            
            # Configurar colores para tema oscuro
            style.configure('TLabel', background=theme["bg"], foreground=theme["label_fg"])
            style.configure('TButton', background=theme["button_bg"], foreground=theme["button_fg"])
            style.configure('TEntry', background=theme["entry_bg"], foreground=theme["entry_fg"])
            style.configure('TFrame', background=theme["frame_bg"])
            style.configure('TLabelframe', background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure('TLabelframe.Label', background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure('TNotebook', background=theme["bg"], foreground=theme["fg"])
            style.configure('TNotebook.Tab', background=theme["button_bg"], foreground=theme["button_fg"])
            
        else:
            # Tema claro
            style.theme_use('default')
            
            # Configurar colores para tema claro
            style.configure('TLabel', background=theme["bg"], foreground=theme["label_fg"])
            style.configure('TButton', background=theme["button_bg"], foreground=theme["button_fg"])
            style.configure('TEntry', background=theme["entry_bg"], foreground=theme["entry_fg"])
            style.configure('TFrame', background=theme["frame_bg"])
            style.configure('TLabelframe', background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure('TLabelframe.Label', background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure('TNotebook', background=theme["bg"], foreground=theme["fg"])
            style.configure('TNotebook.Tab', background=theme["button_bg"], foreground=theme["button_fg"])
        
        return theme

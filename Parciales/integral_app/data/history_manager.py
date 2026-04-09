import json
import os
from datetime import datetime
from typing import List, Dict, Any

class HistoryManager:
    def __init__(self, history_file: str = "data/history.json"):
        self.history_file = history_file
        self.ensure_data_directory()
        self.history = self.load_history()
    
    def ensure_data_directory(self):
        """Asegura que el directorio de datos exista"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Carga el historial desde el archivo"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def save_history(self):
        """Guarda el historial en el archivo"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_entry(self, function: str, integral_type: str):
        """Añade una entrada al historial"""
        entry = {
            'function': function,
            'type': integral_type,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': datetime.now().timestamp()
        }
        
        self.history.append(entry)
        
        # Mantener solo los últimos 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        self.save_history()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las entradas del historial"""
        return self.history
    
    def clear(self):
        """Limpia el historial"""
        self.history = []
        self.save_history()
    
    def export_to_file(self, filename: str = None):
        """Exporta el historial a un archivo de texto"""
        if filename is None:
            filename = f"integral_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("HISTORIAL DE INTEGRALES\n")
                f.write("=" * 50 + "\n\n")
                
                for i, entry in enumerate(self.history, 1):
                    f.write(f"{i}. Función: {entry['function']}\n")
                    f.write(f"   Tipo: {entry['type']}\n")
                    f.write(f"   Fecha: {entry['date']}\n")
                    f.write("-" * 30 + "\n")
        except Exception as e:
            raise Exception(f"No se pudo exportar el historial: {e}")

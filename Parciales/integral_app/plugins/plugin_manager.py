"""
Plugin Manager for Integral Calculator
Extensible plugin system for additional functionality
"""
import os
import sys
import json
import logging
import importlib
import inspect
from typing import Dict, List, Tuple, Optional, Any, Callable
from abc import ABC, abstractmethod
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class PluginInterface(ABC):
    """Abstract base class for all plugins"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get plugin name"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get plugin version"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get plugin description"""
        pass
    
    @abstractmethod
    def get_author(self) -> str:
        """Get plugin author"""
        pass
    
    @abstractmethod
    def initialize(self, main_app) -> bool:
        """Initialize plugin with main application reference"""
        pass
    
    @abstractmethod
    def get_menu_items(self) -> List[Dict]:
        """Get menu items to add to main application"""
        pass
    
    def cleanup(self):
        """Cleanup resources when plugin is unloaded"""
        pass
    
    def get_settings_schema(self) -> Optional[Dict]:
        """Get settings schema for plugin configuration"""
        return None
    
    def apply_settings(self, settings: Dict):
        """Apply plugin settings"""
        pass


class PluginManager:
    """Manages loading, unloading, and coordination of plugins"""
    
    def __init__(self, plugin_directory: str = None):
        """Initialize plugin manager"""
        self.plugin_directory = plugin_directory or os.path.join(os.path.dirname(__file__), 'plugins')
        self.loaded_plugins: Dict[str, PluginInterface] = {}
        self.plugin_metadata: Dict[str, Dict] = {}
        self.plugin_settings: Dict[str, Dict] = {}
        self.main_app = None
        
        # Ensure plugin directory exists
        os.makedirs(self.plugin_directory, exist_ok=True)
        
        # Load plugin settings
        self._load_plugin_settings()
        
        logger.info(f"Plugin manager initialized with directory: {self.plugin_directory}")
    
    def set_main_app(self, main_app):
        """Set reference to main application"""
        self.main_app = main_app
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directory"""
        try:
            plugins = []
            
            for item in os.listdir(self.plugin_directory):
                item_path = os.path.join(self.plugin_directory, item)
                
                # Check for Python files
                if item.endswith('.py') and not item.startswith('__'):
                    plugins.append(item[:-3])  # Remove .py extension
                
                # Check for plugin directories
                elif os.path.isdir(item_path):
                    init_file = os.path.join(item_path, '__init__.py')
                    if os.path.exists(init_file):
                        plugins.append(item)
            
            logger.info(f"Discovered {len(plugins)} plugins: {plugins}")
            return plugins
            
        except Exception as e:
            logger.error(f"Error discovering plugins: {str(e)}")
            return []
    
    def load_plugin(self, plugin_name: str) -> Dict:
        """Load a specific plugin"""
        try:
            if plugin_name in self.loaded_plugins:
                logger.warning(f"Plugin {plugin_name} is already loaded")
                return {'success': False, 'error': 'Plugin already loaded'}
            
            logger.info(f"Loading plugin: {plugin_name}")
            
            # Add plugin directory to Python path
            if self.plugin_directory not in sys.path:
                sys.path.insert(0, self.plugin_directory)
            
            # Import plugin module
            try:
                plugin_module = importlib.import_module(plugin_name)
            except ImportError as e:
                # Try loading from subdirectory
                subdirectory_path = os.path.join(self.plugin_directory, plugin_name)
                if os.path.exists(subdirectory_path):
                    sys.path.insert(0, subdirectory_path)
                    plugin_module = importlib.import_module(plugin_name)
                else:
                    raise e
            
            # Find plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(plugin_module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginInterface) and 
                    obj != PluginInterface):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                return {'success': False, 'error': 'No valid plugin class found'}
            
            # Create plugin instance
            plugin_instance = plugin_class()
            
            # Get plugin metadata
            metadata = {
                'name': plugin_instance.get_name(),
                'version': plugin_instance.get_version(),
                'description': plugin_instance.get_description(),
                'author': plugin_instance.get_author(),
                'module': plugin_name,
                'loaded_at': datetime.now().isoformat()
            }
            
            # Validate plugin
            if not self._validate_plugin(plugin_instance):
                return {'success': False, 'error': 'Plugin validation failed'}
            
            # Initialize plugin
            if self.main_app:
                init_success = plugin_instance.initialize(self.main_app)
                if not init_success:
                    return {'success': False, 'error': 'Plugin initialization failed'}
            
            # Store plugin
            self.loaded_plugins[plugin_name] = plugin_instance
            self.plugin_metadata[plugin_name] = metadata
            
            # Apply saved settings
            if plugin_name in self.plugin_settings:
                plugin_instance.apply_settings(self.plugin_settings[plugin_name])
            
            logger.info(f"Plugin {plugin_name} loaded successfully")
            return {'success': True, 'metadata': metadata}
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def unload_plugin(self, plugin_name: str) -> Dict:
        """Unload a specific plugin"""
        try:
            if plugin_name not in self.loaded_plugins:
                logger.warning(f"Plugin {plugin_name} is not loaded")
                return {'success': False, 'error': 'Plugin not loaded'}
            
            logger.info(f"Unloading plugin: {plugin_name}")
            
            plugin = self.loaded_plugins[plugin_name]
            
            # Cleanup plugin
            plugin.cleanup()
            
            # Remove from loaded plugins
            del self.loaded_plugins[plugin_name]
            del self.plugin_metadata[plugin_name]
            
            logger.info(f"Plugin {plugin_name} unloaded successfully")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def load_all_plugins(self) -> Dict:
        """Load all discovered plugins"""
        try:
            discovered_plugins = self.discover_plugins()
            results = {}
            
            for plugin_name in discovered_plugins:
                result = self.load_plugin(plugin_name)
                results[plugin_name] = result
            
            success_count = sum(1 for r in results.values() if r['success'])
            
            logger.info(f"Loaded {success_count}/{len(discovered_plugins)} plugins successfully")
            
            return {
                'total': len(discovered_plugins),
                'successful': success_count,
                'failed': len(discovered_plugins) - success_count,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error loading all plugins: {str(e)}")
            return {'error': str(e)}
    
    def unload_all_plugins(self) -> Dict:
        """Unload all loaded plugins"""
        try:
            plugin_names = list(self.loaded_plugins.keys())
            results = {}
            
            for plugin_name in plugin_names:
                result = self.unload_plugin(plugin_name)
                results[plugin_name] = result
            
            success_count = sum(1 for r in results.values() if r['success'])
            
            logger.info(f"Unloaded {success_count}/{len(plugin_names)} plugins successfully")
            
            return {
                'total': len(plugin_names),
                'successful': success_count,
                'failed': len(plugin_names) - success_count,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error unloading all plugins: {str(e)}")
            return {'error': str(e)}
    
    def get_loaded_plugins(self) -> Dict[str, Dict]:
        """Get information about loaded plugins"""
        return self.plugin_metadata.copy()
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """Get loaded plugin instance"""
        return self.loaded_plugins.get(plugin_name)
    
    def get_all_menu_items(self) -> List[Dict]:
        """Get all menu items from loaded plugins"""
        menu_items = []
        
        for plugin_name, plugin in self.loaded_plugins.items():
            try:
                plugin_menu_items = plugin.get_menu_items()
                for item in plugin_menu_items:
                    item['plugin'] = plugin_name
                    menu_items.append(item)
            except Exception as e:
                logger.error(f"Error getting menu items from plugin {plugin_name}: {str(e)}")
        
        return menu_items
    
    def execute_plugin_command(self, plugin_name: str, command: str, *args, **kwargs) -> Any:
        """Execute a command from a specific plugin"""
        try:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                raise ValueError(f"Plugin {plugin_name} not found")
            
            if hasattr(plugin, command):
                method = getattr(plugin, command)
                return method(*args, **kwargs)
            else:
                raise ValueError(f"Command {command} not found in plugin {plugin_name}")
                
        except Exception as e:
            logger.error(f"Error executing plugin command: {str(e)}")
            raise
    
    def get_plugin_settings(self, plugin_name: str) -> Optional[Dict]:
        """Get settings for a specific plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            return plugin.get_settings_schema()
        return None
    
    def update_plugin_settings(self, plugin_name: str, settings: Dict) -> bool:
        """Update settings for a specific plugin"""
        try:
            plugin = self.get_plugin(plugin_name)
            if not plugin:
                return False
            
            # Apply settings to plugin
            plugin.apply_settings(settings)
            
            # Save settings
            self.plugin_settings[plugin_name] = settings
            self._save_plugin_settings()
            
            logger.info(f"Settings updated for plugin {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating plugin settings: {str(e)}")
            return False
    
    def _validate_plugin(self, plugin: PluginInterface) -> bool:
        """Validate plugin implementation"""
        try:
            # Check required methods
            required_methods = [
                'get_name', 'get_version', 'get_description', 
                'get_author', 'initialize', 'get_menu_items'
            ]
            
            for method in required_methods:
                if not hasattr(plugin, method):
                    logger.error(f"Plugin missing required method: {method}")
                    return False
            
            # Check if method is callable
            for method in required_methods:
                if not callable(getattr(plugin, method)):
                    logger.error(f"Plugin method {method} is not callable")
                    return False
            
            # Try to get basic info
            try:
                name = plugin.get_name()
                version = plugin.get_version()
                description = plugin.get_description()
                author = plugin.get_author()
                
                if not all([name, version, description, author]):
                    logger.error("Plugin returned empty values for required info")
                    return False
                    
            except Exception as e:
                logger.error(f"Error getting plugin info: {str(e)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Plugin validation error: {str(e)}")
            return False
    
    def _load_plugin_settings(self):
        """Load plugin settings from file"""
        try:
            settings_file = os.path.join(self.plugin_directory, 'plugin_settings.json')
            
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    self.plugin_settings = json.load(f)
                    
                logger.info("Plugin settings loaded")
            else:
                self.plugin_settings = {}
                
        except Exception as e:
            logger.error(f"Error loading plugin settings: {str(e)}")
            self.plugin_settings = {}
    
    def _save_plugin_settings(self):
        """Save plugin settings to file"""
        try:
            settings_file = os.path.join(self.plugin_directory, 'plugin_settings.json')
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.plugin_settings, f, indent=2)
                
            logger.info("Plugin settings saved")
            
        except Exception as e:
            logger.error(f"Error saving plugin settings: {str(e)}")
    
    def create_plugin_template(self, plugin_name: str, author: str = "Unknown") -> str:
        """Create a template for a new plugin"""
        template = f'''"""
{plugin_name} Plugin
{plugin_name} functionality for Integral Calculator
"""

import logging
from plugins.plugin_manager import PluginInterface
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class {plugin_name.title().replace(' ', '')}Plugin(PluginInterface):
    """Plugin implementation for {plugin_name}"""
    
    def get_name(self) -> str:
        """Get plugin name"""
        return "{plugin_name}"
    
    def get_version(self) -> str:
        """Get plugin version"""
        return "1.0.0"
    
    def get_description(self) -> str:
        """Get plugin description"""
        return "{plugin_name} plugin for Integral Calculator"
    
    def get_author(self) -> str:
        """Get plugin author"""
        return "{author}"
    
    def initialize(self, main_app) -> bool:
        """Initialize plugin with main application reference"""
        try:
            self.main_app = main_app
            
            # Perform initialization tasks here
            logger.info(f"{{self.get_name()}} plugin initialized")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing {{self.get_name()}} plugin: {{str(e)}}")
            return False
    
    def get_menu_items(self) -> List[Dict]:
        """Get menu items to add to main application"""
        return [
            {{
                'label': '{plugin_name}',
                'command': self.show_{plugin_name.lower().replace(' ', '_')}_dialog,
                'menu': 'Plugins'
            }}
        ]
    
    def show_{plugin_name.lower().replace(' ', '_')}_dialog(self):
        """Show {plugin_name} dialog"""
        try:
            # Create and show your plugin dialog here
            logger.info("{{self.get_name()}} dialog shown")
            
        except Exception as e:
            logger.error(f"Error showing {{self.get_name()}} dialog: {{str(e)}}")
    
    def get_settings_schema(self) -> Optional[Dict]:
        """Get settings schema for plugin configuration"""
        return {{
            'type': 'object',
            'properties': {{
                'enabled': {{
                    'type': 'boolean',
                    'default': True,
                    'title': 'Enable {plugin_name}'
                }}
            }}
        }}
    
    def apply_settings(self, settings: Dict):
        """Apply plugin settings"""
        try:
            # Apply settings here
            logger.info(f"{{self.get_name()}} settings applied: {{settings}}")
            
        except Exception as e:
            logger.error(f"Error applying {{self.get_name()}} settings: {{str(e)}}")
    
    def cleanup(self):
        """Cleanup resources when plugin is unloaded"""
        try:
            # Cleanup resources here
            logger.info(f"{{self.get_name()}} plugin cleaned up")
            
        except Exception as e:
            logger.error(f"Error cleaning up {{self.get_name()}} plugin: {{str(e)}}")


# Plugin factory function
def create_plugin():
    """Create plugin instance"""
    return {plugin_name.title().replace(' ', '')}Plugin()


# Plugin metadata
PLUGIN_INFO = {{
    'name': '{plugin_name}',
    'version': '1.0.0',
    'description': '{plugin_name} plugin for Integral Calculator',
    'author': '{author}',
    'required_version': '4.0.0'
}}
'''
        
        return template
    
    def install_plugin_from_template(self, plugin_name: str, author: str = "Unknown") -> Dict:
        """Install a new plugin from template"""
        try:
            plugin_file = os.path.join(self.plugin_directory, f"{plugin_name.lower().replace(' ', '_')}.py")
            
            if os.path.exists(plugin_file):
                return {'success': False, 'error': 'Plugin file already exists'}
            
            template = self.create_plugin_template(plugin_name, author)
            
            with open(plugin_file, 'w', encoding='utf-8') as f:
                f.write(template)
            
            logger.info(f"Plugin template created: {plugin_file}")
            
            return {
                'success': True,
                'plugin_file': plugin_file,
                'message': f'Plugin template created successfully. Edit {plugin_file} to implement your plugin.'
            }
            
        except Exception as e:
            logger.error(f"Error creating plugin template: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_plugin_statistics(self) -> Dict:
        """Get statistics about loaded plugins"""
        try:
            stats = {
                'total_loaded': len(self.loaded_plugins),
                'plugin_directory': self.plugin_directory,
                'plugins': []
            }
            
            for plugin_name, metadata in self.plugin_metadata.items():
                plugin = self.loaded_plugins[plugin_name]
                
                plugin_stats = {
                    'name': metadata['name'],
                    'version': metadata['version'],
                    'author': metadata['author'],
                    'loaded_at': metadata['loaded_at'],
                    'has_settings': plugin.get_settings_schema() is not None,
                    'menu_items': len(plugin.get_menu_items())
                }
                
                stats['plugins'].append(plugin_stats)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting plugin statistics: {str(e)}")
            return {'error': str(e)}


# Create singleton instance
plugin_manager = PluginManager()

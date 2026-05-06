import importlib.util
import inspect
from pathlib import Path
from personal_manager.core.plugin import Plugin

def load_plugins(plugins_dir="personal_manager/plugins"):
    """
    Dynamically discovers and loads plugins from the specified directory.
    
    Plugins are expected to be in subdirectories, each containing an __init__.py 
    that exports a class inheriting from the base Plugin class.
    
    Args:
        plugins_dir (str): The path to the directory containing plugins.
        
    Returns:
        dict: A dictionary mapping plugin identifiers to instantiated Plugin objects.
    """
    plugins = {}
    plugins_path = Path(plugins_dir)
    
    if not plugins_path.exists():
        return plugins

    # Iterate through subdirectories in the plugins folder
    for item in plugins_path.iterdir():
        if item.is_dir() and not item.name.startswith("__"):
            # Try to load the module dynamically
            try:
                module_name = f"personal_manager.plugins.{item.name}"
                module = importlib.import_module(module_name)
                
                # Look for classes that implement the Plugin interface
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                        plugins[item.name] = obj()
                        break
            except Exception as e:
                print(f"Error loading plugin {item.name}: {e}")
    
    return plugins

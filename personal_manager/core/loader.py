import importlib
import inspect
import pkgutil
from personal_manager.core.plugin import Plugin
import personal_manager.plugins

def load_plugins(plugins_dir=None) -> dict:
    """
    Dynamically discovers and loads plugins from the personal_manager.plugins package.
    Works seamlessly in both interpreted source mode and frozen PyInstaller executables.
    
    Args:
        plugins_dir (str, optional): Ignored. Included for backward compatibility.
        
    Returns:
        dict: A dictionary mapping plugin identifiers to instantiated Plugin objects.
    """
    plugins = {}
    
    try:
        # pkgutil.iter_modules scans modules within personal_manager.plugins package path.
        # This handles dynamic discovery correctly inside frozen binaries/libraries.
        for module_info in pkgutil.iter_modules(personal_manager.plugins.__path__):
            if module_info.ispkg:
                try:
                    module_name = f"personal_manager.plugins.{module_info.name}"
                    module = importlib.import_module(module_name)
                    
                    # Look for classes that implement the Plugin interface
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                            plugins[module_info.name] = obj()
                            break
                except Exception as e:
                    print(f"Error loading plugin {module_info.name}: {e}")
    except Exception as e:
        print(f"Error scanning plugins package: {e}")
        
    return plugins

import tomllib
from pathlib import Path

# The configuration file is expected to be in the project root
CONFIG_FILE = Path("personal_manager.toml")

def load_config():
    """
    Loads the project configuration from the TOML file.
    
    Returns:
        dict: The configuration data. Returns a default structure if the file doesn't exist.
    """
    if not CONFIG_FILE.exists():
        return {"project": {"name": "personal-manager", "version": "0.0.1"}, "plugins": {}}
    
    with CONFIG_FILE.open("rb") as f:
        return tomllib.load(f)

def save_config(config):
    """
    Saves the configuration dictionary back to the TOML file.
    
    Note: Since tomllib is read-only, this uses a simple manual writer for the current structure.
    
    Args:
        config (dict): The configuration data to save.
    """
    # Simple manual writer for this specific structure
    with CONFIG_FILE.open("w") as f:
        f.write("[project]\n")
        f.write(f'name = "{config["project"]["name"]}"\n')
        f.write(f'version = "{config["project"]["version"]}"\n\n')
        
        f.write("[plugins]\n")
        for plugin_name, enabled in config.get("plugins", {}).items():
            val = "true" if enabled else "false"
            f.write(f"{plugin_name} = {val}\n")

def is_plugin_enabled(plugin_name):
    """
    Checks if a specific plugin is enabled in the configuration.
    
    Args:
        plugin_name (str): The identifier of the plugin.
        
    Returns:
        bool: True if enabled, False otherwise.
    """
    config = load_config()
    return config.get("plugins", {}).get(plugin_name, False)

def set_plugin_state(plugin_name, enabled):
    """
    Updates the enabled/disabled state of a plugin and saves the configuration.
    
    Args:
        plugin_name (str): The identifier of the plugin.
        enabled (bool): The new state to set.
    """
    config = load_config()
    if "plugins" not in config:
        config["plugins"] = {}
    config["plugins"][plugin_name] = enabled
    save_config(config)

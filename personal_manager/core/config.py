import tomllib
from pathlib import Path

# The configuration file is stored in a global user-specific directory
CONFIG_FILE = Path.home() / ".personal_manager" / "personal_manager.toml"

def load_config() -> dict:
    """
    Loads the project configuration from the global TOML file.
    
    Returns:
       dict: The configuration data. Returns a default structure if the file doesn't exist.
    """
    if not CONFIG_FILE.exists():
        return {"project": {"name": "personal-manager", "version": "0.0.1"}, "plugins": {}}
    
    try:
        with CONFIG_FILE.open("rb") as f:
            return tomllib.load(f)
    except Exception:
        # Fallback to default if configuration is corrupted
        return {"project": {"name": "personal-manager", "version": "0.0.1"}, "plugins": {}}

def serialize_toml(data: dict) -> str:
    """
    Serializes a dictionary into a simple flat TOML string.
    Supports only one level of nested sections (e.g. [project], [plugins]).
    """
    lines = []
    # Write top-level key-values first
    for k, v in data.items():
        if not isinstance(v, dict):
            if isinstance(v, bool):
                val_str = "true" if v else "false"
            elif isinstance(v, (int, float)):
                val_str = str(v)
            else:
                val_str = f'"{v}"'
            lines.append(f"{k} = {val_str}")
            
    # Write one-level sections
    for section_name, section_data in data.items():
        if isinstance(section_data, dict):
            lines.append(f"\n[{section_name}]")
            for k, v in section_data.items():
                if isinstance(v, bool):
                    val_str = "true" if v else "false"
                elif isinstance(v, (int, float)):
                    val_str = str(v)
                else:
                    val_str = f'"{v}"'
                lines.append(f"{k} = {val_str}")
    return "\n".join(lines) + "\n"

def save_config(config: dict) -> None:
    """
    Saves the configuration dictionary back to the TOML file.
    """
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        toml_str = serialize_toml(config)
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            f.write(toml_str)
    except Exception as e:
        print(f"Error saving configuration: {e}")

def is_plugin_enabled(plugin_name: str) -> bool:
    """
    Checks if a specific plugin is enabled in the configuration.
    """
    config = load_config()
    return config.get("plugins", {}).get(plugin_name, False)

def set_plugin_state(plugin_name: str, enabled: bool) -> None:
    """
    Updates the enabled/disabled state of a plugin and saves the configuration.
    """
    config = load_config()
    if "plugins" not in config:
        config["plugins"] = {}
    config["plugins"][plugin_name] = enabled
    save_config(config)

def ensure_first_run_setup() -> None:
    """
    Checks if the global log directory path is configured. If not, prompts the user.
    """
    config = load_config()
    if "paths" not in config:
        config["paths"] = {}
        
    if "log_dir" not in config["paths"]:
        default_log_dir = Path.home() / ".personal_manager" / "logs"
        # OS-native display path formatting
        native_default = str(default_log_dir.resolve())
        print("\n=== Personal Manager: First-Run Setup ===")
        print("Configure your storage directory for logs.\n")
        user_input = input(f"Enter directory for log files (Default: {native_default}): ").strip()
        
        if not user_input:
            log_path = native_default
        else:
            log_path = str(Path(user_input).resolve())
            
        config["paths"]["log_dir"] = log_path
        save_config(config)
        print(f"Configuration saved successfully to: {CONFIG_FILE.resolve()}")
        print("Note: This file contains all your settings and plugin configuration.")
        print("      Please do not delete or modify it directly as the application requires it to function.\n")

def get_log_dir() -> Path:
    """
    Returns the configured log directory as a Path object.
    """
    config = load_config()
    log_dir = config.get("paths", {}).get("log_dir")
    if not log_dir:
        return Path.home() / ".personal_manager" / "logs"
    return Path(log_dir)

def get_plugin_setting(plugin_name: str, key: str, default_value: str = None) -> str:
    """
    Retrieves a setting for a specific plugin from the configuration.
    """
    config = load_config()
    return config.get(plugin_name, {}).get(key, default_value)

def set_plugin_setting(plugin_name: str, key: str, value: str) -> None:
    """
    Saves a setting for a specific plugin into the configuration.
    """
    config = load_config()
    if plugin_name not in config:
        config[plugin_name] = {}
    config[plugin_name][key] = value
    save_config(config)

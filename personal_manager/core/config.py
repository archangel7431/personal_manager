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
    Verifies that the directory is writable. If not, prompts the user again.
    """
    config = load_config()
    if "paths" not in config:
        config["paths"] = {}
        
    log_path = config["paths"].get("log_dir")
    
    while True:
        if not log_path:
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
                
        # Validate log directory permissions
        try:
            path_obj = Path(log_path)
            
            # Verify home directory constraint
            if not is_path_inside_home(path_obj):
                print(f"\n[ERROR] The log directory '{log_path}' is outside your home directory.")
                print(f"For safety, paths must be located inside '{Path.home().resolve()}'.")
                log_path = None
                if "log_dir" in config["paths"]:
                    del config["paths"]["log_dir"]
                    save_config(config)
                continue
                
            path_obj.mkdir(parents=True, exist_ok=True)
            
            # Test write permission by writing/deleting a temporary file
            test_file = path_obj / ".write_test"
            test_file.touch()
            test_file.unlink()
            
            # If we get here, path is valid and writable!
            config["paths"]["log_dir"] = log_path
            save_config(config)
            print(f"Configuration saved successfully to: {CONFIG_FILE.resolve()}")
            print("Note: This file contains all your settings and plugin configuration.")
            print("      Please do not delete or modify it directly as the application requires it to function.\n")
            break
        except (PermissionError, FileNotFoundError, OSError) as e:
            print(f"\n[ERROR] The log directory '{log_path}' is not writable or could not be created.")
            print(f"Details: {e}")
            # Reset log_path to None so the loop prompts the user again
            log_path = None
            if "log_dir" in config["paths"]:
                del config["paths"]["log_dir"]
                save_config(config)

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

def is_safe_to_delete_dir(p: Path) -> bool:
    """
    Validates if a directory is safe to delete recursively.
    Prevents deletion of home directory, system root, or system folders.
    """
    try:
        resolved = p.resolve()
    except Exception:
        return False
        
    home = Path.home().resolve()
    root = Path("/").resolve()
    
    if resolved == home or resolved == root:
        return False
        
    # Standard system directories
    dangerous_dirs = [
        "/usr", "/var", "/lib", "/bin", "/sbin", "/etc", "/opt", "/boot",
        "/dev", "/proc", "/sys", "/run", "/mnt", "/media", "/srv", "/home"
    ]
    
    system_paths = set()
    for d in dangerous_dirs:
        try:
            dp = Path(d)
            if dp.exists():
                system_paths.add(dp.resolve())
        except Exception:
            pass
            
    if resolved in system_paths:
        return False
        
    # Check if resolved is a parent of home or root
    if resolved in home.parents or resolved in root.parents:
        return False
        
    return True

def find_paths_in_config(config_data: dict) -> tuple[set[Path], set[Path]]:
    """
    Recursively scans the configuration dictionary to find configured file and directory paths.
    
    Returns:
        tuple: (found_files_set, found_dirs_set)
    """
    found_files = set()
    found_dirs = set()
    
    def walk(data):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    try:
                        p = Path(v)
                        # We only clean up absolute paths that exist on disk
                        if p.exists() and p.is_absolute():
                            if p.is_file():
                                found_files.add(p.resolve())
                            elif p.is_dir():
                                found_dirs.add(p.resolve())
                    except Exception:
                        pass
                else:
                    walk(v)
        elif isinstance(data, list):
            for item in data:
                walk(item)
                
    walk(config_data)
    return found_files, found_dirs

def reset_application() -> None:
    """
    Finds and deletes all configured database files, log directories, 
    and the configuration file itself.
    """
    import shutil
    import os
    
    print("\n=== Personal Manager: Reset & Cleanup ===")
    
    # 1. Load active configuration
    config = load_config()
    
    # 2. Scan configuration for files and directories
    found_files, found_dirs = find_paths_in_config(config)
    
    # 3. Add default paths if they exist (just in case they weren't explicitly saved)
    # We resolve defaults relative to CONFIG_FILE.parent to support sandboxing during tests
    default_log_dir = CONFIG_FILE.parent / "logs"
    if default_log_dir.exists() and default_log_dir.is_dir():
        found_dirs.add(default_log_dir.resolve())
        
    default_budget_csv = CONFIG_FILE.parent / "budget.csv"
    if default_budget_csv.exists() and default_budget_csv.is_file():
        found_files.add(default_budget_csv.resolve())

    # Add the configuration file itself to the files list
    if CONFIG_FILE.exists():
        found_files.add(CONFIG_FILE.resolve())
        
    if not found_files and not found_dirs:
        print("No configuration or data files were found to clean up.")
        return
        
    # 4. Filter log dirs using safety check
    safe_dirs = {d for d in found_dirs if is_safe_to_delete_dir(d)}
    unsafe_dirs = found_dirs - safe_dirs
    
    # 5. List items to be deleted
    print("This action will permanently delete the following files and directories:")
    for f in sorted(found_files):
        print(f"  [File]      {f}")
    for d in sorted(safe_dirs):
        print(f"  [Directory] {d} (recursive)")
        
    if unsafe_dirs:
        print("\nSkipping the following directories for safety (not safe to delete recursively):")
        for d in sorted(unsafe_dirs):
            print(f"  [Skipped]   {d}")
            
    # 6. Ask for confirmation
    confirm = input("\nAre you sure you want to proceed with the deletion? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Reset cancelled.")
        return
        
    print("\nStarting cleanup...")
    
    # 7. Delete safe files
    for f in found_files:
        try:
            if f.exists():
                f.unlink()
                print(f"Deleted file: {f}")
        except Exception as e:
            print(f"Error deleting file {f}: {e}")
            
    # 8. Delete safe log directories recursively
    for d in safe_dirs:
        try:
            if d.exists() and d.is_dir():
                shutil.rmtree(d)
                print(f"Deleted directory: {d}")
        except Exception as e:
            print(f"Error deleting directory {d}: {e}")
            
    # 9. Clean up empty parent config folder
    config_parent = CONFIG_FILE.parent
    try:
        if config_parent.exists() and config_parent.is_dir():
            # Check if parent dir is now empty
            if not os.listdir(config_parent):
                config_parent.rmdir()
                print(f"Removed empty configuration folder: {config_parent.resolve()}")
    except Exception as e:
        pass
        
    print("Cleanup completed successfully. The application has been fully reset.\n")

def is_path_inside_home(p: Path) -> bool:
    """
    Checks if a path is located inside the user's home directory or its subdirectories.
    Supports both Windows and Linux/macOS.
    """
    try:
        resolved_path = p.resolve()
    except Exception:
        resolved_path = p.absolute()
        
    try:
        home = Path.home().resolve()
    except Exception:
        home = Path.home().absolute()
        
    try:
        # Check if resolved_path is home itself or is inside home
        return resolved_path == home or home in resolved_path.parents
    except Exception:
        return False

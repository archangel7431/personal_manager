import sys
import os
from personal_manager.core.loader import load_plugins
from personal_manager.core.config import is_plugin_enabled, set_plugin_state, load_config

def clear_screen():
    """
    Clears the terminal screen. Works on both Windows and Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def toggle_plugins_menu(available_plugins):
    """
    Displays an interactive menu to enable or disable available plugins.
    
    Args:
        available_plugins (dict): Dictionary of discovered plugins.
    """
    while True:
        clear_screen()
        print("=== Plugin Management ===")
        plugin_keys = list(available_plugins.keys())
        for i, key in enumerate(plugin_keys, 1):
            enabled = is_plugin_enabled(key)
            status = "[ENABLED]" if enabled else "[DISABLED]"
            print(f"{i}. {available_plugins[key].name} {status}")
        
        print("\nEnter number to toggle, or 'q' to return.")
        choice = input("Choice: ")
        
        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(plugin_keys):
                key = plugin_keys[idx]
                current_state = is_plugin_enabled(key)
                # Toggle the enabled state and save to config
                set_plugin_state(key, not current_state)
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input.")

def main():
    """
    Main entry point for the Personal Manager CLI.
    Handles plugin discovery, state management, and plugin execution.
    """
    # Ensure config exists and load it
    config = load_config()
    
    # Discover all available plugins in the plugins directory
    available_plugins = load_plugins()
    
    if not available_plugins:
        print("No plugins found in personal_manager/plugins/")
        return

    while True:
        clear_screen()
        print("=== Personal Manager CLI ===")
        
        # Filter plugins that are currently enabled in the config
        enabled_plugins = {k: v for k, v in available_plugins.items() if is_plugin_enabled(k)}
        
        if not enabled_plugins:
            print("\nNo plugins enabled.")
        else:
            print("\nEnabled Plugins:")
            plugin_items = list(enabled_plugins.items())
            for i, (key, plugin) in enumerate(plugin_items, 1):
                print(f"{i}. Run {plugin.name}")
        
        print("\nm. Manage Plugins (Toggle on/off)")
        print("q. Exit")
        
        choice = input("\nChoice: ")
        
        if choice.lower() == 'q':
            sys.exit(0)
        elif choice.lower() == 'm':
            toggle_plugins_menu(available_plugins)
        else:
            try:
                idx = int(choice) - 1
                plugin_items = list(enabled_plugins.items())
                if 0 <= idx < len(plugin_items):
                    key, plugin = plugin_items[idx]
                    # Execute the selected plugin
                    plugin.run()
                else:
                    print("Invalid choice.")
                    input("Press Enter...")
            except ValueError:
                print("Invalid input.")
                input("Press Enter...")

if __name__ == "__main__":
    main()

import logging
from pathlib import Path
from personal_manager.core.plugin import Plugin
from personal_manager.logging_config import setup_logging

# Setup logging configuration
setup_logging()
logger = logging.getLogger(__name__)

class BudgetingPlugin(Plugin):
    """
    A plugin for managing personal budgeting and expenses.
    """
    @property
    def name(self) -> str:
        """The display name of the plugin."""
        return "Budgeting"

    @property
    def description(self) -> str:
        """A brief description of the plugin's functionality."""
        return "Manage your expenses and budget."

    def run(self) -> None:
        """
        Executes the main budgeting plugin logic, providing a menu for expense management.
        """
        from .app import Budget
        from personal_manager.core.config import get_plugin_setting, set_plugin_setting
        
        logger.info("Starting Budgeting Plugin")
        
        # Check if the budget file path has already been configured
        expenses_write_file_path = get_plugin_setting("budgeting", "expenses_file_path")
        
        if not expenses_write_file_path:
            # Set up default path OS-compatibly
            default_path = Path.home() / ".personal_manager" / "budget.csv"
            native_default = str(default_path.resolve())
            
            print("\n=== Budgeting Plugin: First-Run Setup ===")
            print("Configure the file path where your budgeting entries will be saved.\n")
            user_input = input(f"Enter path for budget CSV file (Default: {native_default}): ").strip()
            
            if not user_input:
                expenses_write_file_path = native_default
            else:
                expenses_write_file_path = str(Path(user_input).resolve())
                
            set_plugin_setting("budgeting", "expenses_file_path", expenses_write_file_path)
            print(f"Configuration saved successfully to config: {expenses_write_file_path}\n")

        # Ensure the target directories exist before running
        Path(expenses_write_file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize and run the Budget manager
        budget = Budget(0, expenses_write_file_path)
        
        # Simple interactive loop for budgeting
        print("\n--- Budgeting Menu ---")
        print("1. Add Expense")
        print("2. Run Daily Entry")
        print("q. Back to Main Menu")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            budget.add_expense()
        elif choice == '2':
            budget.run_expense_entry_daily()
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")
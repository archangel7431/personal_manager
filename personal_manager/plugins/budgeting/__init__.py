import logging
from pathlib import Path
from personal_manager.core.plugin import Plugin
from logging_config import setup_logging

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
        logger.info("Starting Budgeting Plugin")
        
        # Simple interactive loop for budgeting
        print("\n--- Budgeting Menu ---")
        print("1. Add Expense")
        print("2. Run Daily Entry")
        print("q. Back to Main Menu")
        
        choice = input("Select an option: ")
        
        # Store data in the root 'data/' directory
        root_data_path = Path.cwd() / "data"
        expenses_write_file_path = root_data_path / "budget.csv"
        
        # Ensure the root data directory exists
        expenses_write_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize and run the Budget manager
        budget = Budget(0, str(expenses_write_file_path))
        
        if choice == '1':
            budget.add_expense()
        elif choice == '2':
            budget.run_expense_entry_daily()
        elif choice == 'q':
            return
        else:
            print("Invalid choice.")
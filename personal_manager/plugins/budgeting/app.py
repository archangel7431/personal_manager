from pathlib import Path
from . import logger
from .utils_expense_entry import expense_entry, run_daily


class Budget:
    """
    Manages budget balance and expense entries.
    """
    def __init__(self, initial_balance: float, expenses_file_path: str) -> None:
        """
        Initializes the Budget manager.
        
        Args:
            initial_balance: The starting balance.
            expenses_file_path: Path to the CSV file where expenses are stored.
        """
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0: # type: ignore
            logger.error("Initial balance is wrong.")
            raise ValueError("Initial balance must be a non-negative number.")
        
        if not isinstance(expenses_file_path, str) or expenses_file_path is None: # type: ignore
            logger.error("Expense file path is None or not a string")
            raise ValueError("Expense file path must be a string")
        
        self.balance = initial_balance
        self.expenses_file_path = expenses_file_path
        self.expenses = []
    
    def add_expense(self):
        """
        Interactively adds an expense entry to the storage file.
        """
        expense_entry(write_file_path=self.expenses_file_path)
    
    def run_expense_entry_daily(self):
        """
        Runs the daily expense entry process.
        """
        run_daily()



if __name__ == "__main__":
    # This block is for standalone testing of the Budget class
    logger.debug("Starting the program execution.")

    # In standalone mode, we still use a 'data' folder relative to the root if run from root,
    # or relative to this file if run directly.
    root_data_path = Path.cwd() / "data"
    expenses_write_file_path = root_data_path / "budget.csv"
    
    # Ensure directory exists
    expenses_write_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    budget = Budget(0, str(expenses_write_file_path))
    budget.add_expense()

    logger.debug("Program execution completed.")
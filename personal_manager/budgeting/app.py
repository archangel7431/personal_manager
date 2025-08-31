from . import logger
from .utils_expense_entry import expense_entry


class Budget:
    def __init__(self, initial_balance: float, expenses_file_path: str) -> None:
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
        expense_entry(write_file_path=self.expenses_file_path)
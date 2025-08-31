import unittest

from .utils_expense_entry import expense_entry


class TestBudget(unittest.TestCase):
    def setUp(self):
        """
        This method is run before each test method
        """

        

# Test cases for expense entry function in utils module
def test_expense_entry():
    """
    Test the expense_entry function from the utils module.
    This function tests the main functionality of the expense entry program.
    """
    # Mocking the user input to simulate user interaction
    user_input = [
        "2023-10-01,Groceries,50.00",
        "2023-10-02,Utilities,100.00"
    ]
    
    # Mocking the input function to return predefined user input
    with patch('builtins.input', side_effect=user_input):
        # Call the expense_entry function
        expense_entry(write_file_path="./personal_manager/budgeting/data/test_budget.csv")
    
    # Check if the file was created and contains the expected data
    with open("./personal_manager/budgeting/data/test_budget.csv", 'r') as file:
        content = file.read()
        assert "2023-10-01,Groceries,50.00" in content
        assert "2023-10-02,Utilities,100.00" in content


if __name__ == "__main__":
    # Run the test case
    test_expense_entry()
    print("Test passed successfully.")
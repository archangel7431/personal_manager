import unittest
from unittest.mock import patch, mock_open, MagicMock, Mock
import os
from datetime import date
import csv
from io import StringIO
from typing import Any, Callable

from .utils_expense_entry import (
    checking_for_directory,
    checking_for_file,
    append_to_csv,
    get_user_input,
    expense_entry,
    run_daily
)


class TestBudget(unittest.TestCase):
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.test_dir = "./test_data"
        self.test_file = os.path.join(self.test_dir, "test_budget.csv")
        self.test_data = [
            (date.today(), "Food", "50.00"),
            (date.today(), "Transport", "30.00")
        ]

    def tearDown(self) -> None:
        """Clean up test fixtures after each test method."""
        # Clean up any test files or directories created
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    @patch('os.makedirs')
    def test_checking_for_directory(self, mock_makedirs: Mock) -> None:
        """Test directory creation functionality"""
        # Test normal directory creation
        checking_for_directory(self.test_dir)
        mock_makedirs.assert_called_once_with(self.test_dir, exist_ok=True)

        # Test handling of OSError
        mock_makedirs.side_effect = OSError("Test error")
        checking_for_directory(self.test_dir)  # Should handle the error gracefully

    def test_checking_for_file(self) -> None:
        """Test file creation and header writing"""
        with patch('builtins.open', mock_open()) as mock_file:
            # Test when file doesn't exist
            with patch('os.path.exists', return_value=False):
                checking_for_file(self.test_file)
                mock_file.assert_called_once_with(self.test_file, mode='w', newline='')
                mock_file().write.assert_called()  # Verify write was called

            # Test when file exists
            with patch('os.path.exists', return_value=True):
                checking_for_file(self.test_file)
                # Should not try to create file again
                self.assertEqual(mock_file.call_count, 1)

    def test_append_to_csv(self) -> None:
        """Test appending data to CSV file"""
        mock_csv_content = StringIO()
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.return_value.__enter__.return_value = mock_csv_content
            
            # Test successful append
            append_to_csv(self.test_file, self.test_data)
            
            # Verify data was written
            content = mock_csv_content.getvalue()
            self.assertIn(str(date.today()), content)
            self.assertIn("Food", content)
            self.assertIn("50.00", content)

            # Test file not found error
            mock_file.side_effect = FileNotFoundError
            append_to_csv(self.test_file, self.test_data)  # Should handle error gracefully

    @patch('builtins.input')
    def test_get_user_input(self, mock_input: Mock) -> None:
        """Test user input collection"""
        # Test successful input
        mock_input.side_effect = ["Food", "50.00", "Transport", "30.00", "exit"]
        result = get_user_input()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "Food")
        self.assertEqual(result[0][2], "50.00")

        # Test empty input handling
        mock_input.side_effect = ["", "Food", "50.00", "exit"]
        result = get_user_input()
        self.assertEqual(len(result), 1)

        # Test invalid number input
        mock_input.side_effect = ["Food", "not_a_number", "50.00", "exit"]
        result = get_user_input()
        self.assertEqual(len(result), 1)

    @patch('personal_manager.budgeting.utils_expense_entry.checking_for_directory')
    @patch('personal_manager.budgeting.utils_expense_entry.checking_for_file')
    @patch('personal_manager.budgeting.utils_expense_entry.get_user_input')
    @patch('personal_manager.budgeting.utils_expense_entry.append_to_csv')
    def test_expense_entry(
        self, 
        mock_append: Mock, 
        mock_input: Mock, 
        mock_check_file: Mock, 
        mock_check_dir: Mock
    ) -> None:
        """Test main expense entry function"""
        # Test successful execution
        mock_input.return_value = self.test_data
        expense_entry(self.test_file)
        
        mock_check_dir.assert_called_once()
        mock_check_file.assert_called_once()
        mock_input.assert_called_once()
        mock_append.assert_called_once_with(self.test_file, self.test_data)

        # Test with empty input
        mock_input.return_value = []
        expense_entry(self.test_file)
        self.assertEqual(mock_append.call_count, 1)  # Should not call append_to_csv

    @patch('schedule.every')
    def test_run_daily(self, mock_schedule: Mock) -> None:
        """Test daily scheduling function"""
        test_time = "21:30"
        mock_day = MagicMock()
        mock_schedule.day = mock_day
        mock_at = MagicMock()
        mock_day.at.return_value = mock_at

        run_daily(test_time)
        
        mock_day.at.assert_called_once_with(test_time)
        mock_at.do.assert_called_once_with(job_func=expense_entry)


if __name__ == '__main__':
    unittest.main()
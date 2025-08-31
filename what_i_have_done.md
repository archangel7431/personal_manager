# 28-04-2025
1. I have added a centralized logging. In each submodule, I can call the same logging now. Check `personal_manager/budgeting/__init__.py`
2. I have created a trial budget_tracker CLI which will save data as a csv file into `data/budget.csv`
It will be in this form: date, section_name, section_value
eg: 2025-04-28, expense_food, 50

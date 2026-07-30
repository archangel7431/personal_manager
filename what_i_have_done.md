# 28-04-2025
1. I have added a centralized logging. In each submodule, I can call the same logging now. Check `personal_manager/budgeting/__init__.py`
2. I have created a trial budget_tracker CLI which will save data as a csv file into `data/budget.csv`
It will be in this form: date, section_name, section_value
eg: 2025-04-28, expense_food, 50


# 10-11-2025
1. I have created a class called `Budget` which will have methods related to budgeting in `personal_manager/budgeting/app.py`. It will store data as a csv file in `personal_manager/budgeting/data/`. I have successfully run the `add_expenses()` method.
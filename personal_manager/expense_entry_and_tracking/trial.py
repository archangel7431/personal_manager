# trial run

from datetime import date
from pathlib import Path

trial_file = Path("personal_manager/expense_entry_and_tracking/trial.txt")
with trial_file.open("a") as f:
    print()
    f.write(f"{date.today()}\n")
    while True:
        things = input("Enter the thing for which cost will follow: ")
        if things == "exit":
            break
        cost = input("Enter the cost of the thing: ")
        f.write(things + ":" + cost + "\n")

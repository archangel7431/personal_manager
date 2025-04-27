# trial run

from datetime import date

with open("./personal_manager/budgeting/trial.txt", "a") as f:
    print()
    f.write(f"{date.today()}\n")
    while True:
        things = input("Enter the thing for which cost will follow: ")
        if things == "exit":
            break
        cost = input("Enter the cost of the thing: ")
        f.write(things + ":" + cost + "\n")

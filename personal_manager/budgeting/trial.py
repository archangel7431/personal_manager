# trial run
import csv
import os
from datetime import date
from . import logger

try:
    logger.debug("Starting the program")

    # Check if the directory exists, if not create it
    os.makedirs("./personal_manager/budgeting/data", exist_ok=True)
    logger.debug("Checked/created the data directory")

    # Check if the CSV file exists, if not create it
    file_path = "./personal_manager/budgeting/data/budget.csv"
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="") as file:
            logger.debug("Created budget.csv file")
            # Create a CSV writer object
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Date", "Section_name", "Section_value"])
            logger.debug("Wrote header to budget.csv")
    else:
        logger.debug("budget.csv already exists")


    # Open the CSV file in append mode
    with open("./personal_manager/budgeting/data/budget.csv", mode="a", newline="") as file:
        logger.debug("Opened budget.csv for appending")

        # Create a CSV writer object
        writer = csv.writer(file)
        logger.debug("Created CSV writer object")

        # Write the data row
        print("Enter 'exit' to stop the program")
        while True:
            try:
                thing = input("Enter section name(as section_name): ")

                if thing == "exit":
                    logger.info("User exited the CSV input loop")
                    break

                cost = input("Enter the section_value: ")
                writer.writerow([date.today(), thing, cost])
                logger.info(f"Logged to budget.csv: Section_name={thing}, Section_value={cost}")

            except Exception as e:
                logger.error(f"An error occurred while writing a row: {e}")
                break
except FileNotFoundError as e:
    logger.critical(f"File not found: {e}")
except Exception as e:
    logger.critical(f"An unexpected error occurred: {e}")
finally:
    logger.debug("Program ended")

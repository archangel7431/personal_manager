# trial run
import csv
import os
import schedule
from datetime import date

from . import logger


# Function to check if the directory exists and create it if not
def checking_for_directory(directory_path: str) -> None:
    """
    Check if the directory exists, if not create it.
    Args:
        directory_path (str): The path to the directory.
    Returns:
        None
    """

    logger.debug(f"Entering {checking_for_directory.__name__} function with directory_path: {directory_path}")

    try:
        # Check if the directory exists, if not create it
        os.makedirs(directory_path, exist_ok=True)
        logger.debug(f"Checked/created the directory: {directory_path}")
    except Exception as e:
        logger.error(f"An error occurred while checking/creating the directory: {e}")
    finally:
        logger.debug(f"Exiting {checking_for_directory.__name__} function.")


# Function to check if the CSV file exists and create it if not
def checking_for_file(filepath: str) -> None:
    """
    Check if the CSV file exists, if not create it.
    Args:
        filepath (str): The path to the CSV file.
    Returns:
        None
    """

    logger.debug(f"Entering {checking_for_file.__name__} function with filepath: {filepath}")

    try:
        # Check if the file exists, if not create it
        if not os.path.exists(filepath):
            with open(filepath, mode="w", newline="") as file:
                writer = csv.writer(file)
                section_name = "Section_name"
                section_value = "Section_value"
                writer.writerow(["Date", section_name, section_value])
                logger.debug(f"Created {filepath} and wrote header.")
        else:
            logger.debug(f"{filepath} already exists.")
    except Exception as e:
        logger.error(f"An error occurred while checking/creating the file: {e}")
    finally:
        logger.debug(f"Exiting {checking_for_file.__name__} function.")


# Function to append data to the CSV file
def append_to_csv(filepath: str, data: list[tuple[date, str, str]])-> None:
    """
    Append data to the CSV file.
    Args:
        filepath (str): The path to the CSV file.
        data (list[tuple[date, str, str]]): The data to append as a list of tuples, where each tuple contains (date, section_name, section_value).
    Returns:
        None
    """

    logger.debug(f"Entering {append_to_csv.__name__} function with filepath: {filepath} and data: {data}")

    try:
        # Open the CSV file in append mode and write the data
        with open(filepath, mode="a", newline="") as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            for row in data:
                writer.writerow(row)
                logger.info(f"Appended data = {row} to {filepath}")
            logger.debug(f"Data appended to {filepath} successfully.")

    # Handle file not found and other exceptions
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred while appending data: {e}")
    # Log the exit of the function
    finally:
        logger.debug(f"Exiting {append_to_csv.__name__} function.")


# Function to get data from the user
def get_user_input() -> list[tuple[date, str, str]]:
    """
    Get data to enter from user/input.
    Returns:
        data (tuple[date, str, str]): A tuple containing date, section name and section value.
    """

    logger.debug(f"Starting {get_user_input.__name__} function.")
    # Initialize an empty list to store the data
    data: list[tuple[date, str, str]]= []
    logger.debug("Entering the input loop. Type 'exit' to stop.")
    # Loop to get user input until 'exit' is entered
    while True:
        # Inform the user about how to exit the loop
        print("Enter 'exit' to exit")

        # Get user input for section name and value
        section_name = input("Enter section name: ")
        # Check if the section_name is empty
        if not section_name:
            logger.error("Section_name cannot be empty. Please try again.")
            continue

        # Check if the user wants to exit.
        if section_name.lower() == "exit":
            logger.debug("User exited the input loop.")
            break

        section_value = input("Enter the section_value: ")
        # Check if the section_value is empty or not a number
        try:
            float(section_value)  # Check if section_value can be converted to float
        except ValueError:
            logger.error("Section_value must be a number. Please try again.")
            print("Section_value must be a number. Please try again.")
            continue

        # Append the data as a tuple to the list
        try:
            data.append((date.today(), section_name, section_value))
        except Exception as e:
            logger.error(f"An error occurred while appending data: {e}")
            print("An error occurred while appending data. Please try again.")
            # Continue to the next iteration if an error occurs
            continue
        logger.info(f"User input: Section_name={section_name}, Section_value={section_value}")
    
    logger.debug("User input collection completed and updated to the log.")

    # Log the exit of the function
    logger.debug(f"Exiting {get_user_input.__name__} function")

    return data


# Main function to run the program
def expense_entry(write_file_path: str ="./personal_manager/budgeting/data/budget.csv") -> None:
    """
    Main function to run the program.
    Args:
        write_file_path (str): The path to the CSV file where data will be written. 
        Default is "./personal_manager/budgeting/data/budget.csv".
    Returns:
        None
    """

    logger.debug("Starting the expense entry program.")

    ## Check if the file and directory exist. If not, create them.
    logger.debug(f"Checking for directory and file: {write_file_path}")
    directory_path = os.path.dirname(write_file_path)
    logger.debug(f"Directory path: {directory_path}")

    # Check if the directory exists and create it if not
    try:
        checking_for_directory(directory_path)
        logger.debug("Directory check completed.")
    except Exception as e:
        logger.error(f"An error occurred while checking/creating the directory: {e}")
        return

    # Check if the CSV file exists and create it if not
    try:
        checking_for_file(write_file_path)
        logger.debug("File check completed.")
    except Exception as e:
        logger.error(f"An error occurred while checking/creating the file: {e}")
        return

    ## Get user input
    logger.debug("Getting user input for expense entry.")
    try:
        # Store the user input as `data`
        data = get_user_input()
        logger.debug(f"User input collected successfully. data = {data}")
    except Exception as e:
        logger.error(f"An error occurred while getting user input: {e}")
        return
    
    if not data:
        logger.warning("No data entered by the user. Exiting the program.")
        return

    ## Append data to the CSV file
    logger.debug(f"Appending data to the CSV file: {write_file_path}")
    try:
        append_to_csv(write_file_path, data)
        logger.debug("Data appended to the CSV file successfully.")
    except Exception as e:
        logger.error(f"An error occurred while appending data to the CSV file: {e}")
        return

    # Log the successful completion of the program
    logger.debug("Expense entry program completed successfully.")


# Function to run the main function daily at a specific time
def run_daily(time: str = "21:30") -> None:
    """
    Run the main function daily at a specific time.
    
    Args:
        time (str): The time at which the function should run daily in "HH:MM" format. Default is "21:30".
    Returns:
        None
    """
    logger.debug(f"The function {run_daily.__name__} is for scheduling the daily execution.")

    # Schedule the expense entry function to run daily at the specified time
    schedule.every().day.at(time).do(job_func=expense_entry)
    logger.info(f"Scheduled the expense entry function to run daily at {time}.")

    return None
    

if __name__ == "__main__":
    # Run the main function
    logger.debug("Starting the program execution.")
    write_file_path = "./personal_manager/budgeting/data/budget.csv"
    expense_entry(write_file_path=write_file_path)
    logger.debug("Program execution completed.")
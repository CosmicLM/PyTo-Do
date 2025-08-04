from pytodo.tasks import add_task, view_tasks, complete_task, delete_task
from time import sleep
import os
import argparse

# This script is a simple command-line To-Do list application.
# It allows users to add, view, complete, and delete tasks.
# The tasks are stored in a JSON file for persistence.
# The application is designed to be user-friendly and easy to navigate.
# It uses a simple menu system to guide the user through the available options.
# The script also includes a banner display for a more engaging user experience.
# The banner is displayed at the start of the application, and can be skipped with a command-line argument.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner(): # This function displays a welcome banner for the application.
    # Clear the console
    clear()
    print("""welcome to...
          
          
              ░▒█▀▀█░█░░█░▀▀█▀▀░▄▀▀▄░░░░▒█▀▀▄░▄▀▀▄
              ░▒█▄▄█░█▄▄█░░▒█░░░█░░█░▀▀░▒█░▒█░█░░█
              ░▒█░░░░▄▄▄▀░░▒█░░░░▀▀░░░░░▒█▄▄█░░▀▀░""")
    print("""\n                                  
                     XXXXXXXXXX                   
                    XXXXXXXXXXXXX$$$              
                    XXXXXXXXXXX$$$$$              
                               $$$$    ...        
                                     :::...       
          XX                       ::::::...      
          XXXXX   ::            :::::::::::       
         XXXXX  ::::::        ::::::::::          
         XXXXX ::::::::     ::::::::::            
         XXXXX  ::::::::  ::::::::::   $$         
         XXXXX    ::::::::::::::::     $$$$$      
         XXXX$     ::::::::::::       $$$$$       
          X$$$$      ::::::::         $$$$$       
          $$$$$$      :::::          $$$$$        
            $$$$$$      :               $         
             $$$$$$$$                             
              $$$$$$$$$$$$$$$$                    
                 $$$$$$$$$$$$$$                   
                     $$$$$$$$$$                  """)
    sleep(2)

def get_task_number(): # This function prompts the user to enter a task number and validates the input.
    while True:
        try:
            task_number = int(input("Enter task number: "))
            if task_number > 0:
                return task_number
            else:
                print("Task number must be a positive integer.")
        except ValueError: # Handle non-integer input
            print("Invalid input. Please enter a valid number.")
            sleep(1)
def KeyboardInterrupt(): # This function handles keyboard interrupts (Ctrl+C) gracefully.
    print("\nThank you for Using PyTo-Do! Exiting...")
    sleep(1)
    clear()
    os.system('cls' if os.name == 'nt' else 'clear')
    exit(0)
import signal
signal.signal(signal.SIGINT, lambda s, f: KeyboardInterrupt()) # Register the signal handler
# This function is used to handle the Ctrl+C keyboard interrupt.
# It clears the console and exits the application gracefully.

def menu(): # This function displays the main menu and handles user input.
    while True:
        clear()
        print("Welcome to PyTo-Do!")
        print("1. Add task\n2. View tasks\n3. Complete task\n4. Delete task\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1": # Add a task
            add_task(input("Enter task: "))
        elif choice == "2": # View tasks
            clear()
            print("Viewing tasks")
            view_tasks() 
        elif choice == "3": # Complete a task
            clear()
            print("Select which task to complete")
            view_tasks()
            complete_task(get_task_number())
            sleep(1)
            print("Task completed")
        elif choice == "4": # Delete a task
            clear()
            print("Select which task to delete")
            view_tasks()
            delete_task(get_task_number())
            print("Task deleted")
        elif choice == "5":  # Exit the application
            print("Thank you for using PyTo-Do!\nExiting...")
            sleep(1)
            break
        else:
            print("Invalid choice")
        input("Press enter to continue")

if __name__ == "__main__": # This is the main entry point of the application.
    parser = argparse.ArgumentParser(description="PyTo-Do Application")
    parser.add_argument("--no-banner", action="store_true", help="Skip the banner display")
    args = parser.parse_args()

    if not args.no_banner:
        display_banner()
    menu()
    clear()

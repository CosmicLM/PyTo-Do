#!/usr/bin/env python3
"""
PyTo-Do Standalone - A simple task management CLI application
Self-contained version for better packaging compatibility
"""

import json
import os
import sys
import argparse
from time import sleep
import signal

# Task storage
TASKS_FILE = "storage.json"

def load_tasks():
    """Load tasks from storage file"""
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Save tasks to storage file"""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
        print("Saving tasks...")
        sleep(0.5)
        print("Tasks saved successfully.")
    except Exception as e:
        print(f"Error saving tasks: {e}")

def add_task(task_text, tasks):
    """Add a new task"""
    if not task_text.strip():
        print("Task cannot be empty!")
        return tasks
    
    new_task = {"task": task_text.strip(), "completed": False}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task: '{task_text.strip()}'")
    return tasks

def view_tasks(tasks):
    """Display all tasks"""
    if not tasks:
        print("No tasks in your To-Do list")
        return
    
    print("To-Do List:")
    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else "✗"
        print(f"{i}. {task['task']} - {status}")

def complete_task(task_number, tasks):
    """Mark a task as completed"""
    try:
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number")
            return tasks
        
        task = tasks[task_number - 1]
        if task["completed"]:
            print("Task is already completed!")
            return tasks
            
        task["completed"] = True
        save_tasks(tasks)
        print(f"Completed task: '{task['task']}'")
        return tasks
    except (IndexError, ValueError):
        print("Invalid task number")
        return tasks

def delete_task(task_number, tasks):
    """Delete a task"""
    try:
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number")
            return tasks
            
        task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Deleted task: '{task['task']}'")
        return tasks
    except (IndexError, ValueError):
        print("Invalid task number")
        return tasks

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display welcome banner"""
    clear_screen()
    print("""welcome to...
          
          
              ░▒█▀▀█░█░░█░▀▀█▀▀░▄▀▀▄░░░░▒█▀▀▄░▄▀▀▄
              ░▒█▄▄█░█▄▄█░░▒█░░░█░░█░▀▀░▒█░▒█░█░░█
              ░▒█░░░░▄▄▄▀░░▒█░░░░▀▀░░░░░▒█▄▄█░░▀▀░""")
    print("""

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

def get_task_number():
    """Get valid task number from user"""
    while True:
        try:
            task_number = int(input("Enter task number: "))
            if task_number > 0:
                return task_number
            else:
                print("Task number must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            sleep(1)

def handle_interrupt(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nThank you for using PyTo-Do! Exiting...")
    sleep(1)
    clear_screen()
    sys.exit(0)

def main_menu():
    """Main application menu"""
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, handle_interrupt)
    
    # Load tasks
    tasks = load_tasks()
    
    while True:
        clear_screen()
        print("Welcome to PyTo-Do!")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            task_text = input("Enter task: ")
            tasks = add_task(task_text, tasks)
        elif choice == "2":
            clear_screen()
            print("Viewing tasks")
            view_tasks(tasks)
        elif choice == "3":
            clear_screen()
            print("Select which task to complete")
            view_tasks(tasks)
            if tasks:
                task_num = get_task_number()
                tasks = complete_task(task_num, tasks)
                sleep(1)
        elif choice == "4":
            clear_screen()
            print("Select which task to delete")
            view_tasks(tasks)
            if tasks:
                task_num = get_task_number()
                tasks = delete_task(task_num, tasks)
        elif choice == "5":
            print("Thank you for using PyTo-Do!")
            print("Exiting...")
            sleep(1)
            break
        else:
            print("Invalid choice")
        
        if choice != "5":
            input("Press enter to continue")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PyTo-Do - Task Management Application")
    parser.add_argument("--no-banner", action="store_true", help="Skip the banner display")
    args = parser.parse_args()
    
    if not args.no_banner:
        display_banner()
    
    main_menu()
    clear_screen()

if __name__ == "__main__":
    main()

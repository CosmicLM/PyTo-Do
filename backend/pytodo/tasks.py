import sys
import os
from .storage_processor import TASKS_FILE, save_tasks, load_tasks
from datetime import datetime

# Load tasks from file

tasks = load_tasks()
# Add a task

def add_task(task, due_date=None):
   if due_date is None or due_date=="":
       print("Here A")
       tasks.append({"task": task, "completed": False})
       save_tasks(tasks)
       print(f"Added task: '{task}'")
   else:
       try:
           due_date = datetime.strptime(due_date, "%d/%m/%Y").date().isoformat()
       except:
           print("Invalid date format error")
           return
       tasks.append({"task": task, "completed": False, "due_date": due_date})
       save_tasks(tasks)
       print(f"Added task: '{task}'")

# List task elif choice == "5":
def view_tasks():
   if not tasks:
      print("No tasks in your To-Do list")
   else:
      print("To-Do List:")
   for i, task in enumerate(tasks, 0): # start numbering from 1
       status = "✓" if task["completed"] else "✗"
       print(f"{i+1}. {task['task']} - {status}") 
        
# Mark task as completed
def complete_task(task_number):
    try:
        task = tasks[task_number-1]
    except IndexError:
        print("Invalid task number")
        return
    task["completed"] = True
    save_tasks(tasks)   
    
    # Remove task
    
def delete_task(task_number):
    try:
        task = tasks.pop(task_number-1)
    except IndexError:
        print("Invalid task number")
        return
    save_tasks(tasks)
    print(f"Deleted task: '{task['task']}'")
    

        
import sys
import os
from pstats import add_func_stats

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
def view_tasks(interaction=False):
   if not tasks:
      print("No tasks in your To-Do list")
      return
   if not interaction:
      print("To-Do List:")
      for i, task in enumerate(tasks, 0): # start numbering from 1
         status = "✓" if task["completed"] else "✗"
         if "due_date" in task:
            print(f"{i + 1}. {task['task']} - {status} (Due: {task['due_date']})")
         else:
            print(f"{i+1}. {task['task']} - {status}")
      return
   #sorting
   task_clone = tasks.copy()
   track_complete = True
   track_incomplete = True
   allow_past_due = True
   allow_no_due_date = True
   while(True):
       print("\nTasks:")
       for i, task in enumerate(task_clone, 0):  # start numbering from 1
           status = "✓" if task["completed"] else "✗"
           if status == "✓" and not track_complete:
               continue
           elif status == "✗" and not track_incomplete:
               continue
           elif "due_date" in task and not datetime.strptime(task["due_date"], "%Y-%m-%d").date() > datetime.now().date() and not allow_past_due:
               continue
           elif not "due_date" in task and not allow_no_due_date:
               continue
           if "due_date" in task:
               print(f"{i + 1}. {task['task']} - {status} (Due: {task['due_date']})")
           else:
               print(f"{i + 1}. {task['task']} - {status}")
       print("---------------------------")
       print("1. Sort by entry date\n2. Sort by due date\n3. Toggle completed"
             "\n4. Toggle not completed\n5. Toggle past due\n6. Toggle no due date\n7. Exit")
       choice = input("Choose an option: ")
       if choice == "1":
           task_clone = tasks.copy() # resets list to defacto order
       elif choice == "2":
           task_clone = sorted(
               task_clone,
               key=lambda x:
               (0, datetime.strptime(x["due_date"], "%Y-%m-%d")
               ) if "due_date" in x and x["due_date"] else (1,)
           )
       elif choice == "3":
           track_complete = not track_complete
       elif choice == "4":
           track_incomplete = not track_incomplete
       elif choice == "5":
           allow_past_due = not allow_past_due
       elif choice == "6":
           allow_no_due_date = not allow_no_due_date
       elif choice == "7":
           break
       else:
           print("Invalid choice")

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
    

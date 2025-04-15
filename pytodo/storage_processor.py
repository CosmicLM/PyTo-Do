import json

# file to store tasks
TASKS_FILE = "storage.json"

# load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            return tasks
    except FileNotFoundError:
        # if file does not exist, return an empty list
        return []
    except json.JSONDecodeError:
        # if file is corrupted, reset tasks
        print("Error: Resetting tasks")
    return []
    
    # Save the tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4) # indent for pretty printing
    print("Tasks saved to file")
    
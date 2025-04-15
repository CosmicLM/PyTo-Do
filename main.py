from pytodo.tasks import add_task, view_tasks, complete_task, delete_task
import time

# Main program loop
def menu():
    while True:
        print("\nChoose an option:")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            task = input("Enter task: ")
            add_task(task)
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            task_number = int(input("Enter task number: "))
            complete_task(task_number)
        elif choice == "4":
            task_number = int(input("Enter task number: "))
            delete_task(task_number)
        elif choice == "5":
            print("Tasks saved to file")
            time.sleep(1)
            break
        else:
            print("Invalid choice")
if __name__ == "__main__":
    menu()
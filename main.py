from pytodo.tasks import add_task, view_tasks, complete_task, delete_task
from time import sleep
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear()
    print("""welcome to... ░▒█▀▀█░█░░█░▀▀█▀▀░▄▀▀▄░░░░▒█▀▀▄░▄▀▀▄
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
    sleep(3)

def get_task_number():
    while True:
        try:
            return int(input("Enter task number: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            sleep(1)

def menu():
    while True:
        clear()
        print("\nChoose an option:")
        print("1. Add task\n2. View tasks\n3. Complete task\n4. Delete task\n5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_task(input("Enter task: "))
        elif choice == "2":
            clear()
            view_tasks()
        elif choice == "3":
            clear()
            view_tasks()
            complete_task(get_task_number())
            print("Task completed")
        elif choice == "4":
            clear()
            view_tasks()
            delete_task(get_task_number())
            print("Task deleted")
        elif choice == "5":
            print("Thank you for using PyTo-Do!\nExiting...")
            sleep(1)
            break
        else:
            print("Invalid choice")
        input("Press enter to continue")

if __name__ == "__main__":
    display_banner()
    menu()
    clear()

#!/usr/bin/env python3
"""
PyTo-Do GUI - Graphical User Interface version
Built with tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class PyToDoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyTo-Do - Task Manager")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        # Task storage file
        self.storage_file = "storage.json"
        self.tasks = self.load_tasks()
        
        self.setup_ui()
        self.refresh_task_list()
    
    def load_tasks(self):
        """Load tasks from storage file"""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: Corrupted storage file, starting fresh")
            return []
    
    def save_tasks(self):
        """Save tasks to storage file"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {e}")
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PyTo-Do Task Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Add task section
        ttk.Label(main_frame, text="New Task:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_button = ttk.Button(main_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=1, column=2, sticky=tk.W)
        
        # Task list with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for tasks
        columns = ("Status", "Task", "Added")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=15)
        
        # Configure columns
        self.task_tree.column("#0", width=0, stretch=False)  # Hide tree column
        self.task_tree.column("Status", width=80, anchor=tk.CENTER)
        self.task_tree.column("Task", width=300, anchor=tk.W)
        self.task_tree.column("Added", width=120, anchor=tk.CENTER)
        
        # Configure headings
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Task", text="Task")
        self.task_tree.heading("Added", text="Added")
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        # Action buttons
        ttk.Button(button_frame, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Refresh", command=self.refresh_task_list).pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.update_status("Ready")
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        # Create new task
        new_task = {
            "task": task_text,
            "completed": False,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()
        self.update_status(f"Added task: '{task_text}'")
    
    def complete_task(self):
        """Mark selected task as completed"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to complete!")
            return
        
        item = selected[0]
        task_index = int(self.task_tree.item(item)["tags"][0])
        
        if self.tasks[task_index]["completed"]:
            messagebox.showinfo("Info", "Task is already completed!")
            return
        
        self.tasks[task_index]["completed"] = True
        self.save_tasks()
        self.refresh_task_list()
        self.update_status(f"Completed task: '{self.tasks[task_index]['task']}'")
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
        
        item = selected[0]
        task_index = int(self.task_tree.item(item)["tags"][0])
        task_text = self.tasks[task_index]["task"]
        
        if messagebox.askyesno("Confirm", f"Delete task: '{task_text}'?"):
            self.tasks.pop(task_index)
            self.save_tasks()
            self.refresh_task_list()
            self.update_status(f"Deleted task: '{task_text}'")
    
    def edit_task(self):
        """Edit selected task"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit!")
            return
        
        item = selected[0]
        task_index = int(self.task_tree.item(item)["tags"][0])
        current_task = self.tasks[task_index]["task"]
        
        new_text = simpledialog.askstring("Edit Task", "Enter new task text:", initialvalue=current_task)
        if new_text and new_text.strip():
            self.tasks[task_index]["task"] = new_text.strip()
            self.save_tasks()
            self.refresh_task_list()
            self.update_status(f"Updated task to: '{new_text.strip()}'")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Add tasks to treeview
        for i, task in enumerate(self.tasks):
            status = "✓ Done" if task["completed"] else "○ Pending"
            added_date = task.get("added", "Unknown")
            
            # Insert with alternating colors
            tags = (str(i), "completed" if task["completed"] else "pending")
            self.task_tree.insert("", tk.END, values=(status, task["task"], added_date), tags=tags)
        
        # Configure row colors
        self.task_tree.tag_configure("completed", background="#e8f5e8")
        self.task_tree.tag_configure("pending", background="white")
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task["completed"])
        self.update_status(f"Tasks: {total_tasks} total, {completed_tasks} completed, {total_tasks - completed_tasks} pending")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(f" {message}")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = PyToDoGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\\nGUI closed by user")

if __name__ == "__main__":
    main()

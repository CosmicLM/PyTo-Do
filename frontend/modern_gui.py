#!/usr/bin/env python3
"""
PyTo-Do Modern GUI - Beautiful Task Management Interface
Originally created by CosmicLM | Enhanced by mdnoyon9758
Features: Modern design, dark/light theme, animations, better UX
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import sys

class ModernPyToDoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyTo-Do - Modern Task Manager")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Modern color scheme
        self.colors = {
            'bg': '#f8f9fa',
            'sidebar': '#343a40',
            'primary': '#007bff',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'text': '#495057',
            'white': '#ffffff',
            'light_gray': '#e9ecef',
            'dark_gray': '#6c757d'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Task storage
        self.storage_file = "storage.json"
        self.tasks = self.load_tasks()
        
        # Current filter
        self.current_filter = "all"
        
        self.setup_styles()
        self.setup_ui()
        self.refresh_task_list()
        
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       padding=(15, 10),
                       font=('Segoe UI', 10, 'normal'))
        
        # Configure primary button
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       padding=(15, 10),
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure success button
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['white'],
                       padding=(10, 8),
                       font=('Segoe UI', 9, 'normal'))
        
        # Configure danger button
        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['white'],
                       padding=(10, 8),
                       font=('Segoe UI', 9, 'normal'))
        
        # Configure modern entry
        style.configure('Modern.TEntry',
                       padding=(10, 8),
                       font=('Segoe UI', 11))
        
        # Configure modern treeview
        style.configure('Modern.Treeview',
                       background=self.colors['white'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10),
                       rowheight=35)
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['light_gray'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11, 'bold'),
                       padding=(10, 10))
    
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
        """Setup the modern user interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.setup_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left sidebar
        self.setup_sidebar(content_frame)
        
        # Main content
        self.setup_main_content(content_frame)
        
        # Footer
        self.setup_footer(main_container)
    
    def setup_header(self, parent):
        """Setup the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title and subtitle
        title_label = tk.Label(header_frame, 
                              text="PyTo-Do", 
                              font=('Segoe UI', 28, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['bg'])
        title_label.pack(side=tk.LEFT, pady=10)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Modern Task Management • Originally by CosmicLM",
                                 font=('Segoe UI', 11),
                                 fg=self.colors['dark_gray'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0), pady=15, anchor=tk.S)
        
        # Statistics
        stats_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        stats_frame.pack(side=tk.RIGHT, pady=10)
        
        self.total_label = tk.Label(stats_frame,
                                   text="0 Total",
                                   font=('Segoe UI', 12, 'bold'),
                                   fg=self.colors['text'],
                                   bg=self.colors['bg'])
        self.total_label.pack(side=tk.RIGHT, padx=(0, 15))
        
        self.completed_label = tk.Label(stats_frame,
                                       text="0 Done",
                                       font=('Segoe UI', 12, 'bold'),
                                       fg=self.colors['success'],
                                       bg=self.colors['bg'])
        self.completed_label.pack(side=tk.RIGHT, padx=(0, 15))
        
        self.pending_label = tk.Label(stats_frame,
                                     text="0 Pending",
                                     font=('Segoe UI', 12, 'bold'),
                                     fg=self.colors['warning'],
                                     bg=self.colors['bg'])
        self.pending_label.pack(side=tk.RIGHT, padx=(0, 15))
    
    def setup_sidebar(self, parent):
        """Setup the sidebar with filters and actions"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['sidebar'], width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar_frame.pack_propagate(False)
        
        # Sidebar title
        sidebar_title = tk.Label(sidebar_frame,
                                text="Filters",
                                font=('Segoe UI', 14, 'bold'),
                                fg=self.colors['white'],
                                bg=self.colors['sidebar'])
        sidebar_title.pack(pady=(20, 15))
        
        # Filter buttons
        filters = [
            ("All Tasks", "all", self.colors['primary']),
            ("Pending", "pending", self.colors['warning']),
            ("Completed", "completed", self.colors['success'])
        ]
        
        for text, filter_type, color in filters:
            btn = tk.Button(sidebar_frame,
                           text=text,
                           font=('Segoe UI', 11),
                           bg=color,
                           fg=self.colors['white'],
                           border=0,
                           padx=20,
                           pady=10,
                           cursor='hand2',
                           command=lambda f=filter_type: self.set_filter(f))
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # Separator
        separator = tk.Frame(sidebar_frame, height=1, bg=self.colors['dark_gray'])
        separator.pack(fill=tk.X, padx=15, pady=20)
        
        # Actions
        actions_title = tk.Label(sidebar_frame,
                                text="Actions",
                                font=('Segoe UI', 14, 'bold'),
                                fg=self.colors['white'],
                                bg=self.colors['sidebar'])
        actions_title.pack(pady=(0, 15))
        
        # Action buttons
        actions = [
            ("🗂️ Export Tasks", self.export_tasks),
            ("📁 Import Tasks", self.import_tasks),
            ("🔄 Refresh", self.refresh_task_list),
            ("❌ Clear All", self.clear_all_tasks)
        ]
        
        for text, command in actions:
            btn = tk.Button(sidebar_frame,
                           text=text,
                           font=('Segoe UI', 10),
                           bg=self.colors['dark_gray'],
                           fg=self.colors['white'],
                           border=0,
                           padx=15,
                           pady=8,
                           cursor='hand2',
                           command=command)
            btn.pack(fill=tk.X, padx=15, pady=3)
    
    def setup_main_content(self, parent):
        """Setup the main content area"""
        main_frame = tk.Frame(parent, bg=self.colors['bg'])
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add task section
        add_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        add_frame.pack(fill=tk.X, pady=(0, 20))
        
        add_inner = tk.Frame(add_frame, bg=self.colors['white'])
        add_inner.pack(fill=tk.X, padx=20, pady=15)
        
        add_label = tk.Label(add_inner,
                            text="Add New Task",
                            font=('Segoe UI', 14, 'bold'),
                            fg=self.colors['text'],
                            bg=self.colors['white'])
        add_label.pack(anchor=tk.W, pady=(0, 10))
        
        input_frame = tk.Frame(add_inner, bg=self.colors['white'])
        input_frame.pack(fill=tk.X)
        
        self.task_entry = tk.Entry(input_frame,
                                  font=('Segoe UI', 12),
                                  bg=self.colors['white'],
                                  fg=self.colors['text'],
                                  relief=tk.FLAT,
                                  bd=2)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        add_btn = tk.Button(input_frame,
                           text="Add Task",
                           font=('Segoe UI', 11, 'bold'),
                           bg=self.colors['primary'],
                           fg=self.colors['white'],
                           border=0,
                           padx=20,
                           pady=8,
                           cursor='hand2',
                           command=self.add_task)
        add_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Tasks list section
        list_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # List header
        list_header = tk.Frame(list_frame, bg=self.colors['light_gray'], height=50)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        list_title = tk.Label(list_header,
                             text="Tasks",
                             font=('Segoe UI', 14, 'bold'),
                             fg=self.colors['text'],
                             bg=self.colors['light_gray'])
        list_title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Tasks container with scrollbar
        tasks_container = tk.Frame(list_frame, bg=self.colors['white'])
        tasks_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas and scrollbar for tasks
        canvas = tk.Canvas(tasks_container, bg=self.colors['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tasks_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def setup_footer(self, parent):
        """Setup footer with status and credits"""
        footer_frame = tk.Frame(parent, bg=self.colors['light_gray'], height=40)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_label = tk.Label(footer_frame,
                               textvariable=self.status_var,
                               font=('Segoe UI', 10),
                               fg=self.colors['text'],
                               bg=self.colors['light_gray'])
        status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        credit_label = tk.Label(footer_frame,
                               text="Originally created by CosmicLM • Enhanced by mdnoyon9758",
                               font=('Segoe UI', 9),
                               fg=self.colors['dark_gray'],
                               bg=self.colors['light_gray'])
        credit_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def create_task_widget(self, task, index):
        """Create a modern task widget"""
        task_frame = tk.Frame(self.scrollable_frame, 
                             bg=self.colors['white'], 
                             relief=tk.RAISED, 
                             bd=1)
        task_frame.pack(fill=tk.X, pady=5)
        
        # Task content
        content_frame = tk.Frame(task_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Status indicator
        status_color = self.colors['success'] if task['completed'] else self.colors['warning']
        status_text = "✓" if task['completed'] else "○"
        
        status_label = tk.Label(content_frame,
                               text=status_text,
                               font=('Segoe UI', 16, 'bold'),
                               fg=status_color,
                               bg=self.colors['white'])
        status_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Task details
        details_frame = tk.Frame(content_frame, bg=self.colors['white'])
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        task_label = tk.Label(details_frame,
                             text=task['task'],
                             font=('Segoe UI', 12, 'normal'),
                             fg=self.colors['text'],
                             bg=self.colors['white'],
                             anchor=tk.W)
        task_label.pack(fill=tk.X)
        
        date_label = tk.Label(details_frame,
                             text=f"Added: {task.get('added', 'Unknown')}",
                             font=('Segoe UI', 9),
                             fg=self.colors['dark_gray'],
                             bg=self.colors['white'],
                             anchor=tk.W)
        date_label.pack(fill=tk.X)
        
        # Action buttons
        actions_frame = tk.Frame(content_frame, bg=self.colors['white'])
        actions_frame.pack(side=tk.RIGHT)
        
        if not task['completed']:
            complete_btn = tk.Button(actions_frame,
                                   text="✓",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['success'],
                                   fg=self.colors['white'],
                                   border=0,
                                   width=3,
                                   cursor='hand2',
                                   command=lambda: self.complete_task(index))
            complete_btn.pack(side=tk.LEFT, padx=2)
        
        edit_btn = tk.Button(actions_frame,
                            text="✏️",
                            font=('Segoe UI', 10),
                            bg=self.colors['primary'],
                            fg=self.colors['white'],
                            border=0,
                            width=3,
                            cursor='hand2',
                            command=lambda: self.edit_task(index))
        edit_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = tk.Button(actions_frame,
                              text="🗑️",
                              font=('Segoe UI', 10),
                              bg=self.colors['danger'],
                              fg=self.colors['white'],
                              border=0,
                              width=3,
                              cursor='hand2',
                              command=lambda: self.delete_task(index))
        delete_btn.pack(side=tk.LEFT, padx=2)
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
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
    
    def complete_task(self, index):
        """Mark task as completed"""
        if index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()
            self.refresh_task_list()
            self.update_status(f"Completed task: '{self.tasks[index]['task']}'")
    
    def edit_task(self, index):
        """Edit a task"""
        if index < len(self.tasks):
            current_task = self.tasks[index]["task"]
            new_text = simpledialog.askstring("Edit Task", "Enter new task text:", initialvalue=current_task)
            if new_text and new_text.strip():
                self.tasks[index]["task"] = new_text.strip()
                self.save_tasks()
                self.refresh_task_list()
                self.update_status(f"Updated task to: '{new_text.strip()}'")
    
    def delete_task(self, index):
        """Delete a task"""
        if index < len(self.tasks):
            task_text = self.tasks[index]["task"]
            if messagebox.askyesno("Confirm", f"Delete task: '{task_text}'?"):
                self.tasks.pop(index)
                self.save_tasks()
                self.refresh_task_list()
                self.update_status(f"Deleted task: '{task_text}'")
    
    def set_filter(self, filter_type):
        """Set the current filter"""
        self.current_filter = filter_type
        self.refresh_task_list()
        self.update_status(f"Showing: {filter_type} tasks")
    
    def refresh_task_list(self):
        """Refresh the task list with current filter"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter tasks
        filtered_tasks = []
        if self.current_filter == "all":
            filtered_tasks = [(task, i) for i, task in enumerate(self.tasks)]
        elif self.current_filter == "pending":
            filtered_tasks = [(task, i) for i, task in enumerate(self.tasks) if not task['completed']]
        elif self.current_filter == "completed":
            filtered_tasks = [(task, i) for i, task in enumerate(self.tasks) if task['completed']]
        
        # Create task widgets
        if filtered_tasks:
            for task, original_index in filtered_tasks:
                self.create_task_widget(task, original_index)
        else:
            # Show empty state
            empty_label = tk.Label(self.scrollable_frame,
                                  text=f"No {self.current_filter} tasks found",
                                  font=('Segoe UI', 14),
                                  fg=self.colors['dark_gray'],
                                  bg=self.colors['white'])
            empty_label.pack(pady=50)
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics in header"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        self.total_label.config(text=f"{total} Total")
        self.completed_label.config(text=f"{completed} Done")
        self.pending_label.config(text=f"{pending} Pending")
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        # Auto-clear status after 3 seconds
        self.root.after(3000, lambda: self.status_var.set("Ready"))
    
    def export_tasks(self):
        """Export tasks to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            title="Export Tasks",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                import shutil
                shutil.copy2(self.storage_file, filename)
                self.update_status(f"Tasks exported to: {filename}")
                messagebox.showinfo("Success", "Tasks exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export tasks: {e}")
    
    def import_tasks(self):
        """Import tasks from file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Import Tasks",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported_tasks = json.load(f)
                
                if messagebox.askyesno("Confirm", f"Import {len(imported_tasks)} tasks? This will replace current tasks."):
                    self.tasks = imported_tasks
                    self.save_tasks()
                    self.refresh_task_list()
                    self.update_status("Tasks imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import tasks: {e}")
    
    def clear_all_tasks(self):
        """Clear all tasks"""
        if self.tasks and messagebox.askyesno("Confirm", "Delete all tasks? This cannot be undone."):
            self.tasks = []
            self.save_tasks()
            self.refresh_task_list()
            self.update_status("All tasks cleared")

def main():
    """Main function to run the modern GUI"""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        if os.path.exists("assets/Py-ToDoLogo.png"):
            root.iconphoto(False, tk.PhotoImage(file="assets/Py-ToDoLogo.png"))
    except:
        pass
    
    app = ModernPyToDoGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")

if __name__ == "__main__":
    main()

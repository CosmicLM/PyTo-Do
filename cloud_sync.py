#!/usr/bin/env python3
"""
PyTo-Do Cloud Integration
Sync tasks with Google Drive, Dropbox, and Google Tasks
"""

import json
import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

class CloudSyncGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyTo-Do Cloud Sync")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        self.storage_file = "storage.json"
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PyTo-Do Cloud Sync", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Instructions
        instructions = ttk.Label(main_frame, text="Backup and sync your tasks with cloud services", 
                                font=("Arial", 12), foreground="gray")
        instructions.grid(row=1, column=0, pady=(0, 20))
        
        # Export/Import Section
        export_frame = ttk.LabelFrame(main_frame, text="Local Backup", padding="15")
        export_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        main_frame.rowconfigure(2, weight=0)
        export_frame.columnconfigure(1, weight=1)
        
        ttk.Button(export_frame, text="Export Tasks", command=self.export_tasks).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(export_frame, text="Import Tasks", command=self.import_tasks).grid(row=0, column=1, padx=(10, 0))
        
        # Cloud Services Section
        cloud_frame = ttk.LabelFrame(main_frame, text="Cloud Services", padding="15")
        cloud_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        cloud_frame.columnconfigure(0, weight=1)
        
        # Google Drive
        gdrive_frame = ttk.Frame(cloud_frame)
        gdrive_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        gdrive_frame.columnconfigure(1, weight=1)
        
        ttk.Label(gdrive_frame, text="Google Drive:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(gdrive_frame, text="Setup Instructions", 
                  command=lambda: self.show_instructions("Google Drive")).grid(row=0, column=1, sticky=tk.E)
        
        # Dropbox
        dropbox_frame = ttk.Frame(cloud_frame)
        dropbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dropbox_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dropbox_frame, text="Dropbox:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(dropbox_frame, text="Setup Instructions", 
                  command=lambda: self.show_instructions("Dropbox")).grid(row=0, column=1, sticky=tk.E)
        
        # Google Tasks
        gtasks_frame = ttk.Frame(cloud_frame)
        gtasks_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        gtasks_frame.columnconfigure(1, weight=1)
        
        ttk.Label(gtasks_frame, text="Google Tasks:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(gtasks_frame, text="Setup Instructions", 
                  command=lambda: self.show_instructions("Google Tasks")).grid(row=0, column=1, sticky=tk.E)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="15")
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select an option above")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Task count
        try:
            with open(self.storage_file, 'r') as f:
                tasks = json.load(f)
                task_count = len(tasks)
                completed = sum(1 for task in tasks if task.get('completed', False))
                count_text = f"Current tasks: {task_count} total, {completed} completed"
        except:
            count_text = "No tasks file found"
        
        count_label = ttk.Label(status_frame, text=count_text, foreground="gray")
        count_label.grid(row=1, column=0, sticky=tk.W)
    
    def export_tasks(self):
        """Export tasks to a file"""
        if not os.path.exists(self.storage_file):
            messagebox.showerror("Error", "No tasks file found!")
            return
        
        # Ask user where to save
        filename = filedialog.asksaveasfilename(
            title="Export Tasks",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"pytodo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filename:
            try:
                # Copy the storage file
                import shutil
                shutil.copy2(self.storage_file, filename)
                self.status_var.set(f"Tasks exported to: {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Tasks exported successfully to:\n{filename}")
            except Exception as e:
                self.status_var.set("Export failed")
                messagebox.showerror("Error", f"Failed to export tasks:\n{str(e)}")
    
    def import_tasks(self):
        """Import tasks from a file"""
        filename = filedialog.askopenfilename(
            title="Import Tasks",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Validate the JSON file
                with open(filename, 'r') as f:
                    tasks = json.load(f)
                
                # Confirm with user
                if messagebox.askyesno("Confirm Import", 
                                     f"This will replace your current tasks with {len(tasks)} tasks from the backup.\n\nContinue?"):
                    # Backup current tasks first
                    if os.path.exists(self.storage_file):
                        backup_name = f"storage_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        import shutil
                        shutil.copy2(self.storage_file, backup_name)
                        messagebox.showinfo("Backup Created", f"Current tasks backed up to: {backup_name}")
                    
                    # Import new tasks
                    import shutil
                    shutil.copy2(filename, self.storage_file)
                    self.status_var.set(f"Tasks imported from: {os.path.basename(filename)}")
                    messagebox.showinfo("Success", "Tasks imported successfully!")
                    
                    # Refresh the GUI
                    self.root.destroy()
                    self.root.quit()
                    
            except Exception as e:
                self.status_var.set("Import failed")
                messagebox.showerror("Error", f"Failed to import tasks:\n{str(e)}")
    
    def show_instructions(self, service):
        """Show setup instructions for cloud services"""
        instructions = {
            "Google Drive": {
                "title": "Google Drive Setup Instructions",
                "steps": [
                    "1. Go to the Google Cloud Console (console.cloud.google.com)",
                    "2. Create a new project or select an existing one",
                    "3. Enable the Google Drive API",
                    "4. Create credentials (OAuth 2.0 client ID)",
                    "5. Download the credentials.json file",
                    "6. Install required Python packages:",
                    "   pip install google-auth-oauthlib google-api-python-client",
                    "7. Use the Google Drive API to upload/download your storage.json file",
                    "",
                    "Sample Python code:",
                    "from googleapiclient.discovery import build",
                    "from google_auth_oauthlib.flow import InstalledAppFlow",
                    "",
                    "# Follow Google's quickstart guide for authentication",
                    "# Upload: service.files().create(body=metadata, media_body=media)",
                    "# Download: request = service.files().get_media(fileId=file_id)"
                ],
                "links": [
                    ("Google Drive API Documentation", "https://developers.google.com/drive/api/quickstart/python"),
                    ("Google Cloud Console", "https://console.cloud.google.com")
                ]
            },
            "Dropbox": {
                "title": "Dropbox Setup Instructions",
                "steps": [
                    "1. Go to the Dropbox App Console (dropbox.com/developers/apps)",
                    "2. Create a new app",
                    "3. Choose 'Scoped access' and 'Full Dropbox' access",
                    "4. Generate an access token",
                    "5. Install the Dropbox Python SDK:",
                    "   pip install dropbox",
                    "6. Use the access token to upload/download files",
                    "",
                    "Sample Python code:",
                    "import dropbox",
                    "dbx = dropbox.Dropbox('YOUR_ACCESS_TOKEN')",
                    "",
                    "# Upload: dbx.files_upload(file_data, '/storage.json')",
                    "# Download: dbx.files_download_to_file('storage.json', '/storage.json')"
                ],
                "links": [
                    ("Dropbox API Documentation", "https://dropbox-sdk-python.readthedocs.io/"),
                    ("Dropbox App Console", "https://dropbox.com/developers/apps")
                ]
            },
            "Google Tasks": {
                "title": "Google Tasks Setup Instructions",
                "steps": [
                    "1. Go to the Google Cloud Console (console.cloud.google.com)",
                    "2. Create a new project or select an existing one",
                    "3. Enable the Google Tasks API",
                    "4. Create credentials (OAuth 2.0 client ID)",
                    "5. Download the credentials.json file",
                    "6. Install required Python packages:",
                    "   pip install google-auth-oauthlib google-api-python-client",
                    "7. Use the Google Tasks API to sync tasks",
                    "",
                    "Sample Python code:",
                    "from googleapiclient.discovery import build",
                    "service = build('tasks', 'v1', credentials=creds)",
                    "",
                    "# List tasks: service.tasks().list(tasklist='@default').execute()",
                    "# Add task: service.tasks().insert(tasklist='@default', body=task).execute()",
                    "# Complete task: service.tasks().update(...).execute()"
                ],
                "links": [
                    ("Google Tasks API Documentation", "https://developers.google.com/tasks/quickstart/python"),
                    ("Google Cloud Console", "https://console.cloud.google.com")
                ]
            }
        }
        
        if service in instructions:
            self.show_instruction_window(instructions[service])
    
    def show_instruction_window(self, instruction_data):
        """Show detailed instructions in a new window"""
        inst_window = tk.Toplevel(self.root)
        inst_window.title(instruction_data["title"])
        inst_window.geometry("700x600")
        inst_window.minsize(600, 500)
        
        # Main frame with scrollbar
        canvas = tk.Canvas(inst_window)
        scrollbar = ttk.Scrollbar(inst_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content_frame = ttk.Frame(scrollable_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(content_frame, text=instruction_data["title"], 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Steps
        steps_text = tk.Text(content_frame, wrap=tk.WORD, width=80, height=25, 
                            font=("Consolas", 10))
        steps_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        for step in instruction_data["steps"]:
            steps_text.insert(tk.END, step + "\n")
        
        steps_text.config(state=tk.DISABLED)
        
        # Links
        if "links" in instruction_data:
            links_frame = ttk.Frame(content_frame)
            links_frame.pack(fill=tk.X, pady=(10, 0))
            
            ttk.Label(links_frame, text="Useful Links:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
            
            for link_text, url in instruction_data["links"]:
                link_frame = ttk.Frame(links_frame)
                link_frame.pack(fill=tk.X, pady=2)
                
                link_button = ttk.Button(link_frame, text=link_text, 
                                       command=lambda u=url: webbrowser.open(u))
                link_button.pack(side=tk.LEFT)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def main():
    """Main function to run the Cloud Sync GUI"""
    root = tk.Tk()
    app = CloudSyncGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nCloud Sync closed by user")

if __name__ == "__main__":
    main()





#  PyTo-Do ✅

> **Originally created by [CosmicLM](https://github.com/CosmicLM/PyTo-Do)** | Enhanced and maintained by [mdnoyon9758](https://github.com/mdnoyon9758/PyTo-Do)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![GitHub stars](https://img.shields.io/github/stars/CosmicLM/PyTo-Do?style=social)

![alt text](/assets/Py-ToDoLogo.png)

A **simple yet powerful** task management app built with pure Python. organize your tasks effortlessly with a beautiful modern GUI and reliable CLI!

<p align="center">
  <img src="/assets/image.png">
</p>

## ✨ Features  
✔ **Modern GUI Interface** – Beautiful, responsive design with dark sidebar and clean layout  
✔ **Task Filtering** – View All, Pending, or Completed tasks with one click  
✔ **Real-time Statistics** – Live counters for total, completed, and pending tasks  
✔ **Export/Import** – Backup and restore your tasks easily  
✔ **Full CRUD Operations** – Add, edit, complete, and delete tasks seamlessly  
✔ **Persistent Storage** – Tasks save to `storage.json` automatically  
✔ **Cross-platform** – Works on Windows, Linux, and macOS  
✔ **No Dependencies** – Uses only Python standard library (tkinter)

## 🚀 Getting Started  

### Prerequisites  
- Python 3.8+ (Required)
- Git (for cloning)
- tkinter (usually included with Python)

### 📥 Installation Options

#### Option 1: Download Executable (Easiest) 🎯
1. Go to [Releases](https://github.com/CosmicLM/PyTo-Do/releases)
2. Download `PyTo-Do-GUI.exe` (Windows) - **10MB single file**
3. Double-click to run - No installation required!

#### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/CosmicLM/PyTo-Do
cd PyTo-Do

# Launch interface selector (Recommended)
python launcher.py

# Or run specific interfaces:
# Modern GUI
python frontend/modern_gui.py

# CLI version
python main.py

# Classic GUI
python frontend/gui.py

# Cloud Sync
python frontend/cloud_sync.py
```

### 🔧 Build Your Own Executable
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
python build.py

# Find your executable in ./release/
```

##  Up Coming Features

### Packaging
- [ ] **Setting up .exe and .deb files**

### GUI/CLI Improvements
- [ ] **Separate GUI/CLI implementations** 
- [ ] **GUI Version**
### Cloud Integration
- [ ] **Import/Export tasks from third-party services** (Google Drive, Dropbox)  
- [ ] **Sync with Google Tasks**

## 📜 License
This project is licensed under the MIT License –  [LICENSE](https://github.com/CosmicLM/PyTo-Do/blob/main/LICENSE)


## 💬 Feedback Welcome!
Found a bug? Want a feature? Open an issue or fork and improve!

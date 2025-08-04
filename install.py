#!/usr/bin/env python3
"""
PyTo-Do Installation Script
Handles installation across different platforms
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is supported"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        # Check if pip is available
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Install any requirements if they exist
        if os.path.exists("requirements.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Windows/Linux)"""
    try:
        if os.name == 'nt':  # Windows
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "PyTo-Do.lnk")
            target = os.path.abspath("main.py")
            wDir = os.path.dirname(target)
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wDir
            shortcut.save()
            
            print("✓ Desktop shortcut created")
        else:  # Linux/macOS
            home = os.path.expanduser("~")
            desktop_file = f"""[Desktop Entry]
Name=PyTo-Do
Comment=Task Management Application
Exec={sys.executable} {os.path.abspath('main.py')}
Icon={os.path.abspath('assets/Py-ToDoLogo.png')}
Terminal=true
Type=Application
Categories=Office;Productivity;
"""
            with open(f"{home}/Desktop/PyTo-Do.desktop", "w") as f:
                f.write(desktop_file)
            
            # Make executable
            os.chmod(f"{home}/Desktop/PyTo-Do.desktop", 0o755)
            print("✓ Desktop shortcut created")
            
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")

def setup_storage():
    """Initialize storage file if it doesn't exist"""
    if not os.path.exists("storage.json"):
        with open("storage.json", "w") as f:
            f.write("[]")
        print("✓ Storage file initialized")
    else:
        print("✓ Storage file exists")

def main():
    """Main installation function"""
    print("🚀 PyTo-Do Installation Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Installation completed with warnings")
    
    # Setup storage
    setup_storage()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("  1. Run PyTo-Do CLI: python main.py")
    print("  2. Run PyTo-Do GUI: python gui.py")
    print("  3. Run Cloud Sync: python cloud_sync.py")
    print("  4. Build executable: python build.py")
    print(f"\n📁 Installation directory: {os.path.abspath('.')}")

if __name__ == "__main__":
    main()

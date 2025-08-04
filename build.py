#!/usr/bin/env python3
"""
Build script for PyTo-Do
Creates executable files (.exe, standalone binaries) using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("✓ PyInstaller is available")
        return True
    except ImportError:
        print("📦 PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def build_executable():
    """Build the executable using PyInstaller"""
    if not check_pyinstaller():
        return False
    
    print("🔨 Building PyTo-Do executable...")
    
    # PyInstaller command
    separator = ";" if os.name == "nt" else ":"
    cmd = [
        "pyinstaller",
        "--onefile",                      # Create a single executable file
        "--console",                      # Console application
        "--name", "PyTo-Do",              # Name of the executable
        "--hidden-import=tkinter",        # Handle GUI imports
        "--hidden-import=json",           # Handle JSON imports
        "--hidden-import=datetime",       # Handle datetime imports
        f"--add-data=storage.json{separator}.",   # Include storage.json
        f"--add-data=assets{separator}assets",    # Include assets folder
        f"--add-data=backend{separator}backend",  # Include backend folder
        "main.py"  # Use main.py as entry point
    ]
    
    # Add icon if available
    if os.path.exists("assets/Py-ToDoLogo.png"):
        cmd.extend(["--icon", "assets/Py-ToDoLogo.png"])
    
    # Remove icon option if no icon file exists
    cmd = [arg for arg in cmd if arg is not None]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build completed successfully!")
        exe_name = "PyTo-Do.exe" if os.name == "nt" else "PyTo-Do"
        print(f"📁 Executable location: {os.path.abspath(f'dist/{exe_name}')}")
        
        # Create a release folder
        release_dir = Path("release")
        release_dir.mkdir(exist_ok=True)
        
        # Copy executable to release folder
        exe_name = "PyTo-Do.exe" if os.name == "nt" else "PyTo-Do"
        if os.path.exists(f"dist/{exe_name}"):
            shutil.copy2(f"dist/{exe_name}", release_dir / exe_name)
            print(f"📦 Release package created in: {release_dir.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def clean_build():
    """Clean build artifacts"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    print("🧹 Cleaning build artifacts...")
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed: {dir_name}/")
    
    import glob
    for pattern in files_to_clean:
        for file in glob.glob(pattern):
            os.remove(file)
            print(f"  Removed: {file}")

def main():
    """Main build function"""
    print("🚀 PyTo-Do Build Script")
    print("=" * 30)
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
        return
    
    # Build executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("📋 Usage:")
        exe_name = "PyTo-Do.exe" if os.name == "nt" else "PyTo-Do"
        print(f"  - Run the executable: ./release/{exe_name}")
        print("  - Clean build files: python build.py clean")
    else:
        print("\n❌ Build failed. Please check the error messages above.")

if __name__ == "__main__":
    main()

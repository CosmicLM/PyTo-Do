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
    
    # Ask user for build type
    print("Choose build type:")
    print("1. Modern GUI Application (frontend/modern_gui.py) - Recommended")
    print("2. CLI Application (main.py)")
    print("3. Launcher (all interfaces) - Best option")
    print("4. Both CLI and GUI")
    
    choice = input("Enter choice (1-4): ").strip()
    
    # Default to launcher if invalid choice
    if choice not in ['1', '2', '3', '4']:
        choice = '3'
        print("Invalid choice, defaulting to launcher application")
    
    separator = ";" if os.name == "nt" else ":"
    
    builds = []
    if choice == '1':  # Modern GUI build
        gui_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",                     # No console window for GUI
            "--name", "PyTo-Do-GUI",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.simpledialog",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=json",
            "--hidden-import=datetime",
            f"--add-data=storage.json{separator}.",
            f"--add-data=assets{separator}assets",
            f"--add-data=frontend{separator}frontend",
            f"--add-data=backend{separator}backend",
            "frontend/modern_gui.py"
        ]
        builds.append(("Modern GUI", gui_cmd))
    
    if choice == '2':  # CLI build
        cli_cmd = [
            "pyinstaller",
            "--onefile",
            "--console",
            "--name", "PyTo-Do-CLI",
            "--hidden-import=json",
            "--hidden-import=datetime",
            f"--add-data=storage.json{separator}.",
            f"--add-data=assets{separator}assets",
            f"--add-data=backend{separator}backend",
            "main.py"
        ]
        builds.append(("CLI", cli_cmd))
    
    if choice == '3':  # Launcher build
        launcher_cmd = [
            "pyinstaller",
            "--onefile",
            "--console",
            "--name", "PyTo-Do-Launcher",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.simpledialog",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=json",
            "--hidden-import=datetime",
            f"--add-data=storage.json{separator}.",
            f"--add-data=assets{separator}assets",
            f"--add-data=frontend{separator}frontend",
            f"--add-data=backend{separator}backend",
            "launcher.py"
        ]
        builds.append(("Launcher", launcher_cmd))
    
    if choice == '4':  # Both CLI and GUI
        # Add both builds
        gui_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "PyTo-Do-GUI",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.simpledialog",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=json",
            "--hidden-import=datetime",
            f"--add-data=storage.json{separator}.",
            f"--add-data=assets{separator}assets",
            f"--add-data=frontend{separator}frontend",
            f"--add-data=backend{separator}backend",
            "frontend/modern_gui.py"
        ]
        builds.append(("Modern GUI", gui_cmd))
        
        cli_cmd = [
            "pyinstaller",
            "--onefile",
            "--console",
            "--name", "PyTo-Do-CLI",
            "--hidden-import=json",
            "--hidden-import=datetime",
            f"--add-data=storage.json{separator}.",
            f"--add-data=assets{separator}assets",
            f"--add-data=backend{separator}backend",
            "main.py"
        ]
        builds.append(("CLI", cli_cmd))
    
    # Add icon to builds if available
    icon_path = "assets/Py-ToDoLogo.png"
    if os.path.exists(icon_path):
        for i, (build_type, cmd) in enumerate(builds):
            cmd.extend(["--icon", icon_path])
            builds[i] = (build_type, cmd)
    
    success_count = 0
    total_builds = len(builds)
    
    # Execute builds
    for build_type, cmd in builds:
        print(f"\n🔨 Building {build_type} version...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ {build_type} build completed successfully!")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ {build_type} build failed: {e}")
            if e.stderr:
                print(f"Error output: {e.stderr}")
    
    if success_count > 0:
        # Create release folder and copy executables
        release_dir = Path("release")
        release_dir.mkdir(exist_ok=True)
        
        # Copy built executables
        for exe_file in Path("dist").glob("*"):
            if exe_file.is_file():
                shutil.copy2(exe_file, release_dir / exe_file.name)
                print(f"📦 Copied {exe_file.name} to release folder")
        
        print(f"\n🎉 {success_count}/{total_builds} builds completed successfully!")
        print(f"📁 Executables available in: {release_dir.absolute()}")
        return True
    else:
        print(f"\n❌ All builds failed.")
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

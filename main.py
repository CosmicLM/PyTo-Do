#!/usr/bin/env python3
"""
PyTo-Do - A simple task management CLI application
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Determine the base path for resources
def get_base_path():
    """Get the base path for resources, handling PyInstaller bundle"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def main():
    """Main entry point for PyTo-Do"""
    base_path = get_base_path()
    
    # Add backend to path
    backend_path = os.path.join(base_path, 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    # Set working directory for proper file access
    original_cwd = os.getcwd()
    try:
        # Change to the directory containing storage.json
        storage_dir = os.path.dirname(os.path.abspath(__file__)) if not hasattr(sys, '_MEIPASS') else original_cwd
        os.chdir(storage_dir)
        
        # Import and run the CLI
        import importlib.util
        main_cli_path = os.path.join(base_path, 'backend', 'main-cli.py')
        spec = importlib.util.spec_from_file_location("main_cli", main_cli_path)
        main_cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_cli)
        
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    main()

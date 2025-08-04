#!/usr/bin/env python3
"""
PyTo-Do - A simple task management CLI application
Main entry point for the application
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the main CLI application
if __name__ == "__main__":
    # Change directory to backend to handle relative imports properly
    original_dir = os.getcwd()
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    try:
        # Import the CLI module and run it
        import importlib.util
        spec = importlib.util.spec_from_file_location("main_cli", "main-cli.py")
        main_cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_cli)
    finally:
        # Restore original directory
        os.chdir(original_dir)

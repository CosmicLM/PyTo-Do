"""
PyTo-Do Launcher - Choose your interface
Originally created by CosmicLM | Enhanced by mdnoyon9758
"""

import sys
import os
import subprocess

def show_menu():
    """Show interface selection menu"""
    print("🚀 PyTo-Do Task Manager")
    print("Originally created by CosmicLM | Enhanced by mdnoyon9758")
    print("=" * 50)
    print("Choose your interface:")
    print("1. 🎨 Modern GUI (Recommended)")
    print("2. 🖥️  Classic GUI")
    print("3. ☁️  Cloud Sync Interface")
    print("4. 💻 CLI Interface")
    print("5. 🔨 Build Executable")
    print("0. ❌ Exit")
    print("=" * 50)

def launch_interface(choice):
    """Launch the selected interface"""
    try:
        if choice == "1":
            print("🎨 Launching Modern GUI...")
            import frontend.modern_gui
            frontend.modern_gui.main()
        elif choice == "2":
            print("🖥️ Launching Classic GUI...")
            import frontend.gui
            frontend.gui.main()
        elif choice == "3":
            print("☁️ Launching Cloud Sync...")
            import frontend.cloud_sync
            frontend.cloud_sync.main()
        elif choice == "4":
            print("💻 Launching CLI...")
            import main
            main.main()
        elif choice == "5":
            print("🔨 Running build script...")
            subprocess.run([sys.executable, "build.py"])
        elif choice == "0":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice! Please try again.")
            return False
        return True
    except ImportError as e:
        print(f"❌ Error importing module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error launching interface: {e}")
        return False

def main():
    """Main launcher function"""
    while True:
        show_menu()
        choice = input("Enter your choice (0-5): ").strip()
        
        if choice == "0":
            break
            
        if launch_interface(choice):
            # Ask if user wants to launch another interface
            again = input("\n🔄 Launch another interface? (y/n): ").strip().lower()
            if again not in ['y', 'yes']:
                break
        
        print()  # Add spacing

if __name__ == "__main__":
    main()

# main.py
import os
import sys
from frontend.main_window import MainWindow
from config.settings import Settings

def main():
    """Main entry point for the application"""
    
    # Setup directories
    Settings.setup_directories()
    
    # Check if user data file exists
    if not os.path.exists(Settings.USER_DATA_PATH):
        print(f"ERROR: User data file not found at {Settings.USER_DATA_PATH}")
        print("Please create the user_data.json file using the provided template.")
        sys.exit(1)
    
    # Start the GUI application
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
import sys

# Mulit DB Support
from database import DB
from os import listdir

class GUI(QWidget):
    def __init__(self):
        # Ground Work
        super().__init__() 
        self.initGui()

        # Detect if a PSOChat.db exists
            # Check if defaults table exists
            # Else create defaults table
        # Else check for a defaults.db
            # Check defaults if not
            # Else create one and collect

    # Setup Visuals
    def initGui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setWindowTitle('PSO2Chat Parser ~ Hoes Not Included')
        self.resize(200, 200)
        self.show()

    def prompt_for_chat(self):
        # Ask for chat directory
        # Store directory into defaults table
        pass

    def scan_for_new(self):
        # Scan directory for new files to be imported
        # Compare hashed file contents
            # If filename and hash do not match
            # Prompt for dropping old and importing new
        pass

    def add_new_file(self):
        # Add new file to the database
        pass

    def display_query_results(self):
        # Query database
            # Display results in meaningful way

    # Buttons that concatenate the string to make a query
    # SID       search
        # Pull down checkboxes
    # PID       search
        # Pull down checkboxes
    # Name      search
        # Pull down checkboxes
    # Keyword   search
        # Fill in blank
    # Day       filter
        # Calendar Widget
    # Time      filter
        # Time slider 00:00:00 -> 23:59:59
    # Chat Type filter
        # Checkboxes




if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = GUI()
    sys.exit(app.exec_())
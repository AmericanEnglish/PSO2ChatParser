from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from Crypto.Hash import SHA256 as SHA # for hashing
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
        self.resize(400, 400)
        self.show()

        ########################## Database stuff
        # Scan for "PSO2ChatParser.db"
        if "PSO2ChatParser.db" in listdir("./"):
            # Scan for defaults table
            self.db = DB("sqlite3", "./PSO2ChatParser.db")
            self.defaults = self.db
            # If more defaults besides the database become available
            self.db.execute("""SELECT name, value FROM defaults WHERE name="path" """)
            default_path = self.db.fetchall()[0][1]
            scan_for_new(default_path)
        # Else scan for "ParserDefaults.db"
        elif "ParserDefaults.db" in lsitdir("./"):
            # Dispatch default values
            self.defaults = DB("sqlite3", "ParserDefaults.db")
            prompt_for_posgres()
        # Else prompt for default server settings
        else:
            server_type = prompt_for_server_type()
            # Create "ParserDefaults.db"
            if server_type == "postgres":
                self.defaults = DB("sqlite3", "ParserDefaults.db")
                prompt_for_posgres()
            # Else create "PSO2ChatParser.db"
            else:
                self.db = DB("sqlite3", "PSO2ChatParser.db")
                self.defaults = self.db
                # Create the tables needed
                self.db.create_table("create.sql")

    def prompt_for_posgres(self):
        # For logging into postgresql and handiling postgres startup stuff
        pass

    def prompt_for_chat(self):
        # Ask for chat directory
        # Store directory into defaults table
        pass

    def scan_for_new(self, default_path):
        # Scan directory for new files to be imported
        # Compare hashed file contents
            # If filename and hash do not match
            # Prompt for dropping old and importing new
        pass

    def add_new_file(self, path_to_file):
        # Add new file to the database
        pass

    def display_query_results(self):
        # Query database
            # Display results in meaningful way
        pass
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
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMainWindow, QFileDialog, QMessageBox
from Crypto.Hash import SHA256 # for hashing
import sys
import re

# Mulit DB Support
from database import DB
from os import listdir

class MainGUI(QMainWindow):
    def __init__(self):
        # Ground Work
        super().__init__() 
        self.query_arguments = {
        "SELECT":(
                ("stamp", False),
                ("chat_type", False),
                ("uid", False),
                ("username", False),
                ("text", False)),
        "WHERE":{}
        }
        self.initGui()
        self.initDB()
        self.popups = []

    # Setup Visuals
    def initGui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setWindowTitle('PSO2Chat Parser ~ Hoes Not Included')
        self.resize(400, 400)
        self.show()

    def initDB(self):
        # Scan for "PSO2ChatParser.db"
        if "PSO2ChatParser.db" in listdir("./"):
            # Scan for defaults table
            self.db = DB("sqlite3", "./PSO2ChatParser.db")
            self.defaults = self.db
            # If more defaults besides the database become available
            self.db.execute("""SELECT name, value FROM defaults WHERE name = "default_path";""")
            default_path = self.db.fetchall()[0][1]
            self.scan_for_new(default_path)
        # Else scan for "ParserDefaults.db"
        elif "ParserDefaults.db" in listdir("./"):
            # Dispatch default values
            self.defaults = DB("sqlite3", "ParserDefaults.db")
            self.prompt_for_posgres()
        # Else prompt for default server settings
        else:
            # Will finish this bit later
            # server_type = self.prompt_for_server_type()
            server_type = "sqlite3"
            if server_type == None or server_type == "":
                self.failed_to_select_database()
            # Create "ParserDefaults.db"
            elif server_type == "postgres":
                self.defaults = DB("sqlite3", "ParserDefaults.db")
                self.default.connect()
                self.prompt_for_posgres(create_new=True)
            # Else create "PSO2ChatParser.db"
            else:
                self.db = DB("sqlite3", "PSO2ChatParser.db")
                self.db.connect()
                self.defaults = self.db
                # Create the tables needed
                self.db.execute("""CREATE TABLE defaults (name VARCHAR(15), value VARCHAR(30), PRIMARY KEY (name));""")
                self.db.create_table("./create.sql")
                self.prompt_for_chat()
                self.scan_for_new()


    def prompt_for_posgres(self, create_new=False):
        # For logging into postgresql and handiling postgres startup stuff
        # Open dialog for entering username and password

        # Connect
        self.db = DB("postgres", hostname=hostname, username=username, password=password)
        # Create?
        if create_new == True:
            self.db.create_table("./create.sql")

    def prompt_for_chat(self):
        # Ask for chat directory
        self.default_path = QFileDialog.getExistingDirectory(self, 'Select default chat directory', './', QFileDialog.ShowDirsOnly)
        ################### 
        # Check to see if default path was returned
            # If so then proceed as normal
            # elseif check to see if defined in the database if so proceed
            # else return failure prompt
        ###################
        # Store directory into defaults table
        self.defaults.execute("""INSERT INTO defaults VALUES ("default_path", %s)""", [str(self.default_path)])

    def scan_for_new(self):
        ################ ADD A PROGRESS BAR AT SOME POINT
        # Scan directory for new files to be imported
        allfiles = listdir(self.default_path)
        chat_files = []
        key = SHA256.new()
        total = count(allfiles, ".txt")
        current = 0
        for item in allfiles:
            if item[-4:] == ".txt" and "ChatLog" in item:    
                current += 1
                # Compare hashed file contents
                with open(self.default_path + item, 'r', encoding='utf-16') as doc:
                    # Obtain hash and filenames
                    contents = doc.read()
                key.update(contents.encode(encoding="utf16"))
                log_hash = key.hexdigest()
                self.db.execute("""SELECT hash FROM logs WHERE name = %s;""", [item])
                queried_hash = self.db.fetchall()[0][0]
                self.db.execute("""SELECT name FROM logs WHERE hashed_contents = %s;""", [log_hash])
                queried_name = self.db.fetchall()[0][0]
                # If filename and hash do not match 
                if queried_name == item:
                    if queried_hash == log_hash:
                        print("Processing: {}/{} -> {} -> File Present -> Skipped", current, total, item[7:-4])
                    else:
                        self.add_new_file(self.default_path + item, do_hash=False, log_hash=log_hash)
                        self.db.execute("""UPDATE logs SET hashed_contents = %s WHERE name = %s;""", [log_hash, item])
                elif queried_hash == log_hash:
                    print("Processing: {}/{} -> {}\n\tFile already import but filename is different? -> Skipped", current, total, item[7:-4])
                else:
                    self.add_new_file(log_hash, self.default_path + item)

    def add_new_file(self, path_to_file, do_hash=True, log_hash=None):
        # Begin Hashing process
        if (do_hash):
            with open(path_to_file, 'r', encoding='utf-16') as doc:
                # Obtain hash and filenames
                contents = doc.read()
            key.update(contents.encode(encoding="utf16"))
            log_hash = key.hexdigest()
            ################ COME BACK AND FIX THIS BECAUSE path_to_file != filename
            self.db.execute("""SELECT hash FROM logs WHERE name = %s;""", [path_to_file])
            ################
            queried_hash = self.db.fetchall()[0][0]
            self.db.execute("""SELECT name FROM logs WHERE hashed_contents = %s;""", [log_hash])
            queried_name = self.db.fetchall()[0][0]
            # If filename and hash do not match 
            if queried_name == item:
                if queried_hash == log_hash:
                    print("File has alread been imported! -> Skipped")
                    return # Quit out
            elif queried_hash == log_hash:
                print("File already import but filename is different? -> Skipped")
                return # Quit out
        # Add new file to the database
        key = SHA256.new()
        with open(path_to_file, 'r', encoding='utf-16') as doc:
            buff = []
            self.db.execute("""INSERT INTO logs VALUES (%s, %s);""", [path_to_file, log_hash])
            for line in doc:
                line = re.split("\t", line)
                if len(line) > 6:
                    temp = line[:6]
                    temp.append('\t'.join(line[6:]))
                    line = temp
                if timestamp(line[0]):
                    line.insert(0, log_hash)
                    self.db.execute("""INSERT INTO chat VALUES
                        (%s, %s, %s, %s, %s, %s, %s);""", line)
                    buff = [line[1], line[2], line[4]]
                else:
                    # print('Problem Line {}'.format(buff))
                    self.db.execute("""UPDATE chat
                        SET info = info || %s
                        WHERE stamp = %s AND
                            uid = %s AND
                            line_num = %s;""",
                                [' '.join(line), buff[0], buff[1], buff[2]])
        # cur.execute("""INSERT INTO logs VALUES (%s)""", [iv])

    def prompt_for_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.default_path)
        self.add_new_file(filename)


    def prompt_for_server_type(self):
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

    def failed_to_select_database(self):
        # Throw error popup
        w = QMessageBox.critical(self, 'ERROR', "No database selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        exit()


def count(collection, extension):
    total = 0
    for path_to_file in collection:
        if item[-4:] == extension:
            total += 1
    return total


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = MainGUI()
    sys.exit(app.exec_())
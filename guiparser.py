from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QGridLayout, QFileDialog, QMessageBox, QProgressDialog, QPushButton, QLabel, QLineEdit, QCheckBox
from Crypto.Hash import SHA256 # for hashing
from AdditionalWidgets import *
from timestamp import timestamp
from time import sleep
import sys
import re

# Mulit DB Support
from database import DB
from os import listdir

# class MainGUI(QMainWindow):
class MainGUI(QWidget):
    def __init__(self):
        # Ground Work
        super().__init__() 
        self.query_arguments = {
        "SELECT":{
                    "stamp":False,
                    "chat_type":False,
                    "uid":False,
                    "username":False,
                    "text":False
                },
        "WHERE":{}
        }
        self.initGui()
        self.initDB()

    # Setup Visuals
    def initGui(self):
        self.popups = {}
        self.latest_popup = None
        # self.resize(400, 100)
        grid = QGridLayout()
        grid.setSpacing(10)
        self.setWindowTitle('PSO2ChatParser ~ Hoes Not Included')
        
        # SID       search / filter
        self.popups["SID"] = SegaID()
        SID = QPushButton("SegaID", self)
        SID.clicked.connect(lambda:self.show_latest_popup("SID"))
        SID.setFixedSize(80,80)
        grid.addWidget(SID, 0, 0)
        
        #     Pull down checkboxes
        # PID       search / filter
        self.popups["PID"] = PlayerID()
        PID = QPushButton("Username", self)
        PID.setFixedSize(80, 80)
        PID.clicked.connect(lambda:self.show_latest_popup("PID"))
        grid.addWidget(PID, 0, 1)
        #     Pull down checkboxes

        # Chat Type filter
        self.popups["ChatType"] = ChatTypeWidget()
        ChatTypeButton = QPushButton("Chat Type", self)
        ChatTypeButton.setFixedSize(80, 80)
        ChatTypeButton.clicked.connect(lambda:self.show_latest_popup("ChatType"))
        grid.addWidget(ChatTypeButton, 0, 2)

        #     Fill in blank
        # Day       search / filter
        TimeDat = QPushButton("Time", self)
        TimeDat.setFixedSize(80, 80)
        TimeDat.clicked.connect(lambda:print("TimeDat Open"))
        grid.addWidget(TimeDat,0, 3)


        # Keyword   search
        Keyword = QPushButton("Keyword", self)
        Keyword.setFixedSize(80, 80)
        Keyword.clicked.connect(lambda:print("Keyword Open"))
        grid.addWidget(Keyword, 0, 4)

        SettingsButton = QPushButton("Settings", self)
        SettingsButton.setFixedSize(80, 80)
        SettingsButton.clicked.connect(lambda:print("Settings Open"))
        grid.addWidget(SettingsButton, 0, 5)

        # Begin query button
        GO = QPushButton("GO ->", self)
        GO.setFixedSize(80, 80)
        GO.clicked.connect(lambda:print("Begin Search"))
        grid.addWidget(GO, 0, 6)

        #     Calendar Widget
        # Time      search / filter
        #     Time slider 00:00:00 -> 23:59:59


        #####################################
        self.setLayout(grid)
        self.show()

    def initDB(self):
        # Scan for "PSO2ChatParser.db"
        if "PSO2ChatParser.db" in listdir("./"):
            # Scan for defaults table
            self.db = DB("sqlite3", "./PSO2ChatParser.db")
            self.defaults = self.db
            # If more defaults besides the database become available
            self.db.execute("""SELECT value FROM defaults WHERE name = "default_path";""")
            self.default_path = self.db.fetchall()
            if self.default_path == []:
                self.prompt_for_chat()
            else:
                self.default_path = self.default_path[0][0]
            self.scan_for_new()
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
                self.db.execute("""CREATE TABLE defaults (name VARCHAR(15), value VARCHAR(30) NOT NULL, PRIMARY KEY (name));""")
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
        if self.default_path == None or self.default_path == '':
            # Check to see if defined in the database if so proceed
            self.db.execute("""SELECT value FROM defaults WHERE name =  "default_path";""")
            self.default_path = self.db.fetchall()
            print(self.default_path)
            # If no results returned, failure. 
            if self.default_path == []:
                self.failed_to_select_folder()
            else:
                self.default_path = self.default_path[0][0]
        ###################
        # Store directory into defaults table
        else:
            self.default_path += "/"
            self.defaults.execute("""INSERT INTO defaults VALUES ("default_path", %s);""", [self.default_path])

    def scan_for_new(self):
        ################ ADD A PROGRESS BAR AT SOME POINT
        # Scan directory for new files to be imported
        allfiles = listdir(self.default_path)
        chat_files = seize_chats(allfiles)
        chat_files.sort()
        if chat_files == []:
            return

        
        current = 0
        ################ First Progress bar
        gui_val = 0
        total = len(chat_files)
        FirstProgressBar = QProgressDialog("Starting", "Quit Importing", 0, total, self)
        FirstProgressBar.setWindowTitle('Importing Chat Files . . .')
        FirstProgressBar.setFixedSize(400, 150)
        FirstProgressBar.setMinimumDuration(4)
        FirstProgressBar.setModal(True)
        FirstProgressBar.show()
        print("Progress bar setup")
        ################
        for index, item in enumerate(chat_files):
            key = SHA256.new()
            # FirstProgressBar.show()
            # print("Loop over {}".format(item))
            # print(item)
            if FirstProgressBar.wasCanceled():
                break
            FirstProgressBar.setLabelText(item)
            print("Processing: {}/{} -> {}".format(str(index + 1).zfill(len(str(total))), total, item[-15:-5]))
            FirstProgressBar.show()
            QApplication.processEvents()

            premature_quit = self.add_new_file(self.default_path + item, ProgressBarTuple=(FirstProgressBar, item))
            FirstProgressBar.setValue(index + 1)
            QApplication.processEvents()
            if FirstProgressBar.wasCanceled() or (premature_quit != None and premature_quit):
                break

            # print("Loop Progressed")
        FirstProgressBar.setValue(total)
        FirstProgressBar.destroy()
        print("Progress bar closed")

    def add_new_file(self, path_to_file, do_hash=True, log_hash=None, ProgressBarTuple=None):
        # Begin Hashing process
        update_log_hash = False
        key = SHA256.new()
        if (do_hash):
            with open(path_to_file, 'r', encoding='utf-16') as doc:
                # Obtain hash and filenames
                contents = doc.read()
            key.update(contents.encode(encoding="utf16"))
            log_hash = key.hexdigest()
            # Grab everything
            self.db.execute("""SELECT hashed_contents FROM logs;""")
            queried_hash = self.db.fetchall()
            ######################################
            self.db.execute("""SELECT name FROM logs;""")
            queried_name = self.db.fetchall()
            ######################################
            # If filename and hash do not match 
            if (path_to_file,) in queried_name:
                if (log_hash,) in queried_hash:
                    print("File has alread been imported! -> Skipped")
                    return # Quit out
                else:
                    ### Prepping for reprocessing
                    print("Contents Changed? -> Reprocessing!")
                    update_log_hash = True
            elif (log_hash,) in queried_hash:
                print("File already imported but filename is different? -> Skipped")
                return # Quit out
        # Add new file to the database
        # key = SHA256.new()
        if update_log_hash:
            #### This will be a fix for sqlite only because ON UPDATE CASCADE fails
            if self.db.db_type == "sqlite3":
                # First pull down the original value
                print("SQLite3 DB, DROPPING OLD FILE CONTENTS")
                self.db.execute("""SELECT hashed_contents FROM logs WHERE name = %s;""",
                    [path_to_file])
                results = self.db.fetchall()
                results = results[0][0]
                # Then drop everything because yolo i guess
                self.db.execute("""DELETE FROM chat WHERE log_hash = %s;""", [results])
                self.db.execute("""DELETE FROM logs WHERE hashed_contents = %s""", [results])
                print("-> REDOING FILE CONTENTS")
            else:
                self.db.execute("""UPDATE logs
                        SET hashed_contents = %s
                        WHERE name = %s;""", [log_hash, path_to_file]) # Update the log hash value here
        else:
            self.db.execute("""INSERT INTO logs VALUES (%s, %s);""", 
            [path_to_file, log_hash])
        contents = re.split("\n", contents)
        split_body = []
        for line in contents:
            line = re.split("\t", line)
            if len(line) > 6:
                line[5] = '\t'.join(line[5:])
            elif len(line) < 6:
                split_body[-1][-1] += "\n" + '\t'.join(line)
                continue
            split_body.append(line)
        ############################################
        current = 0
        for line in split_body:
            key = SHA256.new()
            current += 1
            # Update the progress bar
            if ProgressBarTuple != None:
                ProgressBarTuple[0].setLabelText(ProgressBarTuple[1] + "\n{}/{}".format(current, len(split_body)))
                ProgressBarTuple[0].show()
                QApplication.processEvents()
            #########################
            # print("Line {}/{} -> {}".format(current, total_lines, path_to_file[-15:-7]))
            # Hash the line
            # Timestamp, SegaID, ChatType, Info
            # print(line[0] + str(line[3]) + line[2] + line[-1])
            key.update((line[0] + str(line[3]) + line[2] + line[-1]).encode(
                encoding="utf-16"))
            line_hash = key.hexdigest()
            # print(line_hash)
            # Check to see if line exists
            self.db.execute("""SELECT log_hash, line_hash 
                FROM chat WHERE line_hash = %s;""", [line_hash])
            results = self.db.fetchall()
            # If so update the "count"
            # print(results)
            if results != [] and len(results) == 1:
                # Only insert if it's detected in the original file
                if results[0][0] == log_hash:
                    self.db.execute("""UPDATE chat
                        SET occur = occur + 1
                        WHERE line_hash = %s;""", [results[0][1]])
                # print("Line hash exists!")
                    # print("Area 1")
            elif len(results) > 1:
                print("Results of line 215 > 1")
                print(results)
                print(line)
            else:
                # Else insert 
                line.insert(0, line_hash)
                line.insert(0, log_hash)
                line.append(1)
                self.db.execute("""INSERT INTO chat VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)
                # print("Area 2")
                # print(line)

    def prompt_for_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.default_path)
        self.add_new_file(filename)

    def prompt_for_server_type(self):
        pass

    def display_query_results(self):
        # Query database
            # Display results in meaningful way
        pass

    def show_latest_popup(self, popup):
        if self.latest_popup == None:
            self.popups[popup].show()
            self.latest_popup = popup
        else:
            self.popups[self.latest_popup].hide()
            self.latest_popup = popup
            self.popups[self.latest_popup].show()

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
        QMessageBox.critical(self, 'ERROR', "No database selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        exit()

    def failed_to_select_folder(self):
        # Throw error popup
        QMessageBox.critical(self, 'ERROR', "No default folder selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        exit()        
# This will allow a popup with two progress bars




def count(collection, extension):
    total = 0
    for item in collection:
        if item[-4:] == extension:
            total += 1
    return total


def seize_chats(some_list):
    new_list = []
    for item in some_list:
        if ".txt" == item[-4:] and "ChatLog" in item:
            new_list.append(item)
    return new_list


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = MainGUI()
    sys.exit(app.exec_())
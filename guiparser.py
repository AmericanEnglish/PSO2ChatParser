from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFileDialog, QMessageBox, QProgressDialog, QPushButton
from AdditionalWidgets import *
from timestamp import timestamp
import sys
import re
from multiprocessing import freeze_support, Pool

# Mulit DB Support
from database import DB
from os import listdir

# Mapping Functions
from functools import partial
from datetime import datetime
from reader import search_file

# class MainGUI(QMainWindow):
class MainGUI(QWidget):
    def __init__(self):
        # Ground Work
        super().__init__() 
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

        # Date

        #     Fill in blank
        # Day       search / filter
        self.popups["DateDat"] = ChatTime()
        TimeDat = QPushButton("Date", self)
        TimeDat.setFixedSize(80, 80)
        TimeDat.clicked.connect(lambda:self.show_latest_popup("DateDat"))
        grid.addWidget(TimeDat,0, 3)


        # Keyword   search
        self.popups["Keyword"] = KeywordSearch()
        Keyword = QPushButton("Keyword", self)
        Keyword.setFixedSize(80, 80)
        Keyword.clicked.connect(lambda:self.show_latest_popup("Keyword"))
        grid.addWidget(Keyword, 0, 4)

        # Settins
        self.popups["Settings"] = SettingsWidget()
        SettingsButton = QPushButton("Settings", self)
        SettingsButton.setFixedSize(80, 80)
        SettingsButton.clicked.connect(lambda:self.show_latest_popup("Settings"))
        grid.addWidget(SettingsButton, 0, 5)

        # Begin query button
        GO = QPushButton("GO ->", self)
        GO.setFixedSize(80, 80)
        GO.clicked.connect(lambda:self.run())
        grid.addWidget(GO, 0, 6)

        # Get a Reader for displaying text
        self.popups["Reader"] = Reader()

        #####################################
        self.setLayout(grid)
        self.show()

    def initDB(self):
        # Else scan for "ParserDefaults.db"
        if "ParserDefaults.db" in listdir("./"):
            # Dispatch default values
            self.defaults = DB("ParserDefaults.db")
            self.db = DB("ParserDefaults.db")
            self.defaults.connect()
            # If more defaults besides the database become available
            self.defaults.execute("""SELECT value FROM defaults WHERE name = "default_path";""")
            self.default_path = self.defaults.fetchall()
            if self.default_path == []:
                self.prompt_for_chat()
            else:
                self.default_path = self.default_path[0][0]
            
            #  self.scan_for_new()
        # Else prompt for default server settings
        else:
            # Create "ParserDefaults.db"
            self.db = DB("ParserDefaults.db")
            self.db.connect()
            self.defaults = self.db
            # Create the tables needed
            self.defaults.execute("""CREATE TABLE defaults (name VARCHAR(15), value VARCHAR(30) NOT NULL, PRIMARY KEY (name));""")
            self.prompt_for_chat()
            #  self.scan_for_new()
        #  self.popups["Settings"].setDB(self.db.db_type)
        #  self.popups["Settings"].setDB("sqlite3")
        self.popups["SID"].setDB(self.db)
        self.popups["PID"].setDB(self.db)


    def prompt_for_chat(self):
        # Ask for chat directory
        self.default_path = QFileDialog.getExistingDirectory(self, 'Select default chat directory', './', QFileDialog.ShowDirsOnly)
        ################### 
        # Check to see if default path was returned
        if self.default_path == None or self.default_path == '':
            # Check to see if defined in the database if so proceed
            self.defaults.execute("""SELECT value FROM defaults WHERE name =  "default_path";""")
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


    def prompt_for_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', self.default_path)
        self.add_new_file(filename)

    def show_latest_popup(self, popup):
        if self.latest_popup == None:
            self.popups[popup].show()
            self.latest_popup = popup
        elif self.latest_popup == popup:
            self.popups[popup].hide()
            self.latest_popup = None
        else:
            self.popups[self.latest_popup].hide()
            self.latest_popup = popup
            self.popups[self.latest_popup].show()

    def full_query(self):
        query_strings = self.generate_query()
        print(query_strings)
        self.db.execute(query_strings[0][0], query_strings[0][1])
        results = self.db.fetchall()
        print("Total Log Hits: {}".format(len(results)))
#        with open('sample.txt', 'w') as newfile:
#            for item in results:
#                newfile.write(str(item) + "\n")
        # Hits per log
        print("Hits per log:")
        for item in results:
            print("{} -> {}".format(item[0].split("/")[-1], item[2]))

        # Pipe these days to a selection window which will spawn the according windows
        # This should return indices of things to be displayed

        # Then pipe data into Reader
        
    def failed_to_select_folder(self):
        # Throw error popup
        QMessageBox.critical(self, 'ERROR', "No default folder selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        sys.exit(1)        

    def closeEvent(self, event):
        for key in self.popups.keys():
            self.popups[key].deleteLater()
        event.accept()

    def run(self):
        data = []
        # Get all data
        data.append(self.popups["DateDat"].liquidate())
        data.append(self.popups["SID"].liquidate())
        data.append(self.popups["PID"].liquidate())
        data.append(self.popups["ChatType"].liquidate())
        data.append(self.popups["Keyword"].liquidate())
        print(data)
        allFiles = seize_chats(listdir(self.default_path))
        allFiles = list(map(partial(lambda x, base: base + x, base=self.default_path), allFiles))
        if len(allFiles) > 100:
            searchpool = Pool(8)
            print("==========Beginning==========")
            results = list(searchpool.map(partial(search_file, parameters=data), allFiles))
        else:
            results = list(map(partial(search_file, parameters=data), allFiles))
        # Do more stuff
        count = 0
        for index, item in enumerate(results):
            if item != []:
                print(allFiles[index], item)
                count += 1
        print("==========Total Logs of Interest: {}==========".format(count))




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
    freeze_support()
    app = QApplication(sys.argv)
    obj = MainGUI()
    sys.exit(app.exec_())

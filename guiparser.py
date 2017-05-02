from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QFileDialog, QMessageBox, QProgressDialog, QPushButton
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
        GO.clicked.connect(lambda:self.full_query())
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
            self.defaults.connect()
            self.prompt_for_posgres()
            # If more defaults besides the database become available
            self.defaults.execute("""SELECT value FROM defaults WHERE name = "default_path";""")
            self.default_path = self.defaults.fetchall()
            if self.default_path == []:
                self.prompt_for_chat()
            else:
                self.default_path = self.default_path[0][0]
            
            self.scan_for_new()
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
        self.popups["Settings"].setDB("sqlite3")
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
        


    def generate_query(self):
        # Buttons that concatenate the string to make a query
        # Search for query
        find_log = """SELECT name, hashed_contents, COUNT(hashed_contents) FROM logs 
                            INNER JOIN chat ON logs.hashed_contents = chat.log_hash
                             """
        find_strings = [[]]
        find_params = []
        # Filter by queries
        pull_log = "SELECT stamp, username, info, chat_type FROM chat " 
        pull_strings = [[]]
        pull_params = []
        # SID       search -> OR TERMS
        sid = self.popups["SID"].liquidate()
        if sid[0] == True and sid[2] != []:
            # Search for
            # WHERE 
            for term in sid[2]:
                find_strings[-1].append("uid = %s")
                find_params.append(term)
        find_strings.append([])
        
        if sid[1] == True and sid[2] != []:
            # Filter By
            for term in sid[2]:
                pull_strings[-1].append("uid = %s")
                pull_params.append(term)
        pull_strings.append([])

        # Name      search -> OR TERMS
        pid = self.popups["PID"].liquidate()
        if pid[0] == True and pid[2]  != []:
            # Search for
            for term in pid[2]:
                find_strings[-1].append("username = %s")
                find_params.append(term)
        find_strings.append([])
        
        if pid[1] == True and pid[2] != []:
            # Filter By
            for term in pid[2]: 
                pull_strings[-1].append("username = %s")
                pull_params.append(term)
        pull_strings.append([])
        
        # Keyword   search
        keyword = self.popups["Keyword"].liquidate()
        if keyword != []:
            if keyword[0] == "LOWER":
                keyword_phrase = "LOWER(info) LIKE LOWER(%s)"
            else:
                keyword_phrase = "info LIKE %s"
            for term in keyword[1]:
                find_strings[-1].append(keyword_phrase)
                find_params.append("%" + term + "%")
        find_strings.append([])
        
        # Day       search -> DATE MATH
        chatdays = self.popups["DateDat"].liquidate()
        if chatdays != [None, None]:
            # yyyy-MM-ddThh:mm:ss
            if chatdays[0] == None:
                find_strings[-1].append("%s <= stamp")
                find_strings.append(["stamp <= %s"])
                find_params.append(chatdays[1][0])
                find_params.append(chatdays[1][1])
            elif chatdays [1] == None:
                find_strings[-1].append("%s <= stamp")
                find_strings.append(["stamp <= %s"])
                find_params.append(chatdays[0][0])
                find_params.append(chatdays[0][1])
            else:
                find_strings[-1].append("%s <= stamp")
                find_strings.append(["stamp <= %s"])
                find_params.append(chatdays[0][0])
                find_params.append(chatdays[1][1])
            find_strings.append([])



        ChatType = self.popups["ChatType"].liquidate()
        # Chat Type filter -> OR TERMS
        for item in ChatType:
            if item[1] == True:
                pull_strings[-1].append("chat_type = %s")
                pull_params.append(item[0])
        # pull_strings.append([])

        print("Find Strings: {}".format(find_strings))
        # Concatenate it all
        if find_strings != [[], [], [], []]:
            temp = []
            for item in find_strings:
                if item != []:
                    temp.append("(" + ' OR '.join(item) + ")")
            full_find = ' AND '.join(temp)
            find_log += "WHERE " + full_find + " GROUP BY hashed_contents;"
        else:
            find_log += " GOUP BY hashed_contents;"
        print("Pull Strings: {}".format(pull_strings))
        if pull_strings != [[], [], [], []]:
            temp = []
            for item in pull_strings:
                if item != []:
                    temp.append("(" + ' OR '.join(item) + ")")
            full_pull = ' AND '.join(temp)
            pull_log += "WHERE " + full_pull + " "
        else:
            pull_log += " "
#        print("----------------------LOG QUERY------------------")
#        print(pull_log)
#        print("----------------------LOG PARAMS-----------------")
#        print(pull_params)
#        print("----------------------FIND QUERY-----------------")
#        print(find_log)
#        print("----------------------FIND PARAM-----------------")
#        print(find_params)
#        print("##################################################")
        return [(find_log, find_params), (pull_log[:-1], pull_params)]
        

    def failed_to_select_database(self):
        # Throw error popup
        QMessageBox.critical(self, 'ERROR', "No database selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        sys.exit(1)

    def failed_to_select_folder(self):
        # Throw error popup
        QMessageBox.critical(self, 'ERROR', "No default folder selected! This is REQUIRED", QMessageBox.Ok, QMessageBox.Ok)
        # Quit out
        sys.exit(1)        

    def closeEvent(self, event):
        for key in self.popups.keys():
            self.popups[key].deleteLater()
        event.accept()




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

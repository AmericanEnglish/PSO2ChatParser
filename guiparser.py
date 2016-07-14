from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from Crypto.Hash import SHA256 # for hashing
import sys
import re

# Mulit DB Support
from database import DB
from os import listdir

class GUI(QWidget):
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
            self.db.execute("""SELECT name, value FROM defaults WHERE name = chat_directory;""")
            default_path = self.db.fetchall()[0][1]
            self.scan_for_new(default_path)
        # Else scan for "ParserDefaults.db"
        elif "ParserDefaults.db" in listdir("./"):
            # Dispatch default values
            self.defaults = DB("sqlite3", "ParserDefaults.db")
            self.prompt_for_posgres()
        # Else prompt for default server settings
        else:
            server_type = self.prompt_for_server_type()
            # Create "ParserDefaults.db"
            if server_type == "postgres":
                self.defaults = DB("sqlite3", "ParserDefaults.db")
                self.prompt_for_posgres(create_new=True)
            # Else create "PSO2ChatParser.db"
            else:
                self.db = DB("sqlite3", "PSO2ChatParser.db")
                self.defaults = self.db
                # Create the tables needed
                self.db.create_table("./create.sql")
                default_path = prompt_for_chat()
                self.scan_for_new(default_path)


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
        # Store directory into defaults table
        pass

    def scan_for_new(self, default_path):
        # Scan directory for new files to be imported
        allfiles = listdir("default_path")
        chat_files = []
        key = SHA256.new()
        total = count(allfiles, ".txt")
        current = 0
        for item in allfiles:
            if item[-4:] == ".txt" and "ChatLog" in item:    
                current += 1
                # Compare hashed file contents
                with open(default_path + item, 'r', encoding='utf-16') as doc:
                    # Obtain hash and filenames
                    contents = doc.read()
                key.update(contents.encode(encoding="utf16"))
                true_hash = key.hexdigest()
                self.db.execute("""SELECT hash FROM logs WHERE name = %s;""", item)
                queried_hash = self.db.fetchall()[0][0]
                self.db.execute("""SELECT name FROM logs WHERE hashed_contents = %s;""", true_hash)
                queried_name = self.db.fetchall()[0][0]
                # If filename and hash do not match 
                if queried_name == item:
                    if queried_hash == true_hash:
                        print("Processing: {}/{} -> {} -> File Present -> Skipped", current, total, item[7:-4])
                    else:
                        self.add_new_file(default_path + item, do_hash=False)
                        self.db.execute("""UPDATE logs SET hashed_contents = %s WHERE name = %s;""", [true_hash, item])
                elif queried_hash == true_hash:
                    print("Processing: {}/{} -> {}\n\tFile already import but filename is different? -> Skipped", current, total, item[7:-4])
                else:
                    self.add_new_file(true_hash, default_path + item)

    def add_new_file(self, log_hash, path_to_file, do_hash=True):
        # Add new file to the database
        key = SHA256.new()
        with open(default_path + item, 'r', encoding='utf-16') as doc:
            buff = []
            self.db.execute("""INSERT INTO logs VALUES (%s, %s);""", [item, log_hash])
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
        pass

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


def count(collection, extension):
    total = 0
    for item in collection:
        if item[-4:] == extension:
            total += 1
    return total


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = GUI()
    sys.exit(app.exec_())
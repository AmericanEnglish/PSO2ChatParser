from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
import sys

# Mulit DB Support
import psycopg2
import sqlite3

class GUI(QWidget):
    def __init__(self):
        # Ground Work
        super().__init__() 
        self.initGui()

    # Setup Visuals
    def initGui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setWindowTitle('PSO2Chat Parser ~ Hoes Not Included')
        self.resize(200, 200)
        self.show()


    # Parsing Commands

    # Database Command Util

    # Displaying Chat

class DB():
    """Used for interacting with a database by cutting down on some database
    specific interactions."""
    # Database Skeleton
    def __init__(self, db_type, db_name, host='localhost', username=None, password=None):
        self.db_type = db_type
        self.host = localhost
        self.username = username
        self.password = password
        self.con = None
        self.cur = None

    def connect(self):
        if db_type == 'sqlite3':
            self.con = sqlite3.connect(database=db_name)
            return True, None

        elif db_type == 'postgres':
            try:
                self.con = psycopg2.connect(host=host, database=db_name, user=username, password=password)
                self.password = None
                return True, None
            except psycopg2.OperationalError as err:
                return False, err

    def cur_gen(self):
        self.cur = self.con.cursor()

    def commit(self):
        self.con.commit()

    def execute(self, string, arguments=None):
        if arguments == None:
            try:
                self.cur.execute(string)
                return True, None
            except psycopg2.Error as err:
                self.con.rollback()
                return False, err
        else:
            try:
                self.cur.execute(string, arguments)
                return True, None
            except psycopg2.Error as err:
                self.con.rollback()
                return False, err 

    def table_gen(self):
        """(DB object) -> int, str

        This method will submite the correct SQL statements to the database.
        table_gen returns 1 if the tables waere successfully created, a 0 if
        the tables were not created because they already existed, or a -1 if 
        the tables were not created because of some eror."""
        if self.cur == None:
            return -1, "Database cursor hasn't been generated"
        elif self.con == None:
            return -1, "Database hasn't been connected to yet"
        else:
                cmd = self.execute("""SELECT * FROM logs;""")
                if cmd[0] == True:
                    return 0, None
                else:
                    with open('create.sql', 'r') as exe:
                        cmd = self.execute(exe.read())
                        if cmd[0] == False:
                            return -1, str(cmd[1])
                        else:
                            self.commit()
                            return 1, None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = GUI()
    sys.exit(app.exec_())
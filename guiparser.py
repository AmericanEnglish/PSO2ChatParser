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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    obj = GUI()
    sys.exit(app.exec_())
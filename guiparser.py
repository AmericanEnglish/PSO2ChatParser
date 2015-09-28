# Will be cleaner when finished, for not just use it all
from tkinter import *

# Mulit DB Support
import psycopg2
import sqlite3

class GUI:
    def __init__(self):
        self.root = Tk()
        self.master = root.frame()

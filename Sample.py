from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from os import listdir
from sys import argv
import psycopg2
import sqlite3
import re

try:
    print("Try: 1")
    conn = psycopg2.connect(host="localhost", database="pso2chat",
                            user=argv[1], password=argv[2])
    cur = conn.cursor()
    print("Try: 2")
except psycopg2.OperationalError as err:
    print("Except: 1")
    if "authentication failed" in str(err):
        print(err)
        exit()
    conn = psycopg2.connect(host="localhost", database="postgres", user=argv[1], password=argv[2])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE pso2chat;")
    cur.close()
    conn.close()
    conn = psycopg2.connect(host="localhost", database="pso2chat", user=argv[1], password=argv[2])
    cur = conn.cursor()
    print("Except: 2")

allfiles = listdir("./Chats/")
# allfiles.sort()
for item in allfiles[:1]:
    with open("./Chats/" + item, 'r', encoding='utf-16') as doc:
        for line in doc:
            line = re.split("\t", line)
            print(line)
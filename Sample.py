from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sys import argv
import psycopg2
import sqlite3

username = argv[1]
password = argv[2]

try:
    print("Try: 1")
    conn = psycopg2.connect(host="localhost", database="pso2chat",
                            user=username, password=password)
    cur = conn.cursor()
    print("Try: 2")
except psycopg2.OperationalError as err:
    print("Except: 1")
    if "authentication failed" in str(err):
        print(err)
        exit()
    conn = psycopg2.connect(host="localhost", database="postgres", user=username, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE pso2chat;")
    cur.close()
    conn.close()
    conn = psycopg2.connect(host="localhost", database="pso2chat", user=username, password=password)
    cur = conn.cursor()
    print("Except: 2")

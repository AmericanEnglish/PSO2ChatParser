from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from timestamp import timestamp
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
    with open('destroy.sql', 'r') as exe:
        cur.execute(exe.read())
    with open('create.sql', 'r') as exe:
        cur.execute(exe.read())
    conn.commit()
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
    with open('create.sql', 'r') as exe:
        cur.execute(exe.read())
    conn.commit()
    print("Except: 2")

allfiles = listdir("./Chats/")
# allfiles.sort()
print('Loop Begin')
for item in allfiles[:1]:
    with open("./Chats/" + item, 'r', encoding='utf-16') as doc:
        buff = []
        cur.execute("""INSERT INTO logs VALUES (%s);""", [item])
        for line in doc:
            line = re.split("\t", line)
            if len(line) > 6:
                line = line[:6]
                line.append('\t'.join(line[6:]))
            if timestamp(line[0]):
                temp = [item]
                temp.extend(line)
                line = temp
                cur.execute("""INSERT INTO chat VALUES
                    (%s, %s, %s, %s, %s, %s, %s)""", line)
                conn.commit()
                buff = [line[1], line[2], line[4]]
            else:
                print('Problem Line {}'.format(buff))
                cur.execute("""UPDATE chat
                    SET info = info || %s
                    WHERE stamp = %s AND
                        uid = %s AND
                        line_num = %s;""", 
                        [' '.join(line), buff[0], buff[1], buff[2]])
                conn.commit()

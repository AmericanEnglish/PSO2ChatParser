from sys import argv
import psycopg2
import sqlite3
def postgres():
    with psycopg2.connect(host='localhost', database='pso2chat', user=argv[2], password=argv[3]) as con:
        with con.cursor() as cur:
            if argv[1].isdigit():
                cur.execute("SELECT * FROM chat WHERE uid = %s;", [argv[1]])
                print("Total Entries: {}".format(len(cur.fetchall())))
            elif argv[1].isalnum():
                cur.execute("SELECT * FROM chat WHERE username = %s;", [argv[1]])
                print("Total Entries: {}".format(len(cur.fetchall())))

def sqlite():
    con = sqlite3.connect(database='PSO2Chat.db')
    cur = con.cursor()
    cur.execute("""SELECT * FROM chat WHERE uid = ?;""", [argv[2]])
    for item in cur.fetchall():
        print(item)

if __name__ == '__main__':
    if argv[1] == 'sqlite3':
        print(argv)
        sqlite()

    else:
        postgres()


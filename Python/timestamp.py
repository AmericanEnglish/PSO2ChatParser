#!/usr/bin/python
# URL that generated this code:
# http://txt2re.com/index-python.php3?s=2015-06-25T19:59:57&1
from sys import argv
import re
def timestamp(argument, main=False):
    txt=argument

    re1='((?:2|1)\\d{3}(?:-|\\/)(?:(?:0[1-9])|(?:1[0-2]))(?:-|\\/)(?:(?:0[1-9])|(?:[1-2][0-9])|(?:3[0-1]))(?:T|\\s)(?:(?:[0-1][0-9])|(?:2[0-3])):(?:[0-5][0-9]):(?:[0-5][0-9]))'    # Time Stamp 1

    rg = re.compile(re1,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    # print(m)
    if main:
        if m:
            timestamp1=m.group(1)
            print("("+timestamp1+")"+"\n")
    else:
        if m == None:
            return False
        else:
            return True
#-----
# Paste the code into a new python file. Then in Unix:'
# $ python x.py 
#-----

if __name__ == "__main__":
    timestamp(argv[1], True)
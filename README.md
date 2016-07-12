PSO2ChatParser
==============

Python
=============

Sample.py
 - Used as a workspace for testing the validity of SQL insertion. The main focus is on pumping chatlogs into a PostgreSQL server.

timestamp.py
 - Used for detecting PSO2 timestamps in logs that will indicate a valid newline that was generated by the game not by a user typing "LOL\nOLO". 

chatparser.py
 - An older version of the parser. This is a command line only interface. If you're on Windows you will need to use the .bat because CMD does not support UTF encodings, many japanese characters will still look like gibberish because it doesn't even properly supoort UTF16.
 - This program supports two things
  1. You can search: num, phrase  . Every detected user is assigned a number
  2. You can seperate chats. This will pull out general chat and make it generally more readable than sorting through the several types of chat.

guiparser.py
 - This as of now is a WIP and may be written in either PyQT5 or TK. Whichever BETTER supports UTF16 to prevent the abusive "str".decode.encode business

main.bat
 - Runs chatparser.py on windows.


Updates will start being pushed out in python now! As luck would have the pyinstaller people have managed to get a "passing" build for windows. So I will continue to push this through. Although my alterior reason is that C++ has very poor UTF16 support when it comes to cross compiling. Excluding the UTF8CPP package which would take more time than it is worth for me to learn it the in's and out's of.

Packages Used
=============
 1. psycopg2
  * For using PostgreSQL as an option 
 2. sqlite3
  * For using SQLite3


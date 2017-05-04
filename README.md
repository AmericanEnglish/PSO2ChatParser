PSO2ChatParser
==============

Python
=============

timestamp.py
 - Used for detecting PSO2 timestamps in logs that will indicate a valid newline that was generated by the game not by a user typing "LOL\nOLO". 

guiparser.py
 - This as of now is a WIP and may be written in either PyQT5 or TK. Whichever BETTER supports UTF16 to prevent the abusive "str".decode.encode business

database.py
 - Used to abstract database jargin. Currently support the use of PostgreSQL and SQLite3. I doubt I'll look into MySQL or other variants until someone complains about it.

AdditionalWidgets.py
 - It contains custom PyQt5 widgets. Basically every button causes it's own custom window to appear. Those windows are found in this file

Updates will start being pushed out in python now! As luck would have the pyinstaller people have managed to get a "passing" build for windows. So I will continue to push this through. Although my alterior reason is that C++ has very poor UTF16 support when it comes to cross compiling. Excluding the UTF8CPP package which would take more time than it is worth for me to learn it the in's and out's of. I've tried writing this program in several languages at this point. I'll catalog them at the bottom and why they didn't work.

I've also decided to take a very different approach to the problem. 
It would turn out that many of my test users complained about the speed of SQL transaction for the initial insertion. 
This I agree is very heavy for the first run because the program is inserting hundreds of thousands of lines of text and hashing every file.
This took a while for my laptop. Probably an hour.
This initial run time is a big drawback but it allows for the easy use of SQL to do the searching.
Some users reported and upwards insertion time of 5 seconds per line and no amount of optimization made this faster.
My guess is that using a slow HDD and a slow processor will substantially increase the time it takes for these transactions.
I've opted instead to just open every file using parallel maps. This shows great promise in performance with the scanning of 1000 files in about 600ms.
Until I can switch to a compiled language I feel this is good enough.

Goals
=====
1. SID       search
    * Pull down checkboxes
2. ~~PID       search~~ -> Chat logs are not accurate enough for this. Usernames and PlayerIDs are not distinguishable at this point
    * ~~Pull down checkboxes~~
3. Name      search
    * Pull down checkboxes
4. Keyword   search
    * Fill in blank
5. Day       ~~filter~~ search
    * Calendar Widget
    * Refines the days the program will search. Range or singular days
6. ~~Time      filter~~ -> This is actually purposeless
    * ~~Time slider 00:00:00 -> 23:59:59~~
7. Chat Type filter
    * Checkboxes
8. Search by logname
    * This would allow a user to pseudo-filter a log by filename if they wanted too
9. Query SEGA's player database in hopes of build a similar, more local, version of a player's character structure
    * SID: 123456789
    * PID: 123456 <- autofilled
    * Character Names <- autofilled
    * This should help expand the searches to be much more inclusive.

Packages Used
=============
1. MultiProcessing
  * For using parallel mapping
2. sqlite3
  * For using SQLite3 to handle user settings
3. PyQt5
  * The GUI packages

Current Progress
================
1. ~~Designing Windows~~
    * All rough drafts have been finished
2. ~~Remove all database integration for PostgreSQL~~
    * Finally. Everything is gone.
3. ~~Update windows to use new functional approach~~
    * Parallel Mapping has not been implemented. Either the program combs the files in parallel or sequentially. If you have more than a 100 parallel combing kicks in by starting up 8 processes. After some minor testing I determined that 8 processes is the cap for time scanning files and max cpu usage. Maybe this can be converted to a setting with a little slider.
4. ~~Design the ChatLogReader~~
    * The reader is still being improved but it in a minimal and fully working state.
5. Finish the "Log Selection" window where queried logs can be opened by the reader.
6. Mark a v0.80 that has little exception handiling but technically works.

Languages Attempted
===================
1. Clojure
    * Clojure, like Java, enjoys reading in utf16 files as BE even if there exists a BOM indicating LE. The work around for this in Clojure is absolutely ghastly and the GUI support for Clojure using JavaFX is just mind blowingly perplexing at first glance.
2. C/C++
    * C++11 added some basics for unicode support but I have major problems trying to figure out how anyone is supposed use any of it. I'll install the Visual C++ compiler tools at a later date and maybe I'll find solace in WChar support.
    * C -> WChar support is just poorly document. Many examples are using english text with always works quite well but there is little documentation on using Asian text like Hiragana. This might be solved if I were to switch to MS VS C++ and compile my C code with CL.exe as opposed to MinGW. I had this vain hope that I MinGW would "just work" and was sorely let down. If I get around to installing VS C++ stuff I'll try to rewrite this whole program using the Win32API for gui's and text processing.
3. GOlang
    * There is just so much wrong with Golang and this project. The fact that golang is a systems language and therefore doesn't have any standard gui. I could use one of the packages though if needed. Then there is the lack of unicode support unless I want to use Runes and Glyphs firsthand. Perhaps I'll fine a package that abstracts this away but until then. No go. Also there is the problem of finding a gui that also lets you USE these Unicode characters.
4. C#
    * C# actually worked beautifully. I, however, abhore using WPF and Visual Studio. Maybe if I care or have the time I'll look more into it. Maybe.

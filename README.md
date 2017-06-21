PSO2ChatParser
==============

I was inspired by frustration to create this project. 
Phantasy Star Online 2 dumps just an unnatural amount of logs for the game which can usually be found at USER/Documents/SEGA/PHANTASTYSTARONLINE2/log. 
These range from SymbolArtChatLogs to regular ChatLogs. 
This parser focuses on helping a user sift through these logs.
Some reasons
* Logs are .txt there isn't any nice highlighting you might expect 
like in game.
    * The parser changes this. Logs opened with the parser are colored in a 
fashion that is similar to the game.
* Using Window's built in search is inadequate and not field sensitive.
    * The parser offers the option to search fields like SEGA ID,
PID/Character Name, Date, Keywords, Possibly more.
* It could take windows a couple minutes to scrape all the files!
    * The parser uses all of your cores and takes 2-4 seconds to search every file.

Packages Used
=============
1. Qt - Full static
    * For the gui
2. Microsoft Visual C++ 2015 Standalone Tools
    * For compiling on the MS Windows platform
3. Jom
    * For compiling with all of your cores.
3. SQLite3
    * Allows the Parser to save defaults by the user. 
4. OpenMP
    * Simplified parallelifcation of code.

How To Download
===============

The easiest way to get the program is just to download the latest binaries
for 32bit or 64 bit Windows [here](https://github.com/AmericanEnglish/PSO2ChatParser/releases).
Hopefully these are updated often so please check back!

How To Compile
==============

If you want the program to be entirely static please read [this](https://dummy.link)
StackOverflow post about how to compile Qt5 to be FULLY static. 
If you don't follow this guide by adding the correct flags you'll still have
Qt dll dependancies even if the Window's Runtime is statically linked.

Get Jom from [here](https://wiki.qt.io/Jom).

Once you have every in place just follow these steps:
```
> qmake
> jom release
```

Done!

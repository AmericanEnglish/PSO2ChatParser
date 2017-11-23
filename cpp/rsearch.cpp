#include <iostream>
#include <ctime>
#include <QString>
#include <QStringList>
#include <QTextStream>
#include <QFile>
#include <QList>
#include <QDate>
#include <QMap>
#include <QDebug>
#include <QRegularExpression>
#include <rsearch.h>
// This will be like search.cpp except
// it will search using regular expressions
// and additionally it will also be designed to
// be done with QThread in conjuction with a 
// master thread reading it data as it worked
rSearch::rSearch(QStringList Dates, QMap<QString, QRegularExpression> Params, QString Base, QStringList Files, QStringList *Entries, bool *Complete) {
    // Fill internal variables
    dates = Dates;
    params = Params;
    base = Base;
    files = Files;
    entries = Entries;
    complete = Complete;
    // Call run method
    // Function should take,
    // 1. List of regex terms
    // 2. Filenames
    // 3. Dates
    // 4. Pointers to two heap allocated arrays
    //      a. QStringList array but make sure it's null
    //      b. an integer array which can be incremented when a thread "finishes"
}

void rSearch::run() {
    int len = files.length();
    // Run
    qDebug() << "=rSearch: Beginning...";
    // #pragma omp parallel for
    for (int i = 0; i < len; i++) {
        entries[i] = searchFile(i);
        // Thread Saftey at its finest
        complete[i] = true;
    }
    // #pragma omp barrier
    qDebug() << "=rSearch: Finished!";
    // Finished
    emit finished();
}

// Dates have to be done with QStringList
bool rSearch::dateCheck(QString date) {
    // std::cout << "Place 7 paramlen=" << parameters.length() << std::endl;
    if (!dates.at(0).isEmpty()) {
        if (!dates.at(1).isEmpty()) {
            return (dates.at(0) <= date) && (date <= dates.at(1));
        }
        return dates.at(0) <= date;
    }
    else if (!dates.at(1).isEmpty()) {
        return date <= dates.at(1);
    }
    return true;
}


// SID is only numbers therefore not able to be case sensitive
// Takes a regular expression
bool rSearch::sidCheck(QString num) {
    return params["sid"].match(num).hasMatch();
}

bool rSearch::pidCheck(QString name) {
    return params["pid"].match(name).hasMatch();
}

bool rSearch::chatCheck(QString term) {
    return params["chat"].match(term).hasMatch();
}

// PID and Keyword check is the same. However they might be expanded differntly in the future
bool rSearch::keywordCheck(QString message) {
    return params["word"].match(message).hasMatch();
}

// Corrects a tabbing issue that may occur
QStringList rSearch::too_many_tabs(QStringList line){
    QStringList fodder;
    int i = 0;
    while (fodder.length() < 5) {
        fodder.append(line.at(i));
        line.removeFirst();
        i++;
    }
    fodder.append(line.join("\t"));
    return fodder;
}

// Rebuilds the line recursively
QStringList rSearch::buildLine(QStringList file, QString str, int start) {
    QStringList line = file.at(start).split("\t");
    // std::cout << "buildLine line len=" << line.length() << std::endl;
    if (line.length() == 6) {
        QString temp = line.at(5) + "\n" + str;
        line.removeLast();
        line.append(temp);
        return line;
    }
    else {
        return buildLine(file, file.at(start) + "\n" + str, start - 1);
    }
}

// Main Functions
bool rSearch::full_check(QStringList line) {
    // std::cout << "Place 6 linelen=" << line.length() << std::endl;
    bool res1 = dateCheck(line.at(0));// &&
    // std::cout << "Place 12" << std::endl;
    bool res2 = sidCheck(line.at(3)); // &&
    // std::cout << "Place 13" << std::endl;
    bool res3 = pidCheck(line.at(4)); // && 
    // std::cout << "Place 14" << std::endl;
    bool res4 = chatCheck(line.at(2));// &&
    // std::cout << "Place 15" << std::endl;
    bool res5 = keywordCheck(line.at(5));
    // std::cout << "Place 16" << std::endl;
    return res1 && res2 && res3 && res4 && res5;
}

// QStringList searchfile(QMap<QString, QStringList> parameters, QString filename) {
QStringList rSearch::searchFile(int i) {
    QString filename = base + files[i];
    QFile file(filename);
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream input(&file);
    input.setCodec("UTF-16LE");
    // Split file on newlines
    QStringList contents = input.readAll().split("\n");
    // QString contents = input.readAll();
    // Not closing the file causes a crash
    file.close();
    // ^ this most likely has to do with a bad FP on the stack?
    // Begin the rest of the work VVVV
    /*
     * The leading entry in all data will be the suspect lines and the 
     * remaining will be the file contents. This allows for faster quicker and 
     * smoother Reader interactions.
     */
    QList<QStringList> allData;
    int count = 0;
    QStringList keepLine, line, results;
    QString message;
    int len;
    // std::cout << "Place 1, len=" << contents.length() << std::endl;
    while (count < contents.length()) {
        line = contents.at(count).split("\t");
        len = line.length();
        // std::cout << "Line len=" << line.length() << std::endl;
        // Possibly empty
        if (line.isEmpty()) {
            continue;
        }
        // Too many tabs
        if (len > 6) {
            // std::cout << "Place 2" << std::endl;
            line = too_many_tabs(line);
        }

        // Victim of a bad newline
        if (len < 6) {
            // std::cout << "Place 3" << std::endl;
            line = buildLine(contents, line.join("\t"), count - 1);
            // std::cout << "Line len=" << line.length() << std::endl;
        }

        if (full_check(line)) {
            // std::cout << "Place 4" << std::endl;
            message = line.at(4) + ": " + line.at(5);
            results.append(message);
            // Append the line to data
        }
        count++;

    }
    if (results.isEmpty()) {
        return QStringList();
    }
    
    return results;
}


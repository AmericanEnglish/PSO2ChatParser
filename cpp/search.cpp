#include <iostream>
#include <ctime>
#include <omp.h>
// #include <string>
#include <QtCore>

/*************************************************************************
 * Search is the heart and soul of the program. The main prupose of      *
 * search is to take in the user's queries and to return the filenames   *
 * that match the users wants. search is built with several helper       *
 * functions and is designed such that it can be run in parallel maps.   *
 *************************************************************************/
// Helper Functions

bool date_check(QStringList parameters, QString item) {
    // std::cout << "Place 7 paramlen=" << parameters.length() << std::endl;
    if (!parameters.at(0).isEmpty()) {
        if (!parameters.at(1).isEmpty()) {
            return (parameters.at(0) <= item) && (item <= parameters.at(1));
        }
        return parameters.at(0) <= item;
    }
    else if (!parameters.at(1).isEmpty()) {
        return item <= parameters.at(1);
    }
    return true;
}

// SID is only numbers therefore not able to be case sensitive
bool sid_check(QStringList parameters, QString num) {
    // std::cout << "Place 8" << std::endl;
    int len = parameters.length();
    // Relative, Sensitive, Terms
    if (len > 1) {
        // If relative
        if (parameters.at(0) == "relative") {
            // Loop
            for (int i = 2; i < len; i++) {
                if (parameters.at(i).contains(num)) {
                    return true;
                }
            }
        }
        else {
            // Absolute term matching
            for (int i = 2; i < len; i++) {
                if (parameters.at(i) == num) {
                    return true;
                }
            }
        }
        return false;

    }
    return true;
}

bool pid_check(QStringList parameters, QString name) {
    int len = parameters.length();
    // std::cout << "Place 9 paramslen=" << len << std::endl;
    // Relative, Sensitive, Terms
    if (len > 2) {
        // If relative
        if (parameters.at(0) == "relative") {
            // Loop
            for (int i = 2; i < len; i++) {
                // Casing
                if (parameters.at(1) == "sensitive") {
                    if (parameters.at(i).contains(name)) {
                        return true;
                    }
                }
                else {
                    if (parameters.at(i).toLower().contains(name.toLower())) {
                        return true;
                    }
                }
            }
        }
        else {
            // Absolute term matching
            for (int i = 2; i < len; i++) {
                // Casing
                if (parameters.at(1) == "sensitive") {
                    if (parameters.at(i) == name) {
                        return true;
                    }
                }
                else {
                    if (parameters.at(i).toLower() == name.toLower()) {
                        return true;
                    }
                }
            }
        }
        return false;

    }
    return true;

}

bool chat_check(QStringList parameters, QString term) {
    // std::cout << "Place 10" << std::endl;
    int len = parameters.length();
    if (len != 0) {
        for (int i = 0; i < len; i++) {
            if (parameters.at(i) == term) {
                return true;
            }
        }
        return false;
    }
    return true;
}

// PID and Keyword check is the same. However they might be expanded differntly in the future
bool keyword_check(QStringList parameters, QString message) {
    // std::cout << "Place 11" << std::endl;
    int len = parameters.length();
    // Relative, Sensitive, Terms
    if (len > 2) {
        // If relative
        if (parameters.at(0) == "relative") {
            // Loop
            for (int i = 2; i < len; i++) {
                // Casing
                if (parameters.at(1) == "sensitive") {
                    if (parameters.at(i).contains(message)) {
                        return true;
                    }
                }
                else {
                    if (parameters.at(i).toLower().contains(message.toLower())) {
                        return true;
                    }
                }
            }
        }
        else {
            // Absolute term matching -> change this to regular expressions to account for punctuation
            for (int i = 2; i < len; i++) {
                // Casing
                if (parameters.at(1) == "sensitive") {
                    if (parameters.at(i) == message) {
                        return true;
                    }
                }
                else {
                    if (parameters.at(i).toLower() == message.toLower()) {
                        return true;
                    }
                }
            }
        }
        return false;

    }
    return true;

}

bool full_check(QMap<QString, QStringList> parameters, QStringList line) {
    // std::cout << "Place 6 linelen=" << line.length() << std::endl;
    bool res1 = date_check(parameters["dates"], line.at(0));// &&
    // std::cout << "Place 12" << std::endl;
    bool res2 = sid_check(parameters["sid"], line.at(3)); // &&
    // std::cout << "Place 13" << std::endl;
    bool res3 = pid_check(parameters["pid"], line.at(4)); // && 
    // std::cout << "Place 14" << std::endl;
    bool res4 = chat_check(parameters["chat"], line.at(2));// &&
    // std::cout << "Place 15" << std::endl;
    bool res5 = keyword_check(parameters["keyword"], line.at(5));
    // std::cout << "Place 16" << std::endl;
    return res1 && res2 && res3 && res4 && res5;
}

// Corrects a tabbing issue that may occur
QStringList too_many_tabs(QStringList line){
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
QStringList buildLine(QStringList file, QString str, int start) {
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

QStringList searchfile(QMap<QString, QStringList> parameters, QString filename) {
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
    int count = 0;
    QStringList line, results;
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

        if (full_check(parameters, line)) {
            // std::cout << "Place 4" << std::endl;
            message = line.at(4) + ": " + line.at(5);
            results.append(message);
        }
        count++;

    }
    
    return results;
}

QStringList *loopSearch(QMap<QString, QStringList> parameters, QString base, QStringList allFiles) {
// QList<QStringList> loopSearch(QString base, QStringList allFiles) {
    int len = allFiles.length();
    // For returning a QList
    // QStringList temp[len];
    // For returning an array of QStringLists
    QStringList *temp = new QStringList[len];
    std::cout << "Using " << omp_get_max_threads() << " threads" << std::endl;
    #pragma omp parallel for
    for (int i = 0; i < allFiles.length(); i++) {
        QString name = allFiles.at(i);
        // qDebug() << name;
        temp[i] = searchfile(parameters, base + name);
    }
    #pragma omp barrier

    // Convert array to QList
    // QList results = QList();
    // for (int i = 0; i < len; i++) {
        // results.push_back(temp[i])
    // }
    return temp;
    
}


// int main() {
//     // Open an input text stream
//     QString dirname = ;
//     QDir directory =  QDir(dirname);
//     QStringList allFiles = directory.entryList();
//     allFiles.removeOne(".");
//     allFiles.removeOne("..");
//     // Parameters will be an array of strings
//     QStringList dates;
//     dates.append(QString()); // Begin
//     dates.append(QString()); // End
//     QStringList sid;
//     sid << "relative";
//     // sid["use"] = "False"
//     // sid["relative"] = "False";
//     // sid["sensitive"] = "False";
//     // sid["terms"] = QString(); // Needs to be split
//     QStringList pid;
//     pid << "relative"; // Relative
//     pid << "sensitive"; // Sensitive
//     pid << "AmericanEnglish"; // 2 -> End are terms
//     QStringList chatType;
//     // chatType << "Public"; // Only append the terms to be checked
//     // chatType << "PARTY";
//     // chatType << "GUILD";
//     chatType << "REPLY";
//     QStringList keywords;
//     keywords << "relative";
//     keywords << "sensitive" ; // Casing
//     // keywords << "terms"; // Append terms to be searched
// 
//     QMap<QString, QStringList> parameters;
//     parameters["dates"] = dates;
//     parameters["sid"] = sid;
//     parameters["pid"] = pid;
//     parameters["chat"] = chatType;
//     parameters["keywords"] = keywords;
// 
//     std::cout << "Begin (SEQ) - Using " << allFiles.length() << " files" << std::endl;
//     QString name;
//     int lenFiles = allFiles.length();
//     clock_t start = clock();
//     for (int i = 0; i < lenFiles; i++) {
//         name = allFiles.at(i);
//         searchfile(parameters, dirname + name);
//     }
//     clock_t stop = clock();
//     std::cout << "Execution Time: " << double(stop - start) / CLOCKS_PER_SEC  << "s" << std::endl;
//     // scanfile(filename);
//     std::cout << "Begin (PAR) - Using " << allFiles.length() << " files" << std::endl;
//     start = clock();
//     QStringList *results = loopSearch(parameters, dirname, allFiles);
//     stop = clock();
//     // for (int i = 0; i < lenFiles; i++) {
//         // qDebug() << results[i];
//     // }
//     // for (int i = 0; i < lenFiles; i++) {
//         // if (success[i] == 0) {
//             // qDebug() << allFiles.at(i);
//         // }
//     // }
//     std::cout << "Execution Time: " << double(stop - start) / CLOCKS_PER_SEC << "s" << std::endl;
// }

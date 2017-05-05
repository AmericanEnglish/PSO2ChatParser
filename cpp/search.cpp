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

bool date_check() {

}

bool sid_check() {

}

bool pid_check() {

}

bool chat_check() {

}

bool keyword_check() {

}

bool full_check() {

}

// Corrects a tabbing issue that may occur
QStringList too_many_tabs(QStringList line){
    QStringList fodder;
    int i = 0;
    while (fodder.length() < 5) {
        fodder.append(list.at(i));
        list.removeFirst();
        i++;
    }
    fodder.append(list.join("\t"));
    return fodder;
}

// Rebuilds the line recursively
QString buildLine(QStringList file, QString str, int start) {
    QStringList line = file.at(start).split("\t");
    if (line.length() == 6) {
        QString temp = line.at(5) + "\n" + str;
        line.removeLast();
        line.append(temp);
        return line;
    }
    else {
        return buildLine(file, file.at(i) + "\n" + str, start - 1);
    }
}

// Main Functions

QStringList searchfile(QString filename) {
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
    while (count < contents.length()) {
        count++;
        line = QStringList.at(count).split("\t");
        len = line.length();
        // Possibly empty
        if (line.isEmpty()) {
            continue;
        }
        // Too many tabs
        if (len > 6) {
            line = too_many_tabs(line);
        }

        // Victim of a bad newline
        if (len < 6) {
            line = buildLine(contents, line.join("\t"), count - 1);
        }

        if (full_check(parameters, line)) {
            message = line.at(4) + ": " + line.at(5);
            results.append(message);
        }

    }
    
    return messages;
}

QStringList *loopSearch(QString base, QStringList allFiles) {
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
        temp[i] = searchfile(base + name);
    }
    #pragma omp barrier

    // Convert array to QList
    // QList results = QList();
    // for (int i = 0; i < len; i++) {
        // results.push_back(temp[i])
    // }
    return temp;
    
}


int main() {
    // Open an input text stream
    QString dirname = "C:\\Users\\12bar\\Documents\\code\\pso2parser\\logs\\";
    QDir directory =  QDir(dirname);
    QStringList allFiles = directory.entryList();
    allFiles.removeOne(".");
    allFiles.removeOne("..");
    std::cout << "Begin (SEQ) - Using " << allFiles.length() << " files" << std::endl;
    QString one = ".";
    QString two = "..";
    QString name;
    int lenFiles = allFiles.length();
    clock_t start = clock();
    for (int i = 0; i < lenFiles; i++) {
        name = allFiles.at(i);
        if (name != one && name != two) {
            searchfile(dirname + name);
        }
    }
    clock_t stop = clock();
    std::cout << "Execution Time: " << double(stop - start) / CLOCKS_PER_SEC  << "s" << std::endl;
    // scanfile(filename);
    std::cout << "Begin (PAR) - Using " << allFiles.length() << " files" << std::endl;
    start = clock();
    QStringList *results = loopSearch(dirname, allFiles);
    stop = clock();
    // for (int i = 0; i < lenFiles; i++) {
        // qDebug() << results[i];
    // }
    // for (int i = 0; i < lenFiles; i++) {
        // if (success[i] == 0) {
            // qDebug() << allFiles.at(i);
        // }
    // }
    std::cout << "Execution Time: " << double(stop - start) / CLOCKS_PER_SEC << "s" << std::endl;
}

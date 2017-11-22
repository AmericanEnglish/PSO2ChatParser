#include <reader.h>
// #include <search.h>
#include <QAbstractTableModel>
#include <QBrush>
#include <QColor>
#include <QDate>
#include <QDebug>
#include <QFile>
#include <QList>
#include <QMap>
#include <QModelIndex>
#include <QObject>
#include <QHBoxLayout>
#include <QStringList>
#include <QVariant>
#include <QVBoxLayout>
#include <QWidget>
#include <QHeaderView>
#include "search.h"
#include "rsearch.h"

Reader::Reader(QString basepath, QMap<QDate, QStringList> allData, QWidget *parent) : QWidget(parent) {
    qDebug() << "Reader has been spawned!";
    allData = allData;
    // Build the GUI
    initGui();
    // Build Data
    qDebug() << "Setting up initial data...";
    refresh(basepath, allData);
}

// Dynamic Reader!
Reader::Reader(QString basepath, QStringList Files, QStringList Dates, QMap<QString, QRegularExpression> Params, QWidget *parent) : QWidget(parent) {
    initGui();
    int len = Files.length();
    // Build additional objects on the heap
    entries = new QStringList[len];
    complete = new bool[len];
    // Build the search object
    searchObj = new rSearch(Dates, Params, basepath, Files, entries, complete);
    // Move the thing to a QThread
    searchThd = new QThread;
    // Move object to thread
    searchObj->moveToThread(searchThd);
    // Connect all of it!
    connect(searchObj, SIGNAL(error(QString)), this, SLOT(errorString(QString)));
    connect(searchThd, SIGNAL(started()), searchObj, SLOT(run()));
    connect(searchObj, SIGNAL(finished()), searchThd, SLOT(quit()));
    connect(searchObj, SIGNAL(finished()), searchObj, SLOT(deleteLater()));
    connect(searchThd, SIGNAL(finished()), searchThd, SLOT(deleteLater()));
    // Start the threads!
    searchThd->start();

    // Establish a timer to poll every second
    // Use it to poll the QThread
    // QThread finished should shutdown the timer as well
    
    // Will need to write a new refresh method
}

void Reader::initGui() {
    setWindowTitle("PSO2 Chat Reader");
    resize(900, 500);
    // Build Table
    table = new QTableView(this);
    table->setSortingEnabled(false);
    // (table->verticalHeader)()->setVisible(false);
    QHeaderView *vv = table->verticalHeader();
    vv->setVisible(false);
    connect(
        table->horizontalHeader(),
        SIGNAL(sectionResized(int, int, int)),
        table,
        SLOT(resizeRowsToContents()));

    // Build Tree
    tree = new QTreeView(this);
    tree->setFixedWidth(300);
    tree->header()->hide();
    treeModel = new QStandardItemModel(this);

    connect(tree, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(updateContent(QModelIndex)));
    
    headers = QStringList({"Time", "PID/SID", "Message"});
    
    logTitle = new QLabel("", this);


    // Setup
    QVBoxLayout *vbox = new QVBoxLayout(this);
    vbox->addWidget(logTitle);
    vbox->addWidget(table);
    QWidget *vboxWidget = new QWidget(this);
    vboxWidget->setLayout(vbox);
    QHBoxLayout *hbox = new QHBoxLayout(this);
    hbox->addWidget(tree);
    hbox->addWidget(vboxWidget);

    setLayout(hbox);
}

void Reader::generateTree(QMap<QDate, QStringList> allData, QStandardItem *parent) {
    QList<QDate> keys = allData.keys();
    qSort(keys.begin(), keys.end());
    int len = keys.length();
    int lines;
    QStandardItem *topItem;
    QStandardItem *subItem;
    QStringList suspectLines;
    QDate key;
    for (int i = 0; i < len; i++) {
        key = keys.at(i);
        topItem = new QStandardItem(key.toString("MMM dd, yyyy"));
        topItem->setEditable(false);
        parent->appendRow(topItem);
        suspectLines = allData[key];
        lines = suspectLines.length();
        for (int j = 0; j < lines; j++) {
            subItem = new QStandardItem(suspectLines.at(j));
            subItem->setEditable(false);
            topItem->appendRow(subItem);
        }

    }

}

void Reader::newTree(QMap<QDate, QStringList> allData) {
    // Easier to just clear and rebuild the tree
    treeModel->clear();
    generateTree(allData, treeModel->invisibleRootItem());
    tree->setModel(treeModel);

}

void Reader::updateContent(QModelIndex index) {
    while (index.parent().isValid()) {
        index = index.parent();
    }
    QVariant data = tree->model()->data(index);
    QDate newDate = QDate::fromString(data.toString(), "MMM dd, yyyy");
    //qDebug() << "QVariant:" << data.toString() << "\n\tQDate:" << newDate;
    QList<QDate> keys = alltables.keys();
    if (!keys.contains(newDate)) {
        // Reuse
        QList<QStringList> sheet = digestFile(this->base + newDate.toString("ChatLogyyyyMMdd_00.txt"));
        alltables[newDate] = new ChatTable(headers, sheet, this);
    }
    logTitle->setText(newDate.toString("MMM dd, yyyy"));
    table->setModel(alltables[newDate]);
    table->resizeColumnToContents(0);
    table->resizeColumnToContents(1);
    table->resizeRowsToContents();
    QHeaderView *hh = table->horizontalHeader();
    hh->setStretchLastSection(true);
    table->setWordWrap(true);
}

void Reader::refresh(QString basepath, QMap<QDate, QStringList> allData) {
    qDebug() << "Reader here! Keys:" << allData.keys();
    // Reset the table map
    //alltables = QMap<QDate, ChatTable*>();
    qDeleteAll(alltables);
    alltables.clear();
    // Get Keys
    base = basepath;
    QList<QDate> keys = allData.keys();
    qSort(keys.begin(), keys.end());



    // Refresh Tree
    newTree(allData);
    QDate first = keys.at(0);
    // First log of the bunch
    qDebug() << "Begin digestion of:" << first;
    QList<QStringList> sheet = digestFile(base + first.toString("ChatLogyyyyMMdd_00.txt"));
    // Refresh Table
    logTitle->setText(first.toString("MMM dd,  yyyy"));
    // Store the tables in a map
    alltables[first] = new ChatTable(headers, sheet, this);
    
    table->setModel(alltables[first]);
    table->resizeColumnToContents(0);
    table->resizeColumnToContents(1);
    table->resizeRowsToContents();
    QHeaderView *hh = table->horizontalHeader();
    hh->setStretchLastSection(true);
    table->setWordWrap(true);
    //table->show();
    //table->update();
    show();

}
QList<QStringList> Reader::digestFile(QString filename) {
    /* When given a filename, it produces a special watered down
     * version of the chat to be taken in by the chat table. 
     * This version of the log contain minimal amounts of data
     * so most of the data can be left off or elegantly hidden.
     */
    QList<QStringList> allData;
    QFile file(filename);
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream input(&file);
    QStringList contents = input.readAll().split("\n");
    file.close();
    int count = 0;
    QStringList keepLine, line, results;
    QString message;
    int len;
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

        len = line.length();
        if (len == 6) {
            QStringList usable;
            // Time
            usable << line.at(0).split("T").at(0);
            // IDs
            usable << line.at(4) + QString("\n") + line.at(3);
            // Message
            usable << line.at(5);
            // Chat Type
            usable << line.at(2);
            // Add this modified line
            allData << usable;
        }
        count++;
    }
    qDebug() << filename << "has been digested!";
    qDebug() << "Length:" << allData.length();
    return allData;
}

// For the chats!
ChatTable::ChatTable(QStringList headers, QList<QStringList> logdata, QObject *parent) : QAbstractTableModel(parent) {
    /* logData contains extra leading data 
     * the first line are suspectLines
     * the first column of normal data is the chat type.
     */
    log = logdata;
    headerdata = headers;
}

int ChatTable::rowCount(const QModelIndex &parent) const {
    Q_UNUSED(parent);
    if (!log.isEmpty()) {
        return log.length();
    }
    return 0;
}
int ChatTable::columnCount(const QModelIndex &parent) const {
    Q_UNUSED(parent);
    if (!log.isEmpty() && !log.at(0).isEmpty()) {
        return log.at(0).length() - 1;
    }
    return 0;

}

QVariant ChatTable::data(const QModelIndex &index, int role) const {
    if (!index.isValid()) {
        return QVariant();
    }
    else if (role == Qt::BackgroundRole) {
        // Colors!
        QStringList chat_info = log.at(index.row());
        QString chat = chat_info.at(chat_info.length() - 1);
        if (chat == "PUBLIC") {
            return QBrush(Qt::lightGray);
        }
        else if (chat == "PARTY") {
            return QBrush(Qt::cyan);
        }
        else if (chat == "GUILD") {
            // Gold
            return QBrush(QColor(230, 157, 36));
        }
        else if (chat == "REPLY") {
            return QBrush(Qt::magenta);
        }
    }
    else if (role != Qt::DisplayRole) {
        return QVariant();
    }
    return log.at(index.row()).at(index.column());
}

QVariant ChatTable::headerData(int section, Qt::Orientation orientation, int role) const {
    if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
        return QVariant(headerdata.at(section));
    }
    return QVariant();
}

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
#include <QTimer>
#include <QApplication>
#include <QClipboard>
#include <QAbstractItemView>
#include "search.h"
#include "rsearch.h"

Reader::Reader(QString basepath, QMap<QDate, QStringList> allData, QWidget *parent) : QWidget(parent) {
    qDebug() << "Reader has been spawned!";
    allData = allData;
    // Build the GUI
    initGui();
    // Build Data
    qDebug() << "Setting up initial data...";
    // refresh(basepath, allData);
}

// Dynamic Reader!
Reader::Reader(QString basepath, QStringList Files, QStringList Dates, QMap<QString, QRegularExpression> Params, QWidget *parent) : QWidget(parent) {
    qDebug() << "New reader has been spawned!";
    initGui();
    newSearch(basepath, Files, Dates, Params);
}

void Reader::newSearch(QString basepath, QStringList Files, QStringList Dates, QMap<QString, QRegularExpression> Params) {
    base = basepath;
    int len = Files.length();
    files = Files;
    qDebug() << "+Reader: Building additional objects on the heap...";
    entries = new QStringList[len];
    complete = new bool[len];
    qDebug() << "+Reader: Building the search object...";
    searchObj = new rSearch(Dates, Params, basepath, Files, entries, complete);
    stopped = new bool;
    *stopped = false;
    searchObj->setStop(stopped);
    qDebug() << "+Reader: Moving searchObj to a QThread...";
    searchThd = new QThread;
    // Move object to thread
    searchObj->moveToThread(searchThd);
    // Connect all of it!
    qDebug() << "+Reader: Connecting the slots and signals...";
    connect(searchObj, SIGNAL(error(QString)), this, SLOT(errorString(QString)));
    connect(searchThd, SIGNAL(started()), searchObj, SLOT(run()));
    connect(searchObj, SIGNAL(finished()), searchThd, SLOT(quit()));
    connect(searchObj, SIGNAL(finished()), searchObj, SLOT(deleteLater()));
    connect(searchThd, SIGNAL(finished()), searchThd, SLOT(deleteLater()));
    // Start the threads!
    qDebug() << "+Reader: Start the threads!";
    searchThd->start();

    // Establish a timer to poll every second
    qDebug() << "+Reader: Establishing the polling system...";
    poll = new QTimer(this);
    // Use it to poll the QThread
    connect(poll, SIGNAL(timeout()), this, SLOT(tRefresh()));
    poll->start(100); // ms
    qDebug() << "+Reader: Established!";

    // The signal should start the updating
}


void Reader::initGui() {
    setWindowTitle("PSO2 Chat Reader");
    resize(900, 500);
    // Build Table
    // table = new QTableView(this);
    table = new SimpleTableView(this);
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

void Reader::generateTree() {
    QStandardItem *parent = treeModel->invisibleRootItem();
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

void Reader::appendToTree(QDate newDate) {
    QStandardItem *parent = treeModel->invisibleRootItem();
    QStandardItem *topItem = new QStandardItem(newDate.toString("MMM dd, yyyy"));
    topItem->setEditable(false);
    parent->appendRow(topItem);
    QStringList suspectLines = allData[newDate];
    int lines = suspectLines.length();
    QStandardItem *subItem;
    for (int j = 0; j < lines; j++) {
        subItem = new QStandardItem(suspectLines.at(j));
        subItem->setEditable(false);
        topItem->appendRow(subItem);
    }
}

void Reader::newTree() {
    // Easier to just clear and rebuild the tree
    treeModel->clear();
    generateTree();
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

void Reader::stopExecution() {
    // Stops QThread if it's still running
    if (searchThd->isRunning()) {
        *stopped = true;
    }
}

void Reader::clear() {
    stopExecution();
    if (poll->isActive()) {
        poll->stop();
    }
    tickCount = 0;
    totalComplete = 0;
    qDeleteAll(alltables);
    alltables.clear();
    treeModel->clear();
    allData.clear();
    stopped = new bool;
    *stopped = false;
}

void Reader::tRefresh() {
    tickCount++;
    qDebug() << "+Reader: Tick! Time to refresh!" << tickCount;

    // Check how many have been complete thus far
    int currentComplete = 0;
    int len = files.length();
    for (int i = 0; i < len; i++) {
        if (complete[i]) {
            currentComplete++;
        }
    }
    
    if ((currentComplete > totalComplete) || (currentComplete == files.length())) {
        // Searching has finished!
        if (totalComplete == 0) {
            tree->setModel(treeModel);
        }
        // This should stop the tree from being rebuilt if everything is done
        if (currentComplete == files.length()) {
            poll->stop();
            // delete searchObj;
            // delete searchThd;
        }

        // Add new values to the map
        QDate newDate;
        // for (int i = totalComplete; i < len; i++) {
        for (int i = 0; i < len; i++) {
            if (complete[i]) { // Add complete entries only
                if (!entries[i].isEmpty()) { // Add only entries which matter
                    newDate =  QDate::fromString(files.at(i), "ChatLogyyyyMMdd_00.txt");
                    if (!allData.contains(newDate)) { // Add new data only
                        // qDebug() << "+Reader: Match!" << newDate;
                        allData[newDate] = entries[i];
                        appendToTree(newDate);
                    }
                }
            }
        }
        totalComplete = currentComplete;
        // Eventually add a progress bar, then update that here
        // Rebuild tree
        // newTree();
    }
    // Else means no additonal files have been completed
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
            usable << line.at(0).split("T").at(1);
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

void Reader::errorString(QString err) {
    qDebug() << err;
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

SimpleTableView::SimpleTableView(QWidget *parent) : QTableView(parent) {
    setSelectionBehavior(QAbstractItemView::SelectRows);
}

void SimpleTableView::keyPressEvent(QKeyEvent *event) {
    // If Ctrl-C typed
    // Or use event->matches(QKeySequence::Copy)
    if (event->key() == Qt::Key_C && (event->modifiers() & Qt::ControlModifier))
    {
        QModelIndexList cells = this->selectionModel()->selectedIndexes();
        qDebug() << "+Reader: Copy count" << cells.count();
        qSort(cells); // Necessary, otherwise they are in column order
        QString toClip;
        // QModelIndex cell;
        for (int i = 0; i < cells.count() / 3; i++) {
            // qDebug() << cells.at(i).row() << cells.at(i).column();
            // First column
            toClip += "[" + cells.at(3*i + 0).data().toString() + "] ";
            // Second column
            toClip += cells.at(3*i + 1).data().toString().split(QRegExp("\\s+")).at(0) +  ": ";
            // Third column
            toClip += cells.at(3*i+2).data().toString() + "\n";
        }
        // QString text;
        // int currentRow = 0; // To determine when to insert newlines
        // foreach (const QModelIndex& cell, cells) {
            // if (text.length() == 0) {
                // // First item
            // } else if (cell.row() != currentRow) {
                // // New row
                // text += '\n';
            // } else {
                // // Next cell
                // text += '\t';
            // }
            // currentRow = cell.row();
            // text += cell.data().toString();
        // }
//
        qDebug() << toClip;
        QApplication::clipboard()->setText(toClip);
    }
}

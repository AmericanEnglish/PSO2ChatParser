#include <reader.h>
// #include <search.h>
#include <QAbstractTableModel>
#include <QBrush>
#include <QColor>
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

Reader::Reader(QStringList allFiles, QStringList allData, QWidget *parent) : QWidget(parent) {
    setWindowTitle("PSO2 Chat Reader");
    resize(900, 500);
    allData = allData;
    // Build Table
    table = new QTableView(this);
    table->setWordWrap(true);
    table->setSortingEnabled(false);
    // (table->verticalHeader)()->setVisible(false);
    QHeaderView *vv = table->verticalHeader();
    vv->setVisible(false);

    // Build Tree
    tree = new QTreeView(this);
    tree->setFixedWidth(300);
    treeModel = new QStandardItemModel(this);
    // tree->setModel(treeModel);
    connect(tree, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(updateContent(QModelIndex)));
    
    headers = QStringList({"Time", "PID/SID", "Message"});
    
    refresh(allData);

    // Setup
    QVBoxLayout *vbox = new QVBoxLayout(this);
    logTitle = new QLabel("", this);
    vbox->addWidget(logTitle);
    vbox->addWidget(table);
    QWidget *vboxWidget = new QWidget(this);
    vboxWidget->setLayout(vbox);
    QHBoxLayout *hbox = new QHBoxLayout(this);
    hbox->addWidget(tree);
    hbox->addWidget(vboxWidget);

    setLayout(hbox);

    // Build Data

}

void Reader::generateTree(QMap<QString, QList<QStringList>> allData, QStandardItem *parent) {
    QStringList keys = allData.keys();
    keys.sort();
    int len = keys.length();
    int lines;
    QStandardItem *topItem;
    QStandardItem *subItem;
    QStringList suspectLines;
    QString key;
    for (int i = 0; i < len; i++) {
        key = keys.at(i);
        topItem = new QStandardItem(key);
        topItem->setEditable(false);
        parent->appendRow(topItem);
        // Leading element are the suspect lines
        suspectLines = allData[key].at(0);
        lines = suspectLines.length();
        for (int j = 0; j < lines; j++) {
            subItem = new QStandardItem(suspectLines.at(j));
            subItem->setEditable(false);
            topItem->appendRow(subItem);
        }

    }

}

void Reader::newTree(QMap<QString, QList<QStringList>> allData) {
    // Easier to just clear and rebuild the tree
    treeModel->clear();
    generateTree(allData, treeModel->invisibleRootItem());
    tree->setModel(treeModel);

}

void Reader::updateContent(QModelIndex index) {

}

void Reader::refresh(QMap<QString, QList<QStringList>> allData) {
    /* Currently the structure is
     * filename 1
     * => QStringList(Suspect File Lines)
     * => FILE LINE 1
     * => FILE LINE 2
     * => ...
     * filename 2
     */
    // Get Keys
    QStringList keys = allData.keys();
    keys.sort();



    // Refresh Tree
    newTree(allData);
    QList<QStringList> sheet = allData[keys.at(0)];
    // Refresh Table
    logTitle->setText(keys.at(0));
    ChatTable *temp = new ChatTable(headers, sheet, this);
    table->setModel(temp);
    table->update();

}

// For the chats!
ChatTable::ChatTable(QStringList headers, QList<QStringList> logdata, QObject *parent) : QAbstractTableModel(parent) {
    /* logData contains extra leading data 
     * the first line are suspectLines
     * the first column of normal data is the chat type.
     */
    logdata = logdata;
    headerdata = headers;
}

int ChatTable::rowCount(const QModelIndex &parent) const {
    if (!logdata.isEmpty()) {
        return logdata.length() - 1;
    }
    return 0;
}
int ChatTable::columnCount(const QModelIndex &parent) const {
    if (!logdata.isEmpty() && !logdata.at(0).isEmpty()) {
        return logdata.at(1).length() - 1;
    }
    return 0;

}

QVariant ChatTable::data(const QModelIndex &index, int role) const {
    if (!index.isValid()) {
        return QVariant();
    }
    else if (role == Qt::BackgroundRole) {
        // Colors!
        QString chat = logdata.at(index.row() + 1).at(0);
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
    return QVariant(logdata.at(index.row() + 1).at(index.column() + 1));
}

QVariant ChatTable::headerData(int section, Qt::Orientation orientation, int role) const {
    if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
        return QVariant(headerdata.at(section));
    }
    return QVariant();
}

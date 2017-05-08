#include <QAbstractTableModel>
#include <QVariant>
#include <QList>
#include <QStringList>
#include <QObject>
#include <QBrush>
#include <QColor>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <search.h>
#include <QFile>

Reader::Reader(QMap<QString, QList<QString, QList<QStringList>> allData, QWidget *parent) : QWidget(parent) {
    setWindowTitle("PSO2 Chat Reader");
    resize(900, 500);
    allData = allData;
    // Build Table
    table = QTableView(this);
    table->setWordWrap(true);
    table->setSortingEnable(false);
    table->verticalHeader()->setVisible(false);

    // Build Tree
    tree = new QTreeView(this);
    tree.setFixedWidth(300);
    tree_model = new QStandardItemModel();
    tree.setModel(tree_model);
    connect(tree, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(updateContent(QModelIndex)));
    
    headers = {"Time", "PID/SID", "Message"};
    

    // Setup
    QVBoxLayout vbox = new VBoxLayout(this);
    logTitle = new QLabel("", this);
    vbox->addWidget(logTitle);
    vbox->addWidget(table);

    QHBoxLayout *hbox = new HBoxLayout(this);
    hbox->addWidget(tree);
    hbox->addLayout(vbox);

}

void Reader::generateTree(QMap<QString, QList<QStringList>> allData, QStandardItem *parent) {
    QStringList keys = allData.keys();
    keys.sort();
    int len = keys.length();
    int lines;
    QStandardItem topItem, subItem;
    QStringList suspectLines;
    QString key;
    for (int i = 0; i < len; i++) {
        key = keys.at(i);
        topItem = QStanardItem(key);
        topItem.setEditable(false);
        parent->append(topItem);
        // Leading element are the suspect lines
        suspectLines = allData[key].at(0);
        lines = suspectLines.length();
        for (int j = 0; j < lines; j++) {
            subItem = QStandardItem(suspectLines.at(j));
            subItem.setEditable(false);
            topItem.appendRow(subItem);        }

    }

}

void Reader::newTree(QMap<QString, QList<QStringList>> allData) {
    // Easier to just clear and rebuild the tree
    treeModel->clear();
    generateTree(allData, tree_model->invisibleRootItem());

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

    // Refresh Table
    logTitle = keys.at(0);
    ChatTable temp = new ChatTable()

}

// No longer needed with the updated search
void Reader::digest(QString filename) {
    // Special digestion of the file
    QList<QStringList> data;
    // Store data like so:
    // CHATTYPE, TIME, PID/SID, MESSAGE
    // THEN change the table to only access columns 2->4 of the data structures. 
    // thus hiding the first column
    QFile file(filename);
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QTextStream input(&file);
    input.setCodec("UTF-16LE");
    // Split file on newlines
    QStringList contents = input.readAll().split("\n");
    file.close();
    int count = 0;
    QStringList line
    QStringList message;
    int len;
    while (count < contents.length()) {
        message = QStringList();
        line = contents.at(count).split("\t");
        len = line.length();
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
            // Prevents duplicates
            data.remove_last();
        }
        // Build the message
        // Chat Type
        message << line.at(2);
        // Time
        message << line.at(0).split("T").at(0);
        // PID / SID
        message << (line.at(4) + "\n" + line.at(3));
        // The text
        message << line.at(5);
        data.append(message);
        count++;

    }
    
    return data;


}



// For the chats!
ChatTable::ChatTable(QStringList headers, QList<QStringList> logdata, QObject *parent) : QAbstractTableModel(parent) {
    logdata = logdata;
    headerdata = headers;
}

int rowCount(const QModelIndex &parent) const {
    if (logdata.isValid()) {
        return logdata.length();
    }
    return 0;
}
int columnCount(const QModelIndex &parent) const {
    if (logdata.isValid() && logdata.at(0).isValid()) {
        return logdata.at(0).length() - 1;
    }
    return 0;

}
QVariant data(QModelIndex &index, int role) const {
    if (!index.isValid()) {
        return QVariant();
    }
    else if (rol == Qt::BackgroundRole) {
        // Colors!
        QString chat = logdata.at(index.row()).at(0);
        if (chat == "PUBLIC") {
            return QBrush(Qt.lightGray);
        }
        else if (chat == "PARTY") {
            return QBrush(Qt.cyan);
        }
        else if (chat == "GUILD") {
            // Gold
            return QBrush(QColor(230, 157, 36));
        }
        else if (chat == "REPLY") {
            return QBrush(Qt.magenta);
        }
    }
    else if (role != Qt::DisplayRole) {
        return QVariant()
    }
    return QVariant(logdata.at(index.row()).at(index.column() + 1));
}

QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const {
    if (orientation == Qt::Horizontal && role == Qt::DisplayRole) {
        return QVariant(headerdata.at(section))
    }
    return QVariant();
}

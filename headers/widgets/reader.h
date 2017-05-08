// Includes

class Reader : public QWidget {

    Q_OBJECT

    public:
        Reader(QWidget parent = 0);
        
        // Methods
        void refresh(QStringList filenames);

    private slots:
        updateContent(QModelIndex);
        
    private:
        // Variables
        QStringList headers;
        QTableView table;
        QTreeView tree;
        QLabel logTitle;
        QStandardItemModel tree_model;

        // Methods
        generateTree();
        newTree();
        digestFile(QString filename);


};

class ChatTable : public QAbstractTableModel {
    
    Q_OBJECT

    public:
        ChatTable(QStringList headers, QStringList logdata, QObject *parent = 0) : QAbstractTableMode(parent);
        
        int rowCount(const QModelIndex &parent) const;
        int columnCount(const QModelIndex &parent) const;
        QVariant data(QModelIndex &index, int role) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const;

    private:
        QStringList headerdata;
        QList<QStringList> logdata;
        QStringList chatTypes;
        QMap<QString, QList<QStringList>> allData;
};



#pragma once
// Includes
#include <QAbstractTableModel>
#include <QStandardItemModel>
#include <QTableWidget>
#include <QTableView>
#include <QTreeView>
#include <QWidget>
#include <QString>
#include <QStringList>
#include <QObject>
#include <QLabel>
#include <QMap>
#include <QList>
#include <QVariant>
#include <QThread>
#include "rsearch.h"

class ChatTable : public QAbstractTableModel {
    
    Q_OBJECT

    public:
        ChatTable(QStringList headers, QList<QStringList> logdata, QObject *parent = 0);// : QAbstractTableModel(parent);
        
        int rowCount(const QModelIndex &parent) const;
        int columnCount(const QModelIndex &parent) const;
        QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const;

    private:
        QStringList headerdata;
        QList<QStringList> log;
        QStringList chatTypes;
};

class SimpleTableView : public QTableView {
    Q_OBJECT
    public:
        SimpleTableView(QWidget *parent = Q_NULLPTR);
    protected:
        void keyPressEvent(QKeyEvent *event);


};



class Reader : public QWidget {

    Q_OBJECT

    public:
        Reader(QString basepath, QMap<QDate, QStringList> allData, QWidget *parent = 0);
        Reader(QString basepath, QStringList Files, QStringList Dates, QMap<QString, QRegularExpression> Params, QWidget *parent = 0);
        
        // Methods
        // void refresh(QString basepath, QMap<QDate, QStringList> allData);
        void newSearch(QString basepath, QStringList Files, QStringList Dates, QMap<QString, QRegularExpression> Params);
        void clear();
        void stopExecution();

    private slots:
        void updateContent(QModelIndex index);
        // Need a slot for the timer polling here
        void tRefresh();
        void errorString(QString err);
        
    private:
        void initGui();
        rSearch *searchObj;
        QThread *searchThd;
        // Variables
        QString base;
        QStringList headers;
        // QTableView *table;
        SimpleTableView *table;
        QTreeView *tree;
        QLabel *logTitle;
        QStandardItemModel *treeModel;
        QMap<QDate, ChatTable*> alltables;

        // Methods
        void generateTree();
        void newTree();
        QList<QStringList> digestFile(QString filename);

        // Dynamic Reader
        QStringList *entries;
        bool *complete;
        QTimer *poll;
        int totalComplete = 0;
        QStringList files;
        QMap<QDate, QStringList> allData;
        void appendToTree(QDate newDate);
        int tickCount = 0;
        bool *stopped;


};


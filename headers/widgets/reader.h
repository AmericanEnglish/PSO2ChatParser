#pragma once
// Includes
#include <QAbstractTableModel>
#include <QStandardItemModel>
#include <QTableView>
#include <QTreeView>
#include <QWidget>
#include <QStringList>
#include <QObject>
#include <QLabel>
#include <QMap>
#include <QList>
#include <QVariant>

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


class Reader : public QWidget {

    Q_OBJECT

    public:
        Reader(QString basepath, QMap<QDate, QStringList> allData, QWidget *parent = 0);
        
        // Methods
        void refresh(QString basepath, QMap<QDate, QStringList> allData);

    private slots:
        void updateContent(QModelIndex index);
        
    private:
        // Variables
        QString base;
        QStringList headers;
        QTableView *table;
        QTreeView *tree;
        QLabel *logTitle;
        QStandardItemModel *treeModel;
        QMap<QDate, ChatTable*> alltables;

        // Methods
        void generateTree(QMap<QDate, QStringList> allData, QStandardItem *parent);
        void newTree(QMap<QDate, QStringList> allData);
        QList<QStringList> digestFile(QString filename);


};


#pragma once
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

class rSearch : public QObject {
    Q_OBJECT

    public:
        rSearch(QStringList Dates, QMap<QString, QRegularExpression> Params, QString Base, QStringList Files, QStringList *Entries, bool *Complete);
        // Variables
        QStringList dates; 
        QMap<QString, QRegularExpression> params;
        QString base;
        QStringList files; 
        QStringList *entries; 
        bool *complete;
    public slots:
        void run();
        void setStop(bool *cond);

    signals:
        void finished();
        void error(QString err);

    private:
        bool full_check(QStringList line);
        bool sidCheck(QString num);
        bool pidCheck(QString name);
        bool chatCheck(QString term);
        bool keywordCheck(QString message);
        bool dateCheck(QString date);
        QStringList too_many_tabs(QStringList line);
        QStringList buildLine(QStringList file, QString str, int start);
        QStringList searchFile(int i);
        // bool stopped = false;
        // Allows the object to be stopped outside of the thread
        bool *stopped;

};

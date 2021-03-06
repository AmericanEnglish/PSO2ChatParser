#pragma once


// Include
#include <QString>
#include <QStringList>
#include <QTextStream>
#include <QFile>
#include <QList>
#include <QMap>

// Functions
bool date_check(QStringList parameters, QString item);
bool sid_check(QStringList parameters, QString num);
bool pid_check(QStringList parameters, QString name);
bool chat_check(QStringList parameters, QString term);
bool keyword_check(QStringList parameters, QString message);

QStringList too_many_tabs(QStringList line);
QStringList buildLine(QStringList file, QString str, int start);
QStringList searchFile(QMap<QString, QStringList> parameters, QString filename);
//QStringList *loopSearch(QMap<QString, QStringList> parameters, QString base, QStringList allFiles);
 QMap<QDate, QStringList> loopSearch(QMap<QString, QStringList> parameters, QString base, QStringList allFiles);


#pragma once


// Include
#include <QString>
// Functions
bool date_check(QStringList parameters, QString item);
bool sid_check(QStringList parameters, QString num);
bool pid_check(QStringList parameters, QString name);
bool chat_check(QStringList parameters, QString term);
bool keyword_check(QStringList parameters, QString message);
QStringList too_many_tabs(QStringList line);
QStringList buildLine(QStringList file, QString str, int start);
QList<QStringList> searchfile(QMap<QString, QStringList> parameters, QString filename);
QMap<QString, QList<QStringList>> loopSearch(QMap<QString, QStringList> parameters, QString base, QStringList allFiles);

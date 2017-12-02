#pragma once

// Includes
#include <QLabel>
#include <QCalendarWidget>
#include <QDate>
#include <QWidget>

class ChatDate : public QWidget {

    Q_OBJECT

    public:
        ChatDate(QWidget *parent = 0);
        // Methods
        QList<QDate> liquidate();

        // Variables

    private slots:
        void setDate1();
        void clearDate1();
        void setDate2();
        void clearDate2();

    private:
        QCalendarWidget *bigCalendar;
        QLabel *beginLabel;
        QLabel *endLabel;
        QDate begin;
        QDate end;
};

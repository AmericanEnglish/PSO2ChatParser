#include <chatdate.h>
#include <QGridLayout>
#include <QLabel>
#include <QPushButton>
#include <QDate>
#include <QCalendarWidget>

ChatDate::ChatDate(QWidget *parent) : QWidget(parent) {
    // Grid
    QGridLayout *grid = new QGridLayout();

    // Cal
    bigCalendar = new QCalendarWidget(this);


    // Begin Date
    QPushButton *beginButton = new QPushButton("Begin Date:", this);
    QPushButton *clearBeginButton = new QPushButton("Clear", this);
    beginLabel = new QLabel(QString(), this);
    connect(beginButton, SIGNAL(clicked()), this, SLOT(setDate1()));
    connect(clearBeginButton, SIGNAL(clicked()), this, SLOT(clearDate1()));
    begin = QDate();

    // End Date
    QPushButton *endButton = new QPushButton("End Date:", this);
    QPushButton *clearEndButton = new QPushButton("Clear", this);
    endLabel = new QLabel(QString(), this);
    connect(endButton, SIGNAL(clicked()), this, SLOT(setDate2()));
    connect(clearEndButton, SIGNAL(clicked()), this, SLOT(clearDate2()));
    end = QDate();

    // Set Layout
    grid->addWidget(bigCalendar, 0, 0, 3, 4);
    grid->addWidget(beginButton, 4, 0);
    grid->addWidget(beginLabel,  4, 1);
    grid->addWidget(clearBeginButton, 4, 2);
    grid->addWidget(endButton,   5, 0);
    grid->addWidget(endLabel,    5, 1);
    grid->addWidget(clearEndButton, 5, 2);

    setLayout(grid);

}


void ChatDate::setDate1() {
    begin = bigCalendar->selectedDate();
    if (end.isValid()) {
        if (begin > end) {
            QDate temp = begin;
            begin = end;
            end = temp;
            endLabel->setText(end.toString("MM-dd-yyyy"));
        }
    }
    beginLabel->setText(begin.toString("MM-dd-yyyy"));
}

void ChatDate::clearDate1() {
    begin = QDate();
    beginLabel->setText(QString());
}

void ChatDate::setDate2() {
    end = bigCalendar->selectedDate();
    // Swap dates if ordered incorrectly
    if (begin.isValid()) {
        if (end < begin) {
            QDate temp = end;
            end = begin;
            begin = temp;
            beginLabel->setText(begin.toString("MM-dd-yyyy"));
        }
    }
    endLabel->setText(end.toString("MM-dd-yyyy"));
}

void ChatDate::clearDate2() {
    end = QDate();
    endLabel->setText(QString());
}

QStringList ChatDate::liquidate() {
    QStringList results;
    if (begin.isValid()) {
        results << begin.toString("yyyy-MM-dd") + "T00:00:00";
    }
    else {
        results << QString();
    }
    if (end.isValid()) {
        results << end.toString("yyyy-MM-dd") + "T23:59:59";
    }
    else {
        results << QString();
    }

    return results;
}

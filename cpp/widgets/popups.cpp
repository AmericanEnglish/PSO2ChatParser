#include <QDialog>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>
#include <QString>
#include "popups.h"


NoResults::NoResults(QString message, QWidget *parent) : QDialog(parent) {
    QVBoxLayout *layout = new QVBoxLayout(this);
    QLabel *displayMessage = new QLabel(message, this);
    QPushButton *acceptButton = new QPushButton("OK", this);

    connect(acceptButton, SIGNAL(clicked()), this, SLOT(accept()));

    layout->addWidget(displayMessage);
    layout->addWidget(acceptButton);
    setModal(true);
    setLayout(layout);
}



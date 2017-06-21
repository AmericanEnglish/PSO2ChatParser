#include <QDialog>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>
#include <QString>
#include "popups.h"


NoResults::NoResults(QString message, QWidget *parent) : QDialog(parent) {
   QVBoxLayout *layout = new QVBoxLayout(this);
   QLabel *displayMessage = new QLabel(message, this);
   QPushButton *accept = new QPushButton("OK", this);

   layout->addWidget(displayMessage);
   layout->addWidget(accept);
   setLayout(layout);
}



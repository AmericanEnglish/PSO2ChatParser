#include <pid.h>
#include <QCheckBox>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QString>
#include <QStringList>
#include <QWidget>

// Constructor
PID::PID(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Player ID");
    // Setup the grid
    QGridLayout *grid = new QGridLayout(this);
    
    // Setup controls
    PIDEdit = new QLineEdit(this);
    QLabel *label = new QLabel("Player ID#(s): ", this);
    label->setBuddy(PIDEdit);
    relative = new QCheckBox("Absolute Match", this);
    casing = new QCheckBox("Case Sensitive", this);
    searchFor = new QCheckBox("Use", this);

    // Setup Grid
    grid->addWidget(label,     0, 0);
    grid->addWidget(PIDEdit,   0, 1);
    grid->addWidget(searchFor, 1, 0);
    grid->addWidget(casing,    1, 1);
    grid->addWidget(relative,  1, 2);

    setLayout(grid);
}

void PID::browsePID() {

}

QStringList PID::liquidate() {
    if (searchFor->isChecked()) {
        QStringList result = PIDEdit->text().split(QRegExp("\\s+|,"));
        if (casing->isChecked()){
            result.push_front("sensitive");
        }
        else {
            result.push_front("not sensitive");
        }
        if (relative->isChecked()) {
            result.push_front("relative");
        }
        else {
            result.push_front("not relative");
        }
        return result;
    }
    else {
        return QStringList();
    }
    
}

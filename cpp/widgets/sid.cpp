#include <sid.h>
#include <QCheckBox>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QString>
#include <QStringList>
#include <QWidget>
#include <iostream>

// Constructor
SID::SID(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Sega ID");
    // Setup the grid
    QGridLayout *grid = new QGridLayout(this);
    
    // Setup controls
    SIDEdit = new QLineEdit(this);
    QLabel *label = new QLabel("SID#(s): ", this);
    label->setBuddy(SIDEdit);
    relative = new QCheckBox("Absolute Match", this);
    casing = new QCheckBox("Case Sensitive", this);
    searchFor = new QCheckBox("Use", this);

    // Setup Grid
    grid->addWidget(label,     0, 0);
    grid->addWidget(SIDEdit,   0, 1);
    grid->addWidget(searchFor, 1, 0);
    grid->addWidget(casing,    1, 1);
    grid->addWidget(relative,  1, 2);

    setLayout(grid);
}

void SID::browseSID() {

}

QStringList SID::liquidate() {
    std::cout << "Processing SID" << std::endl;
    if (searchFor->isChecked()) {
        std::cout << "Parsing SID..." << std::endl;
        QStringList result = SIDEdit->text().split(QRegExp("\\s+|,"));
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
    std::cout << "SID Not Used" << std::endl;
    return QStringList();
    
}


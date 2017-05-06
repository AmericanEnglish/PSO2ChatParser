#include <sid.h>
#include <QCheckBox>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QString>
#include <QStringList>
#include <QWidget>

// Constructor
SID::SID(QWidget *parent) : QWidget(parent) {
    setWindowTitle("Sega ID");
    // Setup the grid
    QGridLayout *grid = new QGridLayout(this);
    
    // Setup controls
    QLineEdit *SIDEdit = new QLineEdit(this);
    QLabel *label = new QLabel("SID#(s): ", this);
    label->setBuddy(SIDEdit);
    QCheckBox *relative = new QCheckBox("Absolute Match", this);
    QCheckBox *casing = new QCheckBox("Case Sensitive", this);
    QCheckBox *searchFor = new QCheckBox("Use", this);

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
    if (searchFor->isChecked()) {
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
    else {
        return QStringList();
    }
    
}


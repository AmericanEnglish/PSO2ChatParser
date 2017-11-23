#include <pid.h>
#include <QCheckBox>
#include <QGridLayout>
#include <QLabel>
#include <QLineEdit>
#include <QString>
#include <QStringList>
#include <QWidget>
#include <QRegularExpression>
#include <iostream> 

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

QRegularExpression PID::rLiquidate() {
    std::cout << "Processing PID" << std::endl;
    QRegularExpression re;
    if (searchFor->isChecked()) {
        std::cout << "Parsing PID..." << std::endl;
        QStringList results = PIDEdit->text().split(QRegExp("\\s+|,"));
        if (casing->isChecked()){
            if (relative->isChecked()) { // Absolute
                // Build a partial regex
                QStringList adjusted;
                for (int i = 0; i < results.length(); i++) {
                    adjusted.append("^" + results.at(i) + "$");
                }
                re.setPattern(adjusted.join("|"));
            }
            else {
                re.setPattern(results.join("|"));
            }
            re.setPatternOptions(
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
        }
        else {
            if (relative->isChecked()) {
                QStringList adjusted;
                for (int i = 0; i < results.length(); i++) {
                    adjusted.append( "^" + results.at(i) + "$");
                }
                re.setPattern(adjusted.join("|"));
            }
            else {
                re.setPattern(results.join("|"));
            }
            re.setPatternOptions(QRegularExpression::CaseInsensitiveOption | 
                    QRegularExpression::UseUnicodePropertiesOption |
                    QRegularExpression::OptimizeOnFirstUsageOption);
        }
        return re;
    }
    std::cout << "SID Not Used" << std::endl;
    // Matches whitespace and not Whitespace aka everything
    re.setPattern("[\\s\\S]*");
    re.setPatternOptions(
        QRegularExpression::UseUnicodePropertiesOption |
        QRegularExpression::OptimizeOnFirstUsageOption);
    return re;
}

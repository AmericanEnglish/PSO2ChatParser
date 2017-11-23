#pragma once

// Includes
#include <QWidget>
#include <QLineEdit>
#include <QLabel>
#include <QCheckBox>
#include <QRegularExpression>

// Declaration
class SID : public QWidget {

    Q_OBJECT
    
    public:
        // Constructor
        SID(QWidget *parent = 0);

        // Methods
        void browseSID();
        QRegularExpression rLiquidate();

    private:
        QCheckBox *searchFor;
        QCheckBox *relative;
        QCheckBox *casing;
        QLineEdit *SIDEdit;
};

#pragma once

// Includes
#include <QWidget>
#include <QLineEdit>
#include <QLabel>
#include <QCheckBox>
#include <QGridLayout>
#include <QStringList>
#include <Qstring>

// Declaration
class PID : public QWidget {
    
    Q_OBJECT

    public:
        // Constructor
        PID(QWidget *parent = 0);

        // Methods
        void browsePID();
        QStringList liquidate();

    private:

        // QLabel label;
        QCheckBox *searchFor;
        QCheckBox *relative;
        QCheckBox *casing;
        QLineEdit *PIDEdit;
};


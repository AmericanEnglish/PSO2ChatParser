#pragma once
// Include
#include <QCheckBox>
#include <QStringList>
#include <QRegularExpression>

// Declaration
class ChatType : public QWidget {
    
    Q_OBJECT

    public:
        ChatType(QWidget *parent = 0);

        // Methods
        QRegularExpression rLiquidate();

    private:

        // Variables
        QCheckBox *publix;
        QCheckBox *party;
        QCheckBox *guild;
        QCheckBox *reply;

};

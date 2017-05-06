#pragma once
// Include
#include <QCheckBox>
#include <QStringList>
// Declaration
class ChatType : public QWidget {
    
    Q_OBJECT

    public:
        ChatType(QWidget *parent = 0);

        // Methods
        QStringList liquidate();

    private:

        // Variables
        QCheckBox *publix;
        QCheckBox *party;
        QCheckBox *guild;
        QCheckBox *reply;

};

#pragma once
// Includes
#include <QWidget>
#include <QPlainTextEdit>
#include <QRadioButton>
#include <QCheckBox>
#include <QStringList>
#include <QRegularExpression>

class Keywords : public QWidget {
    
    Q_OBJECT

    public:
        // Constructor
        Keywords(QWidget *parent = 0);

        // Methods
        QRegularExpression rLiquidate();

    private:
        QPlainTextEdit *text;
        QRadioButton *phrase;
        QRadioButton *words;
        QRadioButton *nothing;
        QButtonGroup *radioGroup;
        QCheckBox *casing;
        QCheckBox *relative;


};

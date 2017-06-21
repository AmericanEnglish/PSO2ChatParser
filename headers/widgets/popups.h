#pragma once
#include <QDialog>

// All additional popups go here

class NoResults : public QDialog {
    
    Q_OBJECT

    public:
        // Constructor here
        NoResults(QString message = QString(), QWidget *parent = 0);
    
    private:
        // Nothing?

};

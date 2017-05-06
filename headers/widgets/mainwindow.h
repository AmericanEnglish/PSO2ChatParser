#pragma once

// Needed includes
#include <sid.h>
#include <pid.h>
#include <QWidget>
#include <QApplication>
#include <QGridLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QPushButton>
#include <QCloseEvent>
#include <QMap>

// Class declaration
class MainWindow : public QWidget {

    Q_OBJECT
    
    
    public:
        // Constructor
        MainWindow(QWidget *parent = 0);
        
        // Methods
        //void

        // Public Variables
        QString default_path;

    private slots:
        void showSID();
        void showLatest();
    
    protected:

    private:
        // Methods
        void initDB();
        void initGUI();
        void add_new_file();
        void closeEvent(QCloseEvent *event) override;
        void run();
        // Private Variables
        QWidget *latest_window;
        QWidget *segaid;
        QWidget *playerid;
        QMap<QString, QWidget*> popups;
        
        
        // SQLITE STUFF HERE
        // after I figure out how that stuff works
};

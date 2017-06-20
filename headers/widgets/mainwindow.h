#pragma once

// Needed includes
// #include <sid.h>
// #include <pid.h>
// #include <chattype.h>
#include <QWidget>
#include <QApplication>
#include <QGridLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QPushButton>
#include <QCloseEvent>
#include <QMap>
#include <QSqlDatabase>
#include <sid.h>
#include <pid.h>
#include <chattype.h>
#include <chatdate.h>
#include <keywords.h>
#include <reader.h>
#include <search.h>

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
        void showLatest();
        void run();
    
    private:
        // Methods
        void initDB();
        void initGUI();
        void add_new_file();
        void closeEvent(QCloseEvent *event) override;
        QMap<QString, QStringList> fullLiquidate();
        // Private Variables
        QWidget *latest_window;
        SID *segaid;
        PID *playerid;
        ChatType *chat;
        ChatDate *datez;
        Keywords *keywords;
        QMap<QString, QWidget*> popups;
        Reader *reader;
        QDir defaultPath;
        QSqlDatabase db;
        
        
        // SQLITE STUFF HERE
        // after I figure out how that stuff works
};

#include <mainwindow.h>
#include <sid.h>
#include <pid.h>
#include <chattype.h>
#include <chatdate.h>
#include <keywords.h>
#include <reader.h>
#include <search.h>
#include <QWidget>
#include <QApplication>
#include <QGridLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QPushButton>
#include <QCloseEvent>
#include <QMap>
#include <QDir>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <iostream>
#include <QDebug>
#include <QFileDialog>
#include <QSqlError>
#include <QSqlRecord>
#include <QRegExp>
// For threading
#include <QThread>
#include <QRegularExpression>

#include "popups.h"

MainWindow::MainWindow(QWidget *parent) : QWidget(parent) {
    initGUI();
    initDB();

}

void MainWindow::initDB() {
    QDir current = QDir(".");
    db = QSqlDatabase::addDatabase("QSQLITE");
    if (current.exists("parserData.db")) {
        // Connect to db
        db.setDatabaseName(current.absolutePath() + "\\" + "parserData.db");
        db.open();
        // Grab default path
        QSqlQuery query;
        bool noErr = query.exec("SELECT value "
                "FROM defaults "
                "WHERE name = 'path'");
        if (!noErr) {
            qDebug() << "ERROR:\n" << query.lastError().text();
        }
        else {
            query.next();
            QSqlRecord result = query.record();
            QString pth = result.value("value").toString();
            qDebug() << "Path found is:" << pth;
            defaultPath = QDir(pth);
        }
    }
    else {
        // Create database
        db.setDatabaseName(current.absolutePath() + "\\" + "parserData.db");
        db.open();
        // Ask for default path
        QString dir = QFileDialog::getExistingDirectory(this, "Select PSO2 Log Folder",
                                                "./",
                                                QFileDialog::ShowDirsOnly
                                                | QFileDialog::DontResolveSymlinks);
        qDebug() << "Path selected:" << dir;
        // INSERT into db
        QSqlQuery query;
        bool noErr = query.exec("CREATE TABLE defaults "
                "(name VARCHAR PRIMARY KEY," 
                "value VARCHAR)");
        if (!noErr) {
            qDebug() << "ERROR:\n" << query.lastError().text();
        }
        else {
            query.prepare("INSERT INTO defaults VALUES (:name, :value)");
            query.bindValue(":name",  "path");
            query.bindValue(":value", dir);
            noErr = query.exec();
            defaultPath = QDir(dir);
        }
    }
    // Check if default path is valid
    // if valid
    // else grab again

}

void MainWindow::initGUI() {
    setWindowTitle("PSO2ChatParser ~ Hoes Not Included");

    // Start the grid
    QGridLayout *grid = new QGridLayout();
    grid->setSpacing(10);

    // Buttons
    QPushButton *button1 = new QPushButton("SegaID", this);
    button1->setFixedSize(80, 80);
    grid->addWidget(button1, 0, 0);
    connect(button1, SIGNAL(clicked()), this, SLOT(showLatest()));
    
    QPushButton *button2 = new QPushButton("Player ID", this);
    button2->setFixedSize(80, 80);
    grid->addWidget(button2, 0, 1);
    connect(button2, SIGNAL(clicked()), this, SLOT(showLatest()));

    QPushButton *button3 = new QPushButton("Chat Type", this);
    button3->setFixedSize(80 ,80);
    grid->addWidget(button3, 0, 2);
    connect(button3, SIGNAL(clicked()), this, SLOT(showLatest()));

    QPushButton *button4 = new QPushButton("Chat Date", this);
    button4->setFixedSize(80, 80);
    grid->addWidget(button4, 0, 3);
    connect(button4, SIGNAL(clicked()), this, SLOT(showLatest()));

    QPushButton *button5 = new QPushButton("Keywords", this);
    button5->setFixedSize(80, 80);
    grid->addWidget(button5, 0, 4);
    connect(button5, SIGNAL(clicked()), this, SLOT(showLatest()));

    QPushButton *button6 = new QPushButton("Settings", this);
    button6->setFixedSize(80, 80);
    grid->addWidget(button6, 0, 5);
    connect(button6, SIGNAL(clicked()), this, SLOT(showLatest()));
    button6->setEnabled(false);

    QPushButton *button7 = new QPushButton("FIND IT!", this);
    button7->setFixedSize(80, 80);
    grid->addWidget(button7, 0, 6);
    connect(button7, SIGNAL(clicked()), this, SLOT(run()));
    // button7->setEnabled(false);

    // Additional Windows
    // popups
    segaid = new SID();
    playerid = new PID();
    chat = new ChatType();
    datez = new ChatDate();
    keywords = new Keywords();
    // settings = new Settings();
    reader = nullptr;

    popups["SegaID"] = segaid;
    popups["Player ID"] = playerid;
    popups["Chat Type"] = chat;
    popups["Chat Date"] = datez;
    popups["Keywords"] = keywords;
    // popups["Settings"] = settings;

    // Figure out filters laters
    // defaultPath.setFilter(QDir::NoDotAndDotDot);

    latest_window = nullptr;



    // Final touches
    setLayout(grid);
    show();
}

void MainWindow::add_new_file() {

}

void MainWindow::run() {
    QRegExp filepattern("^ChatLog\\d{8}\\_00.txt$");
    std::cout << "Run begin" << std::endl;
    QMap<QString, QRegularExpression> parameters = fullRLiquidate();
    std::cout << "Liquidation of assests complete" << std::endl;
    QStringList allFiles  = defaultPath.entryList();
    allFiles = allFiles.filter(filepattern);
    qDebug() << allFiles;
    // allFiles.removeOne(".");
    // allFiles.removeOne("..");
    // qDebug() << allFiles;
    std::cout << "Files Gathered!" << std::endl;
    // QMap<QDate, QStringList> results = loopSearch(parameters, defaultPath.absolutePath() + "\\", allFiles);
    // qDebug() << "Search complete, Empty?: " << results.keys().isEmpty() << results.keys();
    // qDebug() << results;
    // if (results.keys().isEmpty()) {
        // // Show some dialog box
        // NoResults *noresults = new NoResults("No Logs Matched Your Search!", this);
        // noresults->exec();
        // delete noresults;
    // }
    if (reader == nullptr) {
        // std::cout << "Opening New Reader..." << std::endl;
        reader = new Reader(defaultPath.absolutePath() + "\\", allFiles, datez->liquidate(), parameters);
        reader->show();
    }
    else {
        // std::cout << "Refreshing Old Reader.." << std::endl;
        reader->clear();
        reader->newSearch(defaultPath.absolutePath() + "\\", allFiles, datez->liquidate(), parameters);
    }

}

void MainWindow::showLatest() {
    QPushButton* button = qobject_cast<QPushButton*>(sender());
    QString name = button->text();

    // segaid->show();
    if (latest_window == nullptr) {
        // latest_window = segaid;
        latest_window = popups[name];
        latest_window->show();
    }
    else if (latest_window == popups[name]) {
    // else if (latest_window == segaid) {
        latest_window->hide();
        latest_window = nullptr;
    }
    else {
        latest_window->hide();
        // latest_window = segaid;
        latest_window = popups[name];
        latest_window->show();
    }
}

void MainWindow::closeEvent(QCloseEvent *event) {
    QList<QString> toClose = popups.keys();
    int len = toClose.length();
    for (int i = 0; i < len; i++) {
        popups[toClose.at(i)]->deleteLater();
    }
    if (reader != nullptr) {
        reader->deleteLater();
    }
    // segaid->deleteLater();
    event->accept();
}


QMap<QString, QRegularExpression> MainWindow::fullRLiquidate() {
    QMap<QString, QRegularExpression> results;
    // QStringList keys = popups.keys();
    // int len = keys.length();
    // QString key;
    // for (int i = 0; i < len; i++) {
        // key = keys.at(i);
        // results[key] = popups[key]->liquidate();
    // }
    std::cout << "Checking Assests.." << std::endl;
    results["sid"] = segaid->rLiquidate();
    std::cout << "SID finished" << std::endl;
    results["pid"] = playerid->rLiquidate();
    std::cout << "PID finished" << std::endl;
    results["chat"] = chat->rLiquidate();
    std::cout << "Chat Type finished" << std::endl;
    results["word"] = keywords->rLiquidate();
    std::cout << "Keywords finished" << std::endl;

    return results;
}


int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow window;
    // window.resize(800, 200);
    return app.exec();
}

#include <mainwindow.h>
#include <sid.h>
#include <pid.h>
#include <chattype.h>
#include <chatdate.h>
#include <keywords.h>
#include <QWidget>
#include <QApplication>
#include <QGridLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QPushButton>
#include <QCloseEvent>
#include <QMap>

MainWindow::MainWindow(QWidget *parent) : QWidget(parent) {
    initGUI();
    initDB();

}

void MainWindow::initDB() {

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
    button7->setEnabled(false);

    // Additional Windows
    // popups
    segaid = new SID();
    playerid = new PID();
    chat = new ChatType();
    datez = new ChatDate();
    keywords = new Keywords();
    // settings = new Settings();

    popups["SegaID"] = segaid;
    popups["Player ID"] = playerid;
    popups["Chat Type"] = chat;
    popups["Chat Date"] = datez;
    popups["Keywords"] = keywords;
    // popups["Settings"] = settings;

    latest_window = nullptr;



    // Final touches
    setLayout(grid);
    show();
}

void MainWindow::add_new_file() {

}

void MainWindow::run() {

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
    // segaid->deleteLater();
    event->accept();
}


int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow window;
    // window.resize(800, 200);
    return app.exec();
}

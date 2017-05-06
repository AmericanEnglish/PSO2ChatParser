CONFIG += qt debug console
QT += widgets
INCLUDEPATH += headers/widgets headers/
HEADERS += headers/widgets/mainwindow.h headers/widgets/sid.h headers/widgets/pid.h
SOURCES += cpp/widgets/mainwindow.cpp cpp/widgets/sid.cpp cpp/widgets/pid.cpp
QMAKE_CXXFLAGS += /openmp /EHsc
# LIBS += fopenmp

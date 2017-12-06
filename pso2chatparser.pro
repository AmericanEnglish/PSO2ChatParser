CONFIG += qt debug_and_release console
QT += widgets sql
INCLUDEPATH += headers/widgets headers/
HEADERS += headers/widgets/mainwindow.h headers/widgets/sid.h headers/widgets/pid.h headers/widgets/chattype.h headers/widgets/chatdate.h headers/widgets/keywords.h headers/widgets/reader.h headers/widgets/popups.h headers/search.h headers/rsearch.h
SOURCES += cpp/widgets/mainwindow.cpp cpp/widgets/sid.cpp cpp/widgets/pid.cpp cpp/widgets/chattype.cpp cpp/widgets/chatdate.cpp cpp/widgets/keywords.cpp cpp/widgets/reader.cpp cpp/widgets/popups.cpp cpp/search.cpp cpp/rsearch.cpp
QMAKE_CXXFLAGS += /openmp /EHsc
# LIBS += openmp
CHASH=$$system( git rev-parse --short HEAD)
message(Hash: $$CHASH)
DEFINES += CHASH=\\\"$$CHASH\\\"

cmake_minimum_required(VERSION 3.10)
project(PSO2ChatParser)

enable_language("CXX")
#set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set("SRCBASE" "${PROJECT_SOURCE_DIR}/cpp")
set("WIDGETS" "${SRCBASE}/widgets")

set("SRC"
    "${SRCBASE}/rsearch.cpp"
    "${SRCBASE}/search.cpp"
    "${WIDGETS}/chatdate.cpp"
    "${WIDGETS}/chattype.cpp"
    "${WIDGETS}/keywords.cpp"
    "${WIDGETS}/pid.cpp"
    "${WIDGETS}/popups.cpp"
    "${WIDGETS}/reader.cpp"
    "${WIDGETS}/sid.cpp"
    #"${WIDGETS}/"
    )

# Header files
set("HEADERS" "${PROJECT_SOURCE_DIR}/headers")
set("HWIDGETS" "${HEADERS}/widgets")
include_directories(
    "${HEADERS}/"
    "${HEADERS}/widgets"
)
set("HEADER_FILES"
    "${HEADERS}/rsearch.h"
    "${HEADERS}/search.h"
    "${HWIDGETS}/chatdate.h"
    "${HWIDGETS}/chattype.h"
    "${HWIDGETS}/keywords.h"
    "${HWIDGETS}/pid.h"
    "${HWIDGETS}/popups.h"
    "${HWIDGETS}/reader.h"
    "${HWIDGETS}/sid.h"
    )


# Enable Automoc
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Required packages
find_package(Qt5 COMPONENTS REQUIRED Widgets Sql Core)
find_package(OpenMP REQUIRED)

# The main executable
add_executable("PSO2ChatParser" 
    "${WIDGETS}/mainwindow.cpp" 
    "${HWIDGETS}/mainwindow.h"
    "${SRC}" 
    "${HEADER_FILES}"
    )

# Link packages
target_link_libraries(PSO2ChatParser OpenMP::OpenMP_CXX)
target_link_libraries(PSO2ChatParser Qt5::Core Qt5::Widgets Qt5::Sql)

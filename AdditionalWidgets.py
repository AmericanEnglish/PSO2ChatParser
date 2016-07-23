from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QCalendarWidget, QRadioButton, QButtonGroup
# Sega ID Window
class SegaID(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        SIDEdit = QLineEdit(self)
        SIDLabel = QLabel("SID#: ", self)
        SIDLabel.setBuddy(SIDEdit)
        SearchByCheckbox = QCheckBox("Search For SID", self)
        FilterByCheckbox = QCheckBox("Filter By SID", self)
        SearchForAnIDButton = QPushButton("Search For SID#", self)
        # Setup Grid
        grid.addWidget(SIDLabel,            0, 0)
        grid.addWidget(SIDEdit,             0, 1)
        grid.addWidget(SearchByCheckbox,    1, 1)
        grid.addWidget(FilterByCheckbox,    2, 1)
        grid.addWidget(SearchForAnIDButton, 3, 1)
        # QCheckBox.isChecked() -> Bool
        self.setWindowTitle("Sega ID Options")


# Player ID Window
class PlayerID(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        PIDEdit = QLineEdit(self)
        PIDLabel = QLabel("PlayerID: ", self)
        PIDLabel.setBuddy(PIDEdit)
        SearchByCheckbox = QCheckBox("Search For PID", self)
        FilterByCheckbox = QCheckBox("Filter By PID", self)
        SearchForAnIDButton = QPushButton("Search For PID", self)
        # Setup Grid
        grid.addWidget(PIDLabel,            0, 0)
        grid.addWidget(PIDEdit,             0, 1)
        grid.addWidget(SearchByCheckbox,    1, 1)
        grid.addWidget(FilterByCheckbox,    2, 1)
        grid.addWidget(SearchForAnIDButton, 3, 1)
        # QCheckBox.isChecked() -> Bool
        self.setWindowTitle("Player ID Options")

        # Add an option later so that you can comb through ALL usernames for searching
        # each with their own filter and search by settings


class ChatTypeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        grid = QGridLayout()
        self.setLayout(grid)
        PUBLIC = QCheckBox("Public", self)
        PUBLIC.setChecked(True)
        PARTY = QCheckBox("Party", self)
        PARTY.setChecked(True)
        GUILD = QCheckBox("Team", self)
        GUILD.setChecked(True)
        WHISPER = QCheckBox("Whisper", self)
        WHISPER.setChecked(True)
        grid.addWidget(PUBLIC,  0, 0)
        grid.addWidget(PARTY,   1, 0)
        grid.addWidget(GUILD,   2, 0)
        grid.addWidget(WHISPER, 3, 0)
        self.setWindowTitle("Chat Options")


class ChatTime(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        # Calendar Widget
        self.BigCalendar = QCalendarWidget(self)
        grid.addWidget(self.BigCalendar, 0, 0, 3, 4)
        # Begin button and date
        BeginButton = QPushButton("Begin:", self)
        BeginLabel = QLabel("", self)
        BeginLabel.setBuddy(BeginButton)
        BeginButton.clicked.connect(lambda:BeginLabel.setText(
                                        self.getdate()))
        grid.addWidget(BeginLabel,  4, 1)
        grid.addWidget(BeginButton, 4, 0)
        # End Date
        EndButton = QPushButton("End:", self)
        EndLabel = QLabel("", self)
        EndLabel.setBuddy(EndButton)
        EndButton.clicked.connect(lambda:EndLabel.setText(self.getdate()))
        grid.addWidget(EndLabel,  5, 1)
        grid.addWidget(EndButton, 5, 0)
        # Use Checkboxes
        BeginUseCheck = QCheckBox("Use", self)
        EndUseCheck = QCheckBox("Use", self)
        grid.addWidget(BeginUseCheck, 4, 2)
        grid.addWidget(EndUseCheck,   5, 2)

        self.setWindowTitle("Chat Date Options")

    def getdate(self):
        return self.BigCalendar.selectedDate().toString("yyyy - MM - dd")

    def options(Name):
        pass


class KeywordSearch(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        # Label and Field
        KeywordLabel = QLabel("Phrase:", self)
        KeywordField = QLineEdit(self)
        # Case Sensitive
        KeywordCheckbox = QCheckBox("Case Sensitive?", self)
        # Clear Button
        ClearButton = QPushButton("Clear Field", self)
        # Word Or Sentence Search
        RadioLabel = QLabel("Search As A")
        RadioGroup = QButtonGroup(self)
        WordRadio = QRadioButton("Sentence", self)
        RadioGroup.addButton(WordRadio, 0)
        SentenceRadio = QRadioButton("Collection Of Words", self)
        RadioGroup.addButton(SentenceRadio, 1)

        grid.addWidget(KeywordLabel,    0, 0)
        grid.addWidget(KeywordField,    0, 1)
        grid.addWidget(ClearButton,     0, 2)
        grid.addWidget(KeywordCheckbox, 1, 1)
        grid.addWidget(WordRadio,       1, 0)
        grid.addWidget(SentenceRadio,   1, 2)
        self.setWindowTitle("Keyword Search Options")


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        # Database Options ---> Also autoset these options to the defaults
        self.sqlgroup = QButtonGroup(self)
        DBOptionLabel = QLabel("Database Selection\nRead Help If This Is Confusing", self)
        DBOptionSQLite = QRadioButton("SQLite3", self)
        DBOptionSQLite.clicked.connect(self.DBChange())
        DBOptionPGSQL = QRadioButton("PostgreSQL", self)
        DBOptionPGSQL.clicked.connect(self.DBChange())
        self.sqlgroup.addButton(DBOptionSQLite, 0)
        self.sqlgroup.addButton(DBOptionPGSQL,  1)
        # 24 or 12 Hour Format
        self.timegroup = QButtonGroup(self)
        TimeOptionLabel = QLabel("Time Format")
        TimeOptionTwenty4 = QRadioButton("24 Hour", self)
        TimeOptionTwelve  = QRadioButton("12 Hour", self)
        self.timegroup.addButton(TimeOptionTwenty4, 0)
        self.timegroup.addButton(TimeOptionTwelve,  1)
        # Add several options for how timestamps should be displayed in the logs
        # yyyy/mm/dd:
        # Jan, dd, yyyy:
        
        # Language
        LanguageOptionLabel = QLabel("Language", self)
        self.languagegroup = QButtonGroup(self)
        LanguageOptionENG = QRadioButton("English")
        LanguageOptionSPA = QRadioButton(u"Español")
        LanguageOptionSPA.setEnabled(False)
        self.languagegroup.addButton(LanguageOptionENG, 0)
        self.languagegroup.addButton(LanguageOptionSPA, 1)
        ################### Putting it together ####################
        grid.addWidget(DBOptionLabel,       0, 1)
        grid.addWidget(DBOptionSQLite,      1, 0)
        grid.addWidget(DBOptionPGSQL,       1, 2)

        grid.addWidget(TimeOptionLabel,     3, 1)
        grid.addWidget(TimeOptionTwelve,    4, 0)
        grid.addWidget(TimeOptionTwenty4,   4, 2)

        grid.addWidget(LanguageOptionLabel, 6, 1)
        grid.addWidget(LanguageOptionENG,   7, 0)
        grid.addWidget(LanguageOptionSPA,   7, 2)

        # Some scroll bar widget here someday
        self.setWindowTitle("Settings")

        def DBChange(self):
            # Throwup Long Custom Warning Message
            # If DB needs to be changed throw signal to main window


class Reader(QWidget):
    def __init__(self):
        super().__init__()

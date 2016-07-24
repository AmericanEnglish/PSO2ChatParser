from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QCalendarWidget, QRadioButton, QButtonGroup
# Sega ID Window
class PostgreSQLogin(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)

        # Labels
        HostLabel = QLabel("Hostname:", self)
        # PortLabel = QLabel("Port:", self)
        DatabaseNameLabel = QLabel("Database Name:", self)
        UserLabel = QLabel("Username", self)
        PassLabel = QLabel("Password", self)
        # Fields
        self.HostField = QLineEdit(self)
        self.PortField = QLineEdit(self)
        self.DatabaseNameField = QLineEdit(self)
        self.UserField = QLineEdit(self)
        self.PassField = QLineEdit(self)

        AcceptButton = QPushButton("Accept", self)
        AcceptButton.clicked.connect(lambda:self.success())
        RejectButton = QPushButton("Cancel", self)
        RejectButton.clicked.connect(lambda:self.failure())
        # Set Defaults
        self.HostField.setText("localhost")
        # self.PortField.setText("default")
        self.PassField.setEchoMode(2)
        self.setModal(True)
        # Setup Interface
        grid.addWidget(HostLabel,              0, 0)
        grid.addWidget(self.HostField,         0, 1, 0, 2)
        grid.addWidget(DatabaseNameLabel,      1, 0)
        grid.addWidget(self.DatabaseNameField, 1, 1, 1, 2)
        grid.addWidget(UserLabel,              2, 0)
        grid.addWidget(self.UserField,         2, 1, 2, 2)
        grid.addWidget(PassLabel,              3, 0)
        grid.addWidget(self.PassField,         3, 1, 3, 2)
        grid.addWidget(AcceptButton,           4, 1)
        grid.addWidget(RejectButton,           4, 2)

    def success(self):
        data = [str(self.DatabaseNameField.getText()), str(self.HostField.getText()), 
                str(self.UserField.getText()), str(self.PassField.getText())]
        return data

    def failure(self):
        return None


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
        SearchForAnIDButton = QPushButton("Browse SID#'s", self)
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
        PIDLabel = QLabel("Username: ", self)
        PIDLabel.setBuddy(PIDEdit)
        SearchByCheckbox = QCheckBox("Search For Username", self)
        FilterByCheckbox = QCheckBox("Filter By Username", self)
        SearchForAnIDButton = QPushButton("Browse Usernames", self)
        # Setup Grid
        grid.addWidget(PIDLabel,            0, 0)
        grid.addWidget(PIDEdit,             0, 1)
        grid.addWidget(SearchByCheckbox,    1, 1)
        grid.addWidget(FilterByCheckbox,    2, 1)
        grid.addWidget(SearchForAnIDButton, 3, 1)
        # QCheckBox.isChecked() -> Bool
        self.setWindowTitle("Username Options")

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
        self.begin_date = None
        self.end_date = None
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
                                        self.getbegindate()))
        grid.addWidget(BeginLabel,  4, 1)
        grid.addWidget(BeginButton, 4, 0)
        # End Date
        EndButton = QPushButton("End:", self)
        EndLabel = QLabel("", self)
        EndLabel.setBuddy(EndButton)
        EndButton.clicked.connect(lambda:EndLabel.setText(self.getenddate()))
        grid.addWidget(EndLabel,  5, 1)
        grid.addWidget(EndButton, 5, 0)
        # Use Checkboxes
        BeginUseCheck = QCheckBox("Use", self)
        EndUseCheck = QCheckBox("Use", self)
        grid.addWidget(BeginUseCheck, 4, 2)
        grid.addWidget(EndUseCheck,   5, 2)

        self.setWindowTitle("Chat Date Options")

    def getbegindate(self):
        self.end_date = self.BigCalendar.selectedDate()
        return self.end_date.toString("yyyy - MM - dd")

    def getenddate(self):
        self.end_date = self.BigCalendar.selectedDate()
        return self.end_date.toString("yyyy - MM - dd")

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
        ClearButton.clicked.connect(lambda:KeywordField.setText(""))
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


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.buttons = {}
        # Database Options ---> Also autoset these options to the defaults
        self.sqlgroup = QButtonGroup(self)
        DBOptionLabel = QLabel("Database Selection", self)
        self.buttons["sqlite3"] = QRadioButton("SQLite3", self)
        self.buttons["sqlite3"].clicked.connect(lambda:self.DBChange())
        self.buttons["postgres"] = QRadioButton("PostgreSQL", self)
        self.buttons["postgres"].clicked.connect(lambda:self.DBChange())
        self.sqlgroup.addButton(self.buttons["sqlite3"], 0)
        self.sqlgroup.addButton(self.buttons["postgres"],  1)
        # 24 or 12 Hour Format
        self.timegroup = QButtonGroup(self)
        TimeOptionLabel = QLabel("Time Format")
        self.buttons["24hour"] = QRadioButton("24 Hour", self)
        self.buttons["12hour"]  = QRadioButton("12 Hour", self)
        self.timegroup.addButton(self.buttons["24hour"], 0)
        self.timegroup.addButton(self.buttons["12hour"],  1)
        # Add several options for how timestamps should be displayed in the logs
        # yyyy/mm/dd:
        # Jan, dd, yyyy:
        
        # Language, maybe do this in a combo box after it acquires more than three translations
        LanguageOptionLabel = QLabel("Language", self)
        self.languagegroup = QButtonGroup(self)
        self.buttons["english"] = QRadioButton("English")
        self.buttons["spanish"] = QRadioButton(u"Español")
        self.buttons["spanish"].setEnabled(False)
        self.languagegroup.addButton(self.buttons["english"], 0)
        self.languagegroup.addButton(self.buttons["spanish"], 1)
        ################### Putting it together ####################
        grid.addWidget(DBOptionLabel,                0, 0)
        grid.addWidget(self.buttons["sqlite3"],      0, 1)
        grid.addWidget(self.buttons["postgres"],     0, 2)

        grid.addWidget(TimeOptionLabel,              1, 0)
        grid.addWidget(self.buttons["12hour"],             1, 1)
        grid.addWidget(self.buttons["24hour"],       1, 2)

        grid.addWidget(LanguageOptionLabel,          2, 0)
        grid.addWidget(self.buttons["english"],            2, 1)
        grid.addWidget(self.buttons["spanish"],            2, 2)

        # Some scroll bar widget here someday
        self.setWindowTitle("Settings")

    def DBChange(self):
        # Throwup Long Custom Warning Message
        # If DB needs to be changed throw signal to main window
        pass

    def dbSet(self, default):
        self.buttons[default].setChecked(True)

    def setTimeFormat(self, default):
        self.buttons[default].setChecked(True)

    def setLanguage(self, default):
        self.buttons[default].setChecked(True)

class Reader(QWidget):
    def __init__(self):
        super().__init__()

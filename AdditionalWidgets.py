from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QCalendarWidget, QRadioButton, QButtonGroup, QDialog, QDialogButtonBox, QHBoxLayout, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
import re
# Subclass QDialog
class PostgreSQLogin(QDialog):
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
        # self.PortField = QLineEdit(self)
        self.DatabaseNameField = QLineEdit(self)
        self.UserField = QLineEdit(self)
        self.PassField = QLineEdit(self)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        ######################
        ButtonWidget = QWidget()
        ButtonBox = QHBoxLayout()
        ButtonBox.addWidget(self.buttons)
        ButtonWidget.setLayout(ButtonBox)
        #####################
        # Set Defaults
        self.HostField.setText("localhost")
        # self.PortField.setText("default")
        self.PassField.setEchoMode(2)
        self.setModal(True)
        # Setup Interface
        grid.addWidget(HostLabel,              0, 0)
        grid.addWidget(self.HostField,         0, 1)#, 0, 2)
        grid.addWidget(DatabaseNameLabel,      1, 0)
        grid.addWidget(self.DatabaseNameField, 1, 1)#, 1, 2)
        grid.addWidget(UserLabel,              2, 0)
        grid.addWidget(self.UserField,         2, 1)#, 2, 2)
        grid.addWidget(PassLabel,              3, 0)
        grid.addWidget(self.PassField,         3, 1)#, 3, 2)
        grid.addWidget(ButtonWidget,           4, 1)#, 4, 2)
        self.setWindowTitle("PostgreSQL Login Information")
        
    def success(self):
        data = [str(self.DatabaseNameField.text()), str(self.HostField.text()), 
                str(self.UserField.text()), str(self.PassField.text())]
        return data

    def failure(self):
        return None

    def getInfo():
        dialog = PostgreSQLogin()
        results = dialog.exec_()
        return (dialog.success(), results == QDialog.Accepted)


# Subclass QDialog
class ChooseDB(QDialog):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)

        # DatabaseLabel = QLabel("Pick A Database To Use", self)
        self.setWindowTitle("Pick A Database To Use")
        self.SQLite3Button = QRadioButton("SQLite3", self)
        self.SQLite3Button.setChecked(True)
        self.PostgreSQLButton = QRadioButton("PostgreSQL", self)
        DBGroup = QButtonGroup(self)
        DBGroup.addButton(self.SQLite3Button)
        DBGroup.addButton(self.PostgreSQLButton)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


        # Layout
        SQLWidget = QWidget()
        SQLButtons = QHBoxLayout()
        SQLButtons.addWidget(self.SQLite3Button)
        SQLButtons.addWidget(self.PostgreSQLButton)
        SQLWidget.setLayout(SQLButtons)
        ButtonWidget = QWidget()
        ButtonBox = QHBoxLayout()
        ButtonBox.addWidget(self.buttons)
        ButtonWidget.setLayout(ButtonBox)

        grid.addWidget(SQLWidget,     1, 0, 1, 2)
        grid.addWidget(ButtonWidget,  4, 1, 4, 2)


    def checkDB(self):
        if self.SQLite3Button.isChecked():
            return "sqlite3"
        else:
            return "postgres"

    # Workaround found on stack overflow
    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    def getDB():
        dialog = ChooseDB()
        dialog.exec_()
        results = dialog.result()
        return (dialog.checkDB(), results == QDialog.Accepted)


class SegaID(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.SIDEdit = QLineEdit(self)
        SIDLabel = QLabel("SID#(s): ", self)
        SIDLabel.setBuddy(self.SIDEdit)
        self.SearchByCheckbox = QCheckBox("Search For SID", self)
        self.FilterByCheckbox = QCheckBox("Filter By SID", self)
        SearchForAnIDButton = QPushButton("Browse SID#'s", self)
        SearchForAnIDButton.clicked.connect(lambda:self.browseSID())
        SearchForAnIDButton.setEnabled(False)
        # Setup Grid
        grid.addWidget(SIDLabel,                 0, 0)
        grid.addWidget(self.SIDEdit,             0, 1)
        grid.addWidget(self.SearchByCheckbox,    1, 1)
        grid.addWidget(self.FilterByCheckbox,    2, 1)
        grid.addWidget(SearchForAnIDButton,      3, 1)
        # QCheckBox.isChecked() -> Bool
        self.setWindowTitle("Sega ID Options")

    def setDB(self, database):
        self.db = database

    def browseSID(self):
        # Call Window
        newText = BrowseWindow.dumptext(self.fetched)
        if newText != '':
            self.SIDEdit.setText(newText)

    def update():
        self.db.execute("""SELECT DISTINCT uid, username FROM chat;""")
        temp = self.db.fetchall()
        self.fetched = {}
        for item in temp:
            if item[0] in self.fetched:
                self.fetched[item[0]].append(item[1])
            else:
                self.fetched[item[0]] = [item[1]]   

    def liquidate(self):
        fodder = []
        for first in re.split(",", self.SIDEdit.text()):
            for second in re.split(" ", first):
                if second != '':
                    fodder.append(second)
        return [self.SearchByCheckbox.isChecked(), self.FilterByCheckbox.isChecked(), fodder]

# Player ID Window
class PlayerID(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        self.PIDEdit = QLineEdit(self)
        PIDLabel = QLabel("Username(s):", self)
        PIDLabel.setBuddy(self.PIDEdit)
        self.SearchByCheckbox = QCheckBox("Search For Username", self)
        self.FilterByCheckbox = QCheckBox("Filter By Username", self)
        SearchForAnIDButton = QPushButton("Browse Usernames", self)
        SearchForAnIDButton.clicked.connect(lambda:self.browsePID())
        SearchForAnIDButton.setEnabled(False)
        # Setup Grid
        grid.addWidget(PIDLabel,            0, 0)
        grid.addWidget(self.PIDEdit,             0, 1)
        grid.addWidget(self.SearchByCheckbox,    1, 1)
        grid.addWidget(self.FilterByCheckbox,    2, 1)
        grid.addWidget(SearchForAnIDButton, 3, 1)
        # QCheckBox.isChecked() -> Bool
        self.setWindowTitle("Username Options")

        # Add an option later so that you can comb through ALL usernames for searching
        # each with their own filter and search by settings
        self.fetched = None

    def setDB(self, database):
        self.db = database
        self.update()

    def browsePID(self):
        # Call Window
        newText = BrowseWindow.dumptext(self.fetched)
        if newText != '':
            self.PIDEdit.setText(newText)

    def update(self):
        self.db.execute("""SELECT DISTINCT username, uid FROM chat WHERE uid > 5000;""")
        temp = self.db.fetchall()
        self.fetched = {}
        for item in temp:
            if item[0] in self.fetched:
                self.fetched[item[0]].append(str(item[1]))
            else:
                self.fetched[item[0]] = [str(item[1])]

    def liquidate(self):
        fodder = []
        for first in re.split(",", self.PIDEdit.text()):
            for second in re.split(" ", first):
                if second != '':
                    fodder.append(second)
        return [self.SearchByCheckbox.isChecked(), self.FilterByCheckbox.isChecked(), fodder]


class BrowseWindow(QDialog):
    def __init__(self, terms):
        super().__init__()
        # Scrolls Bar
        # Population Loop
        # print(terms)
        self.items = []
        collection = list(terms.keys())
        collection.sort()
        grid = QGridLayout()
        n = 0
        Filler = QWidget()

        for item in collection:
            # Check box, Primary Item, Secondary Items
            self.items.append([QCheckBox(self), item, terms[item]])
            grid.addWidget(self.items[-1][0], n, 0)
            grid.addWidget(QLabel(self.items[-1][1], self), n, 1)
            grid.addWidget(QLabel(', '.join(self.items[-1][2])[:-2], self), n, 2)
            n += 1
        # Pack items into scrolls bar
        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        Filler.setLayout(grid)
        scroll.setWidget(Filler)
        scroll.setWidgetResizable(False)
        # Accepted / Cancel Button
        self.setWindowTitle("Browse Possibilities . . .")

    def dumptext(displayable):
        Browsing = BrowseWindow(displayable)
        Browsing.exec_()
        results = Browsing.results()
        if results == QDialog.Accepted:
            # Get all values
            things = ""
            for thing in items:
                if thing[0].isChecked:
                    things += things[1] + ", "
            return things[:-2]
        else:
            return ''


class ChatTypeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        grid = QGridLayout()
        self.setLayout(grid)
        self.PUBLIC = QCheckBox("Public", self)
        self.PUBLIC.setChecked(True)
        self.PARTY = QCheckBox("Party", self)
        self.PARTY.setChecked(True)
        self.GUILD = QCheckBox("Team", self)
        self.GUILD.setChecked(True)
        self.WHISPER = QCheckBox("Whisper", self)
        self.WHISPER.setChecked(True)
        grid.addWidget(self.PUBLIC,  0, 0)
        grid.addWidget(self.PARTY,   1, 0)
        grid.addWidget(self.GUILD,   2, 0)
        grid.addWidget(self.WHISPER, 3, 0)
        self.setWindowTitle("Chat Options")

    def liquidate(self):
        return [("PUBLIC",self.PUBLIC.isChecked()), ("PARTY", self.PARTY.isChecked()), 
            ("GUILD", self.GUILD.isChecked()), ("REPLY", self.WHISPER.isChecked())]

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
        self.BeginUseCheck = QCheckBox("Use", self)
        self.EndUseCheck = QCheckBox("Use", self)
        grid.addWidget(self.BeginUseCheck, 4, 2)
        grid.addWidget(self.EndUseCheck,   5, 2)

        self.setWindowTitle("Chat Date Options")

    def getbegindate(self):
        self.begin_date = self.BigCalendar.selectedDate()
        return self.begin_date.toString("yyyy - MM - dd")

    def getenddate(self):
        self.end_date = self.BigCalendar.selectedDate()
        return self.end_date.toString("yyyy - MM - dd")

    def liquidate(self):
        items = []
        # yyyy-MM-ddThh:mm:ss
        if self.BeginUseCheck.isChecked():
            begin1 = self.begin_date.toString("yyyy-MM-dd") + "T00:00:00"
            begin2 = self.begin_date.toString("yyyy-MM-dd") + "T23:59:59"
            items.append([begin1, begin2])
        else:
            items.append(None)
        if self.EndUseCheck.isChecked():
            end1 = self.end_date.toString("yyyy-MM-dd") + "T00:00:00"
            end2 = self.end_date.toString("yyyy-MM-dd") + "T23:59:59"
            items.append([end1, end2])
        else:
            items.append(None)
        return items


class KeywordSearch(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        # Label and Field
        KeywordLabel = QLabel("Phrase:", self)
        self.KeywordField = QLineEdit(self)
        # Case Sensitive
        self.KeywordCheckbox = QCheckBox("Case Sensitive?", self)
        self.KeywordCheckbox.setChecked(True)
        # Clear Button
        # ClearButton = QPushButton("Clear Field", self)
        # ClearButton.clicked.connect(lambda:self.KeywordField.setText(""))
        # Word Or Sentence Search
        RadioLabel = QLabel("Search As A")
        RadioGroup = QButtonGroup(self)
        self.SentenceRadio = QRadioButton("Sentence", self)
        self.SentenceRadio.setChecked(True)
        self.WordRadio = QRadioButton("Collection Of Words", self)
        RadioGroup.addButton(self.WordRadio, 0)
        RadioGroup.addButton(self.SentenceRadio, 1)
        RadioHolder = QWidget()
        RadioHBox = QHBoxLayout()
        RadioHolder.setLayout(RadioHBox)
        RadioHBox.addWidget(self.SentenceRadio)
        RadioHBox.addWidget(self.WordRadio)
        grid.addWidget(KeywordLabel,    0, 0)
        grid.addWidget(self.KeywordField,    0, 1)
        # grid.addWidget(ClearButton,     0, 2)
        grid.addWidget(self.KeywordCheckbox, 0, 2)
        # grid.addWidget(self.SentenceRadio,       1, 1)
        # grid.addWidget(self.WordRadio,   1, 2)
        grid.addWidget(RadioHolder, 1, 1)
        self.setWindowTitle("Keyword Search Options")

    def liquidate(self):
        items = []
        if self.KeywordField.text() == "":
            return items
        else:
            if not self.KeywordCheckbox.isChecked():
                items.append("LOWER")
            else:
                items.append(None)
            if self.WordRadio.isChecked():
                fodder = []
                for item in re.split(" ", self.KeywordField.text()):
                    for combo in re.split(",", item):
                        if combo != "":
                            fodder.append(combo)
                items.append(fodder)
                return items
            else:
                items.append([self.KeywordField.text()])
                return items


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
        self.buttons["24hour"].setChecked(True)
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
        self.buttons["english"].setChecked(True)
        self.buttons["spanish"] = QRadioButton(u"Español")
        self.buttons["spanish"].setEnabled(False)
        self.languagegroup.addButton(self.buttons["english"], 0)
        self.languagegroup.addButton(self.buttons["spanish"], 1)
        ################### Putting it together ####################
        grid.addWidget(DBOptionLabel,                0, 0)
        grid.addWidget(self.buttons["sqlite3"],      0, 1)
        grid.addWidget(self.buttons["postgres"],     0, 2)

        grid.addWidget(TimeOptionLabel,              1, 0)
        grid.addWidget(self.buttons["12hour"],       1, 1)
        grid.addWidget(self.buttons["24hour"],       1, 2)

        grid.addWidget(LanguageOptionLabel,          2, 0)
        grid.addWidget(self.buttons["english"],      2, 1)
        grid.addWidget(self.buttons["spanish"],      2, 2)

        # Some scroll bar widget here someday
        self.setWindowTitle("Settings")

    def DBChange(self):
        # Throwup Long Custom Warning Message
        # If DB needs to be changed throw signal to main window
        pass

    def setDB(self, default):
        self.buttons[default].setChecked(True)

    def setTimeFormat(self, default):
        self.buttons[default].setChecked(True)

    def setLanguage(self, default):
        self.buttons[default].setChecked(True)

class Reader(QWidget):
    """This QWidget displays chat logs in a meaningful way. This 
    includes text coloring for different chat types, removing 
    other chat types with some check boxes, and the saving of 
    these filtered logs as their own text documents."""
    def __init__(self):
        super().__init__()


class Selector(QDialog):
    """This QWindow should take a list of tuples and allow the user to 
    select which things they would like to proceed with. When the Dialog 
    is closed it returns a list of indices that have checked and should 
    proceeded with."""
    def __init__(self, items):
        super().__init__()


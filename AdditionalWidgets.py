from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox, QCalendarWidget, QRadioButton, QButtonGroup, QDialog, QDialogButtonBox, QHBoxLayout, QGroupBox, QScrollArea, QTableView, QTreeView, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QVariant, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QBrush, QStandardItemModel, QStandardItem, QColor
from reader import too_many_tabs
import re

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
        self.FilterByCheckbox.setEnabled(False)
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

    def update(self):
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
        self.FilterByCheckbox.setEnabled(False)
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
        # Begin button and dat:
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
        RadioGroup.addButton(self.WordRadio,     0)
        RadioGroup.addButton(self.SentenceRadio, 1)
        RadioHolder = QWidget()
        RadioHBox = QHBoxLayout()
        RadioHolder.setLayout(RadioHBox)
        RadioHBox.addWidget(self.SentenceRadio)
        RadioHBox.addWidget(self.WordRadio)
        grid.addWidget(KeywordLabel,         0, 0)
        grid.addWidget(self.KeywordField,    0, 1)
        # grid.addWidget(ClearButton,        0, 2)
        grid.addWidget(self.KeywordCheckbox, 0, 2)
        # grid.addWidget(self.SentenceRadio, 1, 1)
        # grid.addWidget(self.WordRadio,     1, 2)
        grid.addWidget(RadioHolder,          1, 1)
        self.setWindowTitle("Keyword Search Options")

    def liquidate(self):
        items = []
        if self.KeywordField.text() == "":
            items.append(False)
            items.append([])
            return items
        else:
            #  if not self.KeywordCheckbox.isChecked():
                #  items.append("LOWER")
            #  else:
                #  items.append(None)
            items.append(self.KeywordCheckbox.isChecked())
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
        # 24 or 12 Hour Format
        self.timegroup = QButtonGroup(self)
        TimeOptionLabel = QLabel("Time Format")
        self.buttons["24hour"] = QRadioButton("24 Hour", self)
        self.buttons["24hour"].setChecked(True)
        self.buttons["12hour"]  = QRadioButton("12 Hour", self)
        self.timegroup.addButton(self.buttons["24hour"],  0)
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

    #  def setDB(self, default):
        #  self.buttons[default].setChecked(True)

    def setTimeFormat(self, default):
        self.buttons[default].setChecked(True)

    def setLanguage(self, default):
        self.buttons[default].setChecked(True)


class Reader(QWidget):
    """This QWidget displays chat logs in a meaningful way. This 
    includes text coloring for different chat types, removing 
    other chat types with some check boxes, and the saving of 
    these filtered logs as their own text documents.
    
    filenames is a complex structure that looks like
    [
        [filename1, [line numbers]],
        [filename2, [line numbers]]
    ]"""
    def __init__(self, filenames):
        super().__init__()
        hbox = QHBoxLayout(self)
        # All the files
        self.setLayout(hbox)
        # Set Other Window Params
        self.setWindowTitle("PSO2 Chat Reader")
        self.resize(900, 500)
        # Initial Table
        self.table = QTableView(self)
        self.headers = ["Time", "PID/SID", "Message"]
        # Data (list of  chatTypes, chatlines)
        #  data = self.digest(filenames[0][0])
        #  tablemodel = ChatTable(data, headers, self)
        #  self.table.setModel(tablemodel)

        # Table Details
        self.table.setWordWrap(True)

        vv = self.table.verticalHeader()
        vv.setVisible(False)

        self.table.setSortingEnabled(False)
        

        # The tree structure
        self.tree = QTreeView(self)
        self.tree.doubleClicked.connect(self.update_content)
        self.tree.setFixedWidth(300)

        # A text box containing the log title
        self.logTitle = QLabel("")

        #  self.new_tree(filenames)
        self.refresh(filenames)

        # Add Stuff
        hbox.addWidget(self.tree)
        fluff= QWidget(self)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.logTitle)
        vbox.addWidget(self.table)
        fluff.setLayout(vbox)
        hbox.addWidget(fluff)
        
        
        # Delete this
        #  self.tree.show()
        #  self.table.show()

    def generate_tree(self, allitems, parent):
        for oneFile in allitems:
            top_item = QStandardItem(oneFile[0])
            top_item.setEditable(False)
            parent.appendRow(top_item)
            for index, item in enumerate(oneFile[1]):
                if index < 10:
                    nested_item = QStandardItem(item)
                    nested_item.setEditable(False)
                    top_item.appendRow(nested_item)

    def new_tree(self, filenames):
        tree_model = QStandardItemModel()
        self.tree.setModel(tree_model)
        self.generate_tree(filenames, tree_model.invisibleRootItem())

    def update_content(self, index):
        # Get another
        item = self.tree.selectedIndexes()[0]
        result = item.model().itemFromIndex(index) # .text()
        while result.parent() is not None:
            result = result.parent()
        top = result.text()
        # Top is actually the proper name -> convert to short name
        top = self.ShortsNPropers[0][self.ShortsNPropers[1].index(top)]
        if "contents" not in self.alldata[top].keys():
            # Generate content
            self.alldata[top]["contents"] = self.digest(self.alldata[top]["long"])
            self.alldata[top]["table"] = ChatTable(self.alldata[top]["contents"], self.headers, self)
            self.table.setModel(self.alldata[top]["table"])
            self.logTitle.setText(top)
        else:
            self.table.setModel(self.alldata[top]["table"])
            self.logTitle.setText(top)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(True)
        #  if "chatlog" in result and ".txt"

    def refresh(self, filenames):
        """
        
        alldata = {

            chatlog: { 
                long: C://chatlot
                lines = [lines of chat]
                contents = [list of strings]
                table = ChatTable()
            }
        
        }"""
        self.alldata = {}
        for item in filenames:
            #  self.alldata[item[0][-item[0][::-1].index("/"):]] = {"long": item[0], "lines": item[1]}
            # The real filename
            filename = item[0][-item[0][::-1].index("/"):]
            
            self.alldata[filename] = {"long": item[0], "lines": item[1], "proper": pretty_date(filename)}
        # Pick first item for the view
        keyz = sorted(self.alldata.keys())
        firstkey = keyz[0]
        self.alldata[firstkey]["contents"] = self.digest(self.alldata[firstkey]["long"])
        self.alldata[firstkey]["table"] = ChatTable(self.alldata[firstkey]["contents"], self.headers, self)
        self.table.setModel(self.alldata[firstkey]["table"])
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(True)
        
        # Edit Text Box
        self.logTitle.setText(firstkey)
        # Generate a Tree
        # Gather the lines
        lines = list(map(lambda x: self.alldata[x]["lines"], keyz))
        # Format
        propers = list(map(lambda short: self.alldata[short]["proper"], keyz))
        self.ShortsNPropers = []
        self.ShortsNPropers.append(keyz)
        self.ShortsNPropers.append(propers)
        self.new_tree(list(zip(propers, lines)))
        self.show()

        

    def digest(self, current_file):
        """Takes a chat file and dumps out a list of lists"""
        data = []
        chat_type_data= []
        with open(current_file, "r", encoding="utf16") as cur:
            allText = cur.read()
        # Split file
        split_file = allText.split("\n")
        count = 0
        line_numbers = []
        # Console.WriteLine(current_file);
        for line in split_file:
            # Increment line number
            count += 1
            # Split the line
            split_line = line.split("\t")

            # Possibly empty?
            if len(split_line) == 0: 
                # Console.WriteLine("Line {0}: Split line is empty? Skipping!", count);
                continue;
            # Too many tabs
            if len(split_line) > 6:
                # Console.WriteLine("\tLength > 6!");
                # Console.WriteLine(split_line);
                split_line = too_many_tabs(split_line)

            keep = split_line
            # Victim of a bad newline
            if len(split_line) < 6:
                # Need to find the line that fits!
                tracking_index = count - 1
                keep = [];
                while True:
                    tracking_index -= 1
                    keep = split_file[tracking_index].split("\t")
                    if len(keep) == 6:
                        break
                #  } while (keep.Length < 6) ;
                # Console.WriteLine("\tKeeping:   {0}", String.Join(", ", keep));
                #  for (int i = tracking_index + 1; i <= count - 1; i++) {
                i = tracking_index + 1
                while i <= count - 1:
                    keep[5] += "\n" + split_file[i]
                    i += 1
                # Console.WriteLine("\tFinalized: {0}", String.Join(", ", keep));
            # Time, ChatType, PID\nSID, Message
            split_line = []
            split_line.append(keep[0][keep[0].index("T") + 1:])
            # Chat Type
            #  split_line.append(keep[2])
            chat_type_data.append(keep[2])
            split_line.append("{}\n{}".format(keep[4], keep[3]))
            split_line.append(keep[-1])
            data.append(split_line)

        print("File ({}) read succesfully! {} Lines!".format(current_file, len(data)))
        return chat_type_data, data


class ChatTable(QAbstractTableModel):
    """"""
    def __init__(self, data, headers, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.headerdata = headers
        self.arraydata = data[1]
        self.chat_type_data = data[0]

    def rowCount(self, parent):
        if self.data is not None:
            return len(self.arraydata)
        return 0

    def columnCount(self, parent):
        if self.rowCount(parent) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.BackgroundRole:
            # Begin Coloring?
            if self.chat_type_data[index.row()] == "PUBLIC":
                return QBrush(Qt.lightGray)
            elif self.chat_type_data[index.row()] == "PARTY":
                return QBrush(Qt.cyan)
            elif self.chat_type_data[index.row()] == "GUILD":
                #  return QBrush(Qt.darkYellow)
                return QBrush(QColor(230,157,36))
            elif self.chat_type_data[index.row()] == "REPLY":
                return QBrush(Qt.magenta)
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[section])
        return QVariant()


def rip_filename(filename):
    #  return [filename[0][-filename[0][::-1].index("/"):], filename[1]]
    return filename[0][-filename[0][::-1].index("/"):]

def pretty_date(filename):
    months = {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec"
            }
    start = filename.index("20")
    short = months[int(filename[start + 4:start + 6])]
    # Day Portion of the date
    day = filename[start + 6: start + 8]
    if day[-1] == "1":
        day = " {}st, ".format(int(day))
    elif day[-1] == "2":
        day = " {}nd, ".format(int(day))
    elif day[-1] == "3":
        day = " {}rd, ".format(int(day))
    else:
        day = " {}th, ".format(int(day))
    short += day + filename[start:start + 4]
    return short

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    # This is for testing the reader Widget
    app = QApplication(sys.argv)
    obj = Reader(sys.argv[1])
    sys.exit(app.exec_())

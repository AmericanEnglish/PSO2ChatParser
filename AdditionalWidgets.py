from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox
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


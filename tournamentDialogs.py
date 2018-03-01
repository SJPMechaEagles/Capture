from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
import operator
from datasource import create_test_tournament, current_tournament
import datasource
from datasource import *
from datasource import Match
import re

class ManualMatchesDialog(QDialog):
    def __init__(self, parent=None):
        super(ManualMatchesDialog, self).__init__(parent)
        self.result = ""
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.tableView = VexMatchesTable()
        self.initTableView(self.tableView)
        layout.addWidget(self.tableView)

        self.newRowButton = QPushButton()
        self.newRowButton.setText("New Match")
        self.newRowButton.clicked.connect(self.addRow)

        bottomLayout = QVBoxLayout()
        bottomLayout.addWidget(self.newRowButton)

        buttonsLayout = QHBoxLayout()
        self.buttonOK = QPushButton()
        self.buttonOK.setText("OK")
        self.buttonOK.clicked.connect(self.saveData)
        self.buttonCancel = QPushButton()
        self.buttonCancel.setText("Cancel")
        self.buttonCancel.clicked.connect(self.onQuit)
        buttonsLayout.addWidget(self.buttonOK)
        buttonsLayout.addWidget(self.buttonCancel)

        bottomLayout.setContentsMargins(0,0,0,0)

        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout.addLayout(buttonsLayout)
        layout.addLayout(bottomLayout)
        
        self.setLayout(layout)
        self.setWindowTitle("Match Editor")

    def addRow(self):
        self.tableView.addEmptyMatch()

    def onQuit(self):
        self.close()
    
    # parse and save the table to a file
    def saveData(self):
        self.close()
        
    def getMatches(self):
        pass
        
    def initTableView(self, tableView):
        tableView.setMinimumSize(720, 500)

class TournamentViewModel(QAbstractTableModel):
    tournament = None
    def __init__(self, *args, tournament):
        QAbstractTableModel.__init__(self, *args)
        self.tournament = tournament

    def setHeaderData(self, index, orientation, role=Qt.DisplayRole):
        print(index)
        if role == Qt.DisplayRole:
            return str(index)
        return QAbstractTableModel.headerData(self, index, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.tournament.matches)
    
    def columnCount(self, parent=None, *args, **kwargs):
        return 7

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            if col == 0:
                match = self.tournament.matches[row]
                return match.toId()
            if col == 1:
                return str(self.tournament.matches[row].red1)
            if col == 2:
                return str(self.tournament.matches[row].red2)
            if col == 3:
                return str(self.tournament.matches[row].red3)
            if col == 4:
                return str(self.tournament.matches[row].blue1)
            if col is 5:
                return str(self.tournament.matches[row].blue2)
            if col == 6:
                return str(self.tournament.matches[row].blue3)
        elif role is Qt. FontRole:
            print("font")
            if col is 0:
                return QFont().setBold(True)
        elif role is Qt.BackgroundRole:
            print("Background")
            if row % 2 is 0:
                return Qt.white
            else:
                return Qt.gray
        elif role is Qt.TextAlignmentRole:
            return Qt.AlignCenter + Qt.AlignVCenter
        elif role is Qt.CheckStateRole:
            return QVariant
        return QVariant()

    def headerData(self, selection, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if selection is 0:
                    return "Match Number"
                if selection is 1:
                    return "Red 1"
                if selection is 2:
                    return "Red 2"
                if selection is 3:
                    return "Red 3"
                if selection is 4:
                    return "Blue 1"
                if selection is 5:
                    return "Blue 2"
                if selection is 6:
                    return "Blue 3"
        return QVariant()

    def setData(self, index, value, role=Qt.DisplayRole):
        if(not self.isValidTeamNumber(value)):
            return False
        value = value.upper()
        value = str(value).upper()
        if(index.column()== 0):
            self.tournament.matches[index.row()].num = value
        if (index.column() == 1):
            self.tournament.matches[index.row()].red1 = value
        if (index.column() == 2):
            self.tournament.matches[index.row()].red2 = value
        if (index.column() == 3):
            self.tournament.matches[index.row()].red3 = value
        if (index.column() == 4):
            self.tournament.matches[index.row()].blue1 = value
        if (index.column() == 5):
            self.tournament.matches[index.row()].blue2 = value
        if (index.column() == 6):
            self.tournament.matches[index.row()].blue3 = value

        self.dataChanged.emit(index,index, [Qt.EditRole])
        return True
    def flags(self, index):
        return (Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    
    def editComplete(self):
        pass
    
    def isValidTeamNumber(self, number):
        pattern = re.compile('^[1-9]{1,6}[A-Z]?$')
        return pattern.match(str(number).upper())

class VexMatchesTable(QTableView):
    def __init__(self, *args, data=None):
        QTableView.__init__(self, *args)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.tournamentModel = TournamentViewModel(tournament=datasource.current_tournament)
        self.setModel(self.tournamentModel)
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
    
    def addEmptyMatch(self):
        newIndex = len(datasource.current_tournament.matches)
        global current_tournament
        current_tournament.add_match(0, '', '', '', '')
        # reload model
        self.tournamentModel = TournamentViewModel(tournament=datasource.current_tournament)
        self.setModel(self.tournamentModel)
        # refresh the model
        self.selectRow(newIndex)
        self.scrollToBottom()

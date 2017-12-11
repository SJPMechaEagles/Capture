from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
import operator

class ManualMatchesDialog(QDialog):
    def __init__(self, parent=None):
        super(ManualMatchesDialog, self).__init__(parent)
        self.result = ""
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        #self.tableView = QTableView()
        # self.initTable(self.tableView)
        self.tableWidget = VexMatchesTable()
        self.initTableWidget(self.tableWidget)
        layout.addWidget(self.tableWidget)
        
        buttonsLayout = QHBoxLayout()
        self.buttonOK = QPushButton()
        self.buttonOK.setText("OK")
        self.buttonCancel = QPushButton()
        self.buttonCancel.setText("Cancel")
        buttonsLayout.addWidget(self.buttonOK)
        buttonsLayout.addWidget(self.buttonCancel)
        buttonsLayout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttonsLayout)
        
        self.setLayout(layout)
        # self.addWidget(self.tableView)
    
    def onQuit(self):
        self.close()
        
    def getMatches(self):
        pass
        
    def initTableWidget(self, tableWidget):
    	tableWidget.setMinimumSize(505, 600)

class VexMatchesTable(QTableWidget):
    def __init__(self, *args, data=None):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(25);
        self.horizontalHeader().setStretchLastSection(True)
        self.setColumnCount(5)
        self.setRowCount(250)
        headerLabels = ['Match #', 'Red 1', 'Red 2', 'Blue 1', 'Blue 2']
        self.setHorizontalHeaderLabels(headerLabels)
        self.setSortingEnabled(True)
        # self.setData()
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
 
    # initializes the table with a list of (team name red 1, team name red 2, ...)
    def loadData(self, teams):
        pass

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
        self.tableView = QTableView()
        self.initTable(self.tableView)
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        # self.addWidget(self.tableView)
    
    def onQuit(self):
        self.close()
        
    def getMatches(self):
        pass
        
    def initTable(self, tableView):
        self.tableData = [['Q1', '9228A', '9228B', '9228C', '9228D']]
        header = ['Match #', 'Red 1', 'Red 2', 'Blue 1', 'Blue 2']
        tableModel = VexMatchModel(self.tableData, header, self) 
        tableView.setModel(tableModel)
        tableView.setMinimumSize(500, 250)
        
        # hide vertical header
        vh = tableView.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tableView.horizontalHeader()
        hh.setStretchLastSection(True)
        
        # set column width to fit contents
        tableView.resizeColumnsToContents()
        
        # set row height
        nrows = len(self.tableData)
        for row in range(nrows):
            tableView.setRowHeight(row, 18)
            
        # enable sorting
        tableView.setSortingEnabled(True)
        tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        
class VexMatchModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        # self.emit(SIGNAL("layoutChanged()"))

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from .data import *

class NewTournament(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'New Tournament'
        tourns = get_tournaments(None, None, None, None, None)
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.show()

class FileChoser(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def openFileNameDialog(self):
        path = None
        while path is None:
            options = QFileDialog.Options()
            path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Vex Reocrder Manifest Files (.vman)", options=options)
        return path

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 menu - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        configureMenu = mainMenu.addMenu('Configure')

        loadButton = QAction('Load Manifest', self)
        loadButton.setShortcut('Ctrl+L')
        loadButton.setStatusTip('Load a Manifest File')
        loadButton.triggered.connect(self.load)

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        newTournamentButton = QAction('New Tournament', self)
        newTournamentButton.triggered.connect(self.newTournament)

        fileMenu.addAction(exitButton)
        fileMenu.addAction(loadButton)
        configureMenu.addAction(newTournamentButton)
        mainMenu.setNativeMenuBar(True)

        self.show()

    def load(self):
        csr = FileChoser()
        file = csr.openFileNameDialog()

    def save(self):
        print("save")

    def newTournament(self):
        NewTournament()
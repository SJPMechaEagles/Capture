from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datasource import Tournament
import recordButton
import infoDisplay
from tournamentDialogs import ManualMatchesDialog

import camera

class ConfigurationWindow(QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        

class VideoWindow(QMainWindow):
    def createMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        exitAction = QAction('&File', self)
        exitAction.triggered.connect(VideoWindow.file)
        fileMenu.addAction(exitAction)

        tournamentMenu = menubar.addMenu('&Tournament')
        tournamentAction = QAction('&Tournament', self)
        tournamentAction.triggered.connect(VideoWindow.configure)
        tournamentMenu.addAction(tournamentAction)

    def file(self):
        print("file")

    def configure(self):
        print("loading tournament")
        dialog = ManualMatchesDialog();
        returnCode=dialog.exec_()
        print(returnCode)
        # tourn = Tournament("test")
        # tourn.pull_from_db()

    def toggleRecording(self):
        if (self.isRecording):
            self.stopRecording()
        else:
            self.startRecording()
        # update the window title and status bar
        self.updateStatusDisplay()

    def startRecording(self):
        self.isRecording = True
        self.camera.startRecording()
        self.recordButton.updateStyle(self.isRecording)
        

    def stopRecording(self):
        self.isRecording = False
        self.camera.stopRecording()
        self.recordButton.updateStyle(self.isRecording)

    def onQuit(self):
        self.stopRecording()
        self.close()

    def matchSelected(self, match_number):
        self.match_number = match_number
        # update the window title and status bar
        self.updateStatusDisplay()
        
    def updateStatusDisplay(self):
        self.updateWindowTitle(match_number=self.match_number, teams=['9228A', '9228B', '9228C', '9228D'])
        self.infoDisplay.updateInfo(self.match_number, ['9228A', '9228B', '9228C', '9228D'], self.isRecording)

    def updateWindowTitle(self, match_number=None, teams=None):
        if (match_number == None or teams == None):
            # initialization
            self.setWindowTitle('VEX Match Recorder - [No Match Selected]')
        else:
            if (self.isRecording):
                title = 'VEX Match Recorder - Match ' + match_number + " Teams "
            else:
                title = 'VEX Match Recorder - Match ' + match_number + " Teams "
            # add the teams to the title
            for team in teams:
                title += str(team) + " "
            self.setWindowTitle(title)

    def __init__(self, camera, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.createMenu()
        self.camera = camera
        # quit on alt+f4 or ctrl+w
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)
        # by default, camera recording is off
        self.isRecording = False
        self.match_number = None
        # Create a widget for window contents
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
		
		# create the top information display row
        self.infoDisplay = infoDisplay.InfoDisplay()
		
        # create the bottom control layout with buttons
        self.recordButton = recordButton.RecordButton()
        self.recordButton.clicked.connect(self.toggleRecording)
        self.comboBox = QComboBox()
        self.comboBox.addItem("1")
        self.comboBox.addItem("2")
        self.comboBox.addItem("3")
        self.comboBox.addItem("4")
        self.comboBox.activated[str].connect(self.matchSelected)
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.comboBox)
        controlLayout.addWidget(self.recordButton)

        # create the mainlayout that contains the viewfiner and controls
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.infoDisplay)
        mainLayout.addWidget(self.camera.getViewFinder())
        mainLayout.addLayout(controlLayout)

        # apply the mainlayout
        centralWidget.setLayout(mainLayout)
        self.updateWindowTitle()

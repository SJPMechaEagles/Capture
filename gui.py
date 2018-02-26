from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datasource import get_current_tournament
import recordButton
import infoDisplay
from tournamentDialogs import ManualMatchesDialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from newTournamentWidget import *


from datasource import Tournament, load_from_file
import camera

class ConfigurationWindow(QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        

vWindow = None

class VideoWindow(QMainWindow):
    id = 0
    match_recording = None

    def createMenu(self):
        global vWindow
        vWindow= self
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')

        newAction = QAction('&New', self)
        newAction.triggered.connect(VideoWindow.new_tournament)
        fileMenu.addAction(newAction)

        openAction = QAction('&Open', self)
        openAction.triggered.connect(VideoWindow.open)
        fileMenu.addAction(openAction)

        saveAction = QAction('&Save', self)
        saveAction.triggered.connect(VideoWindow.save)
        fileMenu.addAction(saveAction)

        tournamentMenu = menubar.addMenu('&Tournament')

        tournamentEditAction = QAction('&Edit Matches', self)
        tournamentEditAction.setShortcut("Ctrl+M")
        tournamentEditAction.triggered.connect(self.configure)
        tournamentMenu.addAction(tournamentEditAction)

        tournamentPullAction = QAction('&Update Schedule', self)
        tournamentPullAction.setShortcut("Ctrl+U")
        tournamentPullAction.triggered.connect(self.updatepull)
        tournamentMenu.addAction(tournamentPullAction)

    def reload(self):
        self.update()
        self.reload_combo()
        self.updateStatusDisplay()
        self.updateWindowTitle()
        if get_current_tournament() is not None:
            self.recordButton.setEnabled(True)
        else:
            self.recordButton.setEnabled(False)

    def new_tournament(self):
        t = NewTournamentWidget()
        if t.exec() is 1:
            global vWindow
            vWindow.reload()


    def reload_combo(self):
        for i in range(0, self.comboBox.count()):
            self.comboBox.removeItem(i)
        current_tournament = get_current_tournament()
        print(current_tournament)
        if current_tournament is not None:
            for match in current_tournament.matches:
                self.comboBox.addItem(match.toId())
            self.id = 0
            self.match_recording = None
            self.comboBox.activated.connect(self.matchSelected)

    def save(self):
        if get_current_tournament() is None:
            print("Tournament None")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name,path = QFileDialog.getSaveFileName(None, None, "Save Tournament", None, "Tournament File (*.Tournament)", options=options)
        print(name, path)
        get_current_tournament().save(name)

    def updatepull(self):
        if get_current_tournament() is not None:
            get_current_tournament().update_match_data()
            self.reload()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "",  filter="Tournament File (*.Tournament)", options=options)
        if fileName:
            print(fileName)
            load_from_file(fileName)
            global vWindow
            vWindow.reload_combo()


    def configure(self):
        print("loading tournament")
        dialog = ManualMatchesDialog();
        returnCode=dialog.exec_()
        print(returnCode)

    def toggleRecording(self):
        if get_current_tournament() is None:
            print("Tournament None")
            return

        if (self.isRecording):
            self.stopRecording()
        else:
            self.startRecording()
        # update the window title and status bar
        self.updateStatusDisplay()

    def startRecording(self):
        if get_current_tournament() is None:
            print("Tournament None")
            return
        self.match_recording = get_current_tournament().matches[self.comboBox.currentIndex()]
        self.isRecording = True
        filename = self.match_recording.create_file_name()
        self.camera.startRecording(filename)
        self.match_recording.videos.append(self.match_recording.create_file_name())
        self.recordButton.updateStyle(self.isRecording)
        self.id = self.comboBox.currentIndex()

    def stopRecording(self):
        if get_current_tournament() is None:
            print("Tournament None")
            return
        self.isRecording = False
        self.camera.stopRecording()
        self.recordButton.updateStyle(self.isRecording)
        self.id+=1
        self.comboBox.setCurrentIndex(self.id)
        self.match_recording = None

    def onQuit(self):
        self.stopRecording()
        get_current_tournament().save()
        self.close()

    def matchSelected(self):
        self.match_number = self.comboBox.currentIndex()
        # update the window title and status bar
        self.updateStatusDisplay()
        
    def updateStatusDisplay(self):
        teams = ['','','','']
        if get_current_tournament() is not None and self.match_number is not None:
            if self.match_number is None:
                self.match_number = 0
            r1 = get_current_tournament().matches[self.match_number].red1
            r2 = get_current_tournament().matches[self.match_number].red2
            b1 = get_current_tournament().matches[self.match_number].blue1
            b2 = get_current_tournament().matches[self.match_number].blue2
            teams = [r1, r2, b1, b2]
        self.updateWindowTitle(match_number=self.match_number, teams=teams)
        self.infoDisplay.updateInfo(self.match_number, teams, self.isRecording)

    def updateWindowTitle(self, match_number=None, teams=None):
        if get_current_tournament() is None:
            self.setWindowTitle('VEX Match Recorder - [No Tournament Selected]')
            return
        if (match_number == None or teams == None):
            # initialization
            self.setWindowTitle('VEX Match Recorder - [No Match Selected]')
        else:
            if (self.isRecording):
                title = 'VEX Match Recorder - Match ' + match_number_to_string(match_number) + " Teams "
            else:
                title = 'VEX Match Recorder - Match ' + match_number_to_string(match_number) + " Teams "
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
        current_tournament = get_current_tournament()
        if current_tournament is not None:
            for match in current_tournament.matches:
                self.comboBox.addItem(match.toId())
            self.comboBox.activated.connect(self.matchSelected)
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

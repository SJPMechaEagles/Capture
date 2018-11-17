from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datasource import get_current_tournament
import recordButton
import infoDisplay
from tournamentDialogs import ManualMatchesDialog
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from newTournamentWidget import *
from matchesView import *

import os

from datasource import load_from_file
import camera

vWindow = None

def reload_gui():
    vWindow.reload()

class ConfigurationWindow(QMainWindow):
    def __init__(self):
        super(ConfigurationWindow, self).__init__()
        


class VideoWindow(QMainWindow):
    id = 0
    match_recording = None

    def createMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')

        newAction = QAction('&New', self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.new_tournament)
        fileMenu.addAction(newAction)

        openAction = QAction('&Open', self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.open)
        fileMenu.addAction(openAction)

        saveAction = QAction('&Save', self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.save)
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

        viewMatchesAction = QAction('&View Matches', self)
        viewMatchesAction.setShortcut("Ctrl+V")
        viewMatchesAction.triggered.connect(self.viewMatches)
        tournamentMenu.addAction(viewMatchesAction)

    def viewMatches(self):
        m = RecordedViewMatchDialog()
        if m.exec() is 1:
            self.reload()

    def reload(self):
        self.update()
        self.reload_combo()
        self.updateStatusDisplay()
        self.updateWindowTitle()

    def new_tournament(self):
        t = NewTournamentWidget()
        if t.exec() is 1:
            self.reload()


    def reload_combo(self):
        self.comboBox.clear()
        current_tournament = get_current_tournament()
        print(current_tournament)
        if current_tournament is not None:
            for match in current_tournament.matches:
                self.comboBox.addItem(match.toInfoString())
            self.id = 0
            self.match_recording = None
            self.comboBox.activated.connect(self.matchSelected)
        self.updateStatusDisplay()

    def save(self):
        if get_current_tournament() is None:
            print("Tournament None")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name,path = QFileDialog.getSaveFileName(self, "Save Tournament", filter="Tournament File (*.Tournament)", options=options)
        
        if (path != ""):
            get_current_tournament().save(name)
        self.updateStatusDisplay()

    def updatepull(self):
        if get_current_tournament() is not None:
            get_current_tournament().update_match_data()
            self.reload()
        self.updateStatusDisplay()

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "",  filter="Tournament File (*.Tournament)", options=options)
        if fileName:
            print(fileName)
            load_from_file(fileName)
            self.reload_combo()
            self.remember_default(str(fileName))
        self.updateStatusDisplay()


    def configure(self):
        print("loading tournament")
        dialog = ManualMatchesDialog();
        returnCode=dialog.exec_()
        print(returnCode)
        self.updateStatusDisplay()

    def toggleRecording(self):
        if get_current_tournament() is None:
            return

        if (self.isRecording):
            self.stopRecording()
        else:
            self.startRecording()
        # update the window title and status bar
        self.updateStatusDisplay()

    def startRecording(self):
        self.updateStatusDisplay()
        if get_current_tournament() is None:
            print("Tournament None!")
            return
        self.match_recording = get_current_tournament().matches[self.comboBox.currentIndex()]
        self.isRecording = True
        filename = self.match_recording.create_file_name()
        self.camera.startRecording("videos/" + filename)
        get_current_tournament().matches[self.comboBox.currentIndex()]\
            .videos.append(filename)
        self.recordButton.updateStyle(self.isRecording)
        self.id = self.comboBox.currentIndex()
        self.updateStatusDisplay()

    def stopRecording(self):
        self.updateStatusDisplay()
        if get_current_tournament() is None:
            print("Tournament None")
            return
        self.isRecording = False
        self.camera.stopRecording()
        self.recordButton.updateStyle(self.isRecording)
        self.id+=1
        get_current_tournament().save()
        self.comboBox.setCurrentIndex(self.id)
        self.match_recording = None
        self.updateStatusDisplay()

    def onQuit(self):
        print("quit")
        self.stopRecording()
        self.save()
        self.close()

    def matchSelected(self):
        self.match_number = self.comboBox.currentIndex()
        # update the window title and status bar
        self.updateStatusDisplay()
        
    def updateStatusDisplay(self):
        teams = ['','','','']
        if get_current_tournament() is not None:
            r1 = get_current_tournament().matches[self.comboBox.currentIndex()].red1
            r2 = get_current_tournament().matches[self.comboBox.currentIndex()].red2
            b1 = get_current_tournament().matches[self.comboBox.currentIndex()].blue1
            b2 = get_current_tournament().matches[self.comboBox.currentIndex()].blue2
            teams = [r1, r2, b1, b2]
            print(teams)
            self.updateWindowTitle(match_number=get_current_tournament().
                               matches[self.comboBox.currentIndex()].toId(), teams=teams)
            self.infoDisplay.updateInfo(get_current_tournament().matches[self.comboBox.currentIndex()].toId(), teams, self.isRecording)

    def updateWindowTitle(self, match_number=None, teams=None):
        if get_current_tournament() is None:
            self.setWindowTitle('VEX Match Recorder - [No Tournament Selected]')
            return
        if (match_number == None or teams == None):
            # initialization
            self.setWindowTitle('VEX Match Recorder - [No Match Selected]')
        else:
            if (self.isRecording):
                title = 'VEX Match Recorder - Match ' + (match_number) + " Teams "
            else:
                title = 'VEX Match Recorder - Match ' + (match_number) + " Teams "
            # add the teams to the title
            for team in teams:
                title += str(team) + " "
            self.setWindowTitle(title)

    def closeEvent(self, QCloseEvent):
        self.onQuit()

    def __init__(self, camera, parent=None):
        super(VideoWindow, self).__init__(parent)
        global vWindow
        vWindow = self
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
                self.comboBox.addItem(match.toInfoString())
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

        #load default tournament file
        self.load_default()

        self.recordButton.updateStyle(False)
        self.updateStatusDisplay()

    # loads the default touranment file
    def load_default(self):
        try:
            file = open("defaults.cfg", "r")
        except:
            return # file not fuond
        fileName = file.read()
        if fileName:
            print("loading default: " + fileName)
            try:
                load_from_file(fileName)
                self.reload_combo()
            except:
                print("Failed to load default tournament file!")
        self.updateStatusDisplay()

    def remember_default(self, filename):
        file = open("defaults.cfg", "w")
        file.write(filename)
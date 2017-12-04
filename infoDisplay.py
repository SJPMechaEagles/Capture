from PyQt5.QtWidgets import QHBoxLayout, QLabel, QStyle, QLayout, QSizePolicy
import PyQt5.QtCore

class InfoDisplay(QHBoxLayout):
    def __init__(self, parent= None):
        super(InfoDisplay,self).__init__(parent)
        self.teamsLabel = QLabel()
        self.teamsLabel.setText("[No Teams Selected]")
        self.teamsLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,0.3); color : white; }")
        # set the label width to the width of contained text
        self.teamsLabel.setMaximumWidth(self.teamsLabel.fontMetrics().width(self.teamsLabel.text()))
        # self.teamsLabel.setAlignment(PyQt5.QtCore.Qt.AlignLeft)
        self.addWidget(self.teamsLabel)
        
        self.recordingLabel = QLabel()
        self.recordingLabel.setText("[Not Recording]")
        self.recordingLabel.setStyleSheet("QLabel { background-color : rgba(0,0,0,0.3); color : white; }")
        # set the label width to the width of contained text
        self.recordingLabel.setMaximumWidth(self.recordingLabel.fontMetrics().width(self.recordingLabel.text()))
        self.addWidget(self.recordingLabel)

    def updateInfo(self, match_number, teams, isRecording):
        # the string looks like: Q5: 9228A 9228B ...
        teamsString = match_number + ":"
        for team in teams:
            teamsString += " " + team
        self.teamsLabel.setText(teamsString)
        
        if (isRecording):
            self.recordingLabel.setText("[Recording]")
        else:
            self.recordingLabel.setText("[Not Recording]")

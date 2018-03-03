from PyQt5.QtWidgets import QPushButton, QStyle
from datasource import get_current_tournament

class RecordButton(QPushButton):
    def __init__(self, parent= None):
        super(RecordButton,self).__init__(parent)
        self.isRecording = False
        self.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))
        self.setStyleSheet('QPushButton {background-color: #26c6da}')
        # self.setDisabled(False)

    def updateStyle(self, isRecording):
        self.isRecording = isRecording
        if get_current_tournament() is not None:
            self.setEnabled(True)
        else:
            self.setEnabled(False)

        if (isRecording):
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            # recording color: red
            self.setStyleSheet('QPushButton {background-color: #e57373}')
        else:
            self.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))
            # non-recording color: cyan
            self.setStyleSheet('QPushButton {background-color: #26c6da}')

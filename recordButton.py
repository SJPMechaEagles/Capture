from PyQt5.QtWidgets import QPushButton, QStyle

class RecordButton(QPushButton):
    def __init__(self, parent= None):
        super(RecordButton,self).__init__(parent)
        self.isRecording = False
        self.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))
        self.setStyleSheet('QPushButton {background-color: #26c6da}')
        # self.setDisabled(False)

    def updateStyle(self, isRecording):
        self.isRecording = isRecording
        if (isRecording):
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            # recording color: red
            self.setStyleSheet('QPushButton {background-color: #e57373}')
        else:
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            # non-recording color: cyan
            self.setStyleSheet('QPushButton {background-color: #26c6da}')

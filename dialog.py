from PyQt5.QtWidgets import QDialog, QLabel,QComboBox

import sys

class SelectTournamentDialog(QDialog):
    def __init__(self):
        super(SelectTournamentDialog, self).__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel("Slect Tournament")

        combo = QComboBox(self)
        combo.addItem("Test 1")
        combo.addItem("Test 2")
        combo.addItem("Test 3")

        combo.move(50,50)

        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300,300,300,300)
        self.setWindowTitle("Select Tournament")
        self.show()

        print("Test2")

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
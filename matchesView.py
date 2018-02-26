import PyQt5.Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MatchesViewModel(QAbstractTableModel):
    def __init__(self, *args):
        QAbstractTableModel.__init__(self, *args)

    def data(self, QModelIndex, role):
        pass

class MatchesViewDialog(QDialog, parent=None):
    def __init__(self):
        super(MatchesViewDialog, self).__init__(parent=None)
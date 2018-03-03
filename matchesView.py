from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import operator
from datasource import create_test_tournament, current_tournament
import datasource
from datasource import *
from datasource import Match
import re
import os
import string

videos = []

class RecordedViewMatchDialog(QDialog):
    def __init__(self, parent=None):
        super(RecordedViewMatchDialog, self).__init__(parent)
        self.result = ""
        self.shortcut = QShortcut(QKeySequence.Close, self)
        self.shortcut.activated.connect(self.onQuit)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tableView = RecordedMatchesTable()
        self.initTableView(self.tableView)
        layout.addWidget(self.tableView)

        self.setLayout(layout)
        self.setWindowTitle("Recorded Matches")

    def onQuit(self):
        self.close()

    def initTableView(self, tableView):
        tableView.setMinimumSize(900, 500)

class RecordedMatchesViewModel(QAbstractTableModel):

    def __init__(self, *args, tournament):
        QAbstractTableModel.__init__(self, *args)
        self.tournament = get_current_tournament()
        global videos
        videos = self.getVideos()


    def setHeaderData(self, index, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(index)
        return QAbstractTableModel.headerData(self, index, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        global videos
        return len(videos)

    def getVideos(self):
        print("Videos")
        videos_array = []
        for match in get_current_tournament().matches:
            print(match.videos)
            for video in match.videos:
                video_tuple = (video, match)
                videos_array.append(video_tuple)

        return videos_array


    def columnCount(self, parent=None, *args, **kwargs):
        return 9

    def data(self, index, role=Qt.DisplayRole):
        global videos
        row = index.row()
        col = index.column()
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            if col == 0:
                return str(videos[index.row()][1].toId())
            if col == 1:
                return str(videos[index.row()][1].red1)
            if col == 2:
                return str(videos[index.row()][1].red2)
            if col == 3:
                return str(videos[index.row()][1].red3)
            if col == 4:
                return str(videos[index.row()][1].blue1)
            if col is 5:
                return str(videos[index.row()][1].blue2)
            if col == 6:
                return str(videos[index.row()][1].blue3)
            if col == 7:
                return str(videos[index.row()][0])
            if col == 8:
                return "Watch"

        elif role is Qt.FontRole:
            print("font")
            if col is 0:
                return QFont().setBold(True)
        elif role is Qt.BackgroundRole:
            print("Background")
            if row % 2 is 0:
                return Qt.white
            else:
                return Qt.gray
        elif role is Qt.TextAlignmentRole:
            return Qt.AlignCenter + Qt.AlignVCenter
        elif role is Qt.CheckStateRole:
            return QVariant
        return QVariant()

    def headerData(self, selection, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if selection is 0:
                    return "Match Number"
                if selection is 1:
                    return "Red 1"
                if selection is 2:
                    return "Red 2"
                if selection is 3:
                    return "Red 3"
                if selection is 4:
                    return "Blue 1"
                if selection is 5:
                    return "Blue 2"
                if selection is 6:
                    return "Blue 3"
                if selection is 7:
                    return "Filename"
                if selection is 8:
                    return "Watch Now"
        return QVariant()

    def flags(self, index):
        return (Qt.ItemIsEnabled | Qt.ItemIsSelectable)


class RecordedMatchesTable(QTableView):
    def __init__(self, *args, data=None):
        QTableView.__init__(self, *args)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.tournamentModel = RecordedMatchesViewModel(tournament=datasource.current_tournament)
        self.setModel(self.tournamentModel)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setItemDelegateForColumn(8, WatchPushButtonDelegate(self))

class WatchPushButtonDelegate(QItemDelegate):
    def __init__(self, parent):
        # The parent is not an optional argument for the delegate as
        # we need to reference it in the paint method (see below)
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            #TODO implement player
            self.parent().setIndexWidget(index,QPushButton(index.data(),self.parent(),clicked=
                lambda x: self.play_video(index)
            ))

    def play_video(self, index):
        global videos
        filename = videos[index.row()][0]
        print(filename)
        command = "open \"videos/" + filename + "\""
        print(command)
        os.system(command)


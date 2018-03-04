from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import operator
from datasource import create_test_tournament, current_tournament, get_current_tournament
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
        layout.setContentsMargins(2, 2, 2, 2)

        self.searchBox = QLineEdit()
        self.setMaximumHeight(100)
        self.setMaximumHeight(10)
        self.searchBox.textChanged.connect(self.search)

        self.tableView = RecordedMatchesTable()
        self.initTableView(self.tableView)
        layout.addWidget(self.searchBox)
        layout.addWidget(self.tableView)

        self.setLayout(layout)
        self.setWindowTitle("Recorded Matches")

    def onQuit(self):
        self.close()

    def initTableView(self, tableView):
        tableView.setMinimumSize(900, 500)

    def search(self):
        self.tableView.updateFilter(self.searchBox.text())


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
    def __init__(self, *args, parent=None):
        QTableView.__init__(self, parent)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.filter = MatchFilter()
        self.setModel(self.filter)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setItemDelegateForColumn(8, WatchPushButtonDelegate(self))

    def updateFilter(self, text):
        print(self.filter)
        self.filter.setFilterText(text)


class MatchFilter(QSortFilterProxyModel):
    filterText = ""

    def __init__(self,parent = None):
        QSortFilterProxyModel.__init__(self,parent)
        self.tournamentModel = RecordedMatchesViewModel(tournament=datasource.current_tournament)
        self.setSourceModel(self.tournamentModel)

    def setFilterText(self, text):
        self.filterText = text
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        num_index = self.sourceModel().index(row, 0, parent)
        red1_index = self.sourceModel().index(row, 1, parent)
        red2_index = self.sourceModel().index(row, 2, parent)
        red3_index = self.sourceModel().index(row, 3, parent)
        blue1_index = self.sourceModel().index(row, 4, parent)
        blue2_index = self.sourceModel().index(row, 5, parent)
        blue3_index = self.sourceModel().index(row, 6, parent)


        num_str = self.sourceModel().data(num_index)
        red1_str = self.sourceModel().data(red1_index)
        red2_str = self.sourceModel().data(red2_index)
        red3_str = self.sourceModel().data(red3_index)
        blue1_str = self.sourceModel().data(blue1_index)
        blue2_str = self.sourceModel().data(blue2_index)
        blue3_str = self.sourceModel().data(blue3_index)

        if self.filterText in num_str:
            return True
        if self.filterText in red1_str:
            return True
        if self.filterText in red2_str:
            return True
        if self.filterText in red3_str:
            return True
        if self.filterText in blue1_str:
            return True
        if self.filterText in blue2_str:
            return True
        if self.filterText in blue3_str:
            return True

        return False

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


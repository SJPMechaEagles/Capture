from PyQt5.Qt import QWidget, QLabel, QLayout, QFormLayout, QLineEdit, QDialog
from PyQt5.Qt import *
from datasource import create_tournament_if_valid
from datetime import date, datetime, tzinfo
import dateutil.parser
from datasource import *

class NewTournamentWidget(QDialog):

    select_combo = None
    done_button = None

    options = None

    def __init__(self, parent=None):
        super(NewTournamentWidget, self).__init__(parent)
        self.setMinimumWidth(200)
        self.setMaximumHeight(200)
        self.setModal(True)

        self.mainLayout = QVBoxLayout()
        titleLabel = QLabel("Tournament Search")
        titleLabel.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(titleLabel)

        formLayout = QFormLayout()
        self.nameLine = QLineEdit()
        formLayout.addRow(QLabel("Name"), self.nameLine)
        self.skuLine = QLineEdit()
        formLayout.addRow(QLabel("SKU"), self.skuLine)
        self.requiresTeamEdit = QLineEdit()
        formLayout.addRow(QLabel("Required Team"), self.requiresTeamEdit)

        self.mainLayout.addLayout(formLayout)

        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.search)
        self.mainLayout.addWidget(self.searchButton)

        self.manuallyButton = QPushButton("Create Tournament Manually")
        self.manuallyButton.clicked.connect(self.dontSearch)
        self.mainLayout.addWidget(self.manuallyButton)

        self.setLayout(self.mainLayout)
        self.setWindowTitle("New Tournament")

    def dontSearch(self):
        name = self.nameLine.text()
        sku = self.skuLine.text()
        tournament = Tournament(name)
        tournament.sku = sku
        self.accept()

    def search(self):
        sku = self.skuLine.text()
        team = self.requiresTeamEdit.text()
        name = self.nameLine.text()
        self.options = create_tournament_if_valid(sku, name, team)
        if self.options is not None:
            if self.manuallyButton is not None:
                self.mainLayout.removeWidget(self.manuallyButton)
                self.manuallyButton = None
            if self.select_combo is not None:
                self.mainLayout.removeWidget(self.select_combo)
                self.select_combo = None
            if self.done_button is not None:
                self.mainLayout.removeWidget(self.done_button)
                self.done_button = None
            tournamentsCombo = QComboBox()
            self.select_combo = tournamentsCombo
            for option in self.options:
                date = dateutil.parser.parse(option['start'])
                print(date)
                tournamentsCombo.addItem("Name: " + option['name'] + ", Season: " +
                                         option['season'] + ", Start: " + str(date.month) + "/" + str(date.day) + "/" +
                                         str(date.year))
            self.mainLayout.addWidget(tournamentsCombo)
            self.done_button = QPushButton("Select")
            self.done_button.clicked.connect(self.select)
            self.mainLayout.addWidget(self.done_button)

    def select(self):
        print(self.select_combo.currentText())
        index = self.select_combo.currentIndex()
        sku = self.options[index]['sku']
        name = self.options[index]['name']
        t = Tournament(name)
        t.sku = sku
        t.pull_from_db()
        self.accept()

    def closeEvent(self, QCloseEvent):
        print("close")
        self.reject()
from enum import Enum
import  json, requests
from dialog import SelectTournamentDialog
from PyQt5.QtWidgets import QApplication
from random import *

import sys
import datetime
current_tournament = None

class Match_Type(Enum):
    ELIMINATION = 1
    QUALIFICATION = 2

class Tournament:
    name = None
    sku = None
    date = None
    matches = None
    season = 'In The Zone'

    def  __init__(self, name):
       self.name = name
       self.matches = []

    def update_match_data(self):
        if self.sku is not None:
            self.matches = self.pull_from_db()
        else:
            print("")

    def pull_from_db(self):
        params = dict()
        if self.sku is not None:
            params['sku'] = self.sku
        if self.date is not None:
            params['date'] = self.date
        params['season'] = self.season
        params['program'] = 'VRC'

        resp = requests.get('https://api.vexdb.io/v1/get_events', params)
        json_resp = resp.json()
        if json_resp['status'] is not 1:
            raise 'Failed to get data from DB'
        self.dia = SelectTournamentDialog()


def create_test_tournament():
    global current_tournament
    current_tournament = Tournament('Southern New Englands')
    pass
    for i in range(1,100):
        m = Match(str(randint(1,10000)) + "A", str(randint(1,10000)) + "B", str(randint(1,10000)), str(randint(1,10000)) + "C", num=i)
        current_tournament.matches.append(m)


def add_match(num, r1, r2, b1,b2):
    m = Match(r1, r2, b1,b2, Match_Type.QUALIFICATION, num)
    global current_tournament
    current_tournament.matches.append(m)

class Match:
    def __str__(self) -> str:
        return super().__str__()

    def __init__(self, num):
        self.num = num

    def __init__(self, red1, red2, blue1, blue2, type=Match_Type.QUALIFICATION, num=0):
        self.type = type
        self.num = num
        self.red1 = red1
        self.red2 = red2
        self.blue1 = blue1
        self.blue2 = blue2


    def __str__(self):
        return f'Match {self.num} r1: {self.red1} r2: {self.red2} b1: {self.blue1} b2:{self.blue2}'

class MatchVideo:
    def __init__(self, match):
        self.match = match
        self.start_time = datetime.datetime.now()

    def filename(self):
        str = f'M_{self.match.num}_T_{self.match.type}_R_{self.match.red1}_R_' \
              f'{self.match.red2}_B_{self.match.blue1}_B_{self.match.blue2}_TIME_{self.start_time.timestamp()}'
        return str

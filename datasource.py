from enum import Enum
import  json, requests
from dialog import SelectTournamentDialog
from PyQt5.QtWidgets import QApplication

import sys

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

    def update_match_data(self):
        if self.sku is not None:
            matches = self.pull_from_db()
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



class Match:

    def __init__(self, red1, red2, blue1, blue2, type=Match_Type.QUALIFICATION, num=0 ):
        self.type = type
        self.num = num
        self.red1 = red1
        self.red2 = red2
        self.blue1 = blue1
        self.blue2 = blue2

import datetime
import pickle
from datetime import *
from enum import Enum

import requests

current_tournament = None


def get_current_tournament():
    return current_tournament


def set_current_tournament(tournament):
    global current_tournament
    current_tournament = tournament


class Match_Type(Enum):
    QUALIFICATION = 2
    QUARTERFINAL = 3
    SEMIFINAL = 4
    FINALS = 5


def create_tournament_if_valid(sku, name, team):
    params = dict()
    if sku is not None or sku is not "":
        params['sku'] = sku
    if name is not None or name is not "":
        params['team'] = team
    params['program'] = 'VRC'

    resp = requests.get('https://api.vexdb.io/v1/get_events', params)
    json_resp = resp.json()
    if json_resp['size'] is 0:
        return None
    return json_resp['result']

def match_number_to_string(num):
    return get_current_tournament().matches[num].toId()

class Tournament:
    name = None
    sku = None
    date = None
    matches = None
    season = None
    filename = None

    def  __init__(self, name):
       self.name = name
       self.matches = []
       global current_tournament
       current_tournament = self

    def save(self):
        if self.filename is not None:
            self.save(self.filename)
        else:
            print("Cannot save Filename is None")
            self.save("Autosave_tournament")

    def save(self, filename):
        self.filename = filename
        print("save to " + filename)
        # os.mkdir(filename + ".Tournament.bundle")
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def update_match_data(self):
        if self.sku is not None:
            new_matches = self.update_from_db()

            matches_to_add = []
            old_matches = get_current_tournament().matches

            for new in new_matches:
                old_match_bool = False
                for old in old_matches:
                    if old.toId() == new.toId():
                        print('same')
                        old_match_bool = True
                if not old_match_bool:
                    print('new')

            get_current_tournament().matches.extend(matches_to_add)

    def pull_match_schedule_from_db(self):
        self.matches = self.update_from_db()


    def update_from_db(self):
        params = dict()
        print("Pulling from db")
        if self.sku is None:
            print("cannot pull")
            return
        print(self.sku)
        params['sku'] = self.sku
        print("request")
        resp = requests.get('https://api.vexdb.io/v1/get_matches', params)
        matches = resp.json()['result']
        results = []
        for match in matches:
            print("adding match " + str(match['matchnum']))
            new_match = Match(None, None, None, None)
            new_match.num = match['matchnum']
            new_match.red1 = match["red1"]
            new_match.red2 = match["red2"]
            new_match.blue1 = match["blue1"]
            new_match.blue2 = match["blue2"]
            new_match.type = Match_Type(match['round'])
            new_match.instance = match['instance']
            if match['round'] is not 2:
                # not elimination match
                new_match.red3 = match['red3']
                new_match.blue3 = match['blue3']
            results.append(new_match)
        return results


    def add_match(self, num, r1, r2, b1, b2, type = Match_Type.QUALIFICATION, r3=None, b3=None, instance=None):
        m = Match(r1, r2, b1, b2, type=type, num=num, red3=r3, blue3=b3, instance = instance)
        self.matches.append(m)

def create_test_tournament():
    global current_tournament
    current_tournament = Tournament('Southern New England Championship')
    current_tournament.sku = "RE-VRC-16-1659"
    current_tournament.pull_from_db()

def load_from_file(filename):
    with open(filename, 'rb') as file:
        global current_tournament
        current_tournament = pickle.load(file)
        print(current_tournament)

class Match:

    videos = []

    def __str__(self) -> str:
        return super().__str__()

    def __init__(self, red1, red2, blue1, blue2, red3 = None, blue3 = None, type=Match_Type.QUALIFICATION, num=0, instance=None):
        self.type = type
        self.num = num
        self.red1 = red1
        self.red2 = red2
        self.red3 = red3
        self.blue1 = blue1
        self.blue2 = blue2
        self.blue3 = blue3
        self.instance=instance

    def toId(self, space=True):
        if space:
            if self.type is Match_Type.QUALIFICATION:
                return 'Q# ' + str(self.num)
            if self.type is Match_Type.QUARTERFINAL:
                return 'QF# ' + str(self.instance) + '-' + str(self.num)
            if self.type is Match_Type.SEMIFINAL:
                return 'SF# ' + str(self.instance) + '-' + str(self.num)
            if self.type is Match_Type.FINALS:
                return 'Final# ' + str(self.instance) + '-' + str(self.num)
        if self.type is Match_Type.QUALIFICATION:
            return 'Q#' + str(self.num)
        if self.type is Match_Type.QUARTERFINAL:
            return 'QF#' + str(self.instance) + '-' + str(self.num)
        if self.type is Match_Type.SEMIFINAL:
            return 'SF#' + str(self.instance) + '-' + str(self.num)
        if self.type is Match_Type.FINALS:
            return 'Final#' + str(self.instance) + '-' + str(self.num)

    def toInfoString(self):
        if (self.red3 is None):
            red3 = ""
        else:
            red3 = self.red3
        if(self.blue3 is None):
            blue3 = ""
        else:
            blue3 = self.blue3
        return self.toId() + " Red: %s %s %s | Blue: %s %s %s"%(self.red1, self.red2, red3, self.blue1, self.blue2, blue3)

    def create_file_name(self):
        filename = self.toId() + "_" + str(datetime.isoformat(datetime.now())) + ".mp4"
        return filename

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

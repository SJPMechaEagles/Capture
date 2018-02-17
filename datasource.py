from enum import Enum
import requests

import datetime
current_tournament = None

def get_current_tournament():
    return current_tournament

class Match_Type(Enum):
    QUALIFICATION = 2
    QUARTERFINAL = 3
    SEMIFINAL = 4
    FINALS = 5


class Tournament:
    name = None
    sku = None
    date = None
    matches = None
    season = None

    def  __init__(self, name):
       self.name = name
       self.matches = []
       global current_tournament
       current_tournament = self

    def update_match_data(self):
        if self.sku is not None:
            self.matches = self.pull_match_schedule_from_db()
        else:
            print("")

    def pull_match_schedule_from_db(self):
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
        print(matches)
        for match in matches:
            print("adding match " + str(match['matchnum']))
            if match['round'] is 2:
                self.add_match(match['matchnum'], match["red1"], match["red2"], match["blue1"], match["blue2"])
            else:
                #elimination match
                self.add_match(match['matchnum'], match["red1"], match["red2"],
                               match["blue1"], match["blue2"], r3=match['red3'], b3=match['blue3'],
                               type=Match_Type(match['round']), instance=match['instance'])


    def pull_from_db(self):
        print('finding tournament')
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
            print("failed to get db info")
            return None
        if (json_resp['size'] is 1):
            self.sku = json_resp['result'][0]['sku']
            self.pull_match_schedule_from_db()
        else:
            print(json_resp)
            print("More or less than one")


    def add_match(self, num, r1, r2, b1, b2, type = Match_Type.QUALIFICATION, r3=None, b3=None, instance=None):
        m = Match(r1, r2, b1, b2, type=type, num=num, red3=r3, blue3=b3, instance = instance)
        self.matches.append(m)

def create_test_tournament():
    global current_tournament
    current_tournament = Tournament('Southern New England Championship')
    current_tournament.sku = "RE-VRC-16-1659"
    current_tournament.pull_from_db()

class Match:
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

    def toId(self):
        if self.type is Match_Type.QUALIFICATION:
            return 'Q# ' + str(self.num)
        if self.type is Match_Type.QUARTERFINAL:
            return 'QF# ' + str(self.instance) + '-' + str(self.num)
        if self.type is Match_Type.SEMIFINAL:
            return 'SF# ' + str(self.instance) + '-' + str(self.num)
        if self.type is Match_Type.FINALS:
            return 'Final# ' + str(self.instance) + '-' + str(self.num)


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

import requests
import datetime
import time
import json

def get_tournaments(progam, date, season, country, team):
    payload = {}
    if progam is None:
        payload['program'] = 'vrc'
    else:
        payload['program'] =  progam
    if date is not None:
        payload['date'] = date
    else:
        payload['date'] = datetime.date.isoformat(datetime.date.fromtimestamp(time.time()))
    if season is not None:
        payload['season'] = 'current'
    else:
        payload['season'] = season
    if country is None:
        payload['country'] = 'United States'
    else:
        payload['country'] = country
    if team is not None:
        payload['team'] = team

    r = requests.get('https://api.vexdb.io/v1/get_events', params=payload)
    print(json.dumps(r.json(), indent=4, sort_keys=True))

    results = r.json()['result']

    tournaments = []

    for tourn in results:
        sku = tourn['sku']
        name = tourn['name']
        start = tourn['start']
        end = tourn['end']
        season = tourn['season']

        tournament = Tournament(name, start, end, season, sku)
        tournaments.append(tournament)
    return tournaments

class Tournament:

    def __init__(self, name, start, end, season, sku):
        self.name = name
        self.start = start
        self.end = end
        self.season = season
        self.sku = sku

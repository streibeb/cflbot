from builtins import map, list, dict, zip

import requests

import logging

from models import Standings


class CFLClient(object):
    def __init__(self, base_uri, api_key):
        self.logger = logging.getLogger('cflbot')
        self.BASE_URI = base_uri
        self.API_KEY = api_key

    # End __init__()

    def get_game_ids(self, date):
        self.logger.debug('Getting games for %s', date)
        r = requests.get('{base_uri}/v1/games?filter[date_start][eq]={date}&key={api_key}'.format(
            base_uri=self.BASE_URI, date=date, api_key=self.API_KEY))
        if r.status_code == 200:
            data = r.json().get('data')
            return list(map(lambda x: {'game_id': x.get('game_id'), 'season': x.get('season')}, data))
        else:
            self.logger.error(r.json())
        # End if

    # End get_games()

    def get_game(self, season, game_id, include=[]):
        self.logger.debug('Getting game %s in season %s', game_id, season)
        r = requests.get('{base_uri}/v1/games/{season}/game/{game_id}?include={include}&key={api_key}'.format(
            base_uri=self.BASE_URI, season=season, game_id=game_id, include=','.join(include), api_key=self.API_KEY))
        if r.status_code == 200:
            data = r.json().get('data')
            return data[0]
        else:
            self.logger.error(r.json())
        # End if
    # End get_game()

    def get_standings(self, season):
        self.logger.debug('Getting standings for season %s', season)
        r = requests.get('{base_uri}/v1/standings/{season}?key={api_key}'.format(
            base_uri=self.BASE_URI, season=season, api_key=self.API_KEY))
        if r.status_code == 200:
            data = r.json().get('data')
            west = list(map(lambda x: Standings(x), data.get('divisions').get('west').get('standings')))
            east = list(map(lambda x: Standings(x), data.get('divisions').get('east').get('standings')))
            # print(east + west)
            return dict(zip(list(map(lambda x: x.team_id, west + east)), west + east))
        else:
            self.logger.error(r.json())
        # End if
    # End get_standings()

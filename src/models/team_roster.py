from builtins import list, map

from models import Player


class TeamRoster(object):
    def __init__(self, data):
        self.abbreviation = data.get('abbreviation')
        self.team_id = data.get('team_id')
        self.roster = list(map(lambda x: Player(x), data.get('roster')))

    def get_starters(self):
        return [p for p in self.roster if p.is_starter]

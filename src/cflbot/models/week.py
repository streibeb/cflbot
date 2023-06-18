from datetime import date, datetime
from . import Game

class Week:
    def __init__(self):
        self.id: str
        self.name: str
        self.status: str
        self.start_date: datetime
        self.end_date: datetime
        self.games: list[Game]

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def from_json(cls, json) -> 'Week':
        instance = cls()
        instance.id = json['id']
        instance.name = json['name']
        instance.status = json['status']
        instance.start_date = datetime.fromisoformat(json['startDate'])
        instance.end_date = datetime.fromisoformat(json['endDate'])
        instance.games = list(map(lambda g: Game.from_json(g), json['tournaments']))
        return instance
    
    def is_active(self) -> bool:
        return any(game.is_active() for game in self.games)

    def is_complete(self) -> bool:
        return all(game.is_complete() for game in self.games)
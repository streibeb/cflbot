from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from . import Team

class Game:
    def __init__(self):
        self.id: str
        self.cfl_game_id: str
        self.status: str
        self.game_week: str
        self.start_date: datetime
        self.home_team: Team
        self.home_team_score: int
        self.away_team: Team
        self.away_team_score: int
    
    def __repr__(self):
        return f'Game {self.cfl_game_id}: {self.get_formatted_title(timezone.utc)}'

    @classmethod
    def from_json(cls, json) -> 'Game':
        instance = cls()
        instance.id = json['id']
        instance.cfl_game_id = json['cflId']
        instance.status = json['status']
        instance.start_date = datetime.fromisoformat(json['date'])
        instance.home_team = Team.from_json(json['homeSquad'])
        instance.home_team_score = json['homeSquad']['score']
        instance.away_team = Team.from_json(json['awaySquad'])
        instance.away_team_score = json['awaySquad']['score']
        return instance

    def is_active(self) -> bool:
        return not self.is_scheduled() and not self.is_complete()

    def is_complete(self) -> bool:
        return self.status == 'complete'

    def is_scheduled(self) -> bool:
        return self.status == 'scheduled'

    def get_formatted_title(self, tz: ZoneInfo) -> str:
        return f'{self.get_formatted_participants()} - {self.get_formatted_start_date(tz)}'

    def get_formatted_participants(self) -> str:
        return f'{self.away_team} @ {self.home_team}'

    def get_formatted_start_date(self, tz: ZoneInfo) -> str:
        return self.start_date.astimezone(tz).strftime("%B %-d, %Y")

    def get_formatted_start_time(self, tz: ZoneInfo) -> str:
        return self.start_date.astimezone(tz).strftime("%I:%M %p %Z")
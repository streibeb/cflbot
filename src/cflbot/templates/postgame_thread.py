from cflbot.cfl import CFL
from datetime import datetime, timezone, timedelta
from cflbot.models import Game, Standings
from cflbot.config import Config
from mako.template import Template
from zoneinfo import ZoneInfo
import logging
import os

class PostGameThread:
    def __init__(self, cfl: CFL, config: Config):
        self.logger = logging.getLogger(__name__)
        self.cfl = cfl
        self.config = config

    def build_title(self, game: Game) -> str:
        return f'POST GAME THREAD: {self.__get_title(game)}'

    def build_body(self, game: Game) -> str:
        template = Template(filename=self.__get_file_path('postgame_thread.md'))
        context = {
            'header': self.__get_header(game),
            'starting_lineups': self.__get_lineups(game),
            'linescore': self.__get_linescore(game),
            'scoring_plays': self.__get_scoring_plays(game),
            'footer': self.__get_footer(game)
        }
        return template.render(**context)

    def __get_title(self, game: Game) -> str:
        self.logger.info(f'Getting standings')
        standings = self.cfl.get_standings()
        away_standings = list(filter(lambda t: t.id == game.away_team.id, standings))[0]
        home_standings = list(filter(lambda t: t.id == game.home_team.id, standings))[0]
        return f'{away_standings} @ {home_standings} - {game.get_formatted_start_date(self.config.tz)}'

    def __get_header(self, game):
        template = Template(filename=self.__get_file_path("header.md"))
        context = {
            'matchup': game.get_formatted_title(self.config.tz),
            'game_start_local': game.get_formatted_start_time(game.home_team.timezone),
            'game_start_eastern': game.get_formatted_start_time(ZoneInfo("America/Toronto"))
        }
        return template.render(**context)

    def __get_matchup(self, game) -> str:
        return ''

    def __get_conditions(self, game) -> str:
        return ''

    def __get_lineups(self, game) -> str:
        return ''

    def __get_linescore(self, game) -> str:
        template = Template(filename=self.__get_file_path("linescore.md"))
        context = {
            'away_team': game.away_team.abbreviation,
            'away_team_score_total': game.away_team_score,
            'home_team': game.home_team.abbreviation,
            'home_team_score_total': game.home_team_score
        }
        return template.render(**context)

    def __get_scoring_plays(self, game) -> str:
        return ''

    def __get_broadcast(self, game):
        template = Template(filename=self.__get_file_path("broadcast.md"))
        context = {
            'away_team': game.away_team.abbreviation,
            'away_radio': game.away_team.radio_station,
            'home_team': game.home_team.abbreviation,
            'home_radio': game.home_team.radio_station
        }
        return template.render(**context)

    def __get_footer(self, game) -> str:
        template = Template(filename=self.__get_file_path("footer.md"))
        context = {
            'away_subreddit': game.away_team.subreddit,
            'home_subreddit': game.home_team.subreddit
        }
        return template.render(**context)

    @staticmethod
    def __get_file_path(path) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, path)
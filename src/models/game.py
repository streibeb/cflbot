import logging
from builtins import map, list, range, max, len, str, Exception

import pytz
from dateutil import parser
from mako.template import Template

from models import EventType, EventStatus, Venue, Weather, CoinToss, Team, TeamRoster, Play


class Game(object):
    def __init__(self, cfl_client, season, game_id):
        self.logger = logging.getLogger('cflbot')

        self.CFL_CLIENT = cfl_client

        data = self.CFL_CLIENT.get_game(season, game_id, include=['rosters', 'play_by_play'])
        self.game_id = data.get('game_id')
        self.date_start = parser.parse(data.get('date_start')).astimezone(pytz.UTC)
        self.game_number = data.get('game_number')
        self.week = data.get('week')
        self.season = data.get('season')
        self.event_type = EventType(data.get('event_type'))
        self.event_status = EventStatus(data.get('event_status'))
        self.venue = Venue(data.get('venue'))
        self.weather = Weather(data.get('weather'))
        self.coin_toss = CoinToss(data.get('coin_toss'))
        self.tickets_url = data.get('tickets_url')
        self.team_1 = Team(data.get('team_1'))
        self.team_2 = Team(data.get('team_2'))

        team_1_roster = TeamRoster(data.get('rosters').get('teams').get('team_1'))
        self.team_1_starters = team_1_roster.get_starters()
        team_2_roster = TeamRoster(data.get('rosters').get('teams').get('team_2'))
        self.team_2_starters = team_2_roster.get_starters()

        standings = self.CFL_CLIENT.get_standings(self.season)
        self.team_1_standings = standings[self.team_1.team_id]
        self.team_2_standings = standings[self.team_2.team_id]

        self.play_by_play = list(map(lambda p: Play(p), data.get('play_by_play')))
    # End __init()

    def get_thread_title(self):
        if self.event_type.is_preseason() or self.event_type.is_regular_season():
            return '{matchup} - {date}'.format(
                matchup=self.__get_matchup(),
                date=self.date_start.strftime("%B %-d, %Y")
            )
        else:
            return '{title} | {matchup} - {date}'.format(
                title=self.event_type.title,
                matchup=self.__get_matchup(),
                date=self.date_start.strftime("%B %-d, %Y")
            )
        # End if
    # End get_thread_title()

    def build_post(self):
        template = Template(filename="src/templates/game_thread.md")
        context = {
            'header': self.__get_header(),
            'conditions': self.__get_conditions(),
            'starting_lineups': self.__get_lineups(),
            'linescore': self.__get_linescore(),
            'scoring_plays': self.__get_scoring_plays(),
            'footer': self.__get_footer()
        }
        return template.render(**context)
    # End build_post

    def __get_header(self):
        template = Template(filename="src/templates/header.md")
        context = {
            'matchup': self.__get_matchup(),
            'game_start': self.date_start.strftime("%I:%M %p %Z"),
            'stadium': self.venue.name
        }
        return template.render(**context)

    def __get_matchup(self):
        if self.event_type.is_preseason():
            return '{away_name} at {home_name}'.format(
                title=self.event_type.title,
                away_name=self.team_1.full_name,
                home_name=self.team_2.full_name
            )
        elif self.event_type.is_grey_cup():
            return '{away_name} ({away_standings}) vs {home_name} ({home_standings})'.format(
                away_name=self.team_1.full_name,
                away_standings=self.team_1_standings.to_string(),
                home_name=self.team_2.full_name,
                home_standings=self.team_2_standings.to_string()
            )
        else:
            return '{away_name} ({away_standings}) at {home_name} ({home_standings})'.format(
                away_name=self.team_1.full_name,
                away_standings=self.team_1_standings.to_string(),
                home_name=self.team_2.full_name,
                home_standings=self.team_2_standings.to_string()
            )

    def __get_conditions(self):
        template = Template(filename="src/templates/conditions.md")
        context = {
            'placeholder': '',
            'weather_sky': '',
            'weather_temperature': '',
            'weather_wind_direction': '',
            'weather_wind_speed': '',
            'weather_field_conditions': '',
            'coin_toss_winner': ''
        }

        weather = self.weather
        if weather.sky != "":
            context['weather_sky'] = weather.sky.title()
            context['weather_temperature'] = weather.temperature
            context['weather_wind_direction'] = weather.wind_direction
            context['weather_wind_speed'] = weather.wind_speed
            context['weather_field_conditions'] = weather.field_conditions

        coin_toss = self.coin_toss
        if coin_toss.coin_toss_winner != "":
            context['coin_toss_winner'] = coin_toss.coin_toss_winner_election

        return template.render(**context)

    def __get_lineups(self):
        template = Template(filename="src/templates/lineups.md")
        context = {
            'away_abbr': self.team_1.abbreviation,
            'home_abbr': self.team_2.abbreviation,
            'rosters': []
        }

        def build_row(idx, players):
            cell = {
                    'uniform': '',
                    'first_name': '',
                    'last_name': ''
                }
            if idx < len(players):
                cell['uniform'] = players[idx].uniform
                cell['first_name'] = players[idx].first_name
                cell['last_name'] = players[idx].last_name
            return cell

        for i in range(0, max(len(self.team_1_starters), len(self.team_2_starters))):
            row = {
                'away': build_row(i, self.team_1_starters),
                'home': build_row(i, self.team_2_starters)
            }
            context['rosters'].append(row)

        return template.render(**context)

    def __get_linescore(self):
        overtime = len(self.team_1.linescores) > 4
        filename = "/linescore.md" if not overtime else "/linescore_ot.md"

        template = Template(filename="src/templates/" + filename)

        def get_team_linescore(team):
            row = {
                'abbr': team.abbreviation,
                'total': team.score
            }

            x = 1
            for item in team.linescores:
                quarter = "q" + str(x)
                row[quarter] = item.get('score')
                x = x + 1

            for i in range(x, 6):
                quarter = "q" + str(i)
                row[quarter] = ''

            return row

        context = {
            'teams': [
                get_team_linescore(self.team_1), get_team_linescore(self.team_2)
            ]
        }

        return template.render(**context)

    def __get_scoring_plays(self):
        template = Template(filename="src/templates/scoring_plays.md")
        context = {
            'away_abbr': self.team_1.abbreviation,
            'home_abbr': self.team_2.abbreviation,
            'plays': []
        }

        for play in [x for x in self.play_by_play if x.play_result_points > 0]:
            row = {
                'qtr': play.quarter,
                'time': play.play_clock_start,
                'play': play.play_summary,
                'away_score': play.team_visitor_score,
                'home_score': play.team_home_score
            }
            context['plays'].append(row)

        return template.render(**context)

    def __get_footer(self):
        template = Template(filename="src/templates/footer.md")
        context = {
            'away_subreddit': self.team_1.subreddit,
            'home_subreddit': self.team_2.subreddit
        }

        return template.render(**context)

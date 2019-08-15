from dateutil import parser


class Game(object):
    def __init__(self, data):
        self.game_id = data.get('game_id')
        self.date_start = parser.parse(data.get('date_start'))
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
    # End __init()

    def get_thread_title(self):
        if self.event_type.event_type_id == EventType.PRESEASON:
            return '{away_name} at {home_name} - {date}'.format(
                title=self.event_type.title,
                away_name=self.team_1.full_name,
                home_name=self.team_2.full_name,
                date=self.date_start.strftime("%B %-d, %Y")
            )
        elif self.event_type.event_type_id == EventType.REGULAR_SEASON:
            return '{away_name} ({away_standings}) at {home_name} ({home_standings}) - {date}'.format(
                away_name=self.team_1.full_name,
                away_standings="0-0-0",
                home_name=self.team_2.full_name,
                home_standings="0-0-0",
                date=self.date_start.strftime("%B %-d, %Y")
            )
        elif self.event_type.event_type_id == EventType.PLAYOFFS:
            return '{title} | {away_name} ({away_standings}) at {home_name} ({home_standings}) - {date}'.format(
                title=self.event_type.title,
                away_name=self.team_1.full_name,
                away_standings="0-0-0",
                home_name=self.team_2.full_name,
                home_standings="0-0-0",
                date=self.date_start.strftime("%B %-d, %Y")
            )
        elif self.event_type.event_type_id == EventType.GREY_CUP:
            return '{title} | {away_name} ({away_standings}) vs {home_name} ({home_standings}) - {date}'.format(
                title=self.event_type.title,
                away_name=self.team_1.full_name,
                away_standings="0-0-0",
                home_name=self.team_2.full_name,
                home_standings="0-0-0",
                date=self.date_start.strftime("%B %-d, %Y")
            )
        # End if
    # End get_thread_title()


class EventType(object):
    PRESEASON = 0
    REGULAR_SEASON = 1
    PLAYOFFS = 2
    GREY_CUP = 3

    def __init__(self, data):
        self.event_type_id = data.get('event_type_id')
        self.name = data.get('name')
        self.title = data.get('title')
    # End __init()


class EventStatus(object):
    PRE_GAME = 1
    IN_PROGRESS = 2
    FINAL = 4
    CANCELLED = 9

    def __init__(self, data):
        self.event_status_id = data.get('event_status_id')
        self.is_active = data.get('is_active')
        self.quarter = data.get('quarter')
        self.minutes = data.get('minutes')
        self.seconds = data.get('seconds')
        self.down = data.get('down')
        self.yards_to_go = data.get('yards_to_go')
    # End __init()


class Venue(object):
    def __init__(self, data):
        self.venue_id = data.get('venue_id')
        self.name = data.get('name')
    # End __init()


class CoinToss(object):
    def __init__(self, data):
        self.coin_toss_winner = data.get('coin_toss_winner')
        self.coin_toss_winner_election = data.get('coin_toss_winner_election')
    # End __init()


class Weather(object):
    def __init__(self, data):
        self.sky = data.get('sky')
        self.temperature = data.get('temperature')
        self.wind_speed = data.get('wind_speed')
        self.wind_direction = data.get('wind_direction')
        self.field_conditions = data.get('field_conditions')
    # End __init()


class Team(object):
    def __init__(self, data):
        self.team_id = data.get('team_id')
        self.location = data.get('location')
        self.nickname = data.get('nickname')
        self.abbreviation = data.get('abbreviation')
        self.score = data.get('score')
        self.venue_id = data.get('venue_id')
        self.linescores = data.get('linescores')
        self.is_at_home = data.get('is_at_home')
        self.is_winner = data.get('is_winner')
    # End __init()

    @property
    def full_name(self):
        return self.location + " " + self.nickname

    def get_standings(self):
        return "0-0-0"


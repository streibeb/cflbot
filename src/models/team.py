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

    @property
    def subreddit(self):
        return {
            "BC": "/r/BC_Lions",
            "CGY": "/r/Stampeders",
            "EDM": "/r/Eskimos",
            "SSK": "/r/riderville",
            "WPG": "/r/WinnipegBlueBombers",
            "HAM": "/r/ticats",
            "TOR": "/r/Argonauts",
            "OTT": "/r/redblacks",
            "MTL": "/r/Alouettes"
        }.get(self.abbreviation)

    def get_table_style(self):
        return {
            "BC": "####[](/placeholder)",
            "CGY": "#####[](/placeholder)",
            "EDM": "######[](/placeholder)",
            "SSK": "####[](/placeholder)\n####[](/placeholder)",
            "WPG": "####[](/placeholder)\n#####[](/placeholder)",
            "HAM": "####[](/placeholder)\n######[](/placeholder)",
            "TOR": "#####[](/placeholder)\n####[](/placeholder)",
            "OTT": "#####[](/placeholder)\n#####[](/placeholder)",
            "MTL": "#####[](/placeholder)\n######[](/placeholder)",
        }.get(self.abbreviation)

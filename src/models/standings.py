class Standings(object):
    def __init__(self, data):
        self.season = data.get('season')
        self.division_id = data.get('division_id')
        self.division_name = data.get('division_name')
        self.place = data.get('place')
        self.flags = data.get('flags')
        self.team_id = data.get('team_id')
        self.letter = data.get('letter')
        self.abbreviation = data.get('abbreviation')
        self.location = data.get('location')
        self.nickname = data.get('nickname')
        self.full_name = data.get('full_name')
        self.games_played = data.get('games_played')
        self.wins = data.get('wins')
        self.losses = data.get('losses')
        self.ties = data.get('ties')
        self.points = data.get('points')
        self.winning_percentage = data.get('winning_percentage')
        self.points_for = data.get('points_for')
        self.points_against = data.get('points_against')
        self.home_wins = data.get('home_wins')
        self.home_losses = data.get('home_losses')
        self.home_ties = data.get('home_ties')
        self.away_wins = data.get('away_wins')
        self.away_losses = data.get('away_losses')
        self.away_ties = data.get('away_ties')
        self.division_wins = data.get('division_wins')
        self.division_losses = data.get('division_losses')
        self.division_ties = data.get('division_ties')

    def to_string(self):
        if self.ties != 0:
            return '{wins}-{losses}-{ties}'.format(
                wins=self.wins,
                losses=self.losses,
                ties=self.ties
            )
        else:
            return '{wins}-{losses}'.format(
                wins=self.wins,
                losses=self.losses
            )

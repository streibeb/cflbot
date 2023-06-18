class Standings:
    def __init__(self):
        self.id: str
        self.name: str
        self.abbreviation: str
        self.wins: int
        self.draws: int
        self.losses: int

    def __repr__(self):
        if self.draws > 0:
            return f'{self.name} ({self.wins}-{self.losses}-{self.draws})'
        return f'{self.name} ({self.wins}-{self.losses})'

    @classmethod
    def from_json(cls, json) -> 'Standings':
       instance = cls()
       instance.id = json['id']
       instance.name = json['name']
       instance.abbreviation = json['abbreviation']
       instance.wins = json['wins']
       instance.draws = json['draw']
       instance.losses = json['loss']
       return instance
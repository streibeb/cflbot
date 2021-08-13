class CoinToss(object):
    def __init__(self, data):
        self.coin_toss_winner = data.get('coin_toss_winner')
        self.coin_toss_winner_election = data.get('coin_toss_winner_election')
    # End __init()
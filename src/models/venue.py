class Venue(object):
    def __init__(self, data):
        self.venue_id = data.get('venue_id')
        self.name = data.get('name')
    # End __init()
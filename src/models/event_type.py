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

    def is_preseason(self):
        return self.event_type_id == EventType.PRESEASON

    def is_regular_season(self):
        return self.event_type_id == EventType.REGULAR_SEASON

    def is_playoffs(self):
        return self.event_type_id == EventType.PLAYOFFS

    def is_grey_cup(self):
        return self.event_type_id == EventType.GREY_CUP
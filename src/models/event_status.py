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

    def is_pre_game(self):
        return self.event_status_id == EventStatus.PRE_GAME

    def is_in_progress(self):
        return self.event_status_id == EventStatus.IN_PROGRESS

    def is_final(self):
        return self.event_status_id == EventStatus.FINAL

    def is_cancelled(self):
        return self.event_status_id == EventStatus.CANCELLED
class Weather(object):
    def __init__(self, data):
        self.sky = data.get('sky')
        self.temperature = data.get('temperature')
        self.wind_speed = data.get('wind_speed')
        self.wind_direction = data.get('wind_direction')
        self.field_conditions = data.get('field_conditions')
    # End __init()
class Player(object):
    def __init__(self, data):
        self.cfl_central_id = data.get('cfl_central_id')
        self.first_name = data.get('first_name')
        self.middle_name = data.get('middle_name')
        self.last_name = data.get('last_name')
        self.birth_date = data.get('birth_date')
        self.uniform = data.get('uniform')
        self.position = data.get('position')
        self.is_national = data.get('is_national')
        self.is_starter = data.get('is_starter')
        self.is_inactive = data.get('is_inactive')

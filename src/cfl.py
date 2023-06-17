import requests
from urllib.parse import urljoin, urlencode
from models import Team, Week, Game, Standings
from datetime import datetime, timedelta
from config import CFLConfig

class CFL:
    def __init__(self, config: CFLConfig):
        self._session = requests.Session()
        self._base_url = config.base_url

    def get_rounds_checksum(self): 
        url = urljoin(self._base_url, './checksums.json')
        r = self._session.get(url)
        if r.status_code == 200:
            data = r.json()
            return data['rounds']
        else:
            raise Exception(r.json())

    def get_weeks(self) -> list[Week]:
        url = urljoin(self._base_url, './rounds.json')
        r = self._session.get(url)
        if r.status_code == 200:
            data = r.json()
            return list(map(lambda w: Week.from_json(w), data))
        else:
            raise Exception(r.json())

    def get_week(self, date: datetime) -> Week:
        days_to_add = timedelta(days=1)

        weeks = self.get_weeks()
        return list(filter(lambda w: (w.end_date + days_to_add) > date, weeks))[0]

    def get_standings(self) -> list[Standings]:
        url = urljoin(self._base_url, './squads.json')
        r = self._session.get(url)
        if r.status_code == 200:
            data = r.json()
            return list(map(lambda t: Standings.from_json(t), data))
        else:
            raise Exception(r.json())

    # def get_teams(self) -> list[Team]:
    #     url = urljoin(self._base_url, 'squads.json')
    #     r = self._session.get(url)
    #     if r.status_code == 200:
    #         data = r.json()
    #         return list(map(lambda t: Team.from_json(t), data))
    #     else:
    #         print(r.json())
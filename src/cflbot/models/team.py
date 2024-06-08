from zoneinfo import ZoneInfo
from datetime import timezone

class Team:
    def __init__(self):
        self.id: str
        self.name: str
        self.abbreviation: str

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def from_json(cls, json) -> 'Team':
       instance = cls()
       instance.id = json['id']
       instance.name = json['name']
       instance.abbreviation = json['shortName']
       return instance
    
    @property
    def subreddit(self) -> str:
        return {
            "BC": "/r/BC_Lions",
            "CGY": "/r/Stampeders",
            "EDM": "/r/GoElks",
            "SSK": "/r/riderville",
            "WPG": "/r/WinnipegBlueBombers",
            "HAM": "/r/ticats",
            "TOR": "/r/Argonauts",
            "OTT": "/r/redblacks",
            "MTL": "/r/Alouettes"
        }.get(self.abbreviation)

    @property
    def radio_station(self) -> str:
        return {
            "BC": "[980 CKNW](https://globalnews.ca/radio/cknw/player/) or [Sher-E-Punjab Radio AM 600](https://listen.streamon.fm/ckspam)",
            "CGY": "[770 CHQR](https://globalnews.ca/radio/770chqr/)",
            "EDM": "[630 CHED](https://globalnews.ca/pages/edmonton-elks-audio-clips)",
            "SSK": "[620 CKRM](https://www.620ckrm.com/sportscage/)",
            "WPG": "[680 CJOB](https://globalnews.ca/radio/cjob/player/#/)",
            "HAM": "[Ticats Audio Network](https://ticats.ca/listen)",
            "TOR": "[TSN 1050](https://www.tsn.ca/radio/toronto-1050)",
            "OTT": "[TSN 1200 (en)](https://www.tsn.ca/radio/ottawa-1200) or [104.7 FM (fr)](https://www.fm1047.ca/)",
            "MTL": "[TSN 690 (en)](https://www.tsn.ca/radio/montreal-690) or [98.5 FM (fr)](https://www.985fm.ca/)"
        }.get(self.abbreviation)

    @property
    def timezone(self) -> timezone:
        return {
            "BC": ZoneInfo("America/Vancouver"),
            "CGY": ZoneInfo("America/Edmonton"),
            "EDM": ZoneInfo("America/Edmonton"),
            "SSK": ZoneInfo("America/Regina"),
            "WPG": ZoneInfo("America/Winnipeg"),
            "HAM": ZoneInfo("America/Toronto"),
            "TOR": ZoneInfo("America/Toronto"),
            "OTT": ZoneInfo("America/Toronto"),
            "MTL": ZoneInfo("America/Toronto"),
        }.get(self.abbreviation)
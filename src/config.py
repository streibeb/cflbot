from io import open
from json import load
from zoneinfo import ZoneInfo

class Config:
    def __init__(self):
        logging: LoggingConfig
        cfl: CFLConfig
        database: DatabaseConfig
        reddit: RedditConfig
        subreddit: str
        pregame: bool
        pregame_minutes: int
        game_minutes: int
        postgame: bool
        tz: ZoneInfo

    @classmethod
    def from_file(cls, path) -> 'Config':
        with open(path, 'r') as json_file:
            json = load(json_file)
            return Config.from_json(json)
    
    @classmethod
    def from_json(cls, json) -> 'Config':
        config = Config()
        config.logging = LoggingConfig.from_json(json.get('logging'))
        config.cfl = CFLConfig().from_json(json.get('cfl'))
        config.database = DatabaseConfig.from_json(json.get('database'))
        config.reddit = RedditConfig().from_json(json.get('reddit'))
        config.pregame = json['pregame']
        config.pregame_minutes = json['pregameMinutes']
        config.game_minutes = json['gameMinutes']
        config.postgame = json['postgame']
        config.tz = ZoneInfo(json['tz'])
        return config
#End Config

class LoggingConfig:
    def __init__(self):
        level: str
        format: str

    @classmethod
    def from_json(cls, json) -> 'LoggingConfig':
        config = cls()
        if json is None:
            config.level = 'INFO'
            config.format = '%(asctime)s %(levelname)-10s %(message)s'
        else:
            config.level = json['level'] if 'level' in json is not None else 'INFO'
            config.format = json['format'] if 'format' in json is not None else '%(asctime)s %(levelname)-10s %(message)s'
        return config
#End DatabaseConfig

class CFLConfig:
    def __init__(self):
        base_url: str

    @classmethod
    def from_json(cls, json) -> 'CFLConfig':
        config = cls()
        config.base_url = json['baseUrl']
        config.api_key = json['apiKey']
        return config
#End DatabaseConfig

class DatabaseConfig:
    def __init__(self):
        database_name: str

    @classmethod
    def from_json(cls, json) -> 'DatabaseConfig':
        config = cls()
        config.database_name = json['databaseName']
        return config
#End DatabaseConfig

class RedditConfig:
    def __init__(self):
        enabled: boolean
        reddit_client_id: str
        reddit_client_secret: str
        reddit_user_agent: str
        reddit_refresh_token: str
        subreddit: str

    @classmethod
    def from_json(cls, json) -> 'RedditConfig':
        config = cls()
        config.enabled = json['enabled'] if 'enabled' in json else True
        config.reddit_client_id = json['clientId']
        config.reddit_client_secret = json['clientSecret']
        config.reddit_user_agent = json['userAgent']
        config.reddit_refresh_token = json['refreshToken']
        config.subreddit = json['subreddit']
        return config
#End RedditConfig
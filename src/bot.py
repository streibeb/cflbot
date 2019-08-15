import logging
import requests
import praw
from prawcore.exceptions import PrawcoreException
from datetime import datetime
from time import sleep
from models.game import Game


class Bot(object):
    def __init__(self, config):
        self.logger = logging.getLogger('cflbot')

        cfl_config = config.get('cfl')
        if cfl_config is None:
            raise ValueError('Missing CFL API config')

        self.CFL_API_BASE_URI = cfl_config.get('baseUri')
        if self.CFL_API_BASE_URI is None:
            raise ValueError('Missing CFL baseUri')
        self.CFL_API_KEY = cfl_config.get('apiKey')
        if self.CFL_API_KEY is None:
            raise ValueError('Missing CFL apiKey')

        reddit_config = config.get('reddit')
        if reddit_config is None:
            raise ValueError('Missing Reddit API config')

        self.REDDIT_CLIENT_ID = reddit_config.get('clientId')
        if self.REDDIT_CLIENT_ID is None:
            raise ValueError('Missing Reddit clientId')
        self.REDDIT_CLIENT_SECRET = reddit_config.get('clientSecret')
        if self.REDDIT_CLIENT_SECRET is None:
            raise ValueError('Missing Reddit clientSecret')
        self.REDDIT_USER_AGENT = reddit_config.get('userAgent')
        if self.REDDIT_USER_AGENT is None:
            raise ValueError('Missing Reddit userAgent')
        self.REDDIT_REFRESH_TOKEN = reddit_config.get('refreshToken')
        if self.REDDIT_REFRESH_TOKEN is None:
            raise ValueError('Missing Reddit refreshToken')

        self.r = praw.Reddit(user_agent=self.REDDIT_USER_AGENT,
                             client_id=self.REDDIT_CLIENT_ID,
                             client_secret=self.REDDIT_CLIENT_SECRET,
                             refresh_token=self.REDDIT_REFRESH_TOKEN)
        self.logger.info('Successfully authenticated with Reddit')

        self.PREGAME_THREAD = None
        self.SUBREDDIT = config.get('subreddit')

    # End __init__()

    def run(self):

        while True:
            games = self.__get_games_today()
            self.logger.info('There are %d games today', len(games))

            if len(games) > 0:
                if self.PREGAME_THREAD:
                    self.logger.debug("PREGAME THREAD")

                for game in games:
                    g = Game(game)
                    self.__post_thread(g)

            self.logger.info("Sleeping for 1 minute")
            sleep(1 * 60)
            # End for
        # End while

    # End run()

    def __get_games_today(self):
        today = datetime.today().strftime('%Y-%m-%d')
        self.logger.debug('Getting games for %s', today)
        r = requests.get('{base_uri}/v1/games?filter[date_start][eq]={today}&key={api_key}'.format(
            base_uri=self.CFL_API_BASE_URI, today=today, api_key=self.CFL_API_KEY))
        if r.status_code == 200:
            data = r.json().get('data')
            return data
        else:
            self.logger.error(r.json())
        # End if

    # End __get_games()

    # def __test_get_games(self):
    #     r = requests.get('http://api.cfl.ca/v1/games?filter[game_id][in]=2457,2466,2548,2550,2551&key=T8Mv9BRDdcB7bMQUsQvHqtCGPewH5y8p')
    #     if r.status_code == 200:
    #         data = r.json().get('data')
    #         return data
    #     else:
    #         self.logger.error(r.json())
    #     # End if
    # # End __get_games()

    def __post_thread(self, game, prefix="GAME THREAD"):
        try:
            thread_title = '{prefix}: {title}'.format(prefix=prefix, title=game.get_thread_title())

            subreddit = self.r.subreddit(self.SUBREDDIT)
            submission = None

            self.logger.debug('Searching /r/%s for existing game thread...', subreddit)
            for result in subreddit.new():
                if result.title == thread_title:
                    self.logger.debug('Thread "%s" is already posted', thread_title)
                    submission = result

            if submission is None:
                self.logger.debug('Posting thread "%s"...', thread_title)
                submission = subreddit.submit(thread_title, selftext=datetime.now())
                self.logger.debug('Thread submitted successfully')

            submission.edit(datetime.now())
        except PrawcoreException as e:
            print(e)

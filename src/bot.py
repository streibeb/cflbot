from builtins import ValueError, list, len
from time import sleep

import logging
import praw
import pytz
from datetime import datetime, timedelta
from prawcore.exceptions import PrawcoreException

from cfl_client import CFLClient
from models.game import Game


class Bot(object):
    def __init__(self, config):
        self.logger = logging.getLogger('cflbot')

        cfl_config = config.get('cfl')
        self.__init_cfl_client(cfl_config)

        reddit_config = config.get('reddit')
        self.__init_praw(reddit_config)

        self.PREGAME_THREAD = True
        self.PREGAME_POST_MINUTES_AHEAD = 60
        self.POST_MINUTES_AHEAD = 30
        self.POSTGAME_THREAD = True
        self.SUBREDDIT = config.get('subreddit')

    def __init_cfl_client(self, config):
        if config is None:
            raise ValueError('Missing CFL API config')

        self.CFL_API_BASE_URI = config.get('baseUri')
        if self.CFL_API_BASE_URI is None:
            raise ValueError('Missing CFL baseUri')
        self.CFL_API_KEY = config.get('apiKey')
        if self.CFL_API_KEY is None:
            raise ValueError('Missing CFL apiKey')

        self.CFL_CLIENT = CFLClient(self.CFL_API_BASE_URI, self.CFL_API_KEY)

    def __init_praw(self, config):
        if config is None:
            raise ValueError('Missing Reddit API config')

        self.REDDIT_CLIENT_ID = config.get('clientId')
        if self.REDDIT_CLIENT_ID is None:
            raise ValueError('Missing Reddit clientId')
        self.REDDIT_CLIENT_SECRET = config.get('clientSecret')
        if self.REDDIT_CLIENT_SECRET is None:
            raise ValueError('Missing Reddit clientSecret')
        self.REDDIT_USER_AGENT = config.get('userAgent')
        if self.REDDIT_USER_AGENT is None:
            raise ValueError('Missing Reddit userAgent')
        self.REDDIT_REFRESH_TOKEN = config.get('refreshToken')
        if self.REDDIT_REFRESH_TOKEN is None:
            raise ValueError('Missing Reddit refreshToken')

        self.r = praw.Reddit(user_agent=self.REDDIT_USER_AGENT,
                             client_id=self.REDDIT_CLIENT_ID,
                             client_secret=self.REDDIT_CLIENT_SECRET,
                             refresh_token=self.REDDIT_REFRESH_TOKEN)
        self.logger.info('Successfully authenticated with Reddit')

    def run(self):
        while True:
            today = datetime.today().strftime('%Y-%m-%d')
            game_ids = self.CFL_CLIENT.get_game_ids(today)
            self.logger.info('There are %d games today', len(game_ids))

            while len(game_ids) > 0:
                for game_id in list(game_ids):
                    game = Game(self.CFL_CLIENT, game_id['season'], game_id['game_id'])

                    if game.event_status.is_in_progress():
                        self.logger.info('Making game thread')
                        self.__post_thread(game)
                    elif game.event_status.is_pre_game():
                        now = pytz.UTC.localize(datetime.utcnow())
                        game_post_dt = game.date_start - timedelta(minutes=self.POST_MINUTES_AHEAD)
                        pre_game_post_dt = game.date_start - timedelta(minutes=self.POST_MINUTES_AHEAD)
                        if game_post_dt > now:
                            self.logger.info("Making game thread")
                            self.__post_thread(game)
                        elif pre_game_post_dt > now:
                            self.logger.info("Making pregame thread")
                            self.__post_thread(game, prefix="PRE GAME THREAD")
                    elif game.event_status.is_final():
                        self.logger.info("Making postgame thread")
                        self.__post_thread(game, prefix="POST GAME THREAD")
                        game_ids.remove(game_id)
                    elif game.event_status.is_cancelled():
                        self.logger.info("Game was cancelled. Skipping post...")
                        game_ids.remove(game_id)

                # End for

                self.logger.info("Sleeping for 1 minute")
                sleep(1 * 60)

            # End while

            self.logger.info("Sleeping for 1 day")
            sleep(1 * 60 * 60 * 24)
        # End while

    # End run()

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

            self.logger.debug('Updating thread "%s"...', thread_title)
            submission.edit(game.build_post())
            self.logger.debug('Done')
        except PrawcoreException as e:
            self.logger.error(e)

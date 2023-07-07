from time import sleep

from .config import Config, LoggingConfig
from .reddit import Reddit
from .cfl import CFL
from .templates import PreGameThread, GameThread, PostGameThread
from .db import Database
from .entities import RedditThread
from datetime import datetime, timezone, timedelta
from .models import Game, Standings
from mako.template import Template
from zoneinfo import ZoneInfo
import logging
import os

class Bot:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.db = Database(self.config.database)
        self.reddit = Reddit(self.config.reddit)
        self.cfl = CFL(self.config.cfl)
    #End __init__
        
    def run(self) -> None:
        while True:
            now = datetime.now(timezone.utc)
            week = self.cfl.get_week(now)
            self.logger.info(f'Checking for games in {week.name}')
            for game in week.games:
                self.logger.info(f'Processing game {game.cfl_game_id} with status {game.status}')
                self.__do_pregame_thread(game)
                self.__do_game_thread(game)
                self.__do_postgame_thread(game)
                self.logger.info(f'Finished processing game {game.cfl_game_id}')
            
            self.logger.info(f'Sleeping for one minute')
            sleep(1 * 60)
    #End run

    def __do_pregame_thread(self, game: Game) -> None:
        if not self.config.pregame:
            self.logger.debug(f'Skipping pregame for game {game.cfl_game_id}; not enabled')
            return
        if not game.is_scheduled():
            self.logger.debug(f'Skipping pregame for game {game.cfl_game_id}; game in progress or complete')
            return

        post_date = game.start_date - timedelta(minutes=self.config.pregame_minutes)
        now = datetime.now(timezone.utc)
        if post_date < now:
            thread = self.__get_thread(game.cfl_game_id)

            pre_game_thread = PreGameThread(self.cfl, self.config)
            post_body = pre_game_thread.build_body(game)

            if self.__is_game_archived(game):
                self.logger.info(f'Skipping pregame for game {game.cfl_game_id}; game has been archived')
                return
            elif thread.pregame_thread_id is None:
                self.logger.info(f'Posting pregame thread for game {game.cfl_game_id}')
                title = pre_game_thread.build_title(game)
                submission_id = self.reddit.create_submission(title, post_body)
                thread.pregame_thread_id = submission_id
                self.db.update_reddit_thread(thread)

                self.reddit.set_suggested_sort(submission_id, 'new')
            else:
                self.logger.info(f'Updating pregame thread for game {game.cfl_game_id}')
                self.reddit.update_submission(thread.pregame_thread_id, post_body)
        
    def __do_game_thread(self, game: Game) -> None:
        if game.is_complete():
            self.logger.debug(f'Skipping game for game {game.cfl_game_id}; game is complete')
            return

        post_date = game.start_date - timedelta(minutes=self.config.game_minutes)
        now = datetime.now(timezone.utc)
        if post_date < now:
            thread = self.__get_thread(game.cfl_game_id)

            game_thread = GameThread(self.cfl, self.config)
            post_body = game_thread.build_body(game)

            if self.__is_game_archived(game):
                self.logger.info(f'Skipping game for game {game.cfl_game_id}; game has been archived')
                return
            elif thread.game_thread_id is None:
                self.logger.info(f'Posting game thread for game {game.cfl_game_id}')
                title = game_thread.build_title(game)
                submission_id = self.reddit.create_submission(title, post_body)
                thread.game_thread_id = submission_id
                self.db.update_reddit_thread(thread)

                self.reddit.set_suggested_sort(submission_id, 'new')
            else:
                self.logger.info(f'Updating game thread for game {game.cfl_game_id}')
                self.reddit.update_submission(thread.game_thread_id, post_body)

    def __do_postgame_thread(self, game: Game) -> None:
        if not self.config.postgame:
            self.logger.debug(f'Skipping postgame for game {game.cfl_game_id}; not enabled')
            return

        if game.is_complete():
            thread = self.__get_thread(game.cfl_game_id)

            post_game_thread = PostGameThread(self.cfl, self.config)
            post_body = post_game_thread.build_body(game)

            if self.__is_game_archived(game):
                self.logger.info(f'Skipping postgame for game {game.cfl_game_id}; game has been archived')
                return
            elif thread.postgame_thread_id is None:
                self.logger.info(f'Posting postgame for game {game.cfl_game_id}')
                title = post_game_thread.build_title(game)
                submission_id = self.reddit.create_submission(title, post_body)
                thread.postgame_thread_id = submission_id
                self.db.update_reddit_thread(thread)

                comment = f'[Post game thread here](https://www.reddit.com/r/CFL/comments/{thread.postgame_thread_id})'
                self.reddit.create_comment(thread.game_thread_id, comment)
                self.reddit.lock_submission(thread.game_thread_id)
            else:
                self.logger.info(f'Updating postgame thread for game {game.cfl_game_id}')
                self.reddit.update_submission(thread.postgame_thread_id, post_body)

    def __get_thread(self, cfl_game_id: str) -> RedditThread:
        thread = self.db.find_reddit_thread(cfl_game_id)
        if thread is None:
            thread = self.db.create_reddit_thread(RedditThread(cfl_game_id))
        return thread

    def __is_game_archived(self, game: Game) -> bool:
        end_post_date = game.start_date + timedelta(hours=12)
        now = datetime.now(timezone.utc)
        return end_post_date < now
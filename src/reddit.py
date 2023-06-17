from config import RedditConfig
import praw
from praw.models import Subreddit, Submission
import logging

class Reddit:
    def __init__(self, config: RedditConfig):
        self.logger = logging.getLogger(__name__)

        if config is None:
            raise ValueError('Missing Reddit API config')
        
        self.enabled = config.enabled
        if config.reddit_client_id is None:
            raise ValueError('Missing Reddit client id')
        if config.reddit_client_secret is None:
            raise ValueError('Missing Reddit client secret')
        if config.reddit_user_agent is None:
            raise ValueError('Missing Reddit user agent')
        if config.reddit_refresh_token is None:
            raise ValueError('Missing Reddit refresh token')

        if self.enabled:
            self.logger.info('Authenticating with Reddit')
            self.r = praw.Reddit(user_agent=config.reddit_user_agent,
                                client_id=config.reddit_client_id,
                                client_secret=config.reddit_client_secret,
                                refresh_token=config.reddit_refresh_token)
            self.subreddit_name = config.subreddit
            self.logger.info(f'Successfully authenticated with Reddit with scopes {self.r.auth.scopes()}')
        else:
            self.logger.info('Reddit disabled')
    
    def create_submission(self, title: str, body: str) -> str:
        if not self.enabled:
            return None

        subreddit = self.r.subreddit(self.subreddit_name)

        self.logger.info('Creating submission')
        submission = subreddit.submit(title, selftext=body)

        self.__set_suggested_sort(subreddit, submission, 'new')
        
        return submission.id
        
    def update_submission(self, submission_id: str, body: str) -> None:
        if not self.enabled:
            return
        
        subreddit = self.r.subreddit(self.subreddit_name)
        submission = self.__get_submission(submission_id)

        if submission is None:
            self.logger.error(f'Unable to update submission; Submission {submission_id} does not exist')
        else:
            self.logger.info(f'Submission {submission_id} exists, updating')
            submission.edit(body)

    def __set_suggested_sort(self, subreddit: Subreddit, submission: Submission, suggested_sort: str) -> None:
        if not subreddit.user_is_moderator:
            self.logger.info('User is not moderator, skipping suggested sort')
            return
        
        if submission is None:
            self.logger.error(f'Unable to set suggested sort; Submission {submission.id} does not exist')
        else:
            self.logger.info(f'Updating suggested sort for submission {submission.id}')
            submission.mod.suggested_sort(suggested_sort)

    def create_comment(self, submission_id: str, body: str) -> None:
        if not self.enabled:
            return
        
        submission = self.__get_submission(submission_id)
        if submission is None:
            self.logger.error(f'Unable to create comment; Submission {submission_id} does not exist')
        else:
            self.logger.info(f'Replying to submission {submission_id}')
            submission.reply(body)

    def __get_submission(self, submission_id: str):
        if submission_id is None:
            return None
        return self.r.submission(id=submission_id)
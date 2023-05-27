from builtins import Exception

from io import open

import json
import logging
from slack_log_handler import SlackLogHandler
from bot import Bot

def main():
    with open('./config/config.json', 'r') as json_file:
        config = json.load(json_file)

        logging_config = config.get('logging')
        if logging_config is None:
            logging_config = {}
        logger = setup_logging(logging_config)

        try:
            bot = Bot(config)
            bot.run()
        except Exception as e:
            logger.critical(e)
# End main()


def setup_logging(config):
    logger = logging.getLogger('cflbot')
    logger.setLevel(logging.DEBUG)

    log_format = config.get('format')
    if log_format is None:
        log_format = '%(asctime)s %(levelname)-10s %(message)s'
    formatter = logging.Formatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    config_slack = config.get('slack')
    if config_slack is not None and config_slack.get('enabled'):
        webhook_uri = config_slack.get('webhookUri')
        level = config_slack.get('level')
        logger.info('Slack logging is enabled with level %s', level)

        slack_handler = SlackLogHandler(webhook_uri)
        slack_handler.setFormatter(formatter)
        slack_handler.setLevel(logging.getLevelName(level))
        logger.addHandler(slack_handler)
    # End if

    return logger
# End setup_logging()


if __name__ == '__main__':
    main()

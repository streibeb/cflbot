import argparse
from bot import Bot
from config import Config, LoggingConfig
import logging

VERSION = '3.1.0'

def __init_logger(config: LoggingConfig):
    logger = logging.getLogger()
    logger.setLevel(config.level)

    formatter = logging.Formatter(config.format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
# End setup_logging()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    config = Config.from_file(args.config)
    logger = __init_logger(config.logging)
    logger.info(f'Running cflbot {VERSION}')

    bot = Bot(config)
    bot.run()
# End main()

if __name__ == '__main__':
    main()
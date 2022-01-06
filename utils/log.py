import logging
from sys import stdout

from utils.paths_builder import logs_file_path


class Logger:
    _logger = None

    def __init__(self):
        if Logger._logger is not None:
            raise Exception("Singleton class - single instance only!")
        else:
            self.setup_logger("sms_logger")

    @staticmethod
    def get_logger():
        if Logger._logger is None:
            Logger()
        return Logger._logger

    @staticmethod
    def setup_logger(name):
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m-%d %H:%M:%S"
        )
        file_handler = logging.FileHandler(logs_file_path())
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler(stream=stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        Logger._logger = logger

import logging
from datetime import datetime


class Logger:
    error_log = info_log = None

    # Constructor to setup logger config
    def __init__(self):
        # Add loggers
        self.__add_logger('error_log', "log/error-{:%Y-%m}.log".format(datetime.now()), logging.ERROR)
        self.__add_logger('info_log', "log/info-{:%Y-%m}.log".format(datetime.now()), logging.INFO)

        # Define loggers
        self.error_log = logging.getLogger('error_log')
        self.info_log = logging.getLogger('info_log')

    # Add a new logger
    def __add_logger(self, logger_name, log_file, level):
        logger = logging.getLogger(logger_name)

        # setup handlers
        if not logger.handlers:
            formatter = logging.Formatter("(%(levelname)s) %(asctime)s - %(message)s", "%d-%b-%y %H:%M:%S")
            fileHandler = logging.FileHandler(log_file)
            fileHandler.setFormatter(formatter)

            logger.setLevel(level)
            logger.addHandler(fileHandler)

    # Log error
    def error(self, message):
        self.error_log.error(message)

    # Log info
    def info(self, message):
        self.info_log.info(message)
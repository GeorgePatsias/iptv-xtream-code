import logging
from config import LOGGER_PATH


class LoggerClass():
    def __init__(self):
        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)

        self._handler = logging.FileHandler(LOGGER_PATH)
        self._handler.setLevel(logging.DEBUG)

        self._formatter = logging.Formatter('[%(name)s] - %(levelname)s - %(asctime)s  - %(message)s')
        self._handler.setFormatter(self._formatter)
        self.logger.addHandler(self._handler)

    def getLogger(self):
        return self.logger


logger = LoggerClass().getLogger()

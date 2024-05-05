import logging


# Taken from https://stackoverflow.com/questions/2183233/
def addLoggingLevel(levelName, levelNum):
    methodName = levelName.lower()

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logger.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


# Set custom logging levels
addLoggingLevel("TRACE", logging.DEBUG - 5)
addLoggingLevel("SUCCESS", logging.INFO + 1)
addLoggingLevel("FAILURE", logging.INFO + 2)


# Inspired by https://stackoverflow.com/questions/1343227/
class MyFormatter(logging.Formatter):
    formats = {
        logging.TRACE: "\033[K  %(msg)s",
        logging.DEBUG: "\033[K▌ %(msg)s",
        logging.INFO: "\033[K\033[1;94m▌\033[00m %(msg)s",
        logging.SUCCESS: "\033[K\033[1;92m▌\033[00m %(msg)s",
        logging.FAILURE: "\033[K\033[1;91m▌\033[00m %(msg)s",
        logging.WARNING: "\033[K\033[1;93m▌\033[00m %(msg)s",
        logging.ERROR: "\033[K\033[1;91m▌\033[00m %(msg)s",
        logging.CRITICAL: "\033[K\033[1;91m▌\033[00m %(msg)s",
    }

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style="%")

    def format(self, record):
        temp = self._style._fmt
        self._style._fmt = MyFormatter.formats[record.levelno]
        result = logging.Formatter.format(self, record)
        self._style._fmt = temp
        return result


handler = logging.StreamHandler()
formatter = MyFormatter()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def set_terminator(self, terminator):
    self.handlers[0].terminator = terminator


logging.getLoggerClass().set_terminator = set_terminator

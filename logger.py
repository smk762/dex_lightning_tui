import logging

class CustomFormatter(logging.Formatter):

    black = "\x1b[30m"
    error = "\x1b[31m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    orange = "\x1b[33m"
    blue = "\x1b[34m"
    purple = "\x1b[35m"
    cyan = "\x1b[36m"
    lightgrey = "\x1b[37m"
    table = "\x1b[37m"
    darkgrey = "\x1b[90m"
    lightred = "\x1b[91m"
    lightgreen = "\x1b[92m"
    yellow = "\x1b[93m"
    lightblue = "\x1b[94m"
    status = "\x1b[94m"
    pink = "\x1b[95m"
    lightcyan = "\x1b[96m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"
    datefmt='%d-%b-%y %H:%M:%S'

    FORMATS = {
        logging.DEBUG: lightblue + format + reset,
        logging.INFO: lightgreen + format + reset,
        logging.WARNING: red + format + reset,
        logging.ERROR: lightred + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

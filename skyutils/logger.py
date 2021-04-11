import logging


def setup_logger(name, log_file, level=logging.DEBUG):
    formatter = logging.Formatter(
        '%(asctime)s %(message)s', datefmt='%d-%b-%Y %H:%M:%S::')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class Logger:
    def __init__(self, debug):
        if debug:
            self.raw_logger = setup_logger(
                'raw_logger', 'logs/raw.log')
            self.all_ac_logger = setup_logger(
                'all_ac_logger', 'logs/all_aircrafts.log')
            self.displayed_ac_logger = setup_logger(
                'displayed_ac_logger', 'logs/displayed_aircrafts.log')
            self.metar = setup_logger(
                'metar', 'logs/metar.log')
            self.webserver = setup_logger(
                'webserver', 'logs/webserver.log')

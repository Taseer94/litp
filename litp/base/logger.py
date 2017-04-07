import logging
import os
from os import path


class Logger(object):
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')

    def __init__(self, logger_name, file_path=None):
        self.file_path = '/var/log' if not file_path else file_path

        IF_DEBUG = os.getenv('IF_DEBUG')

        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = 0
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        if IF_DEBUG is not None and IF_DEBUG.lower() == "true":
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

        hdlr = logging.FileHandler('%s/%s.log' % (self.file_path, logger_name))
        hdlr.setFormatter(self.formatter)
        hdlr.setLevel(logging.DEBUG)
        self.logger.addHandler(hdlr)

    @property
    def get(self):
        return self.logger


class LitpLogger(Logger):
    def __init__(self, logger_name):
        self.file_path = path.join(path.dirname(__file__), path.pardir, path.pardir, 'logs')
        if not path.exists(self.file_path):
            os.makedirs(self.file_path)

        super(LitpLogger, self).__init__(logger_name, self.file_path)

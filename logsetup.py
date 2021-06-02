import logging
import sys

logger = logging.getLogger(__name__)

LOG_PREFMT = {
    (logging.DEBUG, '\x1b[38;5;240m>\x1b[38;5;239m>\x1b[38;5;238m> \x1b[38;5;239m[%(name)-8s]\x1b[0m %(message)s\x1b[0m'),
    (logging.INFO,  '\x1b[38;2;255;0;255m>\x1b[38;2;223;0;223m>\x1b[38;2;192;0;192m> \x1b[38;5;239m[%(name)-8s]\x1b[0m %(message)s\x1b[0m'),
    (logging.WARNING, '\x1b[38;5;228m>\x1b[38;5;227m>\x1b[38;5;226m> \x1b[38;5;239m[%(name)-8s]\x1b[38;5;226m %(message)s\x1b[0m'),
    (logging.ERROR, '\x1b[38;5;208m>\x1b[38;5;202m>\x1b[38;5;196m> \x1b[38;5;239m[%(name)-8s]\x1b[38;5;196m %(message)s\x1b[0m'),
    (logging.CRITICAL, '\x1b[48;5;196;38;5;16m>>> [%(name)-8s] %(message)s\x1b[0m'),
}

class MyStreamHandler(logging.StreamHandler):
    def __init__(self, stream, formatters):
        logging.StreamHandler.__init__(self, stream)
        self.formatters = formatters
    def format(self, record):
        return self.formatters[record.levelno].format(record)

def init_logging():
    formatters = {}
    for (level, fmtstr) in LOG_PREFMT:
        formatters[level] = logging.Formatter(fmtstr)
    handler = MyStreamHandler(sys.stdout, formatters)
    logging.basicConfig(level=logging.DEBUG, handlers=[handler])

if __name__ == '__main__':
    init_logging()
    logger.debug('Test debug message')
    logger.info('Test info message')
    logger.warning('Test warning message')
    logger.error('Test error message')
    logger.critical('Test critical message')

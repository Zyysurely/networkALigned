import logging
from logging.handlers import RotatingFileHandler
import os

"""log file path"""
LOGFILE_PATH = os.path.join(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')),
    'E:/graduate/twitter_foursquare/logs/networkfuse.log')

logger = logging.getLogger('NetworkFuse')
logger.setLevel(logging.DEBUG)
ch = RotatingFileHandler(
    LOGFILE_PATH,
    maxBytes=20 * 1024 * 1024,
    backupCount=10000)
ch.setLevel(logging.DEBUG)

cs = logging.StreamHandler()
cs.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    '[%(asctime)s](%(levelname)s)%(name)s[%(module)s]-%(funcName)s-%(lineno)d: %(message)s')
ch.setFormatter(formatter)
cs.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(cs)
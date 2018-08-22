import logging.config
import ConfigParser

from .logging_config import LoggingConfig

logging.config.dictConfig(LoggingConfig)

booker_config = ConfigParser.ConfigParser()
booker_config.read('/data/config/lcc-booker/config.properties')


def check_browser_ipcc(ipcc):
    ipcc_list = booker_config.get('browser', 'ipccList').split(",")
    if ipcc in ipcc_list:
        return True
    return False

def refreshConfig():
    sections = booker_config.sections()
    for section in sections:
        booker_config.remove_section(section)

    booker_config.read('/data/config/lcc-booker/config.properties')
import configparser
import os


_config = None


def get_config(reread=False):
    global _config
    if not reread and _config:
        return _config
    _config = configparser.ConfigParser()
    _config.readfp(open('defaults.cfg'))
    _config.read([os.path.expanduser('~/.console_weather.cfg')])
    return _config

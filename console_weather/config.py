import configparser
import os


CONFIG_PATH = os.path.expanduser('~/.console_weather.cfg')
_config = None


def get_config(reread=False):
    global _config
    if not reread and _config:
        return _config
    _config = configparser.ConfigParser()
    _config.readfp(open('defaults.cfg'))
    _config.read([CONFIG_PATH])
    return _config


def write_config():
    if _config is None:
        get_config()
    if _config is not None:
        with open(CONFIG_PATH, 'w') as config_file:
            _config.write(config_file)

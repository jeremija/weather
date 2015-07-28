import argparse
from colorama import Fore, Style
import datetime
import pytz
import sys
import traceback

from . import services, config


TEMP_COLORS = [
    (6, Fore.BLUE),
    (14, Fore.BLUE),
    (22, Fore.GREEN),
    (30, Fore.YELLOW),
    (100, Fore.RED)
]


def parse_args(argv):
    parser = argparse.ArgumentParser('Displays forecast information')

    parser.add_argument('-l', '--location', nargs='+',
        help='Location to fetch forecast for. Will try to determine your '
            'location automatically when omitted')
    parser.add_argument('-i', '--ignore-config',
        help='Ignores location stored in config and attempts to detect it')
    parser.add_argument('-s', '--save', action='store_true',
        help='Saves location in config (if successful')
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables logging of exceptions')
    parser.add_argument('-n', '--no-color', action='store_true',
        help='Disabled colored output')
    parser.add_argument('--hourly', action='store_true',
        help='Prints hourly forecast')

    return parser.parse_args(argv)


class Printer:

    def __init__(self, colored=True):
        self.colored = colored

    def print(self, color, *args, bright=False, err=False):
        if not self.colored:
            print(*args)
            return
        if bright:
            color += Style.BRIGHT
        if color and len(args) > 0:
            args = list(args)
            args[0] = color + str(args[0])
            args[-1] = str(args[-1]) + Style.RESET_ALL
        print(*args, file=sys.stderr if err else sys.stdout)


PRINTER = Printer()


def fetch_coords(location):
    if not location:
        return services.fetch_location()
    else:
        return services.fetch_city_coords(location)


def fetch_forecast(coords):
    return services.fetch_forecast(coords['lat'], coords['lng'])


def parse_time(time, tz):
    return datetime.datetime.fromtimestamp(time, tz=tz)


def get_color(temp):
    for t, color in TEMP_COLORS:
        if t >= temp:
            break

    return color


def format_hourly_entry(entry):
    summary = entry['summary']
    temp = int(entry['temperature'])
    percip = int(float(entry['precipProbability']) * 100)
    visibility = int(entry['visibility']) if 'visibility' in entry else -1
    color = get_color(temp)

    return color, '{:5d}°C {:5d}% {:5d} km - {}'.format(
        temp, percip, visibility, summary)


def format_daily_entry(entry):
    summary = entry['summary']
    tempMin = int(entry['temperatureMin'])
    tempMax = int(entry['temperatureMax'])
    percip = int(float(entry['precipProbability']) * 100)
    color = get_color(tempMax)

    return color, '{:5d} - {:2d}°C {:5d}% - {}'.format(
        tempMin, tempMax, percip, summary)


def print_forecast(forecast, print_hourly=False):
    tz = pytz.timezone(forecast['timezone'])

    summary = '{} {}'.format(
        forecast['minutely']['summary'] if 'minutely' in forecast else '',
        forecast['hourly']['summary'])
    PRINTER.print(Fore.YELLOW, summary.strip(), bright=True)

    if print_hourly:
        for hour in forecast['hourly']['data']:
            time = parse_time(hour['time'], tz)
            color, hourly = format_hourly_entry(hour)
            weekday = time.strftime('%a')
            PRINTER.print(color, '{} {:3d}h{}'.format(
                weekday, time.hour, hourly))
    else:
        for day in forecast['daily']['data']:
            time = parse_time(day['time'], tz)
            date = time.strftime('%a, %b %d')
            color, daily = format_daily_entry(day)
            PRINTER.print(color, '{} {}'.format(date, daily))


def unsafe_main(args, cfg):
    if not cfg['forecast.io']['api_key']:
        PRINTER.print(
            Fore.RED, 'No [forecast.io] api_key set in config', err=True)
        config.write_config()
        PRINTER.print(Fore.RED, 'A default config file was written to',
            config.CONFIG_PATH, err=True)
        return

    if not args.location and 'coords' in cfg and not args.ignore_config:
        coords = cfg['coords']
    else:
        coords = fetch_coords(args.location)

    if not coords:
        PRINTER.print(Fore.RED, 'Could not obtain location', err=True)
        return

    PRINTER.print(Fore.YELLOW, coords['city'], bright=True)
    forecast = fetch_forecast(coords)
    if not forecast:
        PRINTER.print(Fore.RED, 'Could not obtain forecast', err=True)
        return

    print_forecast(forecast, args.hourly)

    if args.save:
        cfg['coords'] = coords
        config.write_config()
        PRINTER.print(None, 'Saved location to config', err=True)


def main(argv):
    cfg = config.get_config()
    args = parse_args(argv)
    PRINTER.colored = not args.no_color

    try:
        unsafe_main(args, cfg)
        PRINTER.print(Fore.BLUE, 'Powered by http://forecast.io')
    except ConnectionError as e:
        PRINTER.print(
            Fore.RED, 'Error connecting to the service:', e, err=True)
        if args.debug:
            PRINTER.print(Fore.RED, traceback.format_exc(), err=True)
    except Exception as e:
        PRINTER.print(Fore.RED, 'An error occurred:', e, err=True)
        if args.debug:
            PRINTER.print(Fore.RED, traceback.format_exc(), err=True)


if __name__ == '__main__':
    main(sys.argv[1:])

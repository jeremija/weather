import argparse
import sys
from . import services, config
import pytz
import datetime
import colorama


TEMP_COLORS = [
    (6, colorama.Fore.BLUE),
    (14, colorama.Fore.BLUE),
    (22, colorama.Fore.GREEN),
    (30, colorama.Fore.YELLOW),
    (100, colorama.Fore.RED)
]


def yellow(text, bright=False):
    return colorama.Fore.YELLOW + (colorama.Style.BRIGHT if bright else '') +\
        text + colorama.Style.RESET_ALL


def parse_args(argv):
    parser = argparse.ArgumentParser('Displays forecast information')

    parser.add_argument('location', nargs='?', default='',
        help='Location to fetch forecast for. Will try to determine your '
            'location automatically when omitted')
    parser.add_argument('--hourly', action='store_true',
        help='Prints hourly forecast')

    return parser.parse_args(argv)


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

    print(yellow(parse_time(forecast['currently']['time'], tz).strftime(
        '%a, %b %d, %H:%M:%S')))

    summary = '{} {}'.format(
        forecast['minutely']['summary'] if 'minutely' in forecast else '',
        forecast['hourly']['summary'])
    print(yellow(summary.strip(), bright=True))

    if print_hourly:
        for hour in forecast['hourly']['data']:
            time = parse_time(hour['time'], tz)
            color, hourly = format_hourly_entry(hour)
            weekday = time.strftime('%a')
            print('{}{} {:3d}h{}{}'.format(
                color, weekday, time.hour, hourly, colorama.Style.RESET_ALL))
    else:
        for day in forecast['daily']['data']:
            time = parse_time(day['time'], tz)
            date = time.strftime('%a, %b %d')
            color, daily = format_daily_entry(day)
            print('{}{} {}{}'.format(
                color, date, daily, colorama.Style.RESET_ALL))


def main(argv):
    cfg = config.get_config()
    args = parse_args(argv)

    if args.location:
        location = args.location
    elif 'defaults' in cfg and 'location' in cfg['defaults']:
        location = cfg['defaults']['location']
    else:
        location = None

    coords = fetch_coords(location)
    if not coords:
        print('Could not obtain location', file=sys.stderr)
        return

    print(yellow(coords['city'], bright=True))
    forecast = fetch_forecast(coords)
    if not forecast:
        print('Could not obtain forecast', file=sys.stderr)
        return

    print_forecast(forecast, args.hourly)


if __name__ == '__main__':
    main(sys.argv[1:])

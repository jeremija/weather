import argparse
import sys
from . import services
import pytz
import datetime


def parse_args(argv):
    parser = argparse.ArgumentParser('Displays forecast information')

    parser.add_argument('-l', '--location',
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


def format_hourly_entry(entry):
    summary = entry['summary']
    temp = int(entry['temperature'])
    percip = int(float(entry['precipProbability']) * 100)
    visibility = int(entry['visibility'])

    return '{:5d}°C {:5d}% {:5d} km - {}'.format(
        temp, percip, visibility, summary)


def format_daily_entry(entry):
    summary = entry['summary']
    tempMin = int(entry['temperatureMin'])
    tempMax = int(entry['temperatureMax'])
    percip = int(float(entry['precipProbability']) * 100)

    return '{:5d}-{:2d}°C {:5d}% - {}'.format(
        tempMin, tempMax, percip, summary)


def print_forecast(forecast, print_hourly=False):
    tz = pytz.timezone(forecast['timezone'])

    print('Local time is: {}'.format(
        parse_time(forecast['currently']['time'], tz).strftime(
            '%a, %b %d, %H:%M:%S')))

    print(forecast['minutely']['summary'])
    print(forecast['hourly']['summary'])

    if print_hourly:
        for hour in forecast['hourly']['data']:
            time = parse_time(hour['time'], tz)
            hourly = format_hourly_entry(hour)
            weekday = time.strftime('%a')
            print('{} {:3d}h{}'.format(weekday, time.hour, hourly))
    else:
        for day in forecast['daily']['data']:
            time = parse_time(day['time'], tz)
            date = time.strftime('%a, %b %d')
            daily = format_daily_entry(day)
            print('{} {}'.format(date, daily))


def main(argv):
    args = parse_args(argv)

    coords = fetch_coords(args.location)
    if not coords:
        print('Could not obtain location, try using -l flag', file=sys.stderr)
        return

    print('Fetching forecast for', coords['city'])
    forecast = fetch_forecast(coords)
    if not forecast:
        print('Could not obtain forecast', file=sys.stderr)
        return

    print_forecast(forecast, args.hourly)


if __name__ == '__main__':
    main(sys.argv[1:])

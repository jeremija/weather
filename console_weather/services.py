import requests
from . import config


URL_OPEN_STREET_MAPS = 'https://nominatim.openstreetmap.org'
URL_TELIZE = 'https://www.telize.com'
URL_FORECAST = 'https://api.forecast.io/forecast/{}/{},{}?units=si'


def fetch_city_coords(city):
    url = '{}{}'.format(URL_OPEN_STREET_MAPS, '/search')

    r = requests.get(url, params={
        'q': city,
        'format': 'json'
    })
    r.raise_for_status()

    json = r.json()
    if len(json) == 0:
        return None
    json = json[0]
    return {
        'city': json['display_name'],
        'lat': json['lat'],
        'lng': json['lon']
    }


def fetch_location():
    url = '{}{}'.format(URL_TELIZE, '/geoip')

    r = requests.get(url)
    r.raise_for_status()

    json = r.json()

    return {
        'lat': json['latitude'],
        'lng': json['longitude'],
        'city': json['city'],
        'country': json['country']
    }


def fetch_forecast(lat, lng):
    api_key = config.get_config()['forecast.io']['api_key']
    url = URL_FORECAST.format(api_key, lat, lng)

    r = requests.get(url)
    r.raise_for_status()

    return r.json()

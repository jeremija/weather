from console_weather import services
import nose.tools


def test_fetch_city_coords():
    coords = services.fetch_city_coords('Manhattan')

    nose.tools.eq_(coords, {
        'lat': '40.7902778',
        'lng': '-73.9597222',
        'city': 'Manhattan, New York, NYC, New York, United States of America'
    })


def test_fetch_location():
    location = services.fetch_location()

    nose.tools.eq_(['city', 'country', 'lat', 'lng'], sorted(location.keys()))


def test_fetch_forecast():
    forecast = services.fetch_forecast(40.7903, -73.9597)

    print(forecast)

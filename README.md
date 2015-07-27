# Weather

Obtain weather information from the command line. Location can be automatically
detected or set manually.

## Daily

```bash
$ weather
Amsterdam, Centrum, Amsterdam, MRA, Stadsregio Amsterdam, Noord-Holland, Nederland
Mon, Jul 27, 08:48:49
Rain until this evening, starting again tonight.
Mon, Jul 27    14 - 19°C   100% - Rain until evening, starting again overnight.
Tue, Jul 28    15 - 19°C   100% - Light rain throughout the day.
Wed, Jul 29    13 - 18°C    89% - Light rain until afternoon.
Thu, Jul 30    12 - 18°C    97% - Light rain until afternoon.
Fri, Jul 31     9 - 19°C    11% - Partly cloudy starting in the afternoon, continuing until evening.
Sat, Aug 01    12 - 21°C     1% - Partly cloudy in the morning.
Sun, Aug 02    14 - 23°C     7% - Partly cloudy throughout the day.
Mon, Aug 03    16 - 24°C     1% - Partly cloudy in the morning.
```

## Hourly

```
$ weather --hourly
Amsterdam, Centrum, Amsterdam, MRA, Stadsregio Amsterdam, Noord-Holland, Nederland
Mon, Jul 27, 08:49:51
Rain until this evening, starting again tonight.
Mon   8h   15°C    93%     9 km - Light Rain
Mon   9h   15°C   100%     9 km - Light Rain
Mon  10h   16°C   100%     9 km - Rain
Mon  11h   16°C    99%     9 km - Rain
Mon  12h   16°C   100%     9 km - Rain
Mon  13h   17°C   100%     9 km - Rain
Mon  14h   18°C   100%    -1 km - Rain
Mon  15h   18°C   100%    -1 km - Rain
Mon  16h   18°C   100%    -1 km - Light Rain
Mon  17h   19°C    96%    -1 km - Light Rain
Mon  18h   19°C    80%    -1 km - Light Rain
Mon  19h   18°C    57%    -1 km - Light Rain
Mon  20h   18°C    31%    -1 km - Drizzle
Mon  21h   18°C    14%    -1 km - Partly Cloudy
Mon  22h   17°C     5%    -1 km - Partly Cloudy
Mon  23h   16°C     3%    -1 km - Partly Cloudy
Tue   0h   16°C     4%    -1 km - Partly Cloudy
Tue   1h   16°C    12%    -1 km - Mostly Cloudy
Tue   2h   16°C    37%    -1 km - Drizzle
Tue   3h   15°C    65%    -1 km - Light Rain
Tue   4h   15°C    82%    -1 km - Light Rain
Tue   5h   15°C    93%    -1 km - Light Rain
Tue   6h   15°C    99%    -1 km - Light Rain
Tue   7h   15°C   100%    -1 km - Light Rain
Tue   8h   15°C    99%    -1 km - Light Rain
Tue   9h   16°C    97%    -1 km - Light Rain
Tue  10h   16°C    93%    -1 km - Light Rain
Tue  11h   16°C    87%    -1 km - Light Rain
Tue  12h   17°C    68%    -1 km - Light Rain
Tue  13h   18°C    55%    -1 km - Light Rain
Tue  14h   19°C    25%    -1 km - Drizzle
Tue  15h   18°C    50%    -1 km - Drizzle
Tue  16h   18°C    73%    -1 km - Light Rain
Tue  17h   17°C    81%    -1 km - Light Rain
Tue  18h   17°C    85%    -1 km - Light Rain
Tue  19h   17°C    90%    -1 km - Light Rain
Tue  20h   16°C    86%    -1 km - Light Rain
Tue  21h   16°C    76%    -1 km - Light Rain
Tue  22h   16°C    59%    -1 km - Light Rain
Tue  23h   15°C    48%    -1 km - Light Rain
Wed   0h   15°C    43%    -1 km - Light Rain
Wed   1h   15°C    42%    -1 km - Light Rain
Wed   2h   14°C    41%    -1 km - Light Rain
Wed   3h   14°C    27%    -1 km - Drizzle
Wed   4h   14°C    13%    -1 km - Drizzle
Wed   5h   13°C     7%    -1 km - Clear
Wed   6h   13°C     6%    -1 km - Clear
Wed   7h   14°C     5%    -1 km - Clear
Wed   8h   14°C    12%    -1 km - Clear
```

## Installing

```bash
git clone https://github.com/jeremija/weather.git
pip3 install -r requirements.txt
python3 -m console_weather.main
```

TODO: create setup script

# Powered by

 - [Forecast.io](https://forecast.io)
 - [Open Street Map](https://openstreetmap.org)
 - [Telize GeoIP](https://www.telize.com/geoip)

# License
MIT License

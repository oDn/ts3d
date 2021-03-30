from flask import Flask, render_template
from datetime import datetime
import configparser
import requests, requests_cache
import os, json

app = Flask(__name__)

# Load default application configuration file, see README.md for more information.
config = configparser.ConfigParser()
config.read('config.ini')

class Rainbow:
    colors = ('red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet')
    # Lookup table used to map a city to an area
    city_lookup_table = {
        "Central Europe": "Prague",
        "South Africa": "Cape Town",
        "North America": "New York",
        "Western Europe": "Paris",
        "Eastern Europe": "Minsk",
        "Antarctica": "Villa Las Estrellas",
        "Asia": "Hong Kong",
        "North Africa": "Tripoli",
        "South America": "Lima",
        "Australia": "Perth"
    }

    def __init__(self):
        self.data = {}
        self._load_json()
        self._gather_data()

    def get_data(self):
        return self.data

    # Load color quality data from JSON file
    def _load_json(self, filename='color-quality.json'):
        # Build path to color quality JSON file    
        cq_path = os.path.join('data', filename)
        # Load color quality JSON file
        with open(cq_path, 'r') as cq_f:
            self._cq_json = json.load(cq_f)
        return True

    # Determine which production area must be used by finding highest value for quality value
    def _get_best_quality_color_data(self, color):
        return max(self._cq_json[color], key=lambda cq: cq['quality-value'])

    # Query OpenWeatherMap to fetch realtime weather information for a given city/area
    def _get_current_weather(self, area):
        # Query OpenWeatherMap API using raw area name from JSON input data
        r = self._query_api(area)
        debug = {
            'fallback': False,
            'fallback-city': None,
            'cache': r.from_cache
        }
        try:
            weather = r.json()['weather'][0]['main']
        except KeyError:
            if (r.json()['message'] == 'city not found'):
                # Query OpenWeatherMap API using mapped city name
                city = Rainbow.city_lookup_table[area]
                r = self._query_api(city)
                debug['fallback'] = True
                debug['fallback-city'] = city
                debug['cache'] = r.from_cache
                weather = r.json()['weather'][0]['main']
        return weather, debug

    def _query_api(self, area):
        # Cache results for faster page display times (cache expiry = 1h)
        requests_cache.install_cache(
            cache_name=os.path.join('cache', 'owm_api_cache'),
            backend='sqlite',
            expire_after=3600
        )
        # Query the OpenWeatherMap API to obtain current weather for a given area or city
        api_url = f"{config.get('api', 'baseurl')}?q={area}&appid={config.get('api', 'key')}"
        return requests.get(api_url)

    def _gather_data(self):
        for color in Rainbow.colors:
            d = self._get_best_quality_color_data(color)
            d['current-weather'], d['debug'] = self._get_current_weather(d['area-of-production'])
            self.data[color] = d
        return True

@app.route('/')
def home():
    # Create a new Rainbow instance
    my_rainbow = Rainbow()
    github_url = config.get('github', 'url') 
    return render_template('index.html', now=datetime.now(), github_url=github_url, data=my_rainbow.get_data())

@app.route('/about')
def about():
    return render_template('about.html', now=datetime.now())

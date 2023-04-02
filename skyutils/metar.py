import json
from datetime import datetime

import skyutils.config as config
from skyutils.webscraper import get_metar_info
from skyutils.runway import Runway

from bs4 import BeautifulSoup


class Metar():
    def __init__(self, station):
        self.current_time = datetime.now().strftime("%H:%M")
        self.station = station
        self.wind_direction = "N/A"
        self.wind_speed = "N/A"
        self.temp = "N/A"
        get_metar_info(self)

    @staticmethod
    def update_metar():
        metar = Metar(config.get_station())
        runway = Runway(config.get_runway())

        try:
            runway = runway.runway_for_wind(int(metar.wind_direction))
            runway = f"{runway:02d}"
        except ValueError:
            runway = "N/A"

        try:
            temp = float(metar.temp)
            temp = f"{temp:.0f}"
        except ValueError:
            temp = "N/A"

        with open('web/data.json') as f:
            data = json.load(f)

        data['data']['metar'] = f"{metar.current_time} {temp}\u00b0C Wind:{metar.wind_direction}/{metar.wind_speed}kts RWY:{runway}"

        with open("web/data.json", "w") as f:
            json.dump(data, f)

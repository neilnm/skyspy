import os
import urllib.request
import json

from bs4 import BeautifulSoup

from skyutils.webscraper import get_flight_info


def display_aircraft(ac):
    os.system('pkill vlc')
    os.system('cvlc alarm.wav &')

    get_flight_info(ac)

    with open('web/data.json') as f:
        data = json.load(f)

    data['data']['ts'] = ac.ts.strftime("%Y-%m-%d %H:%M")
    data['data']['lastSeen'] = "Just now"
    data['data']['description'] = ac.description
    data['data']['type'] = ac.type
    data['data']['altitude'] = ac.altitude
    data['data']['track'] = ac.track
    data['data']['speed'] = ac.speed
    data['data']['originName'] = ac.origin_name
    data['data']['origin'] = f'({ac.origin})'
    data['data']['destinationName'] = ac.destination_name
    data['data']['destination'] = f'({ac.destination})'

    with open('web/data.json', 'w') as f:
        json.dump(data, f)

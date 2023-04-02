import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

from shapely.geometry import Point, Polygon

from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))
__package__ = "skyutils"

from skyutils.aircraft import Aircraft
from skyutils.logger import Logger
from skyutils.metar import Metar
from skyutils.config import get_geo_fence, get_home_coords, get_user_alt
from skyutils.displayaircraft import display_aircraft
from skyutils.lastseen import update_last_seen
from skyutils.webserver import Webserver


def main():
    path = os.getcwd()
    debug = "-d" in sys.argv
    if debug:
        logger = Logger(debug)

    # setting vars
    geo_fence = Polygon(get_geo_fence())
    home_point = Point(get_home_coords())
    highest_alt = get_user_alt()
    last_hexcode = ""
    last_ts = datetime(2020, 1, 1)  # arbitrary date
    last_dist_to_home = 1000  # arbitrary distance
    last_wind_update = datetime.now()
    last_seen_update = datetime.now()
    update_last_seen()
    Metar.update_metar()


    # test data
    debug_lines = [
        "Hex    Flight   Altitude  Speed   Lat       Lon       Track  Messages Seen   ",
        "--------------------------------------------------------------------------------",
        "a84495 N672QS   6000      247     99.651    -99.558   137   23        0 sec",
        "a8e495 ACA314   3025      247     99.586    -99.572   137   23        0 sec",
        "a8e495 JZA1     3025      247     37.630    -116.830  137   23        0 sec",
    ]
    for line in debug_lines:
        print(line)

        now = datetime.now()
        last_wind_update_mins = (now - last_wind_update).total_seconds() / 60
        if last_wind_update_mins > 1:
            last_wind_update = datetime.now()
            Metar.update_metar()

        last_seen_update_secs = (now - last_seen_update).total_seconds()
        if last_seen_update_secs > 59:
            last_seen_update = datetime.now()
            update_last_seen()

        hexcode_pattern = '[a-z|0-9]{6}'
        if re.search(hexcode_pattern, line[0:6]):
            ac = Aircraft(line)

            # calculcated data
            if ac.coordinates.x != 0 and ac.coordinates.y != 0:
                ac.dist_to_home = ac.coordinates.distance(home_point)
                ac.in_geofence = ac.coordinates.within(geo_fence)

            # booleans for checking if plane should be displayed
            hexcode_changed = last_hexcode != ac.hexcode
            new_ac_closer = (ac.dist_to_home <= last_dist_to_home)
            time_diff_in_mins = (ac.ts - last_ts).total_seconds() / 60
            aircraft_expired = time_diff_in_mins > 2

            # Check if plane should be displayed
            if(ac.in_geofence and int(ac.altitude) < highest_alt and ac.flight and
               hexcode_changed and (new_ac_closer or aircraft_expired)):
                last_hexcode = ac.hexcode
                last_dist_to_home = ac.dist_to_home
                last_ts = ac.ts

                display_aircraft(ac)

                if debug:
                    logger.raw_logger.info(line)
                    logger.displayed_ac_logger.info(vars(ac))


    with open(os.path.dirname(__file__) + "/../tests/data.json") as f:
        test_data = json.load(f)

    with open(os.path.dirname(__file__) + "/../web/data.json") as f:
        data = json.load(f)
        test_data['data']['lastSeen'] = ""
        test_data['data']['ts'] = ""
        test_data['data']['metar'] = ""
        print(json.dumps(test_data))

        data['data']['lastSeen'] = ""
        data['data']['ts'] = ""
        data['data']['metar'] = ""
        data['data']['dataTs'] = ""
        print(json.dumps(data))
        return data == test_data

def test_main():
    assert main() == True
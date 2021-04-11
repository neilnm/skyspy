import os
import re
import subprocess
import sys
import threading
from datetime import datetime, timedelta

from shapely.geometry import Point, Polygon

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

    # start webserver
    webserver = Webserver()
    web_thread = threading.Thread(target=webserver.start, args=[debug])
    web_thread.start()

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
    Metar.update_html_wind()

    # Start process
    process = subprocess.Popen([f'{path}/dump1090/dump1090',
                                '--interactive'],
                               stdout=subprocess.PIPE)

    for line in iter(process.stdout.readline, 'b'):
        line = line.decode('utf-8')
        print(line)

        now = datetime.now()
        last_wind_update_mins = (now - last_wind_update).total_seconds() / 60
        if last_wind_update_mins > 10:
            last_wind_update = datetime.now()
            Metar.update_html_wind()

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


if __name__ == "__main__":
    main()

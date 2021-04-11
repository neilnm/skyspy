from datetime import datetime, timedelta

from shapely.geometry import Point


class Aircraft:

    def __init__(self, line):
        ts = datetime.now()

        self.hexcode = line[0:6]
        self.flight = line[7:14].replace(" ", "")
        self.description = f"{self.flight} (Details N/A)"
        self.altitude = line[15:21].replace(" ", "")
        self.speed = line[26:29]

        lat = line[34:41].replace(" ", "")
        lon = line[44:52].replace(" ", "")
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            lat = 0
            lon = 0
        self.coordinates = Point(lat, lon)

        self.track = line[54:57]
        self.msg = line[60:63]
        self.last = line[69:73]
        self.in_geofence = False
        self.origin = "N/A"
        self.origin_name = "N/A"
        self.destination = "N/A"
        self.destination_name = "N/A"
        self.type = "N/A"
        self.dist_to_home = 1001
        self.ts = ts

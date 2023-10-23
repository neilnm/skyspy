import urllib.request

from bs4 import BeautifulSoup


def get_flight_info(ac):
    try:
        url = f"https://www.radarbox.com/data/flights/{ac.flight}"
        open_url = urllib.request.urlopen(url)
        html_b = open_url.read()
        open_url.close()
        html = BeautifulSoup(html_b, 'html.parser')

        ac.description = html.find("div", {"id":"info-sections-wrapper"}).find("div",{"id":"value"}).text
        ac.description = f"{ac.flight} / {ac.description}"
        ac.origin = html.find("div", {"id":"origin"}).find("div",{"id":"code"}).text
        ac.origin_name = html.find("div", {"id":"origin"}).find("div",{"id":"city"}).text
        ac.destination = html.find("div", {"id":"destination"}).find("div",{"id":"code"}).text
        ac.destination_name = html.find("div", {"id":"destination"}).find("div",{"id":"city"}).text
        ac.type = html.find("div", {"id":"aircraft-info"}).find("div",{"id":"value"}).text

    except Exception:
        pass


def get_metar_info(metar):
    try:
        station = metar.station
        url = ("https://aviationweather.gov/cgi-bin/data/dataserver.php?"
               f"requestType=retrieve&dataSource=metars&stationString={station}"
               "&startTime=1&format=xml&mostRecent=true")
        open_url = urllib.request.urlopen(url)
        xml_b = open_url.read()
        open_url.close()
        xml = BeautifulSoup(xml_b, "lxml-xml")
        metar.wind_speed = xml.find('wind_speed_kt').string
        metar.wind_direction = xml.find('wind_dir_degrees').string
        metar.temp = xml.find('temp_c').string
    except Exception:
        pass

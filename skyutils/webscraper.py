import urllib.request

from bs4 import BeautifulSoup


def get_flight_info(ac):
    try:
        url = f"https://flightaware.com/live/flight/{ac.flight}"
        open_url = urllib.request.urlopen(url)
        html_b = open_url.read()
        open_url.close()
        html = BeautifulSoup(html_b, 'html.parser')

        description = __try_html_data(
            html, ["meta", "property", "og:description", "content"])
        ac.origin = __try_html_data(
            html, ["meta", "name", "origin", "content"])
        ac.destination = __try_html_data(
            html, ["meta", "name", "destination", "content"])
        ac.type = __try_html_data(
            html, ["meta", "name", "aircrafttype", "content"])

        flight_index = description.index("flight")
        ac.description = description[5:flight_index]
        from_index = description.index(" from ")
        to_index = description.index(" to ")
        ac.origin_name = description[from_index + 6:to_index]
        ac.destination_name = description[to_index + 4:]
    except Exception:
        pass


def get_metar_info(metar):
    try:
        station = metar.station
        url = ("https://www.aviationweather.gov/adds/dataserver_current"
               "/httpparam?dataSource=metars&requestType=retrieve&format"
               f"=xml&hoursBeforeNow=3&mostRecent=true&stationString={station}")
        open_url = urllib.request.urlopen(url)
        xml_b = open_url.read()
        open_url.close()
        xml = BeautifulSoup(xml_b, "lxml-xml")
        metar.wind_speed = xml.find('wind_speed_kt').string
        metar.wind_direction = xml.find('wind_dir_degrees').string
        metar.temp = xml.find('temp_c').string
    except Exception:
        pass


def __try_html_data(html, d):
    try:
        return html.find_all(f'{d[0]}', attrs={f'{d[1]}': f'{d[2]}'})[0].attrs[f'{d[3]}']
    except Exception:
        return "N/A"

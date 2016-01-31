# File modified from Kindle Weather Display by Matthew Petroff
# http://mpetroff.net/

import datetime
import io

from xml.dom import minidom
from urllib.request import urlopen
from config import LATITUDE, LONGITUDE, WEATHER_IMAGE
API_URL = 'http://graphical.weather.gov/xml/SOAP_server/ndfdSOAPclientByDay.php'

def fetch_weather_svg():
    lat = str(LATITUDE)
    lng = str(LONGITUDE)
    weather_req = urlopen(API_URL + '?whichClient=NDFDgenByDay&'
            'lat=' + lat + '&lon=' + lng
            + '&format=24+hourly&numDays=4&Unit=m')
    weather_xml = weather_req.read()

    dom = minidom.parseString(weather_xml)

    # Parse temperatures
    xml_temperatures = dom.getElementsByTagName('temperature')
    highs = [None]*4
    lows = [None]*4
    for item in xml_temperatures:
        if item.getAttribute('type') == 'maximum':
            values = item.getElementsByTagName('value')
            for i in range(len(values)):
                highs[i] = int(values[i].firstChild.nodeValue)
        if item.getAttribute('type') == 'minimum':
            values = item.getElementsByTagName('value')
            for i in range(len(values)):
                lows[i] = int(values[i].firstChild.nodeValue)

    # Parse icons
    xml_icons = dom.getElementsByTagName('icon-link')
    icons = [None]*4
    for i in range(len(xml_icons)):
        icons[i] = xml_icons[i].firstChild.nodeValue.split('/')[-1].split('.')[0].rstrip('0123456789')

    # Parse dates
    xml_day_one = dom.getElementsByTagName('start-valid-time')[0].firstChild.nodeValue[0:10]
    day_one = datetime.datetime.strptime(xml_day_one, '%Y-%m-%d')


    # Open SVG to process
    with io.open(WEATHER_IMAGE, 'r',encoding='utf8') as f:
        svg_str = f.read()

    # Insert icons and temperatures
    svg_str = svg_str.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
    svg_str = svg_str.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
    svg_str = svg_str.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

    # Insert days of week
    one_day = datetime.timedelta(days=1)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    svg_str = svg_str.replace('DAY_THREE',days_of_week[(day_one + 2*one_day).weekday()]).replace('DAY_FOUR',days_of_week[(day_one + 3*one_day).weekday()])

    return svg_str


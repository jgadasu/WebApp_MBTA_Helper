# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://open.mapquestapi.com/geocoding/v1/address"
# MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key={}&lat={}&lon={}&format=json"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "u71BIrcSQdPCACkciAGspfxdyooADDGt"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"

import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from pprint import pprint


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def into_url(place_name):
    """
    Given a place name or address, turn that into a url that can then be
    put into Google Maps to find its information
    """
    d = {"address": place_name}
    address = urlencode(d)
    url = MAPQUEST_BASE_URL + '?' + address
    return url


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    url = 'http://open.mapquestapi.com/geocoding/v1/address?key={}&location={}'.format(MAPQUEST_API_KEY, place_name)
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return (response_data['results'][0]['locations'][0]['latLng'])


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    mbta_url_formatted = MBTA_BASE_URL.format(MBTA_DEMO_API_KEY, latitude, longitude)
    stations = get_json(mbta_url_formatted)

    # creating an empty list for all of the stops
    all_stops = []

    # this says that if there are no close stops, say that there are no close stops
    if len(stations["stop"]) == 0:
        return "There are no stops close to your location"

    # this gets rid of the bus stations and only gets subway stations
    else:
        for station in stations["stop"]:
            all_stops.append(station["stop_name"])

        for i, stop_name in enumerate(all_stops):
            if len(stop_name) != 0:
                return stop_name, stations["stop"][i]["distance"]

def find_stop_nears(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    result_text = "{} is {} miles from {}"

    lat, lng = get_lat_long(place_name)['lat'], get_lat_long(place_name)['lng']
    station, distance = get_nearest_station(lat, lng)

    return result_text.format(station, distance, place_name)


def main():
    """
    You can all the functions here
    """

    ##    get_lat_long("Boston")
    ##    get_nearest_station(get_lat_long('Boston')['lat'],get_lat_long('Boston')['lng'])
    ##    find_stop_near('Boston')

    place_name = str(input('Place Name'))
    print(find_stop_nears(place_name))
    return (find_stop_nears(place_name))


if __name__ == '__main__':
    main()

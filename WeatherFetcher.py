import urllib.request
import json
from typing import Optional

import geopy.exc
from geopy.geocoders import Nominatim
from urllib.error import HTTPError, URLError

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,rain"


def prepare_url(location: str) -> Optional[str]:
    latitude, longitude = location_to_coords(location=location)
    # By default, it is set to Gliwice (50.30, 18.68)
    if None not in (latitude, longitude):
        return OPEN_METEO_URL.format(latitude, longitude)
    return None


def get_meteo_data(url: str) -> dict:
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason)
    except TimeoutError:
        print("Request timed out")


def get_data(location: str) -> dict:
    url = prepare_url(location)
    if url:
        if data := get_meteo_data(url):
            data["location"] = location
            return data
    else:
        return {}


def location_to_coords(location: str) -> tuple:
    try:
        locator = Nominatim(user_agent="Weather Fetcher", timeout=30)
        location = locator.geocode(location)
        return location.latitude, location.longitude
    except geopy.exc.GeocoderTimedOut:
        print("Geocoder request timed out")
        return None, None
    except geopy.exc.GeocoderQueryError:
        print("Wrong input/bad response")
        return None, None
